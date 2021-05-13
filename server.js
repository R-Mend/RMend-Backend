const dotenv = require('dotenv');
const express = require('express');
const bodyParser = require('body-parser');
const expressValidator = require('express-validator');
var cookieParser = require('cookie-parser');
const jwt = require('jsonwebtoken');
dotenv.config();

// Set Database
require('./data/report-db');

// Create app
const app = express();

// Setup Body Parser and Express Validator
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(expressValidator());

// Cookie Parser
app.use(cookieParser());

// Auth Checker
var checkAuth = (req, res, next) => {
  console.log("Checking authentication");
  if (typeof req.cookies.nToken === "undefined" || req.cookies.nToken === null) {
    req.user = null;
  } else {
    var token = req.cookies.nToken;
    var decodedToken = jwt.decode(token, { complete: true }) || {};
    req.user = decodedToken.payload;
  }
  next();
};
app.use(checkAuth);

// Setup Controllers
require('./controllers/auth.js')(app);
require('./controllers/reports.js')(app);

// Listen to Port
if(!module.parent){
  app.listen(process.env.PORT, () => {
    console.log(`Report Manager listening on http://localhost:${[process.env.PORT]}`)
  });
}

module.exports = app;