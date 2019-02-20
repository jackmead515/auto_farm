/* @flow weak */

import React, { Component } from 'react';
import { connect } from 'react-redux';

import _ from 'lodash';
import moment from 'moment';
import * as d3 from 'd3';

import TimeUtil from '../../util/TimeUtil';

class Graph extends Component {
  constructor(props) {
      super(props);

      this.state = {
        rendered: false,
        renderCalibrate: false
      }

      this.graphTimeout = null;
  }

  componentWillMount() {}
  componentDidMount() {}
  componentWillReceiveProps(nextProps) {
    const { soil, info, windowWidth, windowHeight, render } = nextProps;

    const initial = (!this.state.rendered && render);
    const windowSizeChanged = (windowWidth !== this.props.windowWidth || windowHeight !== this.props.windowHeight);

    if(initial || windowSizeChanged) {
      if(!this.state.rendered) {
        this.setState({rendered: true})
        this.graphSoil();
      } else {
        if(this.graphTimeout) { clearTimeout(this.graphTimeout); }
        this.graphTimeout = setTimeout(() => {
          this.setState({rendered: true})
          this.graphSoil();
        }, 100);
      }
    }
  }

  graphSoil() {
    const { soil, mobile } = this.props;
    const { info } = this.props.info;

    document.getElementById("soil").innerHTML = "";

    if(Object.keys(info.soil_calibration_values).length <= 0) {
      this.setState({renderCalibrate: true})
      return;
    }

    const bb = d3.select("#soil").node().getBoundingClientRect();
    const width = bb.width-20;
    const height = bb.height-20;
    const padding = 20;

    const limits = [30000, 70000]
    let data = soil;
    data.map((d) => {
     if(d[3] < limits[0]) { d[3] = limits[0]; }
     else if(d[3] > limits[1]) { d[3] = limits[1]; }
     return d
    });
    if(data.length <= 0) { return; }

    const maxTime = data.length > 0 ? moment(data[data.length-1][1]) : 0;
    const minTime = data.length > 0 ? moment(data[0][1]) : 0;
    data = _.groupBy(data, (d) => d[2]);

    for(let i in data){
      this.graphSensor(i, data[i]);
    }

    const svg = d3.select("#soil")
      .append("svg")
      .attr("id", "graph")
      .attr("width", "100%")
      .attr("height", "100%")
      .attr("class", "animated fadeIn dashboard__graph")

    /*const lineHeight = mobile ? height-padding : height-padding*3;
    const lineWidth = mobile ? width-(padding*3) : width-(padding*5);
    const lineX = mobile ? padding*2 : padding*4//boxX;
    const lineY = padding*2//boxY+boxHeight+10+10;
    const lineSoilScaleTicks = mobile ? 5 : 10;
    const lineTimeScaleTicks = mobile ? 2 : 5;

    const graph = svg.append("rect")
      .attr("class", "graph__area")
      .attr("height", lineHeight)
      .attr("width", lineWidth)
      .attr("x", lineX)
      .attr("y", lineY);

    const calPins = Object.keys(info.soil_calibration_values);
    const lineColor = [ "#3399ff", "#00ff00", "#ff66ff", "#b38600"  ]
    const lineTimeScale = d3.scaleLinear().range([0, lineWidth]).domain([minTime.valueOf(), maxTime.valueOf()]);
    const lineSoilScale = d3.scaleLinear().range([0, lineHeight]).domain([limits[1], limits[0]]);
    const lineSoilAxis = d3.axisLeft(lineSoilScale).ticks(lineSoilScaleTicks).tickFormat((d) => d);
    const lineTimeAxis = d3.axisBottom(lineTimeScale).ticks(lineTimeScaleTicks).tickFormat((d) => moment(d).format("MMM Do, k:mm"));

    if(!mobile) {
      const soils = [35000, 40000, 45000, 50000, 55000, 60000, 65000];
      soils.map((t) => {
        svg.append("rect")
          .attr("x", lineX)
          .attr("y", lineY+lineSoilScale(t))
          .attr("width", lineWidth)
          .attr("height", 1)
          .attr("style", "fill: #e3e3e3")
      });
    }

    calPins.map((pin, i) => {
      const cv = info.soil_calibration_values[pin];
      const mps = lineSoilScale(cv.median+cv.std);
      const y = lineY+lineSoilScale(cv.median)
      const by = lineY+mps;
      const h = (y-by)*2;
      svg.append("rect")
        .attr("x", lineX)
        .attr("y", by)
        .attr("width", lineWidth)
        .attr("height", h)
        .attr("style", "fill-opacity: 0.2; fill: " + lineColor[i])
    })

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
          .attr("class", "graph__nightarea")
          .attr("x", stc+lineX)
          .attr("y", lineY+1)
          .attr("width", etc-stc)
          .attr("height", lineHeight-1)

      } else {
        time+=300000;
      }
    }

    const linegraph = d3.line()
      .curve(d3.curveMonotoneX)
      .x((d) => lineTimeScale(moment(d[1]).valueOf()))
      .y((d) => lineSoilScale(d[3]))

    for(let i in data) {
      let d = data[i];
      svg.append("g")
        .attr("class", "graph__line")
        .attr("style", "stroke: " + lineColor[i] + ";")
        .append("path")
        .attr("transform", "translate(" + lineX + "," + lineY + ")")
        .data(d)
        .attr("d", linegraph(d))
    }

    svg.append("g")
      .attr("transform", "translate(" + lineX + "," + lineY + ")")
      .attr("class", "graph__axis")
      .call(lineSoilAxis);

    svg.append("g")
      .attr("transform", "translate(" + lineX + "," + (lineY+lineHeight) + ")")
      .attr("class", "graph__axis")
      .call(lineTimeAxis);

    if(!mobile) {
      svg.append("text")
        .attr("x", 30)
        .attr("y", height/2)
        .attr("text-anchor", "middle")
        .attr("style", "font-size: 15px; fill: red;")
        .attr("transform", "rotate(-90," + 30 + "," + (height/2) + ")")
        .text("Soil Moisture (Percentage)")

      svg.append("text")
        .attr("x", width/2)
        .attr("y", height-15)
        .attr("text-anchor", "middle")
        .attr("style", "font-size: 15px;")
        .text("Time")
    }*/
  }

  renderNightShading(svg, config) {
    const { morning_time, night_time } = this.props.info.info;
    const timeRanges = TimeUtil.getHourRanges(morning_time, night_time);

    let time = config.minTime.valueOf();
    while(time < config.maxTime.valueOf()) {
      if(timeRanges[1].indexOf(moment(time).hour()) !== -1) {
        let startTime = time;
        while(timeRanges[1].indexOf(moment(time).hour()) !== -1) {
          time+=300000;
        }
        let endTime = time;
        if(endTime > config.maxTime.valueOf()) {
          endTime = config.maxTime.valueOf()
        }

        let stc = config.timeScale(startTime)
        let etc = config.timeScale(endTime)

        svg.append("rect")
          .attr("class", "graph__nightarea")
          .attr("x", stc+config.x)
          .attr("y", config.y+1)
          .attr("width", etc-stc)
          .attr("height", config.height-1)

      } else {
        time+=300000;
      }
    }
  }

  graphSensor(i, data) {
    const { mobile } = this.props;
    const { info } = this.props.info;

    const svg = d3.select("#soil")
      .append("svg")
      .attr("id", "graph-" + i)
      .attr("width", "100%")
      .attr("height", "100%")

    const lineColor = [ "#3399ff", "#00ff00", "#ff66ff", "#b38600"  ]
    const padding = 20;
    const x = padding;
    const y = padding/2;
    const height = parseInt(svg.style('height').slice(0, svg.style('height').length-2))-padding*2;
    const width = parseInt(svg.style('width').slice(0, svg.style('width').length-2))-padding;
    const maxTime = data.length > 0 ? moment(data[data.length-1][1]) : 0;
    const minTime = data.length > 0 ? moment(data[0][1]) : 0;
    const maxValue = d3.max(data, (d) => d[3]);
    const minValue = d3.min(data, (d) => d[3]);
    const limits = [minValue-(minValue*0.05), maxValue+(maxValue*0.05)];
    const timeScale = d3.scaleLinear().range([0, width-x]).domain([minTime.valueOf(), maxTime.valueOf()]);
    const soilScale = d3.scaleLinear().range([0, height-y]).domain([limits[1], limits[0]]);
    const soilAxis = d3.axisLeft(soilScale).ticks(5).tickFormat((d) => d/1000 + 'k');
    const timeAxis = d3.axisBottom(timeScale).ticks(3).tickFormat((d) => moment(d).format("MMM Do, k:mm"));
    const cv = info.soil_calibration_values[i];
    const mps = soilScale(cv.median+cv.std);
    const boxY = y+mps;
    const boxHeight = (y+soilScale(cv.median)-boxY)*2;

    svg.append("rect")
      .attr("x", x)
      .attr("y", boxY)
      .attr("width", width-x)
      .attr("height", boxHeight)
      .attr("style", "fill-opacity: 0.2; fill: " + lineColor[i])

    this.renderNightShading(svg, {minTime, maxTime, x, y, height, timeScale});

    const linegraph = d3.line()
      .curve(d3.curveMonotoneX)
      .x((d) => timeScale(moment(d[1]).valueOf()))
      .y((d) => soilScale(d[3]))

    svg.append("g")
      .attr("class", "graph__line")
      .attr("style", "stroke: " + lineColor[i] + ";")
      .append("path")
      .attr("transform", "translate(" + x + "," + y + ")")
      .data(data)
      .attr("d", linegraph(data))

    /*svg.append("g")
      .attr("transform", "translate(" + x + "," + (y*2) + ")")
      .attr("class", "graph__axis")
      .call(soilAxis);*/

    svg.append("g")
      .attr("transform", "translate(" + x + "," + (y+height) + ")")
      .attr("class", "graph__axis")
      .call(timeAxis);
  }

  renderCalibrate() {
    const { renderCalibrate } = this.state;

    if(renderCalibrate) {
      return (
        <div className="dashboard__soilcalibration">
          <p>Click to calibrate soil sensors!</p>
          <p>This process will take approximately 2 minutes.</p>
          <button onClick={() => {}}>Calibrate</button>
        </div>
      )
    }
  }

  render() {
    return (
      <div
        id="soil"
        className={this.props.className}
        style={this.props.style}
      >
        {this.renderCalibrate()}
      </div>
    );
  }
}

const mapStateToProps = (state) => {
  return { ...state };
}

export default connect(mapStateToProps)(Graph);
