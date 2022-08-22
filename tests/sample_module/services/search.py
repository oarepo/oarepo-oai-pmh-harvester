from invenio_records_resources.services import \
    SearchOptions as InvenioSearchOptions

from . import facets


def _(x):
    """Identity function for string extraction."""
    return x



class OaipmhRecordSearchOptions(InvenioSearchOptions):
    """OaipmhRecordRecord search options."""

    facets = {





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