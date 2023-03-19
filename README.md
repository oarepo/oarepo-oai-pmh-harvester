# OARepo OAI-PMH harvester

An OAI-PMH harvesing library for Invenio 3.5+. The library provides initial transformation 
of OAI-PMH payload to an intermediary json representation which is later on transformed by 
a specific transformer to the format of invenio records.

Due to their generic nature, these transformers are not part of this library but have to be 
provided by an application.

The progress and transformation errors are captured within the database.

For now, the library does not provide error notifications, but these will be added. Sentry might 
be used for the logging & reporting.

## Installation

```bash
pip install oarepo-oaipmh-harvester
pip install <your transformer library>
```

## Configuration

All configuration is inside the `OAIHarvesterRecord` record.
There is a command-line tool to add a new record:

```bash
invenio oarepo oai harvester add nusl \
    --name "NUSL harvester" \
    --url http://invenio.nusl.cz/oai2d/ \
    --set global \
    --prefix marcxml \
    --loader sickle \
    --transformer marcxml \
    --transformer nusl \
    --writer 'service{service=nr_documents}'
```

This will register an oai-pmh harvester with code "nusl",
its url, oai set and metadata prefix. Records from this
harvester will be loaded with the sickle loader (default loader 
if not specified) and at first transformed from marcxml to
json format and subsequently by NUSL transformer to get
nr_documents compatible json.

The json is then used by service writer to create/update
the target record.

## Usage

### Command-line

On command line, invoke

```bash
invenio oarepo oai harvester run nusl <optional list of oai identifiers to harvest>
```

Options:

```text
  --all-records      Re-harvest all records, not from the last timestamp
  --on-background    Run harvest on background (via celery task)
  --identifier       Harvest the passed identifier/s
```

You can also pass arguments for "havester add" to override the defaults from the configuration.

## Harvest status

Harvester uses 3 additional types of record:

* Run represents a single run of the harvester
* Batch - the run consists of multiple batches, that is records, that are processed together.
    Each such batch is represented in the `batch` record
* OAI record is a link between harvested record and its original. If there are errors harvesting
    the record, it is still created and its `errors` field is filled with the error 

## Custom parsers and transformers

### Transformer

A piece of code that gets a StreamEntry (or a StreamBatch) instance, processes it and returns modified
StreamEntry. An example is a MarcXML transformer that takes the string with xml representation of the
entry and transforms it into simple json representation `{abcxy: value(s)}`, where abcxy is marc field code.

See `oarepo_runtime.datastream.transformers` package for StreamEntry/StreamBatch interfaces.

The transformer needs to be registered:

```python
# mypkg.transformers

from .impl import MyTransformer

my_transformer = {"class": MyTransformer, "params": {
       # default parameters that will go to the MyTransformer constructor
}}
```

And setup.cfg:

```ini
# setup.cfg

[options.entry_points]
oarepo.oaipmh.transformers =
    my_transformer = mypkg.transformers:my_transformer
```

Then you can use `my_transformer` when creating your harvester.

### Reader

A reader is responsible for fetching records and creating a stream of StreamEntry items.
See `oarepo_runtime.datastreams.readers` for details. Then register the reader into 
`oarepo.oaipmh.readers` entry point with the same syntax as above.