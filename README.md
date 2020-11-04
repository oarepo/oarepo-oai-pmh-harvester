# oarepo-oai-pmh-harvester
OAI-PMH Client for Invenio under OArepo brand.

## Installation

bla

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

## Usage

The package is used to integrate the OAI-PMH client into Invenio. It is a wrapper that is built on the Sickle library.
Provides integration with invenio-records. The purpose of the package is to ensure synchronization with a remote OAI-PMH source.

### Parsers

### Rules

### CLI