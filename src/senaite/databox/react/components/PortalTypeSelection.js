import React from "react"

class PortalTypeSelection extends React.Component {
  constructor(props) {
    super(props)
  }

  render() {
    return (
      <select value={this.props.value}
              onChange={this.props.onChange}
              name={this.props.name}
              className={this.props.className}>

        <option key="analysisrequest" value="AnalysisRequest">AnalysisRequest</option>
        <option key="client" value="Client">Client</option>
        <option key="instrument" value="Instrument">Instrument</option>

      </select>

    )
  }
}

export default PortalTypeSelection
