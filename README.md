# OARepo OAI-PMH harvester

An OAI-PMH harvesing library for Invenio 3.5+. The library provides initial transformation of OAI-PMH payload to an
intermediary json representation which is later on transformed by a specific transformer to invenio records.

Due to their generic nature, these transformers are not part of this library but have to be provided by an application.

The progress and transformation errors are captured within the database.

For now, the library does not provide error notifications, but these will be added. A sentry might be used for the
logging & reporting.

## Installation

```bash
poetry add oarepo-oaipmh-harvester
```

## Configuration

All configuration is inside the database model `OAIHarvesterConfig`.
There is a command-line tool to add a new config:

```bash
invenio oaiharvester add \
  --code nusl \
  --name NUŠL \
  --url "http://invenio.nusl.cz/oai2d/" \
  --set global \
  --prefix marcxml 
  --transformer nusl_oai.transformer.NuslTransformer
```

This will register an oai-pmh harvester with code "nusl",
its url, oai set and metadata prefix. Records from this
harvester will be transformed by the NuslTransformer before
they are written to the repository.

Options:

```bash
Usage: invenio oaiharvester add [OPTIONS]

Options:
  --code TEXT         OAI server code  [required]
  --name TEXT         OAI server name  [required]
  --url TEXT          OAI base url  [required]
  --set TEXT          OAI set  [required]
  --prefix TEXT       OAI metadata prefix  [required]
  --parser TEXT       OAI metadata parser. If not passed, a prefix-based default is used
  --transformer TEXT  Transformer class  [required]
```

## Usage

### Command-line

On command line, invoke

```bash
oaiharvester harvest nusl <optional list of oai identifiers to harvest>
```

Options:

```text
  -a, --all-records  Re-harvest all records, not from the last timestamp
  --background       Start Harvest on background (via celery task), return immediately
  --dump-to TEXT     Do not import records, just dump (cache) them to this
                     directory (mostly for debugging)
  --load-from TEXT   Do not contact oai-pmh server but load the records from
                     this directory (created by dump-to option)
```

### Celery task

```python3
@shared_task
def oai_harvest(
        harvester_id: str, 
        start_from: str, 
        load_from: str = None, 
        dump_to: str = None,
        on_background=False, 
        identifiers=None):
    """
    @param harvester_id: id of the harvester configuration (OAIHarvesterConfig) object
    @param start_from: datestamp (either YYYY-MM-DD or YYYY-MM-DDThh:mm:ss, 
           depends on the OAI endpoint), inclusive
    @param load_from: if set, a path to the directory on the filesystem where 
           the OAI-PMH data are present (in *.json.gz files)
    @param dump_to: if set, harvested metadata will be parsed from xml to json 
           and stored into this directory, not to the repository
    @param on_background: if True, transformation and storage will be started in celery tasks and can run in parallel.
           If false, they will run sequentially inside this task
    @param identifiers: if load_from is set, it is a list of file names within the directory. 
           If load_from is not set, these are oai identifiers for GetRecord. If not set at all, all records from 
           start_from are harvested 
    """
```

## Harvest status

Each harvest creates a row in `OAIHarvestRun` database
table containing first and last datestamps and harvest
status (running, completed, errored, ...)

A run is split into a chunk of records and each chunk
is represented in `OAIHarvestRunBatch` database table.
It contains a chunk status (running, completed, warning,
failed, ...) and a list of identifiers harvested and 
their status (ok, warning during harvesting the identifier,
harvesting the identifier failed). The table also contains
details of the warnings/errors.

## Custom parsers and transformers

The input OAI xml is at first parsed via parsers into
a json format.

MARC-XML and DC parsers are supported out of the box.
See the section below if you need a different parser

The JSON is then transformed into an invenio record
via a transformer class. As different repositories
use different semantic of fields (even in MARC),
this step can not be generic and implementor is required
to provide his/her own transformer class.

### Transformer

A simple transformer, that transforms just the title from MARC-XML
input might look like:

```python3
from typing import List
from oarepo_oaipmh_harvester import OAITransformer, OAIRecord, OAIHarvestRunBatch

from my_record.proxies import current_service
from my_record.records.api import MyRecord

class NuslTransformer(OAITransformer):
    oaiidentifier_search_property = 'metadata_systemIdentifiers_identifier'
    # the name of service filter that accesses the record's OAI identifier
    oaiidentifier_search_path = ('metadata', 'systemIdentifiers', 'identifier')
    # path to the oai record identifier inside the record

    # invenio service that will be used to create/update the record
    record_service = current_service
    # invenio record for this record
    record_model = MyRecord 
    

    def transform_single(self, rec: OAIRecord):
        # add all your transformations here
        rec.transformed.update({
            'metadata': {
                'title': rec['24500a']
            }
        })
```

### Parser

A parser is responsible for transforming the XML document
into an intermediary JSON.

For implementation details see [MarcxmlParser](./oarepo_oaipmh_harvester/parsers.py).