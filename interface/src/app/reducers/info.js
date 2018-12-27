const initialState = {
  status: null,
  info: null
};

export default (state = initialState, action = {}) => {
  switch(action.type) {
    case 'REFRESH_STATUS':
        return {
          ...state,
          status: action.status
        }
    case 'REFRESH_INFO':
      return {
        ...state,
        info: action.info
      }
    default:
      return state;
  }
};
