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
    const { soil, info, windowWidth, windowHeight } = nextProps;

    const initial = (!this.state.rendered && (soil.length > 0) && info !== null);
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

    let data = soil; //normalizeOutliers(soil, 0.05, 0.2, 0, 100);

    const maxTime = moment(data[data.length-1][1]);
    const minTime = moment(data[0][1]);

    data = data.filter((d) => d[3] !== -1);
    data = _.groupBy(data, (d) => d[2]);

    let currentSoil = info.current_soil == null || (info.current_soil && info.current_soil.length <= 0) ? [0.0] : info.current_soil;
    currentSoil = currentSoil.filter((d) => d.value !== -1);
    const currentSoilMedian = d3.median(currentSoil, (d) => d.value);

    const bb = d3.select("#soil").node().getBoundingClientRect();
    const width = bb.width-20;
    const height = bb.height-20;
    const padding = 20;

    const boxHeight = 20;
    const boxWidth = mobile ? width-(padding*3) : width-(padding*5);
    const boxY = padding*2;
    const boxX = mobile ? padding*2 : padding*4;
    const boxScaleTicks = mobile ? 5 : 10;

    const barSoilScale = d3.scaleLinear().range([0, boxWidth]).domain([0, 100]);
    const barSoilAxis = d3.axisTop(barSoilScale).ticks(boxScaleTicks).tickFormat((d) => d);

    const svg = d3.select("#soil")
      .append("svg")
      .attr("id", "graph")
      .attr("width", "100%")
      .attr("height", "100%")
      .attr("class", "animated fadeIn dashboard__graph")

    svg.append("g")
      .attr("transform", "translate(" + boxX + "," + boxY + ")")
      .attr("class", "graph__axis")
      .call(barSoilAxis);

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
      .attr("id", "gradient-soil")
      .attr("gradientUnits", "userSpaceOnUse")

    gradient.append("stop")
      .attr("offset", "0")
      .attr("stop-color", "#efd483")
    gradient.append("stop")
      .attr("offset", "100%")
      .attr("stop-color", "#35b0e0")

    svg.append("rect")
      .attr("height", boxHeight)
      .attr("width", 0)
      .attr("x", boxX)
      .attr("y", boxY+10)
      .attr("fill", "url(#gradient-soil)")
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
      .attr("x", barSoilScale(currentSoilMedian)+boxX-(2.5))

    const lineHeight = mobile ? height-boxY*2-padding : height-boxY*2-padding*3;
    const lineWidth = boxWidth;
    const lineX = boxX;
    const lineY = boxY+boxHeight+10+10;
    const lineSoilScaleTicks = mobile ? 5 : 10;
    const lineTimeScaleTicks = mobile ? 2 : 5;

    const graph = svg.append("rect")
      .attr("class", "graph__area")
      .attr("height", lineHeight)
      .attr("width", lineWidth)
      .attr("x", lineX)
      .attr("y", lineY);

    const lineTimeScale = d3.scaleLinear().range([0, lineWidth]).domain([minTime.valueOf(), maxTime.valueOf()]);
    const lineSoilScale = d3.scaleLinear().range([0, lineHeight]).domain([100, 0]);
    const lineSoilAxis = d3.axisLeft(lineSoilScale).ticks(lineSoilScaleTicks).tickFormat((d) => d);
    const lineTimeAxis = d3.axisBottom(lineTimeScale).ticks(lineTimeScaleTicks).tickFormat((d) => moment(d).format("MMM Do, k:mm"));

    if(!mobile) {
      const soils = [10, 20, 30, 40, 50, 60, 70, 80, 90];
      soils.map((t) => {
        svg.append("rect")
          .attr("x", lineX)
          .attr("y", lineY+lineSoilScale(t))
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

    const linegraph = d3.line()
      .curve(d3.curveMonotoneX)
      .x((d) => lineTimeScale(moment(d[1]).valueOf()))
      .y((d) => lineSoilScale(d[3]))

    const lineColor = [ "#35b0e0", "#00ff00", "#ff6600", "#efd483"  ]
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
    }
  }

  render() {
    return (
      <div
        id="soil"
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
