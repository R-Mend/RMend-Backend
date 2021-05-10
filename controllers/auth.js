const jwt = require('jsonwebtoken');
const User = require("../models/User.js");

module.exports = function(app) {

  app.post('/sign-up', (req, res) => {
    const user = new User(req.body)

    user
      .save()
      .then(user => {
        var token = jwt.sign({ _id: user._id }, process.env.SECRET, { expiresIn: '60 days' });
        res.cookie('nToken', token, { maxAge: 900000, httpOnly: true });
          res.redirect('/');
        })
        .catch(err => {
          console.log(err.message)
          return res.status(400).send({ err: err });
        });
    });

    app.get('/logout', (req, res) => {
      res.clearCookie('nToken');
    });

    app.post('/login', (req, res) => {
      const { username, password } = req.body;

      User.findOne({ username }, 'username password')
        .then(user => {
          if (!user) {
            return res.status(401).send({message: "Wronger Username or Password" });
          }

          user.comparePassword(password, (err, isMatch) => {
            if(!isMatch) {
              return res.status(401).send({message: "Wronger Username or Password" });
            }

            const token = jwt.sign({ _id: user._id, username: user.username }, process.env.SECRET, {
              expiresIn: '60 days'
            })

            res.cookie("nToken", token, { maxAge: 900000, httpOnly: true });
            res.redirect('/');
          });
        })
        .catch(err => {
          console.log(err);
        });
    });
}