import yaml
from flask_resources.responses import ResponseHandler
from flask_resources.serializers.json import JSONSerializer
from invenio_records_resources.resources.records.headers import etag_headers
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import YamlLexer

from oarepo_oaipmh_harvester.models import OAIHarvesterRun


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
        obj_list["hits"]["hits"] = [
            self._convert_to_administration_detail(obj)
            for obj in obj_list["hits"]["hits"]
        ]
        return super().serialize_object_list(obj_list)

    def _convert_to_administration_detail(self, ret):
        ret = {**ret}
        tr = ret.get("transformed_data", {})
        if tr:
            ret["title"] = tr.get("metadata", {}).get("title", "") or tr.get(
                "title", ""
            )
            if ret["title"]:
                ret["title"] = str(ret["title"])
            record_link = tr.get("links", {}).get("self_html")
            if record_link:
                ret["record_id_with_link"] = '<a href="{}">{}</a>'.format(
                    record_link, ret["id"]
                )
            else:
                ret["record_id_with_link"] = ret["id"]
        run = OAIHarvesterRun.query.get(ret["run_id"])
        ret["manual"] = "Yes" if run.manual else "No"
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
