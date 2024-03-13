import {
  createSearchAppsInit,
  parseSearchAppConfigs,
  SearchappSearchbarElement,
} from "@js/oarepo_ui";
import { OaiRecordResultsListItemWithState } from "./components/OaiRecordResultsListItem";

const [searchAppConfig, ..._] = parseSearchAppConfigs();
const { overridableIdPrefix } = searchAppConfig;

export const componentOverrides = {
  [`${overridableIdPrefix}.ResultsList.item`]:
    OaiRecordResultsListItemWithState,
  [`${overridableIdPrefix}.SearchBar.element`]: SearchappSearchbarElement,
};

createSearchAppsInit({ componentOverrides });
