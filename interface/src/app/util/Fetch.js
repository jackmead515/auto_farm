import axios from 'axios';

export const temperature = (start, end) => {
  return new Promise((resolve, reject) => {
    axios.post('/data/temperature', {start, end}).then((data) => {
      resolve(data);
    }).catch((err) => {
      reject(err);
    })
  })
}

export const humidity = (start, end) => {
  return new Promise((resolve, reject) => {
    axios.post('/data/humidity', {start, end}).then((data) => {
      resolve(data);
    }).catch((err) => {
      reject(err);
    })
  })
}

export const heat = (start, end) => {
  return new Promise((resolve, reject) => {
    axios.post('/data/heat', {start, end}).then((data) => {
      resolve(data);
    }).catch((err) => {
      reject(err);
    })
  })
}

export const info = () => {
  return new Promise((resolve, reject) => {
    axios.post('/info').then((data) => {
      resolve(data);
    }).catch((err) => {
      reject(err);
    })
  })
}

export const status = () => {
  return new Promise((resolve, reject) => {
    axios.post('/status').then((data) => {
      resolve(data);
    }).catch((err) => {
      reject(err);
    })
  })
}

export const messages = () => {
  return new Promise((resolve, reject) => {
    axios.post('/data/messages').then((data) => {
      resolve(data);
    }).catch((err) => {
      reject(err);
    })
  })
}

export default {
  temperature,
  info,
  status,
  humidity,
  heat,
  messages
}
