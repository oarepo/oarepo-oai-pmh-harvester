from invenio_records_resources.services.records.schema import (
    BaseRecordSchema,
)
from marshmallow import fields


class OAIHarvesterRunSchema(BaseRecordSchema):
    harvester_id = fields.String(required=True)
    manual = fields.Boolean(default=False, required=True)
    title = fields.String(allow_none=True)
    harvester_config = fields.Dict(default=dict, required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(allow_none=True)
    last_update_time = fields.DateTime(allow_none=True)
    status = fields.String(required=True)
    records = fields.Integer(default=0, required=True)
    finished_records = fields.Integer(default=0, required=True)
    ok_records = fields.Integer(default=0, required=True)
    failed_records = fields.Integer(default=0, required=True)

    class Meta:
        strict = True
