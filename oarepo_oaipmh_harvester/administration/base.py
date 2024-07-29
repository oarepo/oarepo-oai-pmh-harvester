from invenio_administration.marshmallow_utils import custom_mapping, vocabulary_schemas
from invenio_administration.views.base import AdminFormView
from marshmallow import fields
from marshmallow_utils import fields as invenio_fields


class OarepoAdminFormView(AdminFormView):
    """Basic form view."""

    display_edit = False
    display_read = False
    form_fields = None
    display_read_only = True

    def _schema_to_json(self, schema=None, form_fields=None):
        return jsonify_schema(schema, form_fields)

    def get(self, pid_value=None):
        """GET view method."""
        schema = self.get_service_schema()
        serialized_schema = self._schema_to_json(schema, self.form_fields)
        form_fields = self.form_fields
        return self.render(
            **{
                "resource_schema": serialized_schema,
                "form_fields": form_fields,
                "pid": pid_value,
                "api_endpoint": self.get_api_endpoint(),
                "title": self.title,
                "list_endpoint": self.get_list_view_endpoint(),
                "ui_config": self.form_fields,
            }
        )


def find_type_in_mapping(field_type, custom_mapping):
    current_type = field_type
    while current_type:
        if current_type in custom_mapping:
            return custom_mapping[current_type]
        current_type = current_type.__base__

    raise KeyError(f"Unrecognized field type: {field_type}")


def jsonify_schema(schema, form_fields):
    """Marshmallow schema to dict."""
    schema_dict = {}

    for field, field_type in schema.fields.items():
        if field == "_schema":
            continue
        is_links = isinstance(field_type, invenio_fields.links.Links)
        # skip `fields.Method`
        is_method = isinstance(field_type, fields.Method)

        if is_links or is_method:
            continue

        is_read_only = field_type.dump_only
        is_create_only = (
            field_type.metadata["create_only"]
            if "create_only" in field_type.metadata
            else False
        )

        field_type_name = field_type.__class__
        is_required = field_type.required

        nested_field = isinstance(field_type, fields.Nested)
        list_field = isinstance(field_type, fields.List)

        schema_dict[field] = {
            "required": is_required,
            "readOnly": is_read_only,
            "title": (
                field_type.metadata["title"] if "title" in field_type.metadata else None
            ),
            "createOnly": is_create_only,
            "metadata": field_type.metadata,
        }
        if field in form_fields and "type" in form_fields[field]:
            schema_dict[field].update(
                {
                    "type": form_fields[field]["type"],
                }
            )
            continue
        if nested_field:
            if any([isinstance(field_type.schema, x) for x in vocabulary_schemas]):
                schema_type = "vocabulary"
            else:
                schema_type = "object"

            schema_dict[field].update(
                {
                    "type": schema_type,
                    "properties": jsonify_schema(schema, field_type.schema),
                }
            )
        elif list_field and isinstance(field_type.inner, fields.Nested):
            # list of objects (vocabularies or nested)
            schema_dict[field].update(
                {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": jsonify_schema(schema, field_type.inner.schema),
                    },
                }
            )
        elif list_field and not isinstance(field_type.inner, fields.Nested):
            # list of plain types
            schema_dict[field].update(
                {
                    "type": "array",
                    "items": {
                        "type": find_type_in_mapping(
                            field_type.inner.__class__, custom_mapping
                        )
                    },
                }
            )
        else:
            try:
                field_type_mapping = find_type_in_mapping(
                    field_type_name, custom_mapping
                )
                schema_dict[field].update(
                    {
                        "type": field_type_mapping,
                    }
                )
            except KeyError:
                raise Exception(f"Unrecognised schema field {field}: {field_type_name}")
    return schema_dict
