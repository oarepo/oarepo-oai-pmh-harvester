set -e

rm -rf .venv-builder
python3 -m venv .venv-builder

.venv-builder/bin/pip install -U pip setuptools wheel
.venv-builder/bin/pip install 'oarepo-model-builder>=4.0.0' oarepo-model-builder-relations oarepo-model-builder-ui

rm -rf oarepo_oaipmh_harvester/oai_harvester

.venv-builder/bin/oarepo-compile-model models/oaipmh_harvester.yaml --output-directory . -vvv
