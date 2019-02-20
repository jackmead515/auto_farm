import axios from 'axios';

export const images = (index) => {
  return new Promise((resolve, reject) => {
    axios.post('/data/images', {index}).then((data) => {
      resolve(data);
    }).catch((err) => {
      reject(err);
    })
  })
}

export const image = (name) => {
  return new Promise((resolve, reject) => {
    axios.post('/data/image', {name}).then((data) => {
      resolve(data);
    }).catch((err) => {
      reject(err);
    })
  })
}

export const soil = (start, end) => {
  return new Promise((resolve, reject) => {
    axios.post('/data/soil', {start, end}).then((data) => {
      resolve(data);
    }).catch((err) => {
      reject(err);
    })
  })
}

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

export const pump = (start, end) => {
  return new Promise((resolve, reject) => {
    axios.post('/data/pump', {start, end}).then((data) => {
      resolve(data);
    }).catch((err) => {
      reject(err);
    })
  })
}

export const lights = (start, end) => {
  return new Promise((resolve, reject) => {
    axios.post('/data/lights', {start, end}).then((data) => {
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

export const submitPumpControl = (params) => {
  return new Promise((resolve, reject) => {
    axios.post('/submit/pump_control', {...params}).then((data) => {
      resolve(data);
    }).catch((err) => {
      reject(err);
    })
  })
}

export const submitGrowLightControl = (params) => {
  return new Promise((resolve, reject) => {
    axios.post('/submit/growlight_control', {...params}).then((data) => {
      resolve(data);
    }).catch((err) => {
      reject(err);
    })
  })
}

export const submitHeatLightControl = (params) => {
  return new Promise((resolve, reject) => {
    axios.post('/submit/heat_control', {...params}).then((data) => {
      resolve(data);
    }).catch((err) => {
      reject(err);
    })
  })
}

export const submitCameraControl = (params) => {
  return new Promise((resolve, reject) => {
    axios.post('/submit/camera_control', {...params}).then((data) => {
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
  messages,
  image,
  images,
  soil,
  pump,
  lights,
  submitPumpControl,
  submitGrowLightControl,
  submitHeatLightControl,
  submitCameraControl
}
