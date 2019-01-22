/* @flow weak */

import React, { Component } from 'react';
import { connect } from 'react-redux';

import { refreshStatus, refreshInfo } from '../../actions/info';

import Navigator from '../Navigator';

import Fetch from '../../util/Fetch';
import Util from '../../util/Util';

class Settings extends Component {
  constructor(props) {
      super(props);

      this.state = {
        loading: true,
        
        pump_time: 10,
        pump_interval: 30*60,
        pump_mode: "auto",
        pump_enabled: true,
        soil_sensor_limit: 60
      }
  }

  componentWillMount() {
    window.addEventListener("resize", () => this.updateDimensions());
    const dims = Util.getWindowDimensions();
    this.setState({windowHeight: dims.height, windowWidth: dims.width}, () => {
      this.fetchStatusAndInfo().then(() => {
        this.setState({loading: false});
      });
    });
  }

  fetchStatusAndInfo() {
    return new Promise((resolve, reject) => {
      Fetch.status().then((res) => {
        const status = res.data.data;
        Fetch.info().then((res) => {
          const info = res.data.data;
          this.props.dispatch(refreshStatus(status));
          this.props.dispatch(refreshInfo(info));
          resolve();
        });
      });
    });
  }

  updateDimensions() {
    const dims = Util.getWindowDimensions();
    this.setState({windowHeight: dims.height, windowWidth: dims.width});
  }

  renderPumpControl() {
    const { pump_time, pump_interval, pump_mode, pump_enabled, soil_sensor_limit } = this.state;
    const { info } = this.props.info;

    return (
      <div className="settings__pump">
        <h3 className="settings__pump__heading">Pump Control<button>Submit</button></h3>
        <div className="settings__pump__input">
          <div className="settings__pump__pumpenabled">
            <p>Enabled</p>
              <label className="checkbox">
                <input
                  checked={pump_enabled}
                  onChange={(e) => this.setState({pump_enabled: e.target.checked})}
                  type="checkbox"
                />
              <div className="checkmark"/>
              </label>
          </div>
          <div className="settings__pump__pumpmode">
            <p>Pump Mode</p>
            <div className="row">
              <label className="checkbox">
                <input
                  type="radio"
                  checked={pump_mode === "auto" ? true : false}
                  onChange={(e) => this.setState({pump_mode: "auto"})}
                />
              <div className="radiobutton"/>
              </label>
              <span style={{marginRight: 15}}>Auto</span>
              <label className="checkbox">
                <input
                  type="radio"
                  checked={pump_mode === "manual" ? true : false}
                  onChange={(e) => this.setState({pump_mode: "manual"})}
                />
                <div className="radiobutton"/>
              </label>
              <span>Manual</span>
            </div>
          </div>
          <div className="settings__pump__pumptime">
            <p>Pump Time</p>
            <div className="row">
                <input
                  style={{marginRight: 10}}
                  value={pump_time}
                  type="range"
                  min="1"
                  max="30"
                  className="settings__slider"
                  onChange={(e) => this.setState({pump_time: e.target.value})}
                />
                <span>{pump_time + " sec"}</span>
            </div>
          </div>
          <div className="settings__pump__pumpinterval">
            <p>Pump Interval</p>
            <div className="row">
                <input
                  style={{marginRight: 10}}
                  value={pump_interval}
                  type="range"
                  min="1"
                  max="18000"
                  className="settings__slider"
                  onChange={(e) => this.setState({pump_interval: e.target.value})}
                />
              <span>{pump_interval + " sec"}</span>
            </div>
          </div>
          <div className="settings__pump__soillimit">
            <p>Soil Limit</p>
            <div className="row">
              <input
                style={{marginRight: 10}}
                value={soil_sensor_limit}
                type="range"
                min="1"
                max="100"
                className="settings__slider"
                onChange={(e) => this.setState({soil_sensor_limit: e.target.value})}
              />
              <span>{soil_sensor_limit + "%"}</span>
            </div>
          </div>
        </div>
      </div>
    )
  }

  renderLoading() {
    return <div style={{margin: 10}}>{"Loading..."}</div>;
  }

  renderFull() {
    return (
      <div className="settings__container">
        <Navigator />
        {this.renderPumpControl()}
      </div>
    );
  }

  renderMobile() {
    return (
      <div className="settings__container--mobile">
        <Navigator mobile={true} />
        {this.renderPumpControl()}
      </div>
    );
  }

  render() {
    const { loading, windowWidth } = this.state;

    if(loading) {
      return this.renderLoading();
    } else {
      return windowWidth < 700 ? this.renderMobile() : this.renderFull();
    }
  }
}

const mapStateToProps = (state) => {
  return { ...state };
}

export default connect(mapStateToProps)(Settings);
