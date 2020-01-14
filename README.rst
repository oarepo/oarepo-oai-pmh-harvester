===============================
Invenio-NUSL-OAI-PMH Harvester
===============================

.. image:: https://img.shields.io/github/license/oarepo/flask-taxonomies.svg
        :target: https://github.com/oarepo/flask-taxonomies/blob/master/LICENSE

.. image:: https://img.shields.io/travis/oarepo/flask-taxonomies.svg
        :target: https://travis-ci.org/oarepo/flask-taxonomies

.. image:: https://img.shields.io/coveralls/oarepo/flask-taxonomies.svg
        :target: https://coveralls.io/r/oarepo/flask-taxonomies

.. image:: https://img.shields.io/pypi/v/flask-taxonomies.svg
        :target: https://pypi.org/pypi/flask-taxonomies




Quickstart
----------

Run the following commands to bootstrap your environment ::

    TODO: doplnit

Once you have installed your DBMS, run the following to create your app's
database tables and perform the initial migration ::

    invenio db init create
    invenio alembic upgrade heads
    invenio run

If you already have database installed follow next procedure,
for more information please see Invenio-DB documentation (https://invenio-db.readthedocs.io/en/latest/alembic.html)  ::

    invenio alembic stamp
    invenio alembic revision "Create invenio_nusl_oai_pmh_harvester branch." -b invenio_nusl_oai_pmh_harvester -p dbdbc1b19cf2 --empty
    invenio alembic upgrade heads
    invenio alembic revision "Create tables"  -b invenio_nusl_oai_pmh_harvester
    invenio alembic upgrade heads

Python Usage
------------
