===========
Quickstart
===========

The package is used to integrate the OAI-PMH client into Invenio. It is a wrapper that is built on the Sickle library.
Provides integration with invenio-records. The purpose of the package is to ensure synchronization with
a remote OAI-PMH source.

The library has two main parts. The first part ensures the migration of current records in invenio-records and the
second part is responsible for the synchronization of current records with a remote OAI-PMH server.

Migration
==========

Before synchronizing our resources with the remote server,
it is necessary to migrate data about records and their persistent identifiers.

Records migration
------------------

Records are migrated by the **OAIMigration class**. The class needs two parameters. The first parameter is a **handler**
that extracts its ID from the record, and the second parameter is an instance of the **OAIProvider class**.


* The OAIProvider class requires one named mandatory arguments:

    **code**: any label (e.g. my_library). The code only distinguishes other sources in the case of multiple record sources.

* A **handler** is a function that must accept one argument, namely json metadata (python dictionary). The handler is responsible for extracting the id from the metadata and it is entirely up to the user how the handler writes. The handler must return the id as a string.

Example of CLI interface:

.. code-block:: python

    @migration.command('oai')
    @cli.with_appcontext
    def migrate_oai():
        def oai_id_handler(json):
            id_ = json["id"]
            try:
                doc = current_search_client.get(index="nusl_marcxml", id=id_)
            except NotFoundError:
                return
            oai_id = doc["_source"].get("035__") or {}
            oai_id = oai_id.get("a")
            if oai_id:
                return oai_id

        provider = OAIProvider.query.filter_by(code="nusl").one_or_none()
        if not provider:
            provider = OAIProvider(
                code="nusl",
                description="Původní NUŠL na Invenio v1",
                oai_endpoint="https://invenio.nusl.cz/oai2d/",
                metadata_prefix="marcxml"
            )
            db.session.add(provider)
            db.session.commit()
        migrator = OAIMigration(handler=oai_id_handler, provider=provider)
        migrator.run()

The most important part of the code is these two lines:

.. code-block:: python

    migrator = OAIMigration(handler=oai_id_handler, provider=provider)
    migrator.run()

Persistent ID migration
------------------------

We leave the migration of persistent identifiers to the user. Here we give an example of PID migration, where we use RecordIdentifier from Invenio.

.. code-block:: python

    @migration.command('pid')
    @cli.with_appcontext
    def migrate_old_pid():
    records = RecordMetadata.query.paginate()
    while_condition = True
    idx = 0
    try:
        while while_condition:
            for record in records.items:
                idx += 1
                pid = record.json["id"]
                recid = RecordIdentifier.query.get(pid)
                if recid:
                    continue
                recid = RecordIdentifier(recid=pid)
                db.session.add(recid)
                print(f"{idx}. {pid} has been added")
                if idx % 100 == 0:  # pragma: no cover
                    db.session.commit()
                    print("Session was commited")
            while_condition = records.has_next
            records = records.next()
    except IntegrityError: # pragma: no cover
        db.session.rollback()
        raise
    else:
        db.session.commit()
    finally:
        db.session.commit()


OAI Synchronization
====================

Synchronization is provided by the **OAISynchronization class**. The constructor requires a number of parameters:

* **provider**: instance of class **OAIProvider**
* **parser_name**: name of parser function, that is registred with Decorators.parser("name", "provider code") decorator (more information in next sections).
* **unhandled_path**: set of json addresses that are not handled by any rule. More about the rules in the following paragraphs.
* **create record, update_record and delete_record**: Handler function that is responsible for creating, editing and deleting a record. The library leaves the user free to manipulate his records. More about handlers in the next paragraphs.
* **pid_type** (optional): persistent identifier type (see Invenio-PIDStore)
* **validation** (optional): Validation function that tests the correctness of the document. Here again, we leave the freedom to the user to validate his records.

Synchronization is then started by the run method, which is called on the OAISynchronization instance. The **run** method has optional **start, stop, and break_on_error** arguments. Start and stop are all-encompassing and indicate the sequence number where synchronization should start or end. The break_on_error parameter is of Boolean type and determines whether the synchronization should stop on an exception or whether it should continue and record the exception in the database (table oai_record_exc)

.. code-block:: python

    sync = OAISynchronizer(
        provider,
        parser_name="dc",
        unhandled_paths={"json/path/to/nested/field},
        create_record=create_handler,
        update_record=update_handler,
        delete_record=delete_handler,
        pid_type="pid",
        validation=validation_function
    )
    sync.run(start_id=start, start_oai=start_oai, break_on_error=break_on_error)

Provider
---------

The provider is a mandatory argument to the OAISynchronization class. The provider is represented by the OAIProvider
class and its constructor has several mandatory parameters:

* **code**: designation of the provider.
* **end_point**: Endpoint for OAI protocol (e.g.: "https://dspace.example.com/oai/set"
* **set_**: OAI set
* **metadata_prefix**: Metadata prefix, data format we want to download
* **constant_field (optional)**: Python dictionary with fields that each entry has from this provider. E.g. information about the provider
* **description (optional)**: Description of the provider.

Example of creating a provider instance:

.. code-block:: python

    uk_provider = OAIProvider(
            code="uk",
            description="Univerzita Karlova",
            oai_endpoint="https://dspace.cuni.cz/oai/nusl",
            set_="nusl_set",
            metadata_prefix="xoai",
            constant_fields=constant_fields
        )
    db.session.add(uk_provider)
    db.session.commit()

Parser
-------

A function that converts output from OAI-PMH (XML file) to a python dictionary. A function that converts output
from OAI-PMH (XML file) to a python dictionary. The form of the function depends on the user. However,
the function must have one argument, which is etree intance from the lxml library, and must return a python dictionary.

**Parser registration**

The module in which the parser function resides must be listed in **setup.py** in **entry_points**.
The name of the entry_points group is **invenio_oarepo_oai_pmh_harvester.parsers**.

Example entry_points:

.. code-block:: python

    setup(
        ...
        entry_points={
            'invenio_oarepo_oai_pmh_harvester.parsers': [
                'xoai = example.parser'
            ]
        }
        ...
    )

The parser function itself must be registered with the decorator **@Decorators.parser("name", "provider_code")**.

Example of an entire module with a parser:

.. code-block:: python

    from collections import defaultdict

    from invenio_oarepo_oai_pmh_harvester.register import Decorators


    def xml_to_dict_xoai(tree):
        tree_dict = defaultdict(list)
        children = list(tree)
        if len(children) == 0:
            return tree.text
        for child in children:
            name = child.get("name")
            tree_dict[name].append(xml_to_dict_xoai(child))
        remove_key(tree_dict, "none")
        remove_key(tree_dict, "null")
        remove_key(tree_dict, None)
        tree_dict.pop("none", True)
        tree_dict.pop("null", True)
        tree_dict.pop(None, True)
        return tree_dict


    @Decorators.parser("xoai", "uk")
    def parser_refine(etree):
        return xml_to_dict_xoai(list(list(etree)[1])[0])


    def remove_key(tree_dict, key):
        if key in tree_dict:
            for item in tree_dict[key]:
                for k, v in item.items():
                    tree_dict[k].append(v)

Rules
------

The parser converts XML to JSON, the library then transforms this JSON into our desired output. Rules are needed
for this transformation. A rule is a function that gets one field and transforms it into a field according to our
internal rules. The rule function must take these arguments **(paths, el, results, phase, \*\*kwargs)**.
In most cases, not all the information is needed and only these arguments (el, results, * args, ** kwargs) are
enough for the function.

* **el** - element, it is part of the JSON file we want to work with. E.g. the language may be indicated as follows:

    .. code-block:: json

        {
            ...
            "language": ["en", "cs"]
            ...
        }

    In this case we get a python list. el = ["en", "cs"]

* **results** - list of dictionaries - here we want to save the results from the rule. We always store the results in **results[-1]["field_name_in_our_json"]**.

**Rule registration**

The rule function must be registered. The rule is registered using decorators. **@Decorators.rule("name of parser")**
registers the function as a rule, as the decorator argument we have to specify the designation of the parser
(we registered it with the @Decorators.parser decorator).

We must call the module where the rule is stored from entry_points so that the library knows about the rule.
Entrypoint group for rules is: **'invenio_oarepo_oai_pmh_harvester.rules'**. Example of entry_points for rules.:

.. code-block:: python

    entry_points={
        ...
        'invenio_oarepo_oai_pmh_harvester.rules': [
            'abstract = example.rules.uk.abstract',
            'contributor = example.rules.uk.contributor',
            'creator = example.rules.uk.creator',
            'date_accepted = example.rules.uk.date_accepted',
            'defended = example.rules.uk.defended',
            'degree_grantor = example.rules.uk.degree_grantor',
            'doctype = example.rules.uk.doctype',
            'identifier = example.rules.uk.identifier',
            'language = example.rules.uk.language',
            'study_field = example.rules.uk.study_field',
            'subject = example.rules.uk.subject',
            'title = example.rules.uk.title',
        ]
        ...
    }

**JSON source processing phase**

The individual fields / addresses of the source JSON file are processed sequentially according to the depth-first
algorithm. Sometimes, a field may require information from another field that has not yet been processed and we do not
currently have that information. For such cases, we distinguish two stages of processing. If no further information is
required, the so-called **PRE** phase is used and the field is processed immediately. In cases where we need additional
information, the so-called **POST** phase is used. In this case, we will already have the information from the **PRE**
phase stored in the results and we will be able to use it.

Therefore, the rule function requires the determination of the PRE/POST phase, which is done using the
**@Decorators.pre_rule/post_rule("path in source JSON")**

Example of whole rule function:

.. code-block:: python

    @Decorators.rule("xoai")
    @Decorators.pre_rule("/dc/subject")
    def transform_subject(paths, el, results, phase, **kwargs):
        keywords = []
        cz_keywords = el.get("cs_CZ")
        if cz_keywords:
            cz_list = cz_keywords[0]["value"]
            for k in cz_list:
                if k is None:
                    continue
                keywords.append({
                    "value": k,
                    "lang": "cze"
                })
            assert isinstance(cz_list, list)
        en_keywords = el.get("en_US")
        if en_keywords:
            en_list = en_keywords[0]["value"]
            for k in en_list:
                if k is None:
                    continue
                keywords.append({
                    "value": k,
                    "lang": "eng"
                })
            assert isinstance(en_list, list)
        if keywords:
            results[-1]["keywords"] = keywords
        return OAITransformer.PROCESSED


The rule function must return the **OAITransformer.PROCESSED** constant. If it does not return it, the transformer throws
a ValueError exception with a path description in the source JSON file. So all paths must have their function rules
or be listed in the initializer when synchronizing as unhandled_paths.