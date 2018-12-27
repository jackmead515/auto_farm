const initialState = {
  windowWidth: 0,
  windowHeight: 0,
  mouseX: 0,
  mouseY: 0,
};

export default (state = initialState, action = {}) => {
  switch(action.type) {
    case 'REFRESH_WINDOWDIMS':
        return {
          ...state,
          windowWidth: action.windowWidth,
          windowHeight: action.windowHeight
        }
    case 'REFRESH_MOUSEDIMS':
      return {
        ...state,
        mouseX: action.mouseX,
        mouseY: action.mouseY
      }
    default:
      return state;
  }
};
