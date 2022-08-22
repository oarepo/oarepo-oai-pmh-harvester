from invenio_app.factory import create_app

def celery():
    app = create_app()
    celery_ext = app.extensions['invenio-celery']

    celery = celery_ext.celery
