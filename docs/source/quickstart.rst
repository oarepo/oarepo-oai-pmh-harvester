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

bla