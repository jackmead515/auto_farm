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
        pumpLoading: false,
        growLoading: false,
        heatLoading: false,
        cameraLoading: false,

        pump_enabled: true,
        pump_time: 10,
        pump_interval: 30,
        pump_mode: "auto",
        soil_sensor_limit: 60,

        grow_lights_enabled: true,
        morning_time: 5,
        night_time: 20,

        heat_lights_enabled: true,
        heat_time: 10,
        day_temp: 26,
        night_temp: 24,

        cameras_enabled: true,
        image_interval: 30,
        imagedb_host: "",
        imagedb_password: "",
        imagedb_username: "jack",
      }
  }

  componentWillMount() {
    window.addEventListener("resize", () => this.updateDimensions());
    const dims = Util.getWindowDimensions();
    this.setState({windowHeight: dims.height, windowWidth: dims.width, loading: false}, () => {
      this.fetchStatusAndInfo().then(() => {
        this.setState({loading: false, ...this.props.info.info });
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

  submitPumpControl() {
    const { pump_enabled,
    pump_time,
    pump_interval,
    pump_mode,
    soil_sensor_limit } = this.state;
    this.setState({pumpLoading: true}, () => {
      Fetch.submitPumpControl({pump_enabled, pump_time, pump_interval, pump_mode, soil_sensor_limit}).then((res) => {
        this.fetchStatusAndInfo().then(() => {
          this.setState({pumpLoading: false, ...this.props.info.info });
        });
      });
    })
  }

  submitGrowLightControl() {
    const { grow_lights_enabled,
    morning_time,
    night_time } = this.state;
    this.setState({growLoading: true}, () => {
      Fetch.submitGrowLightControl({grow_lights_enabled, morning_time, night_time}).then((res) => {
        this.fetchStatusAndInfo().then(() => {
          this.setState({growLoading: false, ...this.props.info.info });
        });
      });
    })
  }

  submitHeatLightControl() {
    const { heat_lights_enabled,
    heat_time,
    day_temp,
    night_temp } = this.state;
    this.setState({heatLoading: true}, () => {
      Fetch.submitHeatLightControl({heat_lights_enabled, heat_time, day_temp, night_temp}).then((res) => {
        this.fetchStatusAndInfo().then(() => {
          this.setState({heatLoading: false, ...this.props.info.info });
        });
      })
    })
  }

  submitCameraControl() {
    const { cameras_enabled,
    image_interval,
    imagedb_host,
    imagedb_username,
    imagedb_password } = this.state;
    if(!this.validateImageDatabaseHost(imagedb_host).border) {
      this.setState({cameraLoading: true}, () => {
        Fetch.submitCameraControl({cameras_enabled, image_interval, imagedb_host, imagedb_username, imagedb_password}).then((res) => {
          this.fetchStatusAndInfo().then(() => {
            this.setState({cameraLoading: false, ...this.props.info.info });
          });
        });
      })
    }
  }

  validateImageDatabaseHost(imagedb_host) {
    if(imagedb_host && imagedb_host.length > 0 && imagedb_host.match(/^(\d{1,3}\.){3}\d{1,3}$/g)) {
      return {}
    } else {
      return {border: '1px solid red', backgroundColor: 'rgba(255, 0, 0, 0.2)'}
    }
  }

  renderPumpControl() {
    const { pump_time, pump_interval, pump_mode, pump_enabled, soil_sensor_limit, pumpLoading } = this.state;
    const { info } = this.props.info;

    return (
      <div className="settings__pump">
        {pumpLoading ? <div className="settings__loading"><div className="loader--large" /></div> : null}
        <h3 className="settings__pump__heading">
          Pump Control
          <button onClick={() => this.submitPumpControl()}>Submit</button>
        </h3>
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
                  max="1440"
                  className="settings__slider"
                  onChange={(e) => this.setState({pump_interval: e.target.value})}
                />
              <span>{pump_interval + " min"}</span>
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

  renderGrowLightControl() {
    const { grow_lights_enabled, morning_time, night_time, growLoading } = this.state;
    const { info } = this.props.info;

    return (
      <div className="settings__grow">
        {growLoading ? <div className="settings__loading"><div className="loader--large" /></div> : null}
        <h3 className="settings__grow__heading">
          Grow Light Control
          <button onClick={() => this.submitGrowLightControl()}>Submit</button>
        </h3>
        <div className="settings__grow__input">
          <div className="settings__grow__enabled">
            <p>Enabled</p>
              <label className="checkbox">
                <input
                  checked={grow_lights_enabled}
                  onChange={(e) => this.setState({grow_lights_enabled: e.target.checked})}
                  type="checkbox"
                />
              <div className="checkmark"/>
              </label>
          </div>
          <div className="settings__grow__day">
            <p>Morning Hour</p>
            <div className="row">
                <input
                  style={{marginRight: 10}}
                  value={morning_time}
                  type="range"
                  min="0"
                  max="23"
                  className="settings__slider"
                  onChange={(e) => this.setState({morning_time: e.target.value})}
                />
              <span>{morning_time + ":00"}</span>
            </div>
          </div>
          <div className="settings__grow__night">
            <p>Night Hour</p>
            <div className="row">
              <input
                style={{marginRight: 10}}
                value={night_time}
                type="range"
                min="0"
                max="23"
                className="settings__slider"
                onChange={(e) => this.setState({night_time: e.target.value})}
              />
            <span>{night_time + ":00"}</span>
            </div>
          </div>
        </div>
      </div>
    )
  }

  renderHeatLightControl() {
    const { heat_lights_enabled, day_temp, night_temp, heat_time, heatLoading } = this.state;
    const { info } = this.props.info;

    return (
      <div className="settings__heat">
        {heatLoading ? <div className="settings__loading"><div className="loader--large" /></div> : null}
        <h3 className="settings__heat__heading">
          Heat Light Control
          <button onClick={() => this.submitHeatLightControl()}>Submit</button>
        </h3>
        <div className="settings__heat__input">
          <div className="settings__heat__enabled">
            <p>Enabled</p>
              <label className="checkbox">
                <input
                  checked={heat_lights_enabled}
                  onChange={(e) => this.setState({heat_lights_enabled: e.target.checked})}
                  type="checkbox"
                />
              <div className="checkmark"/>
              </label>
          </div>
          <div className="settings__heat__time">
            <p>Max Heat Time</p>
            <div className="row">
              <input
                style={{marginRight: 10}}
                value={heat_time}
                type="range"
                min="1"
                max="60"
                className="settings__slider"
                onChange={(e) => this.setState({heat_time: e.target.value})}
              />
              <span>{heat_time + " mins"}</span>
            </div>
          </div>
          <div className="settings__heat__day">
            <p>Day Temperature</p>
            <div className="row">
                <input
                  style={{marginRight: 10}}
                  value={day_temp}
                  type="range"
                  min="20"
                  max="40"
                  className="settings__slider"
                  onChange={(e) => this.setState({day_temp: e.target.value})}
                />
              <span>{day_temp + " C"}</span>
            </div>
          </div>
          <div className="settings__heat__night">
            <p>Night Temperature</p>
            <div className="row">
              <input
                style={{marginRight: 10}}
                value={night_temp}
                type="range"
                min="20"
                max="40"
                className="settings__slider"
                onChange={(e) => this.setState({night_temp: e.target.value})}
              />
            <span>{night_temp + " C"}</span>
            </div>
          </div>
        </div>
      </div>
    )
  }

  renderCameraControl() {
    const { cameras_enabled,
      image_interval,
      imagedb_host,
      cameraLoading,
      imagedb_password,
      imagedb_username,
      imagedb
    } = this.state;
    const { info } = this.props.info;

    return (
      <div className="settings__camera">
        {cameraLoading ? <div className="settings__loading"><div className="loader--large" /></div> : null}
        <h3 className="settings__camera__heading">
          Cameras Control
          <button onClick={() => this.submitCameraControl()}>Submit</button>
        </h3>
        <div className="settings__camera__input">
          <div className="settings__camera__enabled">
            <p>Enabled</p>
              <label className="checkbox">
                <input
                  checked={cameras_enabled}
                  onChange={(e) => this.setState({cameras_enabled: e.target.checked})}
                  type="checkbox"
                />
              <div className="checkmark"/>
              </label>
          </div>
          <div className="settings__camera__host">
            <p>Image Database Host</p>
            <input
              style={{...this.validateImageDatabaseHost(this.state.imagedb_host)}}
              value={imagedb_host}
              type="text"
              className="settings__input"
              onChange={(e) => this.setState({imagedb_host: e.target.value})}
            />
          </div>
          <div className="settings__camera__username">
            <p>Username</p>
            <input
              value={imagedb_username}
              type="text"
              className="settings__input"
              onChange={(e) => this.setState({imagedb_username: e.target.value})}
            />
          </div>
          <div className="settings__camera__password">
            <p>Password</p>
            <input
              value={imagedb_password}
              type="password"
              className="settings__input"
              onChange={(e) => this.setState({imagedb_password: e.target.value})}
            />
          </div>
          <div className="settings__camera__interval">
            <p>Image Interval</p>
            <div className="row">
                <input
                  style={{marginRight: 10}}
                  value={image_interval}
                  type="range"
                  min="1"
                  max="720"
                  className="settings__slider"
                  onChange={(e) => this.setState({image_interval: e.target.value})}
                />
              <span>{image_interval + " mins"}</span>
            </div>
          </div>
        </div>
      </div>
    )
  }

  renderLoading() {
    return (
      <div style={{display: 'flex', alignItems: 'center', margin: 10}}>
        <div className="loader--small"/>
        <p style={{marginLeft: 10, padding: 0}}>Loading...</p>
      </div>
    )
  }

  renderFull() {
    return (
      <div className="settings__container">
        <Navigator />
        {this.renderPumpControl()}
        {this.renderHeatLightControl()}
        {this.renderGrowLightControl()}
        {this.renderCameraControl()}
      </div>
    );
  }

  renderMobile() {
    return (
      <div className="settings__container--mobile">
        <Navigator mobile={true} />
        {this.renderPumpControl()}
        {this.renderHeatLightControl()}
        {this.renderGrowLightControl()}
        {this.renderCameraControl()}
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
