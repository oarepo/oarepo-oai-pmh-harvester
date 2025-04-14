import yaml
from flask_resources.responses import ResponseHandler
from flask_resources.serializers.json import JSONSerializer
from invenio_records_resources.resources.records.headers import etag_headers
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import YamlLexer


def data_to_html_yaml(data):
    yaml_str = yaml.dump(
        data, default_flow_style=False, sort_keys=False, allow_unicode=True
    )
    html = highlight(yaml_str, YamlLexer(), HtmlFormatter(full=False))
    return html


class AdministrationDetailJSONSerializer(JSONSerializer):
    """JSON serializer for administration API."""

    def serialize_object(self, obj):
        obj = self._convert_to_administration_detail(obj)
        return super().serialize_object(obj)

    def serialize_object_list(self, obj_list):
        obj_list = [self._convert_to_administration_detail(obj) for obj in obj_list]
        return super().serialize_object_list(obj_list)

    def _convert_to_administration_detail(self, ret):
        ret = {**ret}
        ret["errors"] = data_to_html_yaml(ret.get("errors"))
        ret["original_data"] = data_to_html_yaml(ret.get("original_data"))
        ret["transformed_data"] = data_to_html_yaml(ret.get("transformed_data"))
        ret["has_errors"] = "Yes" if ret.get("has_errors") else "No"
        ret["deleted"] = "Yes" if ret.get("deleted") else "No"
        run_link = f"/administration/oarepo/harvest/runs/{ret["run_id"]}"
        ret["run"] = '<a href="{}">Click to see the run ...</a>'.format(run_link)
        return ret


response_handlers = {
    "application/invenio-administration-detail+json": ResponseHandler(
        serializer=AdministrationDetailJSONSerializer(),
        headers=etag_headers,
    )
}
