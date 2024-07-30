from marshmallow import post_dump
from oarepo_runtime.services.schema.marshmallow import BaseRecordSchema


class BaseOaiRecordSchema(BaseRecordSchema):
    @post_dump
    def process_transformers(self, data, **kwargs):
        error_str = ""
        for e in data["errors"]:
            if "info" in e:
                error_str = (
                    error_str + f'{e["location"]}: {e["message"]} - {e["info"]}, '
                )
            else:
                error_str = error_str + f'{e["location"]}: {e["message"]}, '
        data["errors"] = error_str
        return data
