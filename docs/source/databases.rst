======================
Databases and Alembic
======================

Entrypoints
============

Database models and the Alembic migration script folder must be registered at entrypoints in setup.py.

.. code-block:: python

    setup(
    entry_points={
        'invenio_db.models': [
            'invenio_oarepo_oai_pmh_harvester = invenio_oarepo_oai_pmh_harvester.models',
        ],
        'invenio_db.alembic': [
            'invenio_oarepo_oai_pmh_harvester = invenio_oarepo_oai_pmh_harvester:alembic',
        ],
    },
    )

Alembic
========
For more details please see: `Invenio_DB documentation <https://invenio-db.readthedocs.io/en/latest/alembic.html>`_

Init models
------------

1. We will make sure there are no migrations.

    .. code-block:: bash

        invenio alembic upgrade heads

    In order to integrate alembic when there is already a DB in place, we have to create an alembic_version table stamped
    with the revisions matching the current state of the DB:

    .. code-block:: bash

        invenio alembic stamp

2. Each module should have its own branch where its revisions are stored, so we create a new branch. The branch should have its parent. In this case, we want to start from a clean Invenio database that has a revision labeled ``dbdbc1b19cf2``.

    | -b: branch name
    | -p: parent revision
    | --empty: create empty migration script


    .. code-block:: bash

        invenio alembic revision "Create oai client branch" -b invenio_oarepo_oai_pmh_harvester -p dbdbc1b19cf2 --empty

3. Make sure all migrations are up to date and that we have applied our empty migration.

    .. code-block:: bash

        invenio alembic upgrade heads

4. Now edit the database model and create a revision after editing. In the revision we have to specify the parents and the absolute path to the alembic folder (where the migration scripts are stored)

    | -p: parent revision code (it is the revision created before this step, and should be stored in alembic folder)
    | --path: absolute path to the alembic folder (relative path should also work, but the absolute path is unique).

    .. code-block:: bash

     invenio alembic revision "Init OAI Models" --path "/home/semtex/GoogleDrive/Projekty/Pracovní/nusl/invenio-oarepo-oai-pmh-harvester/invenio_oarepo_oai_pmh_harvester/alembic" -p 795da8efcb34

5. Check the created migration script in the alembic folder and apply it with the command:

    .. code-block:: bash

     invenio alembic upgrade heads

Update models
--------------

If you modify the model, repeat steps 4 and 5.