import React from "react"

class QueryTypeSelection extends React.Component {
  constructor(props) {
    super(props)
    this.api = props.api;
    this.state = {
      types: []
    };
  }

  fetch() {
    this.api.fetch_querytypes().then(data => {
      this.setState(
        {types: data}
      );
    });
  }

  componentDidMount() {
    this.fetch();
  }

  buildOptions() {
    let options = [];
    let types = this.state.types;
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
