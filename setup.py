# -*- coding: utf-8 -*-


"""oarepo OAI-PMH converter."""

from setuptools import find_packages, setup

extras_require = {
    "devel": ["oarepo[deploy]==3.2.0.2a9"],
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
]

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
version = "1.0.0"

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
            'oai = invenio_oarepo_oai_pmh_harvester.cli:oai',
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
