###
 * ReactJS controlled component
###
import React from "react"
import ReactDOM from "react-dom"

import DataBoxAPI from "./api.coffee"

import QueryTypeSelection from "./components/QueryTypeSelection.js"
import Messages from "./components/Messages.coffee"


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

    # Bind `this` in methods
    @dismissMessage = @dismissMessage.bind @
    @handleChange = @handleChange.bind(this)
    @on_api_error = @on_api_error.bind(this)

    # root element
    @root_el = @props.root_el

    # get initial configuration data from the HTML attribute
    @query_type = @root_el.dataset.query_type
    @query_types = JSON.parse @root_el.dataset.query_types

    # Initialize the DataBox API
    @api = new DataBoxAPI
      on_api_error: @on_api_error

    # Initialize the state
    @state =
      # alert messages
      messages: []
      # the seleected query type
      query_type: @query_type
      # the available query types
      query_types: @query_types

  componentDidMount: ->
    console.debug "DataBoxController::componentDidMount"

  componentDidUpdate: ->
    console.debug "DataBoxController::componentDidUpdate"

  handleChange: (event) ->
    target = event.target
    value = if target.type is "checkbox" then target.checked else target.value
    name = target.name
    option =
      [name]: value
    console.info "DataBoxController::handleChange: name=#{name} value=#{value}"


  ###*
   * Display a new bootstrap alert message above the table
   *
   * @param title {string} Title to be displayed in the alert box
   *              {object} Config object for all parameters
   * @param text {string} The message text
   * @param traceback {string} Preformatted traceback
   * @param level {string} info, success, warning, danger
   * @returns {bool} true
  ###
  addMessage: (title, text, traceback, level="info") ->
    if typeof title is "object"
      props = Object.assign title
      title = props.title
      text = props.text
      traceback = props.traceback
      level = props.level

    messages = [].concat @state.messages
    messages.push({
      title: title,
      text: text
      traceback: traceback,
      level: level,
    })
    @setState {messages: messages}
    return true


  ###*
   * Dismisses a message by its message index
   *
   * @param index {int} Index of the message to dismiss
   * @returns {bool} true
  ###
  dismissMessage: (index=null) ->
    # dismiss all messages
    if index is null
      @setState {messages: []}
    else
      # dismiss message by index
      messages = [].concat @state.messages
      messages.splice index, 1
      @setState {messages: messages}
    return true


  on_api_error: (response) ->
    console.debug "°°° ListingController::on_api_error: GOT AN ERROR RESPONSE: ", response
    response.text().then (data) =>
      title = _t("Oops, an error occured! 🙈")
      message = _t("The server responded with the status #{response.status}: #{response.statusText}")
      @addMessage title, message, null, level="danger"
    return response

  render: ->
    <div className="databox-container mt-2 mb-4">
      <Messages on_dismiss_message={@dismissMessage} id="messages" className="messages" messages={@state.messages} />
      <div className="input-group">
        <QueryTypeSelection
          name="query_type"
          api={@api}
          value={@state.query_type}
          query_types={@state.query_types}
          onChange={@handleChange}
          className="form-control"
          name="portal_type" />
      </div>
    </div>
