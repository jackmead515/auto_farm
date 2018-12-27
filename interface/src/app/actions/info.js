export const refreshStatus = (status) => {
  return {
    type: 'REFRESH_STATUS',
    status
  }
}

export const refreshInfo = (info) => {
  return {
    type: 'REFRESH_INFO',
    info
  }
}
