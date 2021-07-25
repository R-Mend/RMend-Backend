const dotenv = require("dotenv");
const express = require("express");
const expressValidator = require("express-validator");
var cookieParser = require("cookie-parser");
const jwt = require("jsonwebtoken");
const User = require("./models/User.js");
dotenv.config();

// Set Database
require("./data/report-db");

// Create app
const app = express();

// Setup Body Parser and Express Validator
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(expressValidator());

// Cookie Parser
app.use(cookieParser());

// Auth Checker
var checkAuth = async (req, res, next) => {
    console.log("Checking Authentication.");
    const bearerHeader = req.headers["authorization"];
    var current_user = null;

    if (typeof bearerHeader !== "undefined" && bearerHeader !== null) {
        const bearer = bearerHeader.split(" ");
        const bearerToken = bearer[1];

        try {
            const decodedToken = await jwt.verify(bearerToken, process.env.SECRET);
            current_user = await User.findById(decodedToken._id).populate("authority");
        } catch (err) {
            console.log(err.message);
        }
    }
    req.user = current_user;
    next();
};
app.use(checkAuth);

// Setup Controllers
require("./controllers/auth.js")(app);
require("./controllers/reports.js")(app);
require("./controllers/authorities.js")(app);

// Listen to Port
if (!module.parent) {
    app.listen(process.env.PORT, () => {
        console.log(`Report Manager listening on http://localhost:${[process.env.PORT]}`);
    });
}

module.exports = app;
