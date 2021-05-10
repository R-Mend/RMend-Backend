const mongoose = require("mongoose");
assert = require('assert');

const url = "mongodb://localhost/report-db";
mongoose.Promise = global.Promise;
mongoose.connect(
    url,
    {
        useNewUrlParser: true, 
        useUnifiedTopology: true, 
        useCreateIndex: true, 
        useFindAndModify: false 
    },
    (err, db) => {
        assert.equal(null, err);
        console.log("Connected successfully to database");
        // db.close(); //Turn on for testing 
    }
);
mongoose.connection.on("error", console.error.bind(console, "Mongodb connection Error:"));
mongoose.set("debug", true);

module.exports = mongoose.connection