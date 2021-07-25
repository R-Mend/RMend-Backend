const jwt = require("jsonwebtoken");
const User = require("../models/User.js");

module.exports = function (app) {
    app.post("/sign-up", (req, res) => {
        // TODO: Add more validation so that users can't registure themself into an authority
        const user = new User(req.body);

        user.save()
            .then((user) => {
                var token = jwt.sign({ _id: user._id }, process.env.SECRET, { expiresIn: "7d" });
                return res.status(200).send({ user: { ...user, token } });
            })
            .catch((err) => {
                return res.status(400).send({ err: err });
            });
    });

    app.post("/login", (req, res) => {
        const { email, password } = req.body;

        User.findOne({ email }, "email password")
            .then((user) => {
                // Verify user exist with the given email
                if (!user) {
                    return res.status(401).send({ message: "Could not find user with this email." });
                }

                // Verify password is correct
                user.comparePassword(password, (err, isMatch) => {
                    if (!isMatch) {
                        return res.status(401).send({ message: "Email or password was incorrect." });
                    }

                    // Create jwt token for authentication
                    const token = jwt.sign({ _id: user._id, username: user.username }, process.env.SECRET, {
                        expiresIn: "7d",
                    });

                    // Remove password from user
                    delete user["password"];

                    // Send successful response
                    return res.status(200).send({ user: { ...user, token } });
                });
            })
            .catch((err) => {
                console.log(err);
                return res.status(400).send({ message: err });
            });
    });
};
