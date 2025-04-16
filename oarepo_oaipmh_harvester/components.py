from invenio_drafts_resources.services.records.components import ServiceComponent


class OaiSectionComponent(ServiceComponent):
    def create(self, identity, data=None, record=None, **kwargs):
        record["oai"] = data.get("oai", {})

    def update(self, identity, data=None, record=None, **kwargs):
        record["oai"] = data.get("oai", {})

    def update_draft(self, identity, data=None, record=None, **kwargs):
        record["oai"] = data.get("oai", {})

    def publish(self, identity, draft=None, record=None, **kwargs):
        record["oai"] = draft.get("oai", {})

    def edit(self, identity, draft=None, record=None):
        draft["oai"] = record.get("oai", {})

    def new_version(self, identity, draft=None, record=None):
        draft["oai"] = record.get("oai", {})
