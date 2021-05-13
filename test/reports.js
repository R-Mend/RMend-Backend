const app = require("../server");
const chai = require("chai");
const chaiHttp = require("chai-http");
const expect = chai.expect;
const agent = chai.request.agent(app);

const Report = require('../models/Report.js');
const User = require("../models/User.js");

chai.should();
chai.use(chaiHttp);

describe('Reports', function() {
  // Post that we'll use for testing purposes
  var reportId = "5ddf784f9dbb9f1530b96022";
  var userId = "5ddf76af01c5992ec4fa1c9c";

  before(function (done) {
    agent
      .post('/sign-up')
      .set("content-type", "application/x-www-form-urlencoded")
      .send({_id: userId, username: 'reporttest', password: 'testreport' })
      .then(function (res) {
        done();
      })
      .catch(function (err) {
        done(err);
      });
  });

  before(function(done) {
    const report  = new Report({
      _id: reportId,
      title: 'report',
      details: 'report details',
      author: userId
    });
    report.save()
    done();
  })

  it('should get all reports at GET /reports', function(done) {
    agent
      .get('/reports').then(function (res) {
        res.should.have.status(200);
        expect(res.body).to.be.an('array');
        done();
      })
      .catch(err => {
        done(err);
      })
  })

  it('should create with valid attributes at POST /report/new', function (done) {
    Report.estimatedDocumentCount()
      .then(function (initialDocCount) {
        agent
          .post('/report/new')
          .set('content-type', 'application/x-www-form-urlencoded')
          .send({ title: "report", details: "detials" })
          .then(function(res) {
            Report.estimatedDocumentCount()
              .then(function(newDocCount) {
                expect(res).to.have.status(200);
                expect(newDocCount).to.be.equal(initialDocCount + 1);
                done();
              })
              .catch(function(err) {
                done(err);
              });
          })
          .catch(function(err) {
            done(err);
          });
      })
      .catch(function(err) {
        done(err);
      });
  });

  it('should get specifc report at GET /reports/reportId', function(done) {
    agent
      .get(`/reports/${reportId}`).then(function (res) {
        res.should.have.status(200);
        expect(res.body).to.be.an('object');
        done();
      })
      .catch(err => {
        done(err);
      })
  });

  it('should update specifc report at PUT /reports/reportId', function(done) {
    agent
      .put(`/reports/${reportId}`)
      .set('content-type', 'application/x-www-form-urlencoded')
      .send({ details: 'new details'})
      .then(function (res) {
        res.should.have.status(200);
        expect(res.body).to.be.an('object');
        expect(res.body.details).to.equal('new details');
        done();
      })
      .catch(err => {
        done(err);
      });
  });

  it('should delete report at DELET /reports/reportId', function(done) {
    agent
      .delete(`/reports/${reportId}`)
      .set('content-type', 'application/x-www-form-urlencoded')
      .send().then(function(res) {
        res.should.have.status(200);
        expect(res.body).to.have.property('success');
        done();
      })
      .catch(err => {
        done(err);
      })
  })

  after(function (done) {
    Report.deleteMany({title: 'report'})
    .then(function (res) {
      agent.close()

      User.findByIdAndDelete(userId)
        .then(function (res) {
          done()
        })
        .catch(function (err) {
          done(err);
        });
    })
    .catch(function (err) {
      done(err);
    });
  });
});