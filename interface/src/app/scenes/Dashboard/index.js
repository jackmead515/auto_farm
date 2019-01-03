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
          let promises = [];
          this.state.images.map((image) => {
            promises.push(Fetch.image(image[1]));
          });
          Promise.all(promises).then((data) => {
            data = data.map((d) => d.data.data);
            this.setState({imagedata: data});
          })
        });
      });

      Fetch.messages().then((res) => {
        const messages = res.data.data;
        let comps = this.generateMessages(messages);
        this.setState({messages: comps});
      });

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

                let totalHeatKiloWattHours = Util.getTotalHeatKiloWattHours(200, heat);

                this.props.dispatch(refreshStatus(status));
                this.props.dispatch(refreshInfo(info));

                this.setState({temperature, info, status, humidity, heat, totalHeatKiloWattHours, loading: false}, () => {
                  this.graphTemperature();
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
    this.setState({windowHeight: dims.height, windowWidth: dims.width}, () => {
      this.graphTemperature();
    });
  }

  graphTemperature() {
    const { temperature, humidity, info } = this.state;

    document.getElementById("temperature").innerHTML = "";

    const normalizeOutliers = (data, split, tolerance, minVal, maxVal) => {
      let chunks = _.chunk(data, data.length*split);
      let newArr = [];
      for(let i = 0; i < chunks.length; i++) {
        let chunk = chunks[i];
        let median = d3.median(chunk, (d) => d[2]);
        let maxMedian = median+(median*tolerance);
        let minMedian = median-(median*tolerance);
        let x = chunk.length;
        while(x--) {
          let c = chunk[x][2];
          if(c <= minVal || c >= maxVal) {
            chunk.splice(x, 1);
          } else if(c >= maxMedian || c <= minMedian || c <= minVal || c >= maxVal) {
            chunk[x][2] = median;
          }
        }
        newArr = newArr.concat(chunk);
      }
      return newArr;
    }

    const data = normalizeOutliers(temperature, 0.05, 0.2, 0, 50);
    const data2 = normalizeOutliers(humidity, 0.05, 0.2, 10, 100);

    const currentTemp = data[data.length-1][2];

    const bb = d3.select("#temperature").node().getBoundingClientRect();
    const width = bb.width;
    const height = bb.height-20;
    const padding = 20;

    const maxTime = moment(data[data.length-1][1]);
    const minTime = moment(data[0][1]);

    let boxWidth = width-padding*3.2;
    let boxHeight = 20;
    let boxY = padding;
    let boxX = padding+(padding/2);

    const barTempScale = d3.scaleLinear().range([0, boxWidth]).domain([0, 50]);
    const barTempAxis = d3.axisTop(barTempScale).ticks(10).tickFormat((d) => d + " C");

    const svg = d3.select("#temperature")
      .append("svg")
      .attr("id", "graph")
      .attr("width", width)
      .attr("height", height)
      .attr("class", "animated fadeIn")

    svg.append("g")
      .attr("transform", "translate(" + boxX + "," + boxY + ")")
      .call(barTempAxis);

    svg.append("rect")
      .attr("height", boxHeight)
      .attr("width", boxWidth)
      .attr("x", boxX)
      .attr("y", boxY*1.5)
      .attr("style", "fill-opacity: 0.0; stroke: #999999;")

    var gradient = svg.append("linearGradient")
      .attr("y1", 0)
      .attr("y2", 0)
      .attr("x1", boxY*1.5)
      .attr("x2", boxY*1.5+boxWidth)
      .attr("id", "gradient")
      .attr("gradientUnits", "userSpaceOnUse")

    gradient.append("stop")
      .attr("offset", "0")
      .attr("stop-color", "blue")
    gradient.append("stop")
      .attr("offset", "0.30")
      .attr("stop-color", "blue")
    gradient.append("stop")
      .attr("offset", "0.50")
      .attr("stop-color", "#02fc23")
    gradient.append("stop")
      .attr("offset", "0.70")
      .attr("stop-color", "red")
    gradient.append("stop")
      .attr("offset", "1.0")
      .attr("stop-color", "red")

    svg.append("rect")
      .attr("height", boxHeight)
      .attr("width", 0)
      .attr("x", boxX)
      .attr("y", boxY*1.5)
      .attr("fill", "url(#gradient)")
      .transition()
      .ease(d3.easeExpOut)
      .duration(1000)
      .attr("width", boxWidth)

    svg.append("rect")
      .attr("height", boxHeight)
      .attr("width", 5)
      .attr("x", boxX)
      .attr("y", boxY*1.5)
      .attr("style", "fill: #fff; stroke: #999999")
      .transition()
      .ease(d3.easeBounceOut)
      .duration(1000)
      .attr("x", barTempScale(currentTemp)+boxX-(2.5))

    const lineHeight = height-boxY*2-padding*2;
    const lineWidth = boxWidth;
    const lineX = boxX;
    const lineY = boxY*1.5*2;

    const graph = svg.append("rect")
      .attr("class", "dashboard__graph__area")
      .attr("height", lineHeight)
      .attr("width", lineWidth)
      .attr("x", lineX)
      .attr("y", lineY);

    const lineTimeScale = d3.scaleLinear().range([0, lineWidth]).domain([minTime.valueOf(), maxTime.valueOf()]);
    const lineTempScale = d3.scaleLinear().range([0, lineHeight]).domain([50, 0]);
    const lineHumidScale = d3.scaleLinear().range([0, lineHeight]).domain([100, 10]);
    const lineHumidAxis = d3.axisRight(lineHumidScale).ticks(10).tickFormat((d) => d + " %");
    const lineTempAxis = d3.axisLeft(lineTempScale).ticks(10).tickFormat((d) => d + " C");
    const lineTimeAxis = d3.axisBottom(lineTimeScale).ticks(5).tickFormat((d) => moment(d).format("MMM Do, k:mm"));
    const temps = [5, 10, 15, 20, 25, 30, 35, 40, 45];

    temps.map((t) => {
      svg.append("rect")
        .attr("x", lineX)
        .attr("y", lineY+lineTempScale(t))
        .attr("width", lineWidth)
        .attr("height", 1)
        .attr("style", "fill: #e3e3e3")
    });

    const { morning_time, night_time } = info;
    const timeRanges = TimeUtil.getHourRanges(morning_time, night_time);

    let time = minTime.valueOf();
    while(time < maxTime.valueOf()) {
      if(timeRanges[1].indexOf(moment(time).hour()) !== -1) {
        let startTime = time;
        while(timeRanges[1].indexOf(moment(time).hour()) !== -1) {
          time+=300000;
        }
        let endTime = time;
        if(endTime > maxTime.valueOf()) {
          endTime = maxTime.valueOf()
        }

        let stc = lineTimeScale(startTime)
        let etc = lineTimeScale(endTime)

        svg.append("rect")
          .attr("class", "dashboard__graph__nightarea")
          .attr("x", stc+lineX)
          .attr("y", lineY+1)
          .attr("width", etc-stc)
          .attr("height", lineHeight-1)

      } else {
        time+=300000;
      }
    }

    const humidgraph = d3.line()
      .curve(d3.curveMonotoneX)
      .x((d) => lineTimeScale(moment(d[1]).valueOf()))
      .y((d) => lineHumidScale(d[2]))

    const linegraph = d3.line()
      .curve(d3.curveMonotoneX)
      .x((d) => lineTimeScale(moment(d[1]).valueOf()))
      .y((d) => lineTempScale(d[2]))

    svg.append("g")
      .attr("class", "dashboard__graph__line--humid")
      .append("path")
      .attr("transform", "translate(" + lineX + "," + lineY + ")")
      .data(data2)
      .attr("d", humidgraph(data2))

    svg.append("g")
      .attr("class", "dashboard__graph__line--temp")
      .append("path")
      .attr("transform", "translate(" + lineX + "," + lineY + ")")
      .data(data)
      .attr("d", linegraph(data))

    svg.append("g")
      .attr("transform", "translate(" + lineX + "," + lineY + ")")
      .call(lineTempAxis);

    svg.append("g")
      .attr("transform", "translate(" + lineX + "," + (lineY+lineHeight) + ")")
      .call(lineTimeAxis);

    svg.append("g")
      .attr("transform", "translate(" + (lineX+lineWidth) + "," + lineY + ")")
      .call(lineHumidAxis);

    svg.append("text")
      .attr("x", lineX+10)
      .attr("y", lineY+20)
      .attr("style", "font-size: 15px;")
      .text("Temperature and Humidity")
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

  renderStatus() {
    const { info, status } = this.props.info;
    const { temperature, humidity, heat, messages, totalHeatKiloWattHours } = this.state;

    const currentTemp = status.current_temp == null ? 0 : status.current_temp[2];
    const currentHumid = status.current_humid == null ? 0 : status.current_humid[2];

    return (
      <div className="dashboard__status__box" style={{flex: 2, display: 'flex', flexDirection: 'column', justifyContent: 'space-between'}}>
        <div className="dashboard__headingcontainer">
          <h3 className="dashboard__heading">{"Heat Lamps: " + totalHeatKiloWattHours.toFixed(2) + " kWH"}</h3>
          <h3 className="dashboard__heading">{"Temperature: " + currentTemp + " C"}</h3>
          <h3 className="dashboard__heading">{"Humidity: " + currentHumid + "%"}</h3>
          <div className="dashboard__headingmessages" style={{marginTop: 10}}>
            {messages.length > 0 ? messages : <p className="dashboard__headingmessage">No messages!</p>}
          </div>
        </div>
        <div>
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
      </div>
    )
  }

  renderFull() {
    const { loading, windowHeight, imagedata } = this.state;

    let comps = []
    comps.push((
      <div className="dashboard__status" style={{height: windowHeight*0.75}} key="status">
        {loading ? null : this.renderStatus()}
        <div
          id="temperature"
          className="dashboard__status__box"
          style={{flex: 3}}
        />
      </div>
    ));
    comps.push((
      <div className="dashboard__images" style={{height: windowHeight*0.75}} key="images">
        {imagedata.map((data, i) => {
          return <img key={i} src={"data:image/png;base64," + data} style={{width: 300, height: 300}} alt=""/>
        })}
      </div>
    ))

    return comps;
  }

  renderMobile() {
    const { loading } = this.state;
    return (
        <div className="dashboard__status--mobile">
          <div id="temperature" className="dashboard__status__box">
          </div>
          {loading ? null : this.renderStatus()}
        </div>
    );
  }

  renderLoading() {
    return <p>{"Loading..."}</p>;
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
