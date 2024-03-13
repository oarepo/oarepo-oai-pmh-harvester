import React from "react";
import PropTypes from "prop-types";
import Overridable from "react-overridable";

import _get from "lodash/get";

import { Item } from "semantic-ui-react";
import { withState, buildUID } from "react-searchkit";
import { i18next } from "@translations/oarepo_oaipmh_harvester/i18next";

export const OaiRunResultsListItemComponent = ({ result, appName }) => {
  const id = _get(result, "id");
  const started = _get(result, "started");
  const harvester = _get(result, "harvester.name");
  const viewLink = result.links.self_html;
  return (
    <Overridable
      id={buildUID("RecordsResultsListItem.layout", "", appName)}
      result={result}
      name={id}
    >
      <Item key={result.id}>
        <Item.Content>
          <Item.Extra className="labels-actions"></Item.Extra>
          <Item.Header as="h2">
            <a href={viewLink}>
              {i18next.t("run.label")} - {id}
            </a>
          </Item.Header>
          <Item.Description>
            {harvester}
            <br />
            {i18next.t("run/started.label")} - {started}
          </Item.Description>
        </Item.Content>
      </Item>
    </Overridable>
  );
};

OaiRunResultsListItemComponent.propTypes = {
  currentQueryState: PropTypes.object,
  result: PropTypes.object.isRequired,
  appName: PropTypes.string,
};

OaiRunResultsListItemComponent.defaultProps = {
  currentQueryState: null,
  appName: "",
};

export const OaiRunResultsListItem = (props) => {
  return (
    <Overridable
      id={buildUID("OaiRunResultsListItem", "", props.appName)}
      {...props}
    >
      <OaiRunResultsListItemComponent {...props} />
    </Overridable>
  );
};

OaiRunResultsListItem.propTypes = {
  currentQueryState: PropTypes.object,
  result: PropTypes.object.isRequired,
  appName: PropTypes.string,
};

OaiRunResultsListItem.defaultProps = {
  currentQueryState: null,
  appName: "",
};

export const OaiRunResultsListItemWithState = withState(
  ({ currentQueryState, result, appName }) => (
    <OaiRunResultsListItem
      currentQueryState={currentQueryState}
      result={result}
      appName={appName}
    />
  )
);

OaiRunResultsListItemWithState.propTypes = {
  currentQueryState: PropTypes.object,
  result: PropTypes.object.isRequired,
};

OaiRunResultsListItemComponent.defaultProps = {
  currentQueryState: null,
};
