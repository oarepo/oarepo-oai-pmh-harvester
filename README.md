# oarepo-oai-pmh-harvester
OAI-PMH Client for Invenio under OArepo brand.

[![Build Status](https://travis-ci.org/oarepo/oarepo-oai-pmh-harvester.svg?branch=master)](https://travis-ci.org/oarepo/oarepo-oai-pmh-harvester)
[![Coverage Status](https://coveralls.io/repos/github/oarepo/oarepo-oai-pmh-harvester/badge.svg?branch=master)](https://coveralls.io/github/oarepo/oarepo-oai-pmh-harvester?branch=master)
[![image][4]][5]
[![image][6]][7]
[![image][8]][9]

  [4]: https://img.shields.io/github/tag/oarepo/oarepo-oai-pmh-harvester.svg
  [5]: https://github.com/oarepo/oarepo-oai-pmh-harvester/releases
  [6]: https://img.shields.io/pypi/dm/oarepo-oai-pmh-harvester.svg
  [7]: https://pypi.python.org/pypi/oarepo-oai-pmh-harvester
  [8]: https://img.shields.io/github/license/oarepo/oarepo-oai-pmh-harvester.svg
  [9]: https://github.com/oarepo/oarepo-oai-pmh-harvester/blob/master/LICENSE

## Installation

Library is stored in PyPi repository, so it is commonly installed through pip.

```
pip install oarepo-oai-pmh-harvester
```

## Configuration

Data harvesting must be set in the configuration (invenio.cfg or via app.config). All settings are made via the OAREPO_OAI_PROVIDERS key. Config is a dictionary where the key is the provider code and each provider can have several individual settings / jobs called synchronizer.

```python
OAREPO_OAI_PROVIDERS={
            "provider-name": {
                "description": "Short provider description",
                "synchronizers": [
                    {
                        "name": "xoai",
                        "oai_endpoint": "https://example.com/oai/",
                        "set": "example_set",
                        "metadata_prefix": "oai_dc",
                        "bulk": True,
                        "from": "latest",
                        "unhandled_paths": ["/dc/unhandled"],
                        "default_endpoint": "recid",
                        "endpoint_mapping": {
                            "field_name": "doc_type",
                            "mapping": {
                                "record": "recid"
                            }
                        },
                    }
                ]
            },
        }
```
**Parameters**:
* description: Test description of provider
* synchronizers: Dictionary with individual settings
    * **name**: name of the setting/synchronizer
    * **oai_endpoint**: URL adress
    * **set**: name of OAI set
    * **metadata_prefix**: name of OAI metadata prefix
    * **bulk**: if bulk is True, the records are requested by ListRecords method (OAI-PMH protocol), if bulk is False
     every record is requested by GetRecord method(OAI-PMH protocol). Default is True.
    * **from**: the date from which the synchronization starts, it is optional parameter with three options:
    
        1. **latest**: checks for changes since the last sync
        1. **date** [YYYY-MM-DD]: check for change since entered date
        1. **none**: parameter is omitted, then start full synchronization  
    * **unhandled_paths**: List of paths in json that are not handled by any rule.It must be specified, otherwise the client will report an error that the path was not processed by any rule.
    * **default_endpoint**: The name of the end_point defined in RECORDS_REST_ENDPOINTS from the invenio-records-rest
     library, which will be used as the base unless otherwise specified.
   * **endpoint_mapping**: If multiple invenio-records-rest endpoints are used, it is necessary to set rules for
    which endpoint will be assigned to a particular record. In most cases, an endpoint can be assigned based on a
     metadata field (***field_name***) that is assigned a dictionary ***mapping***, where key is the value of the
      metadata field and the dictionary value is assigned to the endpoint.
      
### Endpoint handler

If endpoint_mapping cannot be expressed using a dictionary, it is possible to use a handler. Handler is a function
 that receives already transformed data and returns the name rest endpoint. It is registered as entry_point
  (***oarepo_oai_pmh_harvester.mapping***) and using the endpoint_handler decorator. More in the example.
  
```python
entry_points={
       'oarepo_oai_pmh_harvester.mapping': [
           '<name> = example.endpoint_handler',
       ],
   }

```

```python
@endpoint_handler(<provider>, <metadataprefix>)
def mapping_handler(data):
    resource = data.get("resource"):
    if resource == "book":
        return "book_model"
    elif resource == "journal":
        return "journal"
    else:
        return "recid"

```

## Usage

The package is used to integrate the OAI-PMH client into Invenio. It is a wrapper that is built on the Sickle library.
Provides integration with invenio-records. The purpose of the package is to ensure synchronization with a remote OAI-PMH source.

Successful data collection requires several steps, which consist of:

1. **Configuration** (see configuration chapter)
1. **Parser**: function that converts XML into JSON
1. **Rules**: functions that convert raw JSON (from parser) into final JSON
1. **Processors (optional)**: two type of function (pre and post), that enable change data either before
 transformation (pre_processor) or after transformation (post_processor)

### Parsers

A function that transforms XML into JSON (implemented as a python dictionary). The module where the function is located must be specified in entry_points and the function itself marked with a decorator. The function takes **lxml.etree._Element** as an argument and returns a dictionary.

* **entry_points**:

The module is registered in entry_points under the keyword ***oarepo_oai_pmh_harvester.parsers***, for example as
 follows: 
 
 ```python
entry_points={
        'oarepo_oai_pmh_harvester.parsers': [
            'xoai = example.parser',
        ],
    }
```

* **decorator**:
The decorator has one parameter, the name of the metadata_format and that must be same as in config metadata_prefix. The function must accept one positional argument (etree._Element) and return a dictionary.

```python
from oarepo_oai_pmh_harvester.decorators import parser

@parser("xoai")
def xml_to_json_parser(etree):
    ...some magic
    return dict_
```

### Rules

The raw parsed JSON is converted to the final JSON in the transformation. The built-in transformer recursively
 traverses the raw JSON and remaps the raw JSON to the final JSON. The transformer searches all paths to see if a
  rule exists for that path or if the path is in an **unhandled path** in the configuration. If it does not meet any
   of the conditions, it raises an error to warn the user that he has forgotten about a metadata field.
   
A rule is a function that accepts the el (element) and kwargs (name parameters) arguments and returns the reworked
 element as a python dictionary. The module that contains the rule must be specified in entry_points and the function itself must be registered using a decorator.
 
* **entry_points**:

The module is registered in entry_points under the keyword ***oarepo_oai_pmh_harvester.rules***, for example as
 follows: 
 
 ```python
entry_points={
        'oarepo_oai_pmh_harvester.rules': [
            'xoai = example.rule',
        ],
    }
```

* **decorator**:

The decorator has four positional arguments and one named argument:
1. provider_name: must be same as in config
2. metadata_prefix: must be same as in config
3. json_path: level is separated with "/"
4. phase: 
    * pre: the rule is applied during the creation of the final JSON.
    * post: the rule is applied after the all pre rules

     
The rule function itself must accept the el (element) and ** kwargs arguments in the signature. El is the JSON value
 at the given JSON address. It must return dictionary (eg: {"title": "Example title"})
 
 Kwargs contain several useful variables:
 * ***paths***: a set containing an absolute JSON path and all subsequent relative levels path eg (/dc/title/en, dc
 /title/en, title/en, en)
 * ***results***: a list of individual results, which will make up the final JSON.
 * ***phase***: pre or post phase
 * ***record***: raw json as defaultdict
 
 Example of a rule:

```python
from oarepo_oai_pmh_harvester.decorators import rule


@rule("provider_name", "metadata_prefix", "/dc/title/en", phase="pre")
def rule(el, **kwargs):
    value_ = el[0]["value"][0]
    return {"title": value_}
```
### Processors
The downloaded XML is first converted to JSON and then this JSON is remapped to JSON according to our model
. Sometimes it is necessary to modify the input or output JSON and the **Processors** are used for this purpose
. There are two types of processors pre and post.

#### Pre-processor
It is used for updating data before transformation. Pre processor is registered similarly as other components. It is
 necessary to register entry point and mark function with decorator.
 
  ```python
entry_points={
        'oarepo_oai_pmh_harvester.pre_processors': [
            '<name> = example.pre_processors',
        ],
    }
```

 Example of a pre_processor:

```python
from oarepo_oai_pmh_harvester.decorators import pre_processor


@pre_processor("provider_name", "metadata_prefix")
def pre_processor_1(data):
    data = data.update({"some_change": "change"})
    return data
```

#### Post-processor
It is used for updating data after transformation.
 
  ```python
entry_points={
        'oarepo_oai_pmh_harvester.post_processors': [
            '<name> = example.post_processors',
        ],
    }
```

 Example of a pre_processor:

```python
from oarepo_oai_pmh_harvester.decorators import post_processor


@post_processor("provider_name", "metadata_prefix")
def pre_processor_1(data):
    data = data.update({"some_change_2": "change_2"})
    return data
```
 

### CLI
If all components (config, parser, rules) are set, the program can be run via the CLI:

```bash
Usage: invenio oai run [OPTIONS]

  Starts harvesting the resources set in invenio.cfg through the
  OAREPO_OAI_PROVIDERS environment variable.

Options:
  -p, --provider TEXT           Code name of provider, defined in invenio.cfg
  -s, --synchronizer TEXT       Code name of OAI-PMH setup, defined in
                                invenio.cfg

  --break / --no-break          Break on error, if true program is terminated
                                when record cause error

  -o, --start_oai TEXT          OAI identifier from where synchronization
                                begin

  -i, --start_id INTEGER        The serial number from which the
                                synchronization starts. This is useful if for
                                some reason the previous synchronization was
                                interrupted at some point.

  -a, --oai TEXT                OAI identifier that will be fetched and
                                synchronized. The field is repeatable. If this
                                option is used, the provider and synchronizer
                                must be specified and star_id or start_oai
                                must not be used

  --overwrite / --no-overwrite  Overwriter record with the same timestamp.
                                Default option is false

  --help                        Show this message and exit.


```
