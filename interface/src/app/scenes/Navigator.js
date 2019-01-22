/* @flow weak */

import React, { Component } from 'react';
import { Link } from 'react-router-dom';

import FAIcon from 'react-fontawesome';

export default class Navigator extends Component {
  constructor(props) {
      super(props);

      this.state = {

      }
  }

  componentWillMount() {}
  componentDidMount() {}
  componentWillUnmount() {}

  render() {
    return (
      <div className={this.props.mobile ? "navigator__container--mobile" : "navigator__container"}>
        <Link to="/" className="navigator__button" title="Dashboard" style={{marginRight: 10}}>
          <FAIcon name="home" />
        </Link>
        <Link to="/settings" className="navigator__button" title="Settings">
          <FAIcon name="sliders-h" />
        </Link>
      </div>
    );
  }
}
