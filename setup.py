# -*- coding: utf-8 -*-


"""oarepo OAI-PMH converter."""
import os

from setuptools import find_packages, setup

tests_require = [
    'pytest',
    'pytest-cov',
    'oarepo'
]

extras_require = {
    "tests": tests_require,
    "postgresql": ["psycopg2-binary"],
    "sqlite": []
}

setup_requires = [
    'pytest-runner>=2.7',
]

install_requires = [
    'sickle',
    'click',
    'boltons'
]

with open("README.md", "r") as f:
    long_description = f.read()

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('oarepo_oai_pmh_harvester', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='oarepo-oai-pmh-harvester',
    version=version,
    description=__doc__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='invenio oarepo oai pmh harvester',
    license='MIT',
    author='Daniel Kopecký',
    author_email='Daniel.Kopecky@techlib.cz',
    url='',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'invenio_db.models': [
            'oarepo_oai_pmh_harvester = oarepo_oai_pmh_harvester.models',
        ],
        'invenio_db.alembic': [
            'oarepo_oai_pmh_harvester = oarepo_oai_pmh_harvester:alembic',
        ],
        'flask.commands': [
            'oai = oarepo_oai_pmh_harvester.cli:oai'
        ],
        'invenio_base.api_apps': [
            'oarepo_oai_pmh_harvester = oarepo_oai_pmh_harvester.ext:OArepoOAIClient',
        ],
        'invenio_base.apps': [
            'oarepo_records_draft = oarepo_oai_pmh_harvester.ext:OArepoOAIClient'
        ]
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
)
