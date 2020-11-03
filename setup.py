# -*- coding: utf-8 -*-


"""oarepo OAI-PMH converter."""
import os

from setuptools import find_packages, setup

extras_require = {
    "devel": ['oarepo>=3.3.0.4, <3.4.0.0'],
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
with open(os.path.join('oarepo_oai_pmh_harvester', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='oarepo-oai-pmh-harvester',
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
            'oarepo_oai_pmh_harvester = oarepo_oai_pmh_harvester.models',
        ],
        'invenio_db.alembic': [
            'oarepo_oai_pmh_harvester = oarepo_oai_pmh_harvester:alembic',
        ],
        'flask.commands': [
            'oai = oarepo_oai_pmh_harvester.cli:oai'
        ],
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
