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
        obj_list = [self._convert_to_administration_detail(obj) for obj in obj_list]
        return super().serialize_object_list(obj_list)

    def _convert_to_administration_detail(self, ret):
        ret = {**ret}
        ret["transformers"] = data_to_html_yaml(ret["transformers"])
        ret["writers"] = data_to_html_yaml(ret["writers"])
        run_url = f"/administration/oarepo/harvest/runs?q=harvester_id:{ret['id']}"
        print(run_url)
        ret["runs"] = '<a href="{}">Click to see runs ...</a>'.format(run_url)
        return ret


response_handlers = {
    "application/invenio-administration-detail+json": ResponseHandler(
        serializer=AdministrationDetailJSONSerializer(),
        headers=etag_headers,
    )
}
