import {
  createSearchAppsInit,
  parseSearchAppConfigs,
  SearchappSearchbarElement,
} from "@js/oarepo_ui";
import { OaiRunResultsListItemWithState } from "./components/OaiRunResultsListItem";

const [searchAppConfig, ..._] = parseSearchAppConfigs();
const { overridableIdPrefix } = searchAppConfig;

export const componentOverrides = {
  [`${overridableIdPrefix}.ResultsList.item`]: OaiRunResultsListItemWithState,
  [`${overridableIdPrefix}.SearchBar.element`]: SearchappSearchbarElement,
};

createSearchAppsInit({ componentOverrides });
