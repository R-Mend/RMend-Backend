const Report = require("../models/Report.js");
const User = require("../models/User.js");

module.exports = function (app) {
    app.get("/reports", async (req, res) => {
        // Veirfy user is logged in
        const user = req.user;
        if (!user) {
            return res.status(401).send({ message: "You need to be logged in to access this route." });
        }

        // Get all reports
        const reports = await Report.find({});

        // Send successful response
        return res.send({ reports });
    });

    app.get("/my/reports", async (req, res) => {
        // Veirfy user is logged in
        const user = req.user;
        if (!user) {
            return res.status(401).send({ message: "You need to be logged in to access this route." });
        }

        // Get all of the user's reports
        const reports = await Report.find({ author: user._id });

        // Send successful response
        return res.send({ reports });
    });

    app.post("/report/new", async (req, res) => {
        // Veirfy user is logged in
        const user = req.user;
        if (!user) {
            return res.status(401).send({ message: "You need to be logged in to access this route." });
        }

        // Create new report and set report author to current user
        const report = new Report({ ...req.body, author: user._id, priority: false, under_review: false });

        // Save report to database
        await report.save();

        // Send successful response
        return res.send({ message: "Successfully created new report." });
    });

    app.get("/reports/:reportId", async (req, res) => {
        // Get url parameters
        const { reportId } = req.params;

        // Veirfy user is logged in
        const user = req.user;
        if (!user) {
            return res.status(401).send({ message: "You need to be logged in to access this route." });
        }

        // Verify requested report exists
        const report = await Report.findById(reportId);
        if (!report) {
            return res.status(400).send({ message: "Could not find requested report." });
        }

        // Return successful response
        return res.send({ report });
    });

    app.put("/reports/:reportId", async (req, res) => {
        // Get url parameters
        const { reportId } = req.params;

        // Veirfy user is logged in
        const user = req.user;
        if (!user) {
            return res.status(401).send({ message: "You need to be logged in to access this route." });
        }

        // Verify requested report exists
        const report = await Report.findById(reportId);
        if (!report) {
            return res.status(400).send({ message: "Could not find requested report." });
        }

        // Verify current user is the reports author
        if (String(report.author) != String(user._id)) {
            return res.status(401).send({ message: "You do not have access to update this report." });
        }

        // Update report
        const updatedReport = await Report.findByIdAndUpdate(report._id, req.body, { new: true });

        // Verify update was successful
        if (!updatedReport) {
            return res.status(400).send({ message: "An error occured while updating report." });
        }

        // Return successful response
        return res.send({ report: updatedReport });
    });

    app.delete("/reports/:reportId", async (req, res) => {
        // Get url parameters
        const { reportId } = req.params;

        // Veirfy user is logged in
        const user = req.user;
        if (!user) {
            return res.status(401).send({ message: "You need to be logged in to access this route." });
        }

        // Verify requested report exists
        const report = await Report.findById(reportId);
        if (!report) {
            return res.status(400).send({ message: "Could not find requested report." });
        }

        // Verify current user is the reports author
        if (String(report.author) != String(user._id)) {
            return res.status(401).send({ message: "You do not have access to update this report." });
        }

        // Delete Report
        try {
            await Report.deleteOne({ _id: reportId });
        } catch (err) {
            return res.status(400).send({ message: err.message });
        }

        // Send a successful response
        return res.send({ message: "Successfully deleted report." });
    });
};
