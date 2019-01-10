/* @flow weak */

import React, { Component } from 'react';
import { connect } from 'react-redux';

import _ from 'lodash';
import moment from 'moment';
import * as d3 from 'd3';

import faker from 'faker';

import { refreshStatus, refreshInfo } from '../../actions/info';

import Fetch from '../../util/Fetch';
import TimeUtil from '../../util/TimeUtil';
import Util from '../../util/Util';
//import temperature from '../../util/samples/temperature.json';

import Graph from './Graph';

import GalleryImage from '../../components/GalleryImage';

import FAIcon from 'react-fontawesome';

class Dashboard extends Component {
  constructor(props) {
      super(props);

      this.state = {
        loading: true,
        info: null,
        temperature: [],
        humidity: [],
        heat: [],
        messages: [],
        images: [],
        imagedata: [],
      }

      this.statusInterval = null;
      this.fetchingStatus = false;
  }

  componentWillMount() {
    window.addEventListener("resize", () => this.updateDimensions());
    const dims = Util.getWindowDimensions();
    this.setState({windowHeight: dims.height, windowWidth: dims.width});
  }

  componentDidMount() {
    this.fetchInitialData().then(() => {

      Fetch.images(0).then((res) => {
        this.setState({images: res.data.data}, () => {
          this.state.images.map((image) => {
            Fetch.image(image[1]).then((res) => {
              let { imagedata } = this.state;
              imagedata.push({name: image[1], date: image[2], data: res.data.data});
              //imagedata = _.sortBy(imagedata, (d) => moment(d.date).valueOf());
              this.setState({imagedata});
            });
          });
        });
      });

      /*Fetch.messages().then((res) => {
        const messages = res.data.data;
        let comps = this.generateMessages(messages);
        this.setState({messages: comps});
      });*/

      this.statusInterval = setInterval(() => {
        if(!this.fetchingStatus) {
          this.fetchingStatus = true;
          this.fetchStatusAndInfo().then(() => {
            this.fetchingStatus = false;
          });
        }
      }, 2000);
    });
  }

  componentWillReceiveProps(nextProps) {

  }

  componentWillUnmount() {
    window.removeEventListener("resize", () => this.updateDimensions());
    clearInterval(this.statusInterval);
    this.statusInterval = null;
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

  fetchInitialData() {
    return new Promise((resolve, reject) => {
      Fetch.status().then((res) => {
        const status = res.data.data;
        Fetch.info().then((res) => {
          const info = res.data.data;
          let now = moment().format("YYYY-MM-DD HH:mm:ss");
          let weekAgo = moment().subtract(2, 'day').format("YYYY-MM-DD HH:mm:ss");
          Fetch.temperature(weekAgo, now).then((res) => {
            let temperature = res.data.data;
            temperature = _.sortBy(temperature, (d) => moment(d[1]).valueOf());
            now = moment().format("YYYY-MM-DD HH:mm:ss");
            weekAgo = moment().subtract(2, 'day').format("YYYY-MM-DD HH:mm:ss");
            Fetch.humidity(weekAgo, now).then((res) => {
              let humidity = res.data.data;
              humidity = _.sortBy(humidity, (d) => moment(d[1]).valueOf());
              now = moment().format("YYYY-MM-DD HH:mm:ss");
              weekAgo = moment().subtract(2, 'day').format("YYYY-MM-DD HH:mm:ss");
              Fetch.heat(weekAgo, now).then((res) => {
                let heat = res.data.data;

                let kwh = Util.getTotalHeatKiloWattHours(200, heat);

                this.props.dispatch(refreshStatus(status));
                this.props.dispatch(refreshInfo(info));

                this.setState({temperature, info, status, humidity, heat, heatKiloWatts: kwh, loading: false}, () => {
                  resolve();
                });

              });
            });
          });
        });
      });
    });
  }

  updateDimensions() {
    const dims = Util.getWindowDimensions();
    this.setState({windowHeight: dims.height, windowWidth: dims.width});
  }

  generateMessages(messages) {
    const headingMessages = [];
    for(let i = messages.length-1; i >= 0; i--) {
      let style = {marginBottom: 10};
      if(i == 0) { style = {border: 0, padding: 0}; }
      const message = messages[i];

      //<div className="dashboard__headingmessage--date">{moment(faker.date.past()).format("MMM Do, k:mm")}</div>
      //<div className="dashboard__headingmessage--text">{faker.lorem.sentences(2)}</div>

      headingMessages.push((
        <div
          key={i}
          style={style}
          className="dashboard__headingmessage"
        >
          <div className="dashboard__headingmessage--date">{moment(message[1]).format("MMM Do, k:mm")}</div>
          <div className="dashboard__headingmessage--title">{message[2]}</div>
          <div className="dashboard__headingmessage--text">{message[3]}</div>
        </div>
      ));
    }

    return headingMessages;
  }

  renderEnergyConsumption() {
    const { heatKiloWatts } = this.state;

    let elapsed = heatKiloWatts.endDate.from(heatKiloWatts.startDate, true);

    return (
      <div className="dashboard__heading">
        <h3><FAIcon className="dashboard__energybolt" name="bolt"/> Energy Usage</h3>
        <p>{"~" + heatKiloWatts.kiloWatts.toFixed(2) + " kWH / " + elapsed}</p>
      </div>
    )
  }

  renderCurrentTemperature() {
    const { info } = this.state;

    const currentTemp = info.current_temp == null ? "n/a" : info.current_temp.toFixed(2);
    const colorScale = d3.scaleLinear().domain([0, 26, 50]).range(["blue", "#02fc23", "red"]);

    return (
      <div className="dashboard__heading">
        <h3><FAIcon className="dashboard__thermometer" name="thermometer-half"/> Temperature</h3>
        <p style={{color: colorScale(currentTemp)}}>{currentTemp} &#8451;</p>
      </div>
    )
  }

  renderCurrentHumidity() {
    const { info } = this.state;

    const currentHumid = info.current_humid == null ? "n/a" : info.current_humid.toFixed(2);

    return (
      <div className="dashboard__heading" style={{border: 0, margin: 0, padding: 0}}>
        <h3><FAIcon className="dashboard__waterdrop" name="tint"/> Humidity</h3>
        <p>{currentHumid} %</p>
      </div>
    )
  }

  renderStatus(mobile) {
    const { info, status } = this.props.info;
    const { temperature, humidity, heat, messages, heatKiloWatts } = this.state;

    const containerStyle = mobile ? {paddingBottom: 0} : {flex: 2}

    return (
      <div className="dashboard__statusinfo" style={containerStyle}>
        <div style={{marginBottom: 10}}>
          <div className="dashboard__device" style={{marginBottom: 10}}>
            <div style={{marginRight: 10}} className={status.cameras ? "dashboard__device--active" : "dashboard__device--inactive"}>
                Cameras
            </div>
            <div className={status.growlights ? "dashboard__device--active" : "dashboard__device--inactive"}>
                Grow Lights
            </div>
          </div>
          <div className="dashboard__device">
            <div style={{marginRight: 10}} className={status.heatlights ? "dashboard__device--active" : "dashboard__device--inactive"}>
                Heat Lamps
            </div>
            <div className={status.pump ? "dashboard__device--active" : "dashboard__device--inactive"}>
                Pump
            </div>
          </div>
        </div>
        <div className="dashboard__headingcontainer">
          {this.renderEnergyConsumption()}
          {this.renderCurrentTemperature()}
          {this.renderCurrentHumidity()}
        </div>
      </div>
    );
  }

  renderFull() {
    const { loading, windowHeight, windowWidth, imagedata, info, humidity, temperature } = this.state;

    let comps = []
    comps.push((
      <div className="dashboard__status" style={{height: windowHeight*0.75}} key="status">
        {loading ? null : this.renderStatus()}
        <Graph
          className="dashboard__graphcontainer"
          windowWidth={windowWidth}
          windowHeight={windowHeight}
          temperature={temperature}
          humidity={humidity}
          info={info}
        />
      </div>
    ));
    comps.push((
      <div className="dashboard__images" key="images">
        {imagedata.map((data, i) => {
          return <GalleryImage key={i} data={"data:image/png;base64," + data["data"]} name={data["name"]}/>
        })}
      </div>
    ))

    return comps;
  }

  renderMobile() {
    const { loading, windowHeight, windowWidth, imagedata, info, humidity, temperature } = this.state;
    return (
        <div className="dashboard__status--mobile">
          {loading ? null : this.renderStatus(true)}
          <Graph
            className="dashboard__graphcontainer--mobile"
            windowWidth={windowWidth}
            windowHeight={windowHeight}
            temperature={temperature}
            humidity={humidity}
            info={info}
          />
        </div>
    );
  }

  renderLoading() {
    return <div style={{margin: 10}}>{"Loading..."}</div>;
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

export default connect(mapStateToProps)(Dashboard);
