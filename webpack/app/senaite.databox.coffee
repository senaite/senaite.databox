###
 * ReactJS controlled component
###
import React from "react"
import ReactDOM from "react-dom"

import PortalTypeSelection from "./components/PortalTypeSelection.js"


# DOCUMENT READY ENTRY POINT
document.addEventListener "DOMContentLoaded", ->
  databoxes = document.getElementsByClassName "databox"
  if databoxes.length > 0
    console.debug("*** SENAITE.DATABOX::DOMContentLoaded: -->
      Loading ReactJS Controller")

  ###*
   * Initialize the edit view of the databoxe
  ###
  window.databoxes ?= {}
  for databox in databoxes
    databox_id = databox.dataset.databox_id
    controller = ReactDOM.render <DataBoxController root_el={databox}/>, databox
    # Keep a reference to the databox
    window.databoxes[databox_id] = controller


class DataBoxController extends React.Component

  constructor: (props) ->
    super(props)
    console.debug "DataBoxController::constructor"

  render: ->
    <div className="form-group">
      <div className="input-group">
        <PortalTypeSelection
          name="form.widgets.query_type:list"
          className="form-control"
          name="portal_type" />
      </div>
    </div>
