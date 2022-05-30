from invenio_records_resources.services import \
    SearchOptions as InvenioSearchOptions

from . import facets


def _(x):
    """Identity function for string extraction."""
    return x



class OaipmhBatchSearchOptions(InvenioSearchOptions):
    """OaipmhBatchRecord search options."""

    facets = {


    'metadata_run_id': facets.metadata_run_id,



    'metadata_status': facets.metadata_status,



    'metadata_exception_keyword': facets.metadata_exception_keyword,



    'metadata_started': facets.metadata_started,



    'metadata_finished': facets.metadata_finished,



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