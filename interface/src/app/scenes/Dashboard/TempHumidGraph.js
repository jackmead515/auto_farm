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
        rendered: false
      }

      this.graphTimeout = null;
  }

  componentWillMount() {}
  componentDidMount() {}
  componentWillReceiveProps(nextProps) {
    const { temperature, humidity, info, windowWidth, windowHeight } = nextProps;

    const initial = (!this.state.rendered && (temperature.length > 0 || humidity.length > 0) && info !== null);
    const windowSizeChanged = (windowWidth !== this.props.windowWidth || windowHeight !== this.props.windowHeight);

    if(initial || windowSizeChanged) {
      if(!this.state.rendered) {
        this.setState({rendered: true})
        this.graphTemperature();
      } else {
        if(this.graphTimeout) { clearTimeout(this.graphTimeout); }
        this.graphTimeout = setTimeout(() => {
          this.setState({rendered: true})
          this.graphTemperature();
        }, 100);
      }

    }
  }

  graphTemperature() {
    const { temperature, humidity, mobile } = this.props;
    const { info } = this.props.info;

    document.getElementById("temperature").innerHTML = "";

    const normalizeOutliers = (data, split, tolerance, minVal, maxVal) => {
      split = data.length*split > 10 ? 10 : data.lenght*split;
      let chunks = _.chunk(data, split);
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
            chunk.splice(x, 1);
            //chunk[x][2] = median;
          }
        }
        newArr = newArr.concat(chunk);
      }
      return newArr;
    }

    const data = normalizeOutliers(temperature, 0.05, 0.2, 0, 50);
    const data2 = normalizeOutliers(humidity, 0.05, 0.2, 10, 100);

    const currentTemp = info.current_temp;

    const bb = d3.select("#temperature").node().getBoundingClientRect();
    const width = bb.width-20;
    const height = bb.height-20;
    const padding = 20;

    const maxTime = moment(data[data.length-1][1]);
    const minTime = moment(data[0][1]);

    const boxHeight = 20;
    const boxWidth = mobile ? width-(padding*3) : width-(padding*7);
    const boxY = padding*2;
    const boxX = mobile ? padding*2 : padding*4;
    const boxScaleTicks = mobile ? 5 : 10;

    const barTempScale = d3.scaleLinear().range([0, boxWidth]).domain([0, 50]);
    const barTempAxis = d3.axisTop(barTempScale).ticks(boxScaleTicks).tickFormat((d) => d);

    const svg = d3.select("#temperature")
      .append("svg")
      .attr("id", "graph")
      .attr("width", "100%")
      .attr("height", "100%")
      .attr("class", "animated fadeIn dashboard__graph")

    svg.append("g")
      .attr("transform", "translate(" + boxX + "," + boxY + ")")
      .attr("class", "graph__axis")
      .call(barTempAxis);

    svg.append("rect")
      .attr("height", boxHeight)
      .attr("width", boxWidth)
      .attr("x", boxX)
      .attr("y", boxY+10)
      .attr("style", "fill-opacity: 0.0; stroke: #999999;")

    var gradient = svg.append("linearGradient")
      .attr("y1", 0)
      .attr("y2", 0)
      .attr("x1", "0%")
      .attr("x2", "100%")
      .attr("id", "gradient")
      .attr("gradientUnits", "userSpaceOnUse")

    gradient.append("stop")
      .attr("offset", "0")
      .attr("stop-color", "blue")
    gradient.append("stop")
      .attr("offset", "30%")
      .attr("stop-color", "blue")
    gradient.append("stop")
      .attr("offset", "50%")
      .attr("stop-color", "#02fc23")
    gradient.append("stop")
      .attr("offset", "70%")
      .attr("stop-color", "red")
    gradient.append("stop")
      .attr("offset", "100%")
      .attr("stop-color", "red")

    svg.append("rect")
      .attr("height", boxHeight)
      .attr("width", 0)
      .attr("x", boxX)
      .attr("y", boxY+10)
      .attr("fill", "url(#gradient)")
      .transition()
      .ease(d3.easeExpOut)
      .duration(1000)
      .attr("width", boxWidth)

    svg.append("rect")
      .attr("height", boxHeight)
      .attr("width", 5)
      .attr("x", boxX)
      .attr("y", boxY+10)
      .attr("style", "fill: #fff; stroke: #999999;")
      .transition()
      .ease(d3.easeBounceOut)
      .duration(1000)
      .attr("x", barTempScale(currentTemp)+boxX-(2.5))

    const lineHeight = mobile ? height-boxY*2-padding : height-boxY*2-padding*3;
    const lineWidth = boxWidth;
    const lineX = boxX;
    const lineY = boxY+boxHeight+10+10;
    const lineHumidScaleTicks = mobile ? 5 : 10;
    const lineTempScaleTicks = mobile ? 5 : 10;
    const lineTimeScaleTicks = mobile ? 2 : 5;

    const graph = svg.append("rect")
      .attr("class", "graph__area")
      .attr("height", lineHeight)
      .attr("width", lineWidth)
      .attr("x", lineX)
      .attr("y", lineY);

    const lineTimeScale = d3.scaleLinear().range([0, lineWidth]).domain([minTime.valueOf(), maxTime.valueOf()]);
    const lineTempScale = d3.scaleLinear().range([0, lineHeight]).domain([50, 0]);
    const lineHumidScale = d3.scaleLinear().range([0, lineHeight]).domain([100, 10]);
    const lineHumidAxis = d3.axisRight(lineHumidScale).ticks(lineHumidScaleTicks).tickFormat((d) => d);
    const lineTempAxis = d3.axisLeft(lineTempScale).ticks(lineTempScaleTicks).tickFormat((d) => d);
    const lineTimeAxis = d3.axisBottom(lineTimeScale).ticks(lineTimeScaleTicks).tickFormat((d) => moment(d).format("MMM Do, k:mm"));

    if(!mobile) {
      const temps = [5, 10, 15, 20, 25, 30, 35, 40, 45];
      temps.map((t) => {
        svg.append("rect")
          .attr("x", lineX)
          .attr("y", lineY+lineTempScale(t))
          .attr("width", lineWidth)
          .attr("height", 1)
          .attr("style", "fill: #e3e3e3")
      });
    }

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

    const humidgraph = d3.line()
      .curve(d3.curveMonotoneX)
      .x((d) => lineTimeScale(moment(d[1]).valueOf()))
      .y((d) => lineHumidScale(d[2]))

    const linegraph = d3.line()
      .curve(d3.curveMonotoneX)
      .x((d) => lineTimeScale(moment(d[1]).valueOf()))
      .y((d) => lineTempScale(d[2]))

    svg.append("g")
      .attr("class", "graph__line--humid")
      .append("path")
      .attr("transform", "translate(" + lineX + "," + lineY + ")")
      .data(data2)
      .attr("d", humidgraph(data2))

    svg.append("g")
      .attr("class", "graph__line--temp")
      .append("path")
      .attr("transform", "translate(" + lineX + "," + lineY + ")")
      .data(data)
      .attr("d", linegraph(data))

    svg.append("g")
      .attr("transform", "translate(" + lineX + "," + lineY + ")")
      .attr("class", "graph__axis")
      .call(lineTempAxis);

    svg.append("g")
      .attr("transform", "translate(" + lineX + "," + (lineY+lineHeight) + ")")
      .attr("class", "graph__axis")
      .call(lineTimeAxis);

    svg.append("g")
      .attr("transform", "translate(" + (lineX+lineWidth) + "," + lineY + ")")
      .attr("class", "graph__axis")
      .call(lineHumidAxis);

    if(!mobile) {
      svg.append("text")
        .attr("x", 30)
        .attr("y", height/2)
        .attr("text-anchor", "middle")
        .attr("style", "font-size: 15px; fill: red;")
        .attr("transform", "rotate(-90," + 30 + "," + (height/2) + ")")
        .text("Temperature (Celcius)")

      svg.append("text")
        .attr("x", width-30)
        .attr("y", height/2)
        .attr("text-anchor", "middle")
        .attr("style", "font-size: 15px; fill: blue;")
        .attr("transform", "rotate(90," + (width-15) + "," + (height/2) + ")")
        .text("Humidity (Percentage)")

      svg.append("text")
        .attr("x", width/2)
        .attr("y", height-15)
        .attr("text-anchor", "middle")
        .attr("style", "font-size: 15px;")
        .text("Time")
    }
  }

  render() {
    return (
      <div
        id="temperature"
        className={this.props.className}
        style={this.props.style}
      />
    );
  }
}

const mapStateToProps = (state) => {
  return { ...state };
}

export default connect(mapStateToProps)(Graph);
