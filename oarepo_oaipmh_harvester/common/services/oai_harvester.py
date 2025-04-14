from invenio_accounts.models import User
from invenio_db import db
from invenio_records_resources.services import (
    RecordLink,
)
from invenio_records_resources.services import (
    RecordService as InvenioRecordService,
)
from invenio_records_resources.services import (
    RecordServiceConfig as InvenioRecordServiceConfig,
)
from invenio_records_resources.services.errors import (
    PermissionDeniedError,
    RecordPermissionDeniedError,
)
from marshmallow import ValidationError, post_dump, pre_load
from oarepo_runtime.services.config import has_permission
from oarepo_runtime.services.schema.marshmallow import BaseRecordSchema

from oarepo_oaipmh_harvester.oai_run.models import OAIHarvesterRun
from oarepo_oaipmh_harvester.services.links import ActionLinks
from oarepo_oaipmh_harvester.tasks import harvest_task


class BaseOaiHarvesterServiceConfig(InvenioRecordServiceConfig):
    @property
    def links_search_item(self):
        return {
            "actions": ActionLinks(
                {
                    "harvest": RecordLink(
                        "{+api}/oai/harvest/harvesters/{id}/start",
                        when=has_permission("run_harvest"),
                    ),
                }
            ),
        }

    @property
    def links_item(self):
        return {
            "actions": ActionLinks(
                {
                    "harvest": RecordLink(
                        "{+api}/oai/harvest/harvesters/{id}/actions/harvest",
                        when=has_permission("run_harvest"),
                    ),
                }
            ),
        }


class BaseOaiHarvesterService(InvenioRecordService):
    def start_harvest(self, identity, id_, **kwargs):
        try:
            record = self.record_cls.pid.resolve(id_)
            self.require_permission(identity, "run_harvest", record=record, **kwargs)
        except PermissionDeniedError:
            raise RecordPermissionDeniedError(action_name="run_harvest", record=record)

        running = (
            db.session.query(OAIHarvesterRun)
            .filter(OAIHarvesterRun.harvester_id == id_)
            .filter(OAIHarvesterRun.status == "running")
            .first()
        )

        if running:
            raise Exception("A harvester is already running for this ID.")

        harvest_task.delay(id_, manual=True)
        return "Harvesting started on the background.", 200


class BaseOaiHarvesterSchema(BaseRecordSchema):
    @pre_load
    def remove_schema(self, data, **kwargs):
        data.pop("_schema", None)
        return data

    @pre_load
    def process_transformers(self, data, **kwargs):
        transformers = data.get("transformers")
        batch_size = data.get("batch_size")
        max_records = data.get("max_records")
        if isinstance(transformers, str):
            data["transformers"] = parse_top_level_components(
                transformers, "transformers"
            )
        if batch_size == "":
            data.pop("batch_size")
        if max_records == "":
            data.pop("max_records")
        return data

    @pre_load
    def process_writers(self, data, **kwargs):
        writers = data.get("writers")
        if isinstance(writers, str):
            data["writers"] = parse_top_level_components(writers, "writers")
        return data

    @pre_load
    def load_harvest_managers(self, data, **kwargs):
        # must be a list of email addresses at the beginning
        harvest_managers = data.get("harvest_managers", [])
        if isinstance(harvest_managers, str):
            harvest_managers = parse_top_level_components(
                harvest_managers, "harvest_managers"
            )
        # for each manager, find a user with that email
        # and replace the email with the user id
        harvest_managers_ids = []
        for email in harvest_managers:
            email = email.strip().lower()
            if not email:
                continue
            user = User.query.filter_by(email=email).first()
            if not user:
                raise ValidationError(
                    f"User with email {email} not found", field_name="harvest_managers"
                )
            harvest_managers_ids.append(
                {
                    "id": user.id,
                    "email": user.email,
                }
            )
        data["harvest_managers"] = harvest_managers_ids
        return data

    @post_dump
    def dump_harvest_managers(self, data, **kwargs):
        # must be a list of user ids at the beginning
        harvest_managers = data.get("harvest_managers", [])
        if not harvest_managers:
            return data
        # for each manager, find a user with that id
        # and replace the id with the email
        data["harvest_managers"] = [x["email"] for x in harvest_managers]
        return data


def parse_top_level_components(input_string, field_name):
    components = []
    current_component = []
    bracket_level = 0

    for char in input_string:
        if char == "{":
            bracket_level += 1
            current_component.append(char)
        elif char == "}":
            if bracket_level == 0:
                raise ValidationError(
                    "Unmatched brackets in input string",
                    field_name=field_name,
                )
            bracket_level -= 1
            current_component.append(char)
        elif char == "," and bracket_level == 0:
            components.append("".join(current_component).strip())
            current_component = []
        else:
            current_component.append(char)

    # Add the last component
    if current_component:
        components.append("".join(current_component).strip())

    if bracket_level != 0:
        raise ValidationError(
            "Unmatched brackets in input string",
            field_name=field_name,
        )

    return components
