const jwt = require("jsonwebtoken");
const User = require("../models/User.js");

module.exports = function (app) {
    app.post("/sign-up", (req, res) => {
        // TODO: Add more validation so that users can't registure themself into an authority
        const user = new User(req.body);

        user.save()
            .then((user) => {
                var token = jwt.sign({ _id: user._id }, process.env.SECRET, { expiresIn: "7d" });
                res.cookie("nToken", token, { maxAge: 900000, httpOnly: true });
                return res.status(200).send({ message: "Successfully registured new account." });
            })
            .catch((err) => {
                return res.status(400).send({ err: err });
            });
    });

    app.get("/logout", (req, res) => {
        res.clearCookie("nToken");
        return res.status(200).send({ message: "Successfully logged out." });
    });

    app.post("/login", (req, res) => {
        const { email, password } = req.body;

        User.findOne({ email }, "email password")
            .then((user) => {
                if (!user) {
                    return res.status(401).send({ message: "Could not find user with this email." });
                }

                user.comparePassword(password, (err, isMatch) => {
                    if (!isMatch) {
                        return res.status(401).send({ message: "Email or password was incorrect." });
                    }

                    const token = jwt.sign({ _id: user._id, username: user.username }, process.env.SECRET, {
                        expiresIn: "7d",
                    });

                    res.cookie("nToken", token, { maxAge: 900000, httpOnly: true });
                    return res.status(200).send({ message: "Successfully signed in." });
                });
            })
            .catch((err) => {
                console.log(err);
                return res.status(400).send({ message: err });
            });
    });
};
