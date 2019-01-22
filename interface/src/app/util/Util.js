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

export const getTotalAppTime = (data) => {
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

export const calculateEnergy = (apps, heat, lights) => {
  //{sensors: 3.5, heat: 200, lights: 70}
  heat = _.sortBy(heat, (d) => moment(d[1]).valueOf());
  lights = _.sortBy(lights, (d) => moment(d[1]).valueOf());

  const startDate = moment(heat[0][1]).valueOf() < moment(lights[0][1]).valueOf() ? moment(heat[0][1]) : moment(lights[0][1]);
  const endDate = moment(heat[heat.length-1][1]).valueOf() > moment(lights[lights.length-1][1]).valueOf() ? moment(heat[heat.length-1][1]) : moment(lights[lights.length-1][1]);

  const idleKiloWatts = (apps.sensors/1000)*((endDate.valueOf()-startDate.valueOf())/3600000)
  const heatKiloWatts = (apps.heat/1000)*(getTotalAppTime(heat)/3600000);
  const lightKiloWatts = (apps.lights/1000)*(getTotalAppTime(lights)/3600000);

  const kiloWatts = idleKiloWatts+heatKiloWatts+lightKiloWatts;

  return { kiloWatts, startDate, endDate };
}

export default {
  getWindowDimensions,
  calculateEnergy
}
