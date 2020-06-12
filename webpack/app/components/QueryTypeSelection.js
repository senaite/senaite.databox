import React from "react"

class QueryTypeSelection extends React.Component {
  constructor(props) {
    super(props)
    this.api = props.api;
  }

  buildOptions() {
    let options = [];
    let types = this.props.query_types;
    for (let [key, value] of Object.entries(types)) {
      options.push(
        <option key={key} value={value}>{value}</option>
      );
    }
    return options;
  }

  render() {
    return (
      <select value={this.props.value}
              onChange={this.props.onChange}
              name={this.props.name}
              className={this.props.className}>
        {this.buildOptions()}
      </select>

    )
  }
}

export default QueryTypeSelection
