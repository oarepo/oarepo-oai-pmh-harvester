from invenio_records_resources.services import \
    SearchOptions as InvenioSearchOptions

from . import facets


def _(x):
    """Identity function for string extraction."""
    return x



class OaipmhConfigSearchOptions(InvenioSearchOptions):
    """OaipmhConfigRecord search options."""

    facets = {


    'metadata_code': facets.metadata_code,



    'metadata_baseurl': facets.metadata_baseurl,



    'metadata_metadataprefix': facets.metadata_metadataprefix,



    'metadata_name': facets.metadata_name,



    'metadata_max_records': facets.metadata_max_records,



    'metadata_batch_size': facets.metadata_batch_size,



    '_id': facets._id,



    'created': facets.created,



    'updated': facets.updated,



    '_schema': facets._schema,


    }
    sort_options = {
            "bestmatch": dict(
                title=_('Best match'),
                fields=['_score'],  # ES defaults to desc on `_score` field
            ),
            "newest": dict(
                title=_('Newest'),
                fields=['-created'],
            ),
            "oldest": dict(
                title=_('Oldest'),
                fields=['created'],
            ),

    }