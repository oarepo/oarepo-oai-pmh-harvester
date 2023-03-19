#!/bin/bash

celery --app invenio_app.celery worker --events --loglevel INFO