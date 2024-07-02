from invenio_requests.services import RequestsServiceConfig
from invenio_requests.services.requests import RequestLink


class HarvestServiceConfig(RequestsServiceConfig):
    links_item = {
        "execute": RequestLink("{+api}/harvest/{harvester_code}/execute"),
    }
