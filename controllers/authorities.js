const Report = require("../models/Report.js");
const User = require("../models/User.js");
const Authority = require("../models/Authority.js");

module.exports = function (app) {
    app.post("/authority/send-request", async (req, res) => {
        // Veirfy user is logged in
        const user = req.user;
        if (!user) {
            return res.status(401).send({ message: "You need to be logged in to access this route." });
        }

        // Verify requested authority exists
        const authority = await Authority.findById(req.body.authorityId);
        if (!authority) {
            return res.status(400).send({ message: "Could not find the requested authority." });
        }

        // Verify that a join request does not already exist
        const joinRequest = authority.requests.some((request) => request.userId == user._id);
        if (joinRequest) {
            return res.status(400).send({ message: "You alreay have a pending request to this authority." });
        }

        // Create user join request
        const newjoinRequest = { userId: user._id, userEmail: user.email };
        const { updateErr, updateRes } = await Authority.updateOne(
            { _id: authority._id },
            { $push: { requests: newjoinRequest } }
        );

        // Verify not errors occured during update
        if (updateErr) {
            return res.status(400).send({ message: updateErr.message });
        }

        // Send a successfull response
        return res.status(200).send({ message: `Successfully sent join request.` });
    });

    app.put("/authority/accept-request/:userId", async (req, res) => {
        // Get authority's name from url params
        const { userId } = req.params;

        // Veirfy user is logged in
        const user = req.user;
        if (!user) {
            return res.status(401).send({ message: "You need to be logged in to access this route." });
        }

        // Verify that user is a part of an authority and is an admin
        const authority = user.authority;
        if (!authority || user.access_level != "admin") {
            // Send a failed response if not found
            return res.status(401).send({ message: "Access denied. You are not authorized with this authority." });
        }

        // Verify there's a join request with the given userId
        const joinRequest = authority.requests.some((request) => request.userId == userId);
        if (!joinRequest) {
            return res.status(400).send({ message: "Could not find a request from this user." });
        }

        // Update users authority and access level
        const updateRes = await User.updateOne({ _id: userId }, { authority: authority._id, access_level: "employee" });

        // Verrify update was successful
        if (updateRes.nModified == 0) {
            return res.status(400).send({ message: "Error occured while adding user." });
        }

        // Delete join request from authority
        const deleteRes = await Authority.updateOne({ _id: authority._id }, { $pull: { requests: { userId } } });

        // Verify no errors occured during deletion
        if (deleteRes.nModified == 0) {
            return res.status(400).send({ message: "Error occured while deleting request." });
        }

        // Send a successfull response
        return res.status(200).send({ message: "User has been accepted into the authority." });
    });

    app.get("/authority/:userId", async (req, res) => {
        // Get authority's name from url params
        const { userId } = req.params;

        // Veirfy user is logged in
        const user = req.user;
        if (!user) {
            return res.status(401).send({ message: "You need to be logged in to access this route." });
        }

        // Verify that user is a part of an authority and is an admin
        const authority = user.authority;
        if (!authority || user.access_level != "admin") {
            // Send a failed response if not found
            return res.status(401).send({ message: "Access denied. You do not enough access to this authority" });
        }

        // Verify requested user exists
        const reqUser = await User.findById(userId);
        if (!reqUser) {
            return res.status(400).send({ message: "Requested user does not exist." });
        }

        // Verify requested user is a member of users authority
        if (reqUser.authority != String(user.authority._id)) {
            return res.status(400).send({ message: "Requested user is not a member of your organization." });
        }

        // Return successful response with requested user
        return res.status(200).send({ user: reqUser });
    });

    app.put("/authority/:userId", async (req, res) => {
        // Get authority's name from url params
        const { userId } = req.params;

        // Veirfy user is logged in
        const user = req.user;
        if (!user) {
            return res.status(401).send({ message: "You need to be logged in to access this route." });
        }

        // Verify that user is a part of an authority and is an admin
        if (!user.authority || user.access_level != "admin") {
            // Send a failed response if not found
            return res.status(401).send({ message: "Access denied. You do not enough access to this authority" });
        }

        // Verify request data is not missing access_level
        const { access_level } = req.body;
        if (!access_level) {
            return res.status(400).send({ message: "Missing required parameter access_level." });
        }

        // Verify access_level is valid option
        if (["admin", "employee", "user"].indexOf(access_level) == -1) {
            return res.status(400).send({ message: "Access level needs to be either admin, employee, or user" });
        }

        // Verify requested user exists
        const reqUser = await User.findById(userId);
        if (!reqUser) {
            return res.status(400).send({ message: "Requested user does not exist." });
        }

        // Verify requested user is a member of the users authority
        if (reqUser.authority != String(user.authority._id)) {
            return res.status(400).send({ message: "Requested user is not a member of your authority." });
        }

        // Update users access_level
        const updateRes = await User.updateOne({ _id: reqUser._id }, { access_level: access_level });

        // Verify update was a success
        if (updateRes.nModified == 0) {
            return res.status(400).send({ message: "Error occured while update users access level." });
        }

        // Send a successful response
        return res.status(200).send({ message: "Successfully update user's acces level." });
    });

    app.delete("/authority/:userId", async (req, res) => {
        // Get authority's name from url params
        const { userId } = req.params;

        // Veirfy user is logged in
        const user = req.user;
        if (!user) {
            return res.status(401).send({ message: "You need to be logged in to access this route." });
        }

        // Verify that user is a part of an authority and is an admin
        const authority = user.authority;
        if (!authority || user.access_level != "admin") {
            // Send a failed response if not found
            return res.status(401).send({ message: "Access denied. You do not enough access to this authority" });
        }

        // Verify requested user exists
        const reqUser = await User.findById(userId);
        if (!reqUser) {
            return res.status(400).send({ message: "Requested user does not exist." });
        }

        // Verify requested user is a member of users authority
        if (reqUser.authority != String(user.authority._id)) {
            return res.status(400).send({ message: "Requested user is not a member of your organization." });
        }

        // Remove requested user from authority
        const updateRes = await User.updateOne({ _id: reqUser._id }, { authority: null, access_level: "user" });

        // Verify removeal was successful
        if (updateRes.nModified == 0) {
            return res.status(400).send({ message: "Error occured while removing user from authority." });
        }

        // Send a successful response
        return res.status(200).send({ message: "Successfully removed user from authority." });
    });

    app.get("/authority/reports", async (req, res) => {
        // Veirfy user is logged in
        user = req.user;
        if (!user) {
            return res.status(401).send({ message: "You need to be logged in to access this route." });
        }

        // Verify that user is a part of an authority
        const authority = user.authority;
        if (!authority || !(user.access_level == "admin" || user.access_level == "employee")) {
            // Send a failed response if not found
            return res.status(400).send({ message: `Access denied. You are not a member of an authority.` });
        }

        // Get reports connected to authority
        Report.find({ authority: authority._id })
            .then((reports) => {
                return res.send(reports);
            })
            .catch((err) => {
                return res.status(400).send({ error: err.message });
            });
    });
};
