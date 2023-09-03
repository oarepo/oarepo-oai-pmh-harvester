import { createSearchAppInit } from '@js/invenio_search_ui'
import {
  ActiveFiltersElement,
  BucketAggregationElement,
  BucketAggregationValuesElement,
  CountElement,
  ErrorElement,
  SearchAppFacets,
  SearchAppSearchbarContainer,
  SearchFiltersToggleElement,
  SearchAppResultOptions,
  SearchAppSort,
  SearchAppLayout
} from '@js/oarepo_ui/search'
import {
  OaiRecordResultsListItemWithState
} from './components'
import { parametrize, overrideStore } from 'react-overridable'

const appName = 'OaiRecord.Search'

const SearchAppSearchbarContainerWithConfig = parametrize(SearchAppSearchbarContainer, { appName: appName })
const ResultsListItemWithConfig = parametrize(OaiRecordResultsListItemWithState, { appName: appName })


export const defaultComponents = {
  [`${appName}.ActiveFilters.element`]: ActiveFiltersElement,
  [`${appName}.BucketAggregation.element`]: BucketAggregationElement,
  [`${appName}.BucketAggregationValues.element`]: BucketAggregationValuesElement,
  [`${appName}.Count.element`]: CountElement,
  [`${appName}.Error.element`]: ErrorElement,
  // [`${appName}.ResultsGrid.item`]: ResultsGridItemWithConfig,
  [`${appName}.ResultsList.item`]: ResultsListItemWithConfig,
  [`${appName}.SearchApp.facets`]: SearchAppFacets,
  [`${appName}.SearchApp.searchbarContainer`]: SearchAppSearchbarContainerWithConfig,
  [`${appName}.SearchApp.sort`]: SearchAppSort,
  [`${appName}.SearchApp.layout`]: SearchAppLayout,
  [`${appName}.SearchApp.resultOptions`]: SearchAppResultOptions,
  [`${appName}.SearchFilters.Toggle.element`]: SearchFiltersToggleElement,
}

const overriddenComponents = overrideStore.getAll()

createSearchAppInit(
  { ...defaultComponents, ...overriddenComponents },
  true,
  'invenio-search-config',
  true,
)