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

## Usage

### Command-line

On command line, invoke

```bash
oaiharvester harvest nusl
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

## Custom parsers and transformers

### Transformer

### Parser