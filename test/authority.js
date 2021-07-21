const app = require('../server');
const chai = require('chai');
const chaiHttp = require('chai-http');

const expect = chai.expect;
const agent = chai.request.agent(app);
const adminAgent = chai.request.agent(app);

const Report = require('../models/Report.js');
const User = require('../models/User.js');
const Authority = require('../models/Authority.js')

chai.should();
chai.use(chaiHttp);

describe('Authorities', function() {
  // Post that we'll use for testing purposes
  var authorityId = '5ddf784f9dbb9f1530b96033'
  var adminId = '5ddf76af01c5992ec4fa1c8c'
  var userId = '5ddf76af01c5992ec4fa1c9c';
  var reportId = '6ddf784f9dbb9f1530b96022';

  before(async function(done) {
    const authority  = new Authority({
      _id: authorityId,
      name: 'testauthority',
      users: [],
      reports: []
    });
    await authority.save();
    done();
  })

  before(async function (done) {
    const admin = new User({
        _id: adminId,
        username: 'testadmin',
        email: 'admin@email.com',
        password: 'password',
        authority: authorityId
    });
    await admin.save();
    done();
  });

  before(async function (done) {
    const user = new User({
        _id: userId,
        username: 'testuser',
        email: 'user@email.com',
        password: 'password',
    });
    await user.save();
    done();
  });

  before(async function(done) {
    const report  = new Report({
      _id: reportId,
      title: 'report',
      details: 'report details',
      author: userId
    });
    await report.save()
    done();
  })

  before(function(done) {
    agent.post("/login")
      .set('content-type', 'application/x-www-form-urlencoded')
      .send({ email: "user@email.com", password: "password" })
      .end(function(err, res) {
        res.status.should.be.equal(200);
        done();
    });
  });

  before(function(done) {
    adminAgent.post("/login")
      .set('content-type', 'application/x-www-form-urlencoded')
      .send({ email: "admin@email.com", password: "password" })
      .end(function(err, res) {
        res.status.should.be.equal(200);
        done();
    });
  });


  it('should create join authority request at POST /authority/authorityName/send-request', function(done) {
    agent
      .post('/authority/testauthority/send-request')
      .set('content-type', 'application/x-www-form-urlencoded')
      .send({})
      .then(function (res) {
        res.should.have.status(200);
         expect(res.body).to.have('success');
        done();
      })
      .catch(err => {
        done(err);
      });
  });

  it('should update user authority with accept at PUT /authority/authorityName/accept/userId', function (done) {
    adminAgent
      .post(`/authority/testauthority/accept/${userId}`)
      .set('content-type', 'application/x-www-form-urlencoded')
      .send({})
      .then(function(res) {
        expect(res).to.have.status(200);
        done();
      })
      .catch(function(err) {
        done(err);
      });
  });

  it('should not update user authority with accept at PUT /authority/authorityName/accept/userId if not authority admin', function (done) {
    agent
      .post(`/authority/testauthority/accept/${userId}`)
      .set('content-type', 'application/x-www-form-urlencoded')
      .send({})
      .then(function(res) {
        expect(res).to.have.status(401);
        expect(res.body).to.be('object');
        expect(res.body).to.have.property('error');
        done();
      })
      .catch(function(err) {
        done(err);
      });
  });

  it('should get specifc user at GET /authority/authorityName/userId', function(done) {
    adminAgent
      .get(`/authority/testauthority/${userId}`)
      .then(function (res) {
        res.should.have.status(200);
        expect(res.body).to.be.an('object');
        done();
      })
      .catch(err => {
        done(err);
      });
  });

  it('should not get specifc user at GET /authority/authorityName/userId is not authority admin', function(done) {
    agent
      .get(`/authority/testauthority/${userId}`)
      .then(function (res) {
        expect(res).to.have.status(401);
        expect(res.body).to.be('object');
        expect(res.body).to.have.property('error');
        done();
      })
      .catch(err => {
        done(err);
      });
  });

  it('should remove user from authority at PUT /authority/authorityName/remove/userId', function(done) {
    adminAgent
      .put(`/authority/testauthority/remove/${userId}`)
      .set('content-type', 'application/x-www-form-urlencoded')
      .send({})
      .then(function (res) {
        res.should.have.status(200);
        expect(res.body).to.be.an('object');
        expect(res.body).to.haveOwnProperty('success')
        done();
      })
      .catch(err => {
        done(err);
      });
  });

  it('should not remove user from authority at PUT /authority/authorityName/remove/userId if not authority admin', function(done) {
    agent
      .put(`/authority/testauthority/remove/${userId}`)
      .set('content-type', 'application/x-www-form-urlencoded')
      .send({})
      .then(function (res) {
        rexpect(res).to.have.status(401);
        expect(res.body).to.be('object');
        expect(res.body).to.have.property('error');
        done();
      })
      .catch(err => {
        done(err);
      });
  });

  after(function (done) {
    Report.deleteMany({})
    .then(function (res) {

      User.deleteMany({})
      .then(function() {

        Authority.deleteMany({})
        .then(function (res) {
          done();
        })
        .catch(function (err) {
          done(err);
        });

      })
      .catch(function (err) {
        done(err);
      });

    })
    .catch(function (err) {
      done(err);
    });
  })
});

function login(email, password) {
  return agent
    .post('/login')
    .set('content-type', 'application/x-www-form-urlencoded')
    .send({email: email, password: password })
}