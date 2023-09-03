from flask_resources import BaseListSchema, MarshmallowSerializer
from flask_resources.serializers import JSONSerializer

from oarepo_oaipmh_harvester.oai_run.services.records.ui_schema import OaiRunUISchema


class OaiRunUIJSONSerializer(MarshmallowSerializer):
    """UI JSON serializer."""

    def __init__(self):
        """Initialise Serializer."""
        super().__init__(
            format_serializer_cls=JSONSerializer,
            object_schema_cls=OaiRunUISchema,
            list_schema_cls=BaseListSchema,
            schema_context={"object_key": "ui"},
        )
