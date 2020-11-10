def test_get_providers(app, db):
    client = app.test_client()
    resp = client.get("/oai-client/providers")
    assert resp.status_code == 200
    assert resp.json == {
        'uk': {
            'description': 'Univerzita Karlova',
            'synchronizers': [{
                'default_endpoint': 'recid',
                'endpoint_mapping': {
                    'field_name': 'doc_type',
                    'mapping': {
                        'record': 'recid'
                    }
                }, 'metadata_prefix': 'xoai',
                'name': 'xoai',
                'from': 'latest',
                'oai_endpoint': 'https://dspace.cuni.cz/oai/nusl',
                'set': 'nusl_set',
                'unhandled_paths': [
                    '/dc/unhandled']
            }]
        }
    }
    print(resp.json)
