export const refreshWindowDims = (windowWidth, windowHeight) => {
  return {
    type: 'REFRESH_WINDOWDIMS',
    windowWidth,
    windowHeight
  }
}

export const refreshMouseDims = (mouseX, mouseY) => {
  return {
    type: 'REFRESH_MOUSEDIMS',
    mouseX,
    mouseY
  }
}
