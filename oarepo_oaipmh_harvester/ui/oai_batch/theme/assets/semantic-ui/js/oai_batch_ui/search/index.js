import { createSearchAppInit } from '@js/invenio_search_ui'
import {
  ActiveFiltersElement,
  BucketAggregationElement,
  BucketAggregationValuesElement,
  ErrorElement,
  SearchAppFacets,
  SearchAppLayout,
  SearchAppResults,
  SearchAppResultOptions,
  SearchAppSearchbarContainer,
  SearchFiltersToggleElement,
  SearchAppSort
} from '@js/oarepo_ui/search'
import {
  OaiBatchResultsListItemWithState
} from './components'
import { parametrize, overrideStore } from 'react-overridable'

const appName = 'OaiBatch.Search'

const SearchAppSearchbarContainerWithConfig = parametrize(SearchAppSearchbarContainer, { appName: appName })
const ResultsListItemWithConfig = parametrize(OaiBatchResultsListItemWithState, { appName: appName })

export const defaultComponents = {
  [`${appName}.ActiveFilters.element`]: ActiveFiltersElement,
  [`${appName}.BucketAggregation.element`]: BucketAggregationElement,
  [`${appName}.BucketAggregationValues.element`]: BucketAggregationValuesElement,
  [`${appName}.Error.element`]: ErrorElement,
  [`${appName}.ResultsList.item`]: ResultsListItemWithConfig,
  [`${appName}.SearchApp.facets`]: SearchAppFacets,
  [`${appName}.SearchApp.layout`]: SearchAppLayout,
  [`${appName}.SearchApp.searchbarContainer`]: SearchAppSearchbarContainerWithConfig,
  [`${appName}.SearchApp.sort`]: SearchAppSort,
  [`${appName}.SearchApp.resultOptions`]: SearchAppResultOptions,
  [`${appName}.SearchApp.results`]: SearchAppResults,
  [`${appName}.SearchFilters.Toggle.element`]: SearchFiltersToggleElement,
}

const overriddenComponents = overrideStore.getAll()

createSearchAppInit(
  { ...defaultComponents, ...overriddenComponents },
  true,
  'invenio-search-config',
  true,
)