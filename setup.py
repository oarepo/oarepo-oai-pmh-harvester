# -*- coding: utf-8 -*-


"""oarepo OAI-PMH converter."""
import os

from setuptools import find_packages, setup

extras_require = {
    "devel": ['oarepo[deploy-es7,taxonomies,draft]>=3.2.1.2'],
    "docs": ["sphinx"]
}
tests_require = [
    'pytest',
    'pytest-cov'
]

setup_requires = [
    'pytest-runner>=2.7',
]

install_requires = [
    'sickle',
    'click',
    'jmespath',
    'prettytable',
    'flask',
    'sqlalchemy',
    'invenio-records'
]

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('invenio_oarepo_oai_pmh_harvester', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='invenio-oarepo-oai-pmh-harvester',
    version=version,
    description=__doc__,
    # long_description=,
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
            'invenio_oarepo_oai_pmh_harvester = invenio_oarepo_oai_pmh_harvester.models',
        ],
        'invenio_db.alembic': [
            'invenio_oarepo_oai_pmh_harvester = invenio_oarepo_oai_pmh_harvester:alembic',
        ],
        'flask.commands': [
            'nusl = example.cli:nusl',
        ],
        'invenio_oarepo_oai_pmh_harvester.parsers': [
            'xoai = example.parser'
        ],
        'invenio_oarepo_oai_pmh_harvester.rules': [
            'abstract = example.rules.uk.abstract',
            'contributor = example.rules.uk.contributor',
            'creator = example.rules.uk.creator',
            'date_accepted = example.rules.uk.date_accepted',
            'defended = example.rules.uk.defended',
            'degree_grantor = example.rules.uk.degree_grantor',
            'doctype = example.rules.uk.doctype',
            'identifier = example.rules.uk.identifier',
            'language = example.rules.uk.language',
            'study_field = example.rules.uk.study_field',
            'subject = example.rules.uk.subject',
            'title = example.rules.uk.title',
        ]
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Development Status :: 3 - Planning',
    ],
)
