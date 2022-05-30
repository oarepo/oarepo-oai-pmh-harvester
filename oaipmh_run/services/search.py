from invenio_records_resources.services import \
    SearchOptions as InvenioSearchOptions

from . import facets


def _(x):
    """Identity function for string extraction."""
    return x



class OaipmhRunSearchOptions(InvenioSearchOptions):
    """OaipmhRunRecord search options."""

    facets = {


    'metadata_harvester_id': facets.metadata_harvester_id,



    'metadata_started': facets.metadata_started,



    'metadata_finished': facets.metadata_finished,



    'metadata_first_datastamp': facets.metadata_first_datastamp,



    'metadata_last_datastamp': facets.metadata_last_datastamp,



    'metadata_status': facets.metadata_status,



    'metadata_exception_keyword': facets.metadata_exception_keyword,



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