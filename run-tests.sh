#!/bin/bash

set -e

OAREPO_VERSION="${OAREPO_VERSION:-11}"

BUILDER_VENV=.venv-builder
if test -d $BUILDER_VENV ; then
	rm -rf $BUILDER_VENV
fi

python3 -m venv $BUILDER_VENV
. $BUILDER_VENV/bin/activate
pip install -U setuptools pip wheel
pip install -U oarepo-model-builder

if test -d test-model ; then
  rm -rf test-model
fi

oarepo-compile-model ./tests/test-model.yaml --output-directory test-model -vvv

VENV=".venv"

if test -d $VENV ; then
  rm -rf $VENV
fi

python3 -m venv $VENV
. $VENV/bin/activate
pip install -U setuptools pip wheel

pip install "oarepo>=${OAREPO_VERSION},<${OAREPO_VERSION%%.*}.9999"
pip install -e ".[tests]"
pip install -e test-model

pip uninstall -y uritemplate
pip install uritemplate

invenio index destroy --force --yes-i-know || true

pytest tests
