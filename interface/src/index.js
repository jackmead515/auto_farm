import React from 'react'
import ReactDOM from 'react-dom'
import { Provider } from 'react-redux'
import axios from 'axios';
import { Route, Router, Redirect, Switch } from 'react-router';
import { persistor, store } from './configureStore';
import { PersistGate } from 'redux-persist/lib/integration/react'
import createBrowserHistory from 'history/createBrowserHistory'
import * as serviceWorker from './serviceWorker';

import './app/styles/index.css';

import Dashboard from './app/scenes/Dashboard';
import Settings from './app/scenes/Settings';

export const SERVERIP = process.env.NODE_ENV === 'development' ? 'http://192.168.1.58' : 'http://192.168.1.58';

export const history = createBrowserHistory();

axios.defaults.headers.common['Content-Type'] = 'application/json';
axios.defaults.baseURL = process.env.NODE_ENV === 'development' ? 'http://192.168.1.58' : 'http://192.168.1.58';

ReactDOM.render((
  <PersistGate persistor={persistor}>
    <Provider store={store}>
      <Router history={history} onUpdate={() => window.scrollTo(0,0)}>
        <Switch>
          <Route exact path="/" component={Dashboard} />
          <Route exact path="/settings" component={Settings} />
          <Route render={() => <Redirect to="/" />} />
        </Switch>
      </Router>
    </Provider>
  </PersistGate>
), document.getElementById('root'));

serviceWorker.unregister();
