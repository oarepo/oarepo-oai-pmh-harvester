set -e

rm -rf .venv-builder-models
python3 -m venv .venv-builder-models

.venv-builder-models/bin/pip install -U pip setuptools wheel
.venv-builder-models/bin/pip install 'oarepo-model-builder>=4.0.0' oarepo-model-builder-relations oarepo-model-builder-ui

# local development
.venv-builder-models/bin/pip install -e ../oarepo-model-builder-relations

rm -rf oarepo_oaipmh_harvester/oai_harvester

if [ -d /tmp/oai_harvester ]; then
  rm -rf /tmp/oai_harvester
fi

# Compile the model
.venv-builder-models/bin/oarepo-compile-model models/oaipmh_harvester.yaml --output-directory /tmp/oai_harvester -vvv


# Copy the compiled model to the current directory
cp -r /tmp/oai_harvester/oarepo_oaipmh_harvester/oai_harvester oarepo_oaipmh_harvester/oai_harvester