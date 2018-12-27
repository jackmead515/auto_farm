import moment from 'moment';
import _ from 'lodash';

export const getWindowDimensions = () => {
  var width = window.innerWidth
  || document.documentElement.clientWidth
  || document.body.clientWidth;

  var height = window.innerHeight
  || document.documentElement.clientHeight
  || document.body.clientHeight;

  return { width, height };
}

export const getTotalHeatTime = (data) => {
  let total = 0;
  let start = -1;
  let lastD = -1;
  for(let i = 0; i < data.length; i++) {
    let d = data[i];
    if(d[2] === 1 && lastD !== 1) {
      start = moment(d[1]).valueOf();
    } else if(d[2] === 0 && start !== -1) {
      let end = moment(d[1]).valueOf();
      total += end-start;
      start = end;
    }
    lastD = d;
  }
  return total;
}

export const getTotalHeatKiloWattHours = (watts, data) => {
  data = _.sortBy(data, (d) => moment(d[1]).valueOf());
  return (watts/1000) * (getTotalHeatTime(data)/3600000);
}

export default {
  getWindowDimensions,
  getTotalHeatTime,
  getTotalHeatKiloWattHours
}
