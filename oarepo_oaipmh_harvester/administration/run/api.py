import yaml
from flask_resources.responses import ResponseHandler
from flask_resources.serializers.json import JSONSerializer
from invenio_records_resources.resources.records.headers import etag_headers
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import YamlLexer


def data_to_html_yaml(data):
    yaml_str = yaml.dump(data, default_flow_style=False, sort_keys=False)
    html = highlight(yaml_str, YamlLexer(), HtmlFormatter(full=False))
    return html


class AdministrationDetailJSONSerializer(JSONSerializer):
    """JSON serializer for administration API."""

    def serialize_object(self, obj):
        obj = self._convert_to_administration_detail(obj)
        return super().serialize_object(obj)

    def serialize_object_list(self, obj_list):
        obj_list["hits"]["hits"] = [
            self._convert_to_administration_detail(obj)
            for obj in obj_list["hits"]["hits"]
        ]
        return super().serialize_object_list(obj_list)

    def _convert_to_administration_detail(self, ret):
        ret = {**ret}
        records_url = f"/administration/oarepo/harvest/records?q=run_id:{ret['id']}"
        ret["records_url"] = '<a href="{}">Click to see records ...</a>'.format(
            records_url
        )
        ret["manual"] = "Yes" if ret.get("manual") else "No"
        return ret


response_handlers = {
    "application/invenio-administration-detail+json": ResponseHandler(
        serializer=AdministrationDetailJSONSerializer(),
        headers=etag_headers,
    )
}
