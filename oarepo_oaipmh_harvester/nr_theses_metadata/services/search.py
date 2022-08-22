from elasticsearch_dsl import Q
from invenio_records_resources.services import SearchOptions as InvenioSearchOptions
from invenio_records_resources.services.records.params import FacetsParam, PaginationParam, QueryParser, QueryStrParam, \
    SortParam
from . import facets


def _(x):
    """Identity function for string extraction."""
    return x

class ExtendedFacetsParam(FacetsParam):
    def apply(self, identity, search, params):
        """Add aggregations representing the facets."""

        for facet_name in self.facets.keys():
            if 'facets' in params and '__expanded__' in params['facets'] and facet_name in params['facets']['__expanded__']:
                self.facets[facet_name]._params['size'] = self.config.max_facet_size
            # else:
            #     self.facets[facet_name]._params['size'] = 10

        params['facets'].pop('__expanded__', None)

        facets_values = dict(params.get("facets", {}))
        for name, values in facets_values.items():
            if '__missing__' in values and name in self.facets:
                self._filters[f"__missing__{name}"] = ~Q('exists', field=self.facets[name]._params['field'])
                values.remove('__missing__')
        
        return super().apply(identity, search, params)
    
    def filter(self, search):
        """Apply a post filter on the search."""
        if not self._filters:
            return search

        filters = list(self._filters.values())

        facet_filter = filters[0]
        for f in filters[1:]:
            facet_filter &= f

        return search.filter(facet_filter)


class NrThesesMetadataSearchOptions(InvenioSearchOptions):
    """NrThesesMetadataRecord search options."""

    params_interpreters_cls = [
        QueryStrParam,
        PaginationParam,
        SortParam,
        ExtendedFacetsParam,
    ]

    # More than that is currently unreasonable slow on all fronts
    max_facet_size = 10000

    facets = {
        "metadata_dateDefended": facets.metadata_dateDefended,
        "metadata_defended": facets.metadata_defended,
        # "metadata_defended_missing": facets.metadata_defended_missing,
        # "metadata_collection": facets.metadata_collection,
        "metadata_resourceType": facets.metadata_resourceType,
        "metadata_dateIssued": facets.metadata_dateIssued,
        "metadata_dateAvailable": facets.metadata_dateAvailable,
        "metadata_dateModified": facets.metadata_dateModified,
        "metadata_abstract": facets.metadata_abstract,
        "metadata_methods": facets.metadata_methods,
        "metadata_technicalInfo": facets.metadata_technicalInfo,
        "metadata_accessRights": facets.metadata_accessRights,
        "metadata_version": facets.metadata_version,
        "metadata_accessibility": facets.metadata_accessibility,
        "metadata_externalLocation_externalLocationURL": facets.metadata_externalLocation_externalLocationURL,
        "metadata_extent": facets.metadata_extent,
        "metadata_originalRecord": facets.metadata_originalRecord,
        "metadata_degreeGrantor": facets.metadata_degreeGrantor,
        "metadata_studyFields": facets.metadata_studyFields,
        "metadata_additionalTitles_title": facets.metadata_additionalTitles_title,
        "metadata_additionalTitles_titleType": facets.metadata_additionalTitles_titleType,
        "metadata_additionalTitles": facets.metadata_additionalTitles,
        "metadata_creators_fullName": facets.metadata_creators_fullName,
        "metadata_creators_nameType": facets.metadata_creators_nameType,
        "metadata_creators_authorityIdentifiers_identifier": facets.metadata_creators_authorityIdentifiers_identifier,
        "metadata_creators_authorityIdentifiers_scheme": facets.metadata_creators_authorityIdentifiers_scheme,
        "metadata_creators_authorityIdentifiers": facets.metadata_creators_authorityIdentifiers,
        "metadata_creators_affiliations": facets.metadata_creators_affiliations,
        "metadata_creators": facets.metadata_creators,
        "metadata_contributors_role": facets.metadata_contributors_role,
        "metadata_contributors_fullName": facets.metadata_contributors_fullName,
        "metadata_contributors_nameType": facets.metadata_contributors_nameType,
        "metadata_contributors_authorityIdentifiers_identifier": facets.metadata_contributors_authorityIdentifiers_identifier,
        "metadata_contributors_authorityIdentifiers_scheme": facets.metadata_contributors_authorityIdentifiers_scheme,
        "metadata_contributors_authorityIdentifiers": facets.metadata_contributors_authorityIdentifiers,
        "metadata_contributors_affiliations": facets.metadata_contributors_affiliations,
        "metadata_contributors": facets.metadata_contributors,
        "metadata_subjects_subjectScheme": facets.metadata_subjects_subjectScheme,
        "metadata_subjects_subject": facets.metadata_subjects_subject,
        "metadata_subjects_valueURI": facets.metadata_subjects_valueURI,
        "metadata_subjects_classificationCode": facets.metadata_subjects_classificationCode,
        "metadata_subjects": facets.metadata_subjects,
        "metadata_subjectCategories": facets.metadata_subjectCategories,
        "metadata_languages": facets.metadata_languages,
        "metadata_rights": facets.metadata_rights,
        "metadata_relatedItems_itemURL": facets.metadata_relatedItems_itemURL,
        "metadata_relatedItems_itemYear": facets.metadata_relatedItems_itemYear,
        "metadata_relatedItems_itemVolume": facets.metadata_relatedItems_itemVolume,
        "metadata_relatedItems_itemIssue": facets.metadata_relatedItems_itemIssue,
        "metadata_relatedItems_itemStartPage": facets.metadata_relatedItems_itemStartPage,
        "metadata_relatedItems_itemEndPage": facets.metadata_relatedItems_itemEndPage,
        "metadata_relatedItems_itemPublisher": facets.metadata_relatedItems_itemPublisher,
        "metadata_relatedItems_itemRelationType": facets.metadata_relatedItems_itemRelationType,
        "metadata_relatedItems_itemResourceType": facets.metadata_relatedItems_itemResourceType,
        "metadata_relatedItems_itemCreators_fullName": facets.metadata_relatedItems_itemCreators_fullName,
        "metadata_relatedItems_itemCreators_nameType": facets.metadata_relatedItems_itemCreators_nameType,
        "metadata_relatedItems_itemCreators_authorityIdentifiers_identifier": facets.metadata_relatedItems_itemCreators_authorityIdentifiers_identifier,
        "metadata_relatedItems_itemCreators_authorityIdentifiers_scheme": facets.metadata_relatedItems_itemCreators_authorityIdentifiers_scheme,
        "metadata_relatedItems_itemCreators_authorityIdentifiers": facets.metadata_relatedItems_itemCreators_authorityIdentifiers,
        "metadata_relatedItems_itemCreators_affiliations": facets.metadata_relatedItems_itemCreators_affiliations,
        "metadata_relatedItems_itemCreators": facets.metadata_relatedItems_itemCreators,
        "metadata_relatedItems_itemContributors_role": facets.metadata_relatedItems_itemContributors_role,
        "metadata_relatedItems_itemContributors_fullName": facets.metadata_relatedItems_itemContributors_fullName,
        "metadata_relatedItems_itemContributors_nameType": facets.metadata_relatedItems_itemContributors_nameType,
        "metadata_relatedItems_itemContributors_authorityIdentifiers_identifier": facets.metadata_relatedItems_itemContributors_authorityIdentifiers_identifier,
        "metadata_relatedItems_itemContributors_authorityIdentifiers_scheme": facets.metadata_relatedItems_itemContributors_authorityIdentifiers_scheme,
        "metadata_relatedItems_itemContributors_authorityIdentifiers": facets.metadata_relatedItems_itemContributors_authorityIdentifiers,
        "metadata_relatedItems_itemContributors_affiliations": facets.metadata_relatedItems_itemContributors_affiliations,
        "metadata_relatedItems_itemContributors": facets.metadata_relatedItems_itemContributors,
        "metadata_relatedItems_itemPIDs_identifier": facets.metadata_relatedItems_itemPIDs_identifier,
        "metadata_relatedItems_itemPIDs_scheme": facets.metadata_relatedItems_itemPIDs_scheme,
        "metadata_relatedItems_itemPIDs": facets.metadata_relatedItems_itemPIDs,
        "metadata_relatedItems": facets.metadata_relatedItems,
        "metadata_fundingReferences_projectID": facets.metadata_fundingReferences_projectID,
        "metadata_fundingReferences_funder": facets.metadata_fundingReferences_funder,
        "metadata_fundingReferences": facets.metadata_fundingReferences,
        "metadata_geoLocations_geoLocationPlace": facets.metadata_geoLocations_geoLocationPlace,
        "metadata_geoLocations_geoLocationPoint_pointLongitude": facets.metadata_geoLocations_geoLocationPoint_pointLongitude,
        "metadata_geoLocations_geoLocationPoint_pointLatitude": facets.metadata_geoLocations_geoLocationPoint_pointLatitude,
        "metadata_geoLocations": facets.metadata_geoLocations,
        "metadata_series_seriesTitle": facets.metadata_series_seriesTitle,
        "metadata_series_seriesVolume": facets.metadata_series_seriesVolume,
        "metadata_series": facets.metadata_series,
        "metadata_objectIdentifiers_identifier": facets.metadata_objectIdentifiers_identifier,
        "metadata_objectIdentifiers_scheme": facets.metadata_objectIdentifiers_scheme,
        "metadata_objectIdentifiers": facets.metadata_objectIdentifiers,
        "metadata_systemIdentifiers_identifier": facets.metadata_systemIdentifiers_identifier,
        "metadata_systemIdentifiers_scheme": facets.metadata_systemIdentifiers_scheme,
        "metadata_systemIdentifiers": facets.metadata_systemIdentifiers,
        "metadata_events_eventDate": facets.metadata_events_eventDate,
        "metadata_events_eventLocation_place": facets.metadata_events_eventLocation_place,
        "metadata_events_eventLocation_country": facets.metadata_events_eventLocation_country,
        "metadata_events": facets.metadata_events,
        "metadata_collections": facets.metadata_collections,
        "_id": facets._id,
        "created": facets.created,
        "updated": facets.updated,
        "_schema": facets._schema,
    }

    # TODO: Expand max results to accommodate more records
    pagination_options = {
        "default_results_per_page": 25,
        "default_max_results": 1000
    }

    sort_options = {
        "bestmatch": dict(
            title=_("Best match"),
            fields=["_score"],  # ES defaults to desc on `_score` field
        ),
        "newest": dict(
            title=_("Newest"),
            fields=["-created"],
        ),
        "oldest": dict(
            title=_("Oldest"),
            fields=["created"],
        ),
    }
