const Report = require('../models/Report.js');
const User = require('../models/User.js');

module.exports = function(app) {

  app.get('/reports', (req, res) => {
    Report.find({})
      .then(reports => {
        res.send(reports);
      })
      .catch(err => {
        res.status(400).send({error: err.message});
      });
  })

  app.post('/report/new', (req, res) => {
    if (req.user) {
      const report  = new Report(req.body);
      report.author = req.user._id;
      report
        .save()
        .then(report => {
          return User.findById(req.user._id);
        })
        .then(user => {
          user.reports.unshift(report);
          user.save();
          res.send(report);
        })
        .catch(err => {
          console.log(err.message);
          res.send({ error: err.message});
        });
    } else {
      return res.status(401);
    }
  });
  
  app.get("/reports/:id", (req, res) => {
    Report.findById(req.params.id).lean()
      .populate('author')
      .then((report) => {
        res.send(report);
      })
      .catch(err => {
        console.log(err.message);
        res.send({ error: err.message});
      });
  });

  app.put("/reports/:id", (req, res) => {
    Report.findById(req.params.id).lean()
      .populate('author')
      .then((report) => {
        if (req.user != null && report.author._id == req.user._id) {
          Report.findByIdAndUpdate(req.params.id, req.body, {new: true})
            .then(report => {
              console.log('===========')
              console.log(report)
              res.send(report);
            })
            .catch(err => {
              console.log(err)
              res.status(400).send({error: err.message});
            });
        } else {
          res.status(400).send({error: "You can only update your reports."})
        }
      })
      .catch(err => {
        console.log(err.message);
        res.status(400).send({error: err.message});
      });
  });

  app.delete("/reports/:id", (req, res) => {
    Report.findById(req.params.id)
      .then(report => {
        if (report.author._id == req.user._id) {
          report.delete().then(() => {
            res.send({ success: `Successfully deleted the report ${req.params.id}`});
          }).catch(err => {
            res.send({ error: err.message });
          });
        } else {
          res.status(401).send({ error: 'You can only delete your own reaports'});
        }
      });
  });
};