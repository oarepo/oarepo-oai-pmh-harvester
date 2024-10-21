from invenio_records_resources.services.records.components import ServiceComponent


class OaiSectionComponent(ServiceComponent):
    def create(self, identity, data=None, record=None, **kwargs):
        record["oai"] = data.get("oai", {})

    def update(self, identity, data=None, record=None, **kwargs):
        record["oai"] = data.get("oai", {})

    def publish(self, identity, draft=None, record=None, **kwargs):
        record["oai"] = draft.get("oai", {})
