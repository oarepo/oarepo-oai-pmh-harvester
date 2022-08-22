import marshmallow as ma
import marshmallow.fields as ma_fields
import marshmallow.validate as ma_valid
from invenio_records_resources.services.records.schema import (
    BaseRecordSchema as InvenioBaseRecordSchema,
)

from .multilingual_schema import MultilingualSchema


class ExternalLocationSchema(
    ma.Schema,
):
    """ExternalLocationSchema schema."""

    externalLocationURL = ma_fields.String()

    externalLocationNote = ma_fields.String()


class AdditionalTitlesSchema(
    ma.Schema,
):
    """AdditionalTitlesSchema schema."""

    title = ma_fields.List(ma_fields.Nested(lambda: MultilingualSchema()))

    titleType = ma_fields.String(
        validate=[
            ma_valid.OneOf(["translatedTitle", "alternativeTitle", "subtitle", "other"])
        ]
    )


class AuthorityIdentifiersSchema(
    ma.Schema,
):
    """AuthorityIdentifiersSchema schema."""

    identifier = ma_fields.String()

    scheme = ma_fields.String(
        validate=[
            ma_valid.OneOf(
                [
                    "orcid",
                    "scopusID",
                    "researcherID",
                    "czenasAutID",
                    "vedidk",
                    "institutionalID",
                    "ISNI",
                    "ROR",
                    "ICO",
                    "DOI",
                ]
            )
        ]
    )


class CreatorsSchema(
    ma.Schema,
):
    """CreatorsSchema schema."""

    fullName = ma_fields.String()

    nameType = ma_fields.String(
        validate=[ma_valid.OneOf(["Organizational", "Personal"])]
    )

    authorityIdentifiers = ma_fields.List(
        ma_fields.Nested(lambda: AuthorityIdentifiersSchema())
    )

    affiliations = ma_fields.List(ma_fields.String())


class ContributorsSchema(
    ma.Schema,
):
    """ContributorsSchema schema."""

    role = ma_fields.String()

    fullName = ma_fields.String()

    nameType = ma_fields.String(
        validate=[ma_valid.OneOf(["Organizational", "Personal"])]
    )

    authorityIdentifiers = ma_fields.List(
        ma_fields.Nested(lambda: AuthorityIdentifiersSchema())
    )

    affiliations = ma_fields.List(ma_fields.String())


class SubjectsSchema(
    ma.Schema,
):
    """SubjectsSchema schema."""

    subjectScheme = ma_fields.String()

    subject = ma_fields.List(ma_fields.Nested(lambda: MultilingualSchema()))

    valueURI = ma_fields.String()

    classificationCode = ma_fields.String()


class ItemCreatorsSchema(
    ma.Schema,
):
    """ItemCreatorsSchema schema."""

    fullName = ma_fields.String()

    nameType = ma_fields.String(
        validate=[ma_valid.OneOf(["Organizational", "Personal"])]
    )

    authorityIdentifiers = ma_fields.List(
        ma_fields.Nested(lambda: AuthorityIdentifiersSchema())
    )

    affiliations = ma_fields.List(ma_fields.String())


class ItemContributorsSchema(
    ma.Schema,
):
    """ItemContributorsSchema schema."""

    role = ma_fields.String()

    fullName = ma_fields.String()

    nameType = ma_fields.String(
        validate=[ma_valid.OneOf(["Organizational", "Personal"])]
    )

    authorityIdentifiers = ma_fields.List(
        ma_fields.Nested(lambda: AuthorityIdentifiersSchema())
    )

    affiliations = ma_fields.List(ma_fields.String())


class ItemPIDsSchema(
    ma.Schema,
):
    """ItemPIDsSchema schema."""

    identifier = ma_fields.String()

    scheme = ma_fields.String(
        validate=[ma_valid.OneOf(["DOI", "Handle", "ISBN", "ISSN", "RIV"])]
    )


class RelatedItemsSchema(
    ma.Schema,
):
    """RelatedItemsSchema schema."""

    itemTitle = ma_fields.String()

    itemURL = ma_fields.String()

    itemYear = ma_fields.Integer()

    itemVolume = ma_fields.String()

    itemIssue = ma_fields.String()

    itemStartPage = ma_fields.String()

    itemEndPage = ma_fields.String()

    itemPublisher = ma_fields.String()

    itemRelationType = ma_fields.String()

    itemResourceType = ma_fields.String()

    itemCreators = ma_fields.List(ma_fields.Nested(lambda: ItemCreatorsSchema()))

    itemContributors = ma_fields.List(
        ma_fields.Nested(lambda: ItemContributorsSchema())
    )

    itemPIDs = ma_fields.List(ma_fields.Nested(lambda: ItemPIDsSchema()))


class FundingReferencesSchema(
    ma.Schema,
):
    """FundingReferencesSchema schema."""

    projectID = ma_fields.String()

    projectName = ma_fields.String()

    fundingProgram = ma_fields.String()

    funder = ma_fields.String()


class GeoLocationPointSchema(
    ma.Schema,
):
    """GeoLocationPointSchema schema."""

    pointLongitude = ma_fields.Float()

    pointLatitude = ma_fields.Float()


class GeoLocationsSchema(
    ma.Schema,
):
    """GeoLocationsSchema schema."""

    geoLocationPlace = ma_fields.String()

    geoLocationPoint = ma_fields.Nested(lambda: GeoLocationPointSchema())


class SeriesSchema(
    ma.Schema,
):
    """SeriesSchema schema."""

    seriesTitle = ma_fields.String()

    seriesVolume = ma_fields.String()


class ObjectIdentifiersSchema(
    ma.Schema,
):
    """ObjectIdentifiersSchema schema."""

    identifier = ma_fields.String()

    scheme = ma_fields.String(
        validate=[ma_valid.OneOf(["DOI", "Handle", "ISBN", "ISSN", "RIV"])]
    )


class SystemIdentifiersSchema(
    ma.Schema,
):
    """SystemIdentifiersSchema schema."""

    identifier = ma_fields.String()

    scheme = ma_fields.String(
        validate=[
            ma_valid.OneOf(
                ["nusl", "nuslOAI", "originalRecordOAI", "catalogueSysNo", "nrOAI"]
            )
        ]
    )


class EventLocationSchema(
    ma.Schema,
):
    """EventLocationSchema schema."""

    place = ma_fields.String()

    country = ma_fields.String()


class EventsSchema(
    ma.Schema,
):
    """EventsSchema schema."""

    eventNameOriginal = ma_fields.String()

    eventDate = ma_fields.String()

    eventLocation = ma_fields.Nested(lambda: EventLocationSchema())

    eventNameAlternate = ma_fields.List(ma_fields.String())


class NrThesesMetadataMetadataSchema(
    ma.Schema,
):
    """NrThesesMetadataMetadataSchema schema."""

    dateDefended = ma_fields.String()

    defended = ma_fields.Boolean()

    collection = ma_fields.String()

    title = ma_fields.String()

    resourceType = ma_fields.String()

    dateIssued = ma_fields.String()

    dateAvailable = ma_fields.String()

    dateModified = ma_fields.String()

    abstract = ma_fields.List(ma_fields.Nested(lambda: MultilingualSchema()))

    methods = ma_fields.List(ma_fields.Nested(lambda: MultilingualSchema()))

    technicalInfo = ma_fields.List(ma_fields.Nested(lambda: MultilingualSchema()))

    accessRights = ma_fields.String()

    version = ma_fields.String()

    accessibility = ma_fields.List(ma_fields.Nested(lambda: MultilingualSchema()))

    externalLocation = ma_fields.Nested(lambda: ExternalLocationSchema())

    extent = ma_fields.String()

    originalRecord = ma_fields.String()

    degreeGrantor = ma_fields.List(ma_fields.String())

    studyFields = ma_fields.List(ma_fields.String())

    additionalTitles = ma_fields.List(
        ma_fields.Nested(lambda: AdditionalTitlesSchema())
    )

    creators = ma_fields.List(ma_fields.Nested(lambda: CreatorsSchema()))

    contributors = ma_fields.List(ma_fields.Nested(lambda: ContributorsSchema()))

    subjects = ma_fields.List(ma_fields.Nested(lambda: SubjectsSchema()))

    publishers = ma_fields.List(ma_fields.String())

    subjectCategories = ma_fields.List(ma_fields.String())

    languages = ma_fields.List(ma_fields.String())

    notes = ma_fields.List(ma_fields.String())

    rights = ma_fields.List(ma_fields.String())

    relatedItems = ma_fields.List(ma_fields.Nested(lambda: RelatedItemsSchema()))

    fundingReferences = ma_fields.List(
        ma_fields.Nested(lambda: FundingReferencesSchema())
    )

    geoLocations = ma_fields.List(ma_fields.Nested(lambda: GeoLocationsSchema()))

    series = ma_fields.List(ma_fields.Nested(lambda: SeriesSchema()))

    objectIdentifiers = ma_fields.List(
        ma_fields.Nested(lambda: ObjectIdentifiersSchema())
    )

    systemIdentifiers = ma_fields.List(
        ma_fields.Nested(lambda: SystemIdentifiersSchema())
    )

    events = ma_fields.List(ma_fields.Nested(lambda: EventsSchema()))

    collections = ma_fields.List(ma_fields.String())


class NrThesesMetadataSchema(
    ma.Schema,
):
    """NrThesesMetadataSchema schema."""

    metadata = ma_fields.Nested(lambda: NrThesesMetadataMetadataSchema())

    id = ma_fields.String()

    created = ma_fields.Date()

    updated = ma_fields.Date()

    _schema = ma_fields.String(data_key="$schema")
