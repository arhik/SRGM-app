// var Promise = require('bluebird');
import {bootstrap} from 'aurelia-bootstrapper-webpack';

// import '../node_modules/bootstrap/dist/css/bootstrap.css';
// import '../node_modules/font-awesome/css/font-awesome.css';
// import '../styles/styles.css';

import '../node_modules/semantic-ui/dist/semantic.js';
import '../node_modules/semantic-ui/dist/semantic.css';
import '../styles/styles.css';
bootstrap(function(aurelia) {
  aurelia.use
    .standardConfiguration()
    .developmentLogging();

  aurelia.start().then(() => aurelia.setRoot('app', document.body));
});
