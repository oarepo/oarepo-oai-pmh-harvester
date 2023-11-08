#!/bin/bash

# This script is used to generate the translations for the project.
cd "$(dirname "$0")" || exit 1

source .venv/bin/activate

pybabel extract -F babel.ini -k lazy_gettext -o oarepo_oaipmh_harvester/ui/translations/messages.pot oarepo_oaipmh_harvester

cd oarepo_oaipmh_harvester/ui/translations || exit 1

pybabel update --no-fuzzy-matching -i messages.pot -d .

pybabel compile -d .