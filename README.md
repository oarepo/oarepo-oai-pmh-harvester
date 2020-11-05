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
                        "unhandled_paths": ["/dc/unhandled"],
                        "default_endpoint": "recid",
                        "use_default_endpoint": True,
                        "endpoint_mapping": {
                            "field_name": "doc_type",
                            "mapping": {
                                "record": "recid"
                            }
                        }
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
    * **unhandled_paths**: List of paths in json that are not handled by any rule.It must be specified, otherwise the client will report an error that the path was not processed by any rule.
    * **default_endpoint**: The name of the end_point defined in RECORDS_REST_ENDPOINTS from the invenio-records-rest
     library, which will be used as the base unless otherwise specified.
   * **endpoint_mapping**: If multiple invenio-records-rest endpoints are used, it is necessary to set rules for
    which endpoint will be assigned to a particular record. In most cases, an endpoint can be assigned based on a
     metadata field (***field_name***) that is assigned a dictionary ***mapping***, where key is the value of the
      metadata field and the dictionary value is assigned to the endpoint.

## Usage

The package is used to integrate the OAI-PMH client into Invenio. It is a wrapper that is built on the Sickle library.
Provides integration with invenio-records. The purpose of the package is to ensure synchronization with a remote OAI-PMH source.

Successful data collection requires several steps, which consist of:

1. **Configuration** (see configuration chapter)
1. **Parser**: function that converts XML into JSON
1. **Rules**: functions that convert raw JSON (from parser) into final JSON

### Parsers


### Rules

### CLI