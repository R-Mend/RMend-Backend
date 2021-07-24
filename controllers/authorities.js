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

        console.log("SENDING SUCCESS RESPONSE");
        // Send a successfull response
        return res.status(200).send({ message: "User has been accepted into the authority." });
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
