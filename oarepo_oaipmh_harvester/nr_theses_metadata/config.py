
from .resources.config import NrThesesMetadataResourceConfig
from .resources.resource import NrThesesMetadataResource
from .services.config import NrThesesMetadataServiceConfig
from .services.facets import metadata_accessRights, metadata_languages, metadata_resourceType
from .services.service import NrThesesMetadataService

NR_THESES_METADATA_RESOURCE_CONFIG = NrThesesMetadataResourceConfig
NR_THESES_METADATA_RESOURCE_CLASS = NrThesesMetadataResource
NR_THESES_METADATA_SERVICE_CONFIG = NrThesesMetadataServiceConfig
NR_THESES_METADATA_SERVICE_CLASS = NrThesesMetadataService


if False:
    import logging

    es_trace_logger = logging.getLogger('elasticsearch.trace')
    es_trace_logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    es_trace_logger.addHandler(handler)


# TODO: generate facet config by model builder
APP_SEARCH_FACETS = {
    'access_status': {
        'facet': metadata_accessRights,
        'ui': {
            'field': 'accessRights',
        }
    },

    'language': {
        'facet': metadata_languages,
        'ui': {
            'field': 'languages',
        }
    },
    'resource_type': {
        'facet': metadata_resourceType,
        'ui': {
            'field': 'resourceType.type',
            'childAgg': {
                'field': 'resourceType.subtype',
            }
        }
    }
}
