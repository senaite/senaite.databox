###
 * ReactJS controlled component
###
import React from "react"
import ReactDOM from "react-dom"

# DOCUMENT READY ENTRY POINT
document.addEventListener "DOMContentLoaded", ->
  databoxes = document.getElementsByClassName "databox"
  if databoxes.length > 0
    console.debug("*** SENAITE.DATABOX::DOMContentLoaded: -->
      Loading ReactJS Controller")

  window.databoxes ?= {}
  for databox in databoxes
    databox_id = databox.dataset.databox_id
    controller = ReactDOM.render <DataBoxController root_el={databox}/>, databox
    # Keep a reference to the listing
    window.databoxes[databox_id] = controller


class DataBoxController extends React.Component

  constructor: (props) ->
    super(props)
    console.debug "DataBoxController::constructor"

  render: ->
    "DATABOX EDIT"
