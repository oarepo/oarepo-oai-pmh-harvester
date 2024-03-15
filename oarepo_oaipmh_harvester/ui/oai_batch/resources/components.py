from invenio_records_resources.services.base.components import BaseServiceComponent


class FilterErrorsComponent(BaseServiceComponent):
    def before_ui_detail(
        self,
        *,
        api_record,
        record,
        identity,
        args,
        view_args,
        ui_links,
        extra_context,
        **kwargs,
    ):
        ok_records, failed_records = [], []
        if record.get("records"):
            for rec in record["records"]:
                if rec.get("errors"):
                    failed_records.append(rec)
                else:
                    ok_records.append(rec)
        extra_context["ok_records"] = ok_records
        extra_context["failed_records"] = failed_records
