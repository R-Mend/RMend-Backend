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

// Setup Controllers
app.get('/', (req, res) => {
  res.send("Loaded API Index");
});

// Listen to Port
app.listen(process.env.PORT, () => {
    console.log(`Report Manager listening on http://localhost:${[process.env.PORT]}`)
});

module.exports = app;