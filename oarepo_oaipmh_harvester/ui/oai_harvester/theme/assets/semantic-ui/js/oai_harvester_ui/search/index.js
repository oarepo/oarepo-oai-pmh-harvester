import {
  createSearchAppsInit,
  parseSearchAppConfigs,
  SearchappSearchbarElement,
} from "@js/oarepo_ui";
import { OaiHarvesterResultsListItemWithState } from "./components/OaiHarvesterResultsListItem";

const [searchAppConfig, ..._] = parseSearchAppConfigs();
const { overridableIdPrefix } = searchAppConfig;

export const componentOverrides = {
  [`${overridableIdPrefix}.ResultsList.item`]:
    OaiHarvesterResultsListItemWithState,
  [`${overridableIdPrefix}.SearchBar.element`]: SearchappSearchbarElement,
};

createSearchAppsInit({ componentOverrides });
