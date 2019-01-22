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

import Navigator from '../Navigator';

import TempHumidGraph from './TempHumidGraph';
import SoilGraph from './SoilGraph';

import GalleryImage from '../../components/GalleryImage';

import FAIcon from 'react-fontawesome';

class Dashboard extends Component {
  constructor(props) {
      super(props);

      this.state = {
        loading: true,
        info: null,
        toggleSoil: false,
        temperature: [],
        humidity: [],
        heat: [],
        lights: [],
        pump: [],
        messages: [],
        images: [],
        imagedata: [],
        energyUsage: null
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
          this.state.images.slice(0, 4).map((image) => {
            Fetch.image(image[1]).then((res) => {
              let { imagedata } = this.state;
              imagedata.push({name: image[1], date: image[2], data: res.data.data});
              this.setState({imagedata});
            });
          });
        });
      });

      let now = moment().format("YYYY-MM-DD HH:mm:ss");
      let weekAgo = moment().subtract(2, 'day').format("YYYY-MM-DD HH:mm:ss");
      Fetch.heat(weekAgo, now).then((res) => {
        const heat = res.data.data;
        now = moment().format("YYYY-MM-DD HH:mm:ss");
        weekAgo = moment().subtract(2, 'day').format("YYYY-MM-DD HH:mm:ss");
        Fetch.lights(weekAgo, now).then((res) => {
          const lights = res.data.data;
          const energyUsage = Util.calculateEnergy({sensors: 3.5, heat: 200, lights: 70}, heat, lights)
          this.setState({heat, lights, energyUsage})
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
              Fetch.soil(weekAgo, now).then((res) => {
                let soil = res.data.data;

                this.props.dispatch(refreshStatus(status));
                this.props.dispatch(refreshInfo(info));

                this.setState({temperature, info, status, humidity, soil, loading: false}, () => {
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
    const { energyUsage } = this.state;

    let comp = null;
    if(energyUsage) {
        let elapsed = energyUsage.endDate.from(energyUsage.startDate, true);
        comp = <p>{"~" + energyUsage.kiloWatts.toFixed(2) + " kWH / " + elapsed}</p>
    } else {
      comp = <div className="loader--small" />
    }

    return (
      <div className="dashboard__heading">
        <h3><FAIcon className="dashboard__energybolt" name="bolt"/> Energy Usage</h3>
        {comp}
      </div>
    )
  }

  renderCurrentTemperature() {
    const { info } = this.props.info;

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
    const { info } = this.props.info;

    const currentHumid = info.current_humid == null ? "n/a" : info.current_humid.toFixed(2);

    return (
      <div className="dashboard__heading">
        <h3><FAIcon className="dashboard__waterdrop" name="tint"/> Humidity</h3>
        <p>{currentHumid} %</p>
      </div>
    )
  }

  renderCurrentSoilMoisture() {
    const { info } = this.props.info;
    const { toggleSoil } = this.state;

    let currentSoil = info.current_soil == null || (info.current_soil && info.current_soil.length <= 0) ? [0.0] : info.current_soil;
    currentSoil = currentSoil.filter((d) => d.value !== -1);
    const median = d3.median(currentSoil, (d) => d.value);

    const medianExpression = median ? "~" + median.toFixed(2) + "%" : 'n/a';

    let sensors = null;
    if(toggleSoil && currentSoil.length > 0) {
      sensors = (
        <div className="animatedFast fadeInDown row" style={{justifyContent: 'space-around', marginTop: 10}}>
          {currentSoil.map((d, i) => {
            return (
              <div key={i} className="dashboard__soilsensor">
                <FAIcon name="filter"/> {d.value} %
              </div>
            )
          })}
        </div>
      )
    }

    return (
      <div className="dashboard__colheading">
        <div className="row" style={{justifyContent: 'space-between', alignItems: 'center'}}>
          <h3><FAIcon className="dashboard__soilwater" name="water"/> Soil Moisture</h3>
          <p>
            <span>{medianExpression}</span>
            <FAIcon
              className="dashboard__soilbutton"
              name={toggleSoil ? "caret-square-left" : "caret-square-down"}
              onClick={() => this.setState({toggleSoil: !this.state.toggleSoil})}
            />
          </p>
        </div>
        {sensors}
      </div>
    )
  }

  renderStatus() {
    const { info, status } = this.props.info;
    const { temperature, humidity, heat, messages, heatKiloWatts } = this.state;

    return (
      <div className="dashboard__statusinfo">
        <div className="dashboard__devicecontainer">
          <div className={status.cameras ? "dashboard__device--active" : "dashboard__device--inactive"}>
              Cameras
          </div>
          <div className={status.growlights ? "dashboard__device--active" : "dashboard__device--inactive"}>
              Grow Lights
          </div>
          <div className={status.heatlights ? "dashboard__device--active" : "dashboard__device--inactive"}>
              Heat Lamps
          </div>
          <div className={status.pump ? "dashboard__device--active" : "dashboard__device--inactive"}>
              Pump
          </div>
        </div>
        <div className="dashboard__headingcontainer">
          {this.renderEnergyConsumption()}
          {this.renderCurrentTemperature()}
          {this.renderCurrentHumidity()}
          {this.renderCurrentSoilMoisture()}
        </div>
      </div>
    );
  }

  renderFull() {
    const { loading, windowHeight, windowWidth, imagedata, info, humidity, temperature, soil } = this.state;

    return (
      <div className="dashboard__container">
        <Navigator />
        {this.renderStatus()}
        <TempHumidGraph
          className="dashboard__graphcontainer--temp"
          windowWidth={windowWidth}
          windowHeight={windowHeight}
          temperature={temperature}
          humidity={humidity}
          info={info}
        />
        <div className="dashboard__images">
          {imagedata.map((data, i) => {
            return <GalleryImage key={i} data={"data:image/png;base64," + data["data"]} name={data["name"]}/>
          })}
          <div className="dashboard__images--viewmore">View more...</div>
        </div>
        <SoilGraph
          className="dashboard__graphcontainer--soil"
          windowWidth={windowWidth}
          windowHeight={windowHeight}
          soil={soil}
          info={info}
        />
      </div>
    );
  }

  renderMobile() {
    const { loading, windowHeight, windowWidth, imagedata, info, humidity, temperature, soil } = this.state;
    return (
        <div className="dashboard__container--mobile">
          <Navigator mobile={true} />
          {this.renderStatus()}
          <TempHumidGraph
            mobile={true}
            style={{height: ((5/14)*windowWidth+(1550/7))}}
            className="dashboard__graphcontainer--mobile"
            windowWidth={windowWidth}
            windowHeight={windowHeight}
            temperature={temperature}
            humidity={humidity}
            info={info}
          />
          <div className="dashboard__images--mobile">
            {imagedata.map((data, i) => {
              return <GalleryImage key={i} data={"data:image/png;base64," + data["data"]} name={data["name"]}/>
            })}
            <div className="dashboard__images--viewmore--mobile">View more...</div>
          </div>
          <SoilGraph
            mobile={true}
            style={{height: ((5/14)*windowWidth+(1550/7))}}
            className="dashboard__graphcontainer--mobile"
            windowWidth={windowWidth}
            windowHeight={windowHeight}
            soil={soil}
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
