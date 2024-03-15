import {
  createSearchAppsInit,
  parseSearchAppConfigs,
  SearchappSearchbarElement,
} from "@js/oarepo_ui";
import { OaiBatchResultsListItemWithState } from "./components/OaiBatchResultsListItem";

const [searchAppConfig, ..._] = parseSearchAppConfigs();
const { overridableIdPrefix } = searchAppConfig;

export const componentOverrides = {
  [`${overridableIdPrefix}.ResultsList.item`]: OaiBatchResultsListItemWithState,
  [`${overridableIdPrefix}.SearchBar.element`]: SearchappSearchbarElement,
};

createSearchAppsInit({ componentOverrides });
