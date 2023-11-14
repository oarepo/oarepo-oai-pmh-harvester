set -e

rm -rf .venv-builder
python3 -m venv .venv-builder

.venv-builder/bin/pip install -U pip setuptools wheel
.venv-builder/bin/pip install 'oarepo-model-builder>=4.0.0' oarepo-model-builder-relations oarepo-model-builder-ui

rm -rf oarepo_oaipmh_harvester/oai_harvester
rm -rf oarepo_oaipmh_harvester/oai_run
rm -rf oarepo_oaipmh_harvester/oai_batch
rm -rf oarepo_oaipmh_harvester/oai_record

.venv-builder/bin/oarepo-compile-model models/oaipmh_harvester.yaml --output-directory . -vvv
.venv-builder/bin/oarepo-compile-model models/oaipmh_run.yaml --output-directory . \
    --include oaipmh-harvester=oarepo_oaipmh_harvester/oai_harvester/models/records.json -vvv
.venv-builder/bin/oarepo-compile-model models/oaipmh_batch.yaml --output-directory . \
    --include oaipmh-harvester=oarepo_oaipmh_harvester/oai_harvester/models/records.json \
    --include oaipmh-run=oarepo_oaipmh_harvester/oai_run/models/records.json -vvv
.venv-builder/bin/oarepo-compile-model models/oaipmh_record.yaml --output-directory . \
    --include oaipmh-batch=oarepo_oaipmh_harvester/oai_batch/models/records.json  \
    --include oaipmh-harvester=oarepo_oaipmh_harvester/oai_harvester/models/records.json \
    --include oaipmh-run=oarepo_oaipmh_harvester/oai_run/models/records.json -vvv
