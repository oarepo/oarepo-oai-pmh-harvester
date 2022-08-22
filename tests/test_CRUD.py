from time import sleep

from oarepo_oaipmh_harvester.cli import add
from oarepo_oaipmh_harvester.cli import _add, _harvest
from oarepo_oaipmh_harvester.oaipmh_record.proxies import current_service as record_service
from oarepo_oaipmh_harvester.nr_theses_metadata.proxies import current_service as theses_service
# from oarepo_oaipmh_harvester.oaipmh_config.proxies import current_service as config_service
from invenio_access.permissions import system_identity
# from ..nusl_oai.tran
# from oarepo_oaipmh_harvester.nusl_oai import NuslTransformer


def test_create_from_service(config_service,config_data, identity):

    harvester = config_service.create(identity, {'metadata': config_data})
    print(harvester)

def test_cmd(cli_runner, db, es):


    #shoud not be possible to make two harvesters with the same code
    #
    # result = cli_runner(add, 'nusl', '--code', 'nusl', '--name', 'NUŠL', '--url', 'http://invenio.nusl.cz/oai2d/',
    #                         '--set', 'global', '--prefix', 'marcxml', '--transformer',
    #                         'nusl_oai.transformer.NuslTransformer')
    result = _add(code='nusl', name='NUŠL', url='http://invenio.nusl.cz/oai2d/', set='global', prefix='marcxml',
                  parser=None,
                  transformer='nusl_oai.transformer.NuslTransformer')
    print(result)
    # assert result.exit_code == 0
    # db.session.commit()
    # db.session.expunge_all()
    # db.session.close()
    #
    # with db.session.begin():
    # result = cli_runner(add, 'nusl', '--code', 'nusl2', '--name', 'NUŠL', '--url', 'http://invenio.nusl.cz/oai2d/',
    #                     '--set', 'global', '--prefix', 'marcxml', '--transformer',
    #                     'nusl_oai.transformer.NuslTransformer')
    # assert result.exit_code == 0
    result = _add(code='nusl2', name='NUŠL', url='http://invenio.nusl.cz/oai2d/', set='global', prefix='marcxml', parser = None,
                  transformer='nusl_oai.transformer.NuslTransformer')

    result = cli_runner(add, 'nusl', '--code', 'nusl2', '--name', 'NUŠL', '--url', 'http://invenio.nusl.cz/oai2d/',
                        '--set', 'global', '--prefix', 'marcxml', '--transformer',
                        'nusl_oai.transformer.NuslTransformer')
    print(result)
    assert result.exit_code == 0


def test_harvest(cli_runner, app, db, es):
    result = _add(code='nusl', name='NUŠL', url='http://invenio.nusl.cz/oai2d/', set='global', prefix='marcxml',
                  parser=None,
                  # transformer=False
                  transformer='oarepo_oaipmh_harvester.nusl_oai.transformer.NuslTransformer'
                  )
    # db.session.expunge_all()
    # cli_runner(add, 'nusl', '--code', 'nusl', '--name', 'NUŠL', '--url', 'http://invenio.nusl.cz/oai2d/',
    #            '--set', 'global', '--prefix', 'marcxml', '--transformer', 'nusl_oai.transformer.NuslTransformer')

    # db.session.commit()

    # sleep(5)
    # db.se
    # ssion.expunge_all()
    result = _harvest(identifiers=['oai:invenio.nusl.cz:456297'], harvester_code='nusl', all_records=False, background=False, dump_to=None, load_from=None)
    # result = cli_runner(harvest, 'nusl', 'nusl', 'oai:invenio.nusl.cz:456299')

    from oarepo_oaipmh_harvester.oaipmh_record.records.api import OaipmhRecordRecord
    OaipmhRecordRecord.index.refresh()
    records = record_service.scan(system_identity)
    hits = list(records.hits)
    print(hits)
    assert len(hits) == 1
    assert hits[0]['metadata']['status'] == 'O'
    theses = theses_service.scan(system_identity, params={'facets': {}})
    hits = list(theses.hits)
    print(hits)
    # for tbl in reversed(db.meta.sorted_tables):
    #     db.get_engine().execute(tbl.delete())
    # # assert result.exit_code == 0


