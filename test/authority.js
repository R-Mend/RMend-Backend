const app = require("../server");
const chai = require("chai");
const chaiHttp = require("chai-http");

const expect = chai.expect;
const agent = chai.request.agent(app);
const adminAgent = chai.request.agent(app);

const Report = require("../models/Report.js");
const User = require("../models/User.js");
const Authority = require("../models/Authority.js");

chai.should();
chai.use(chaiHttp);

describe("Authorities", function () {
    // Post that we'll use for testing purposes
    var authorityId = "5ddf784f9dbb9f1530b96033";
    var adminId = "6ddf86af01c5992ec4fa1c8c";
    var userId = "5ddf76af01c5992ec4fa1c9c";
    var reportId = "6ddf784f9dbb9f1530b96022";
    let adminToken;
    let userToken;

    before(function (done) {
        const authority = new Authority({
            _id: authorityId,
            name: "testauthority",
            users: [],
            reports: [],
        });
        authority.save();
        done();
    });

    before(function (done) {
        adminAgent
            .post("/sign-up")
            .set({ "content-type": "application/json" })
            .send({
                _id: adminId,
                username: "testadmin",
                email: "admin@email.com",
                password: "password",
                authority: authorityId,
                access_level: "admin",
            })
            .end((err, res) => {
                expect(res.status).to.equal(200);
                expect(res.body).to.be.an("object");
                expect(res.body).to.have.property("user");
                expect(res.body.user).to.have.property("token");
                adminToken = res.body.user.token;
                done();
            });
    });

    before(function (done) {
        agent
            .post("/sign-up")
            .set({ "content-type": "application/json" })
            .send({
                _id: userId,
                username: "testuser",
                email: "user@email.com",
                password: "password",
            })
            .end(function (err, res) {
                expect(res.status).to.equal(200);
                expect(res.body).to.be.an("object");
                expect(res.body).to.have.property("user");
                expect(res.body.user).to.have.property("token");
                userToken = res.body.user.token;
                done();
            });
    });

    before(function (done) {
        const report = new Report({
            _id: reportId,
            title: "report",
            details: "report details",
            author: userId,
            authority: authorityId,
            priority: false,
            in_review: false,
        });
        report.save();
        done();
    });

    it("should create join authority join request at POST /authority/send-request", function (done) {
        agent
            .post("/authority/send-request")
            .set({ Authorization: `Bearer ${userToken}` })
            .set("content-type", "application/json")
            .send({ authorityId })
            .end((err, res) => {
                console.log(res.body);
                expect(res.status).to.equal(200);
                done();
            });
    });

    it("should update user authority with accept at PUT /authority/accept-request/:userId", function (done) {
        adminAgent
            .put(`/authority/accept-request/${userId}`)
            .set({ Authorization: `Bearer ${adminToken}` })
            .set("content-type", "application/json")
            .send({})
            .end((err, res) => {
                console.log(res.body);
                expect(res.status).to.equal(200);
                done();
            });
    });

    it("should not update user authority with accept at PUT /authority/accept-request/:userId if not authority admin", function (done) {
        agent
            .put(`/authority/accept-request/${userId}`)
            .set({ Authorization: `Bearer ${userToken}` })
            .set("content-type", "application/json")
            .send({})
            .end((err, res) => {
                expect(res).to.have.status(401);
                expect(res.body).to.have.property("message");
                done();
            });
    });

    it("should get specifc user at GET /authority/users/:userId", function (done) {
        adminAgent
            .get(`/authority/users/${userId}`)
            .set({ Authorization: `Bearer ${adminToken}` })
            .end((err, res) => {
                console.log(res.body);
                expect(res).to.have.status(200);
                expect(res.body).to.be.an("object");
                done();
            });
    });

    it("should not get specifc user at GET /authority/users/:userId is not authority admin", function (done) {
        agent
            .get(`/authority/users/${userId}`)
            .set({ Authorization: `Bearer ${userToken}` })
            .end((err, res) => {
                console.log(res.body);
                expect(res).to.have.status(401);
                expect(res.body).to.be.an("object");
                expect(res.body).to.have.property("message");
                done();
            });
    });

    it("should update specifc user access_level at PUT /authority/users/:userId", function (done) {
        adminAgent
            .put(`/authority/users/${userId}`)
            .set({ Authorization: `Bearer ${adminToken}` })
            .set("content-type", "application/json")
            .send({ access_level: "employee" })
            .end((err, res) => {
                console.log(res.body);
                expect(res).to.have.status(200);
                done();
            });
    });

    it("should not update specifc user access_level at PUT /authority/users/:userId if not authority admin", function (done) {
        agent
            .put(`/authority/users/${userId}`)
            .set({ Authorization: `Bearer ${userToken}` })
            .set("content-type", "application/json")
            .send({ access_level: "employee" })
            .end((err, res) => {
                console.log(res.body);
                expect(res).to.have.status(401);
                done();
            });
    });

    it("should remove user from authority at DELETE /authority/users/:userId", function (done) {
        adminAgent
            .delete(`/authority/users/${userId}`)
            .set({ Authorization: `Bearer ${adminToken}` })
            .set("content-type", "application/json")
            .send({})
            .then(function (res) {
                res.should.have.status(200);
                expect(res.body).to.be.an("object");
                expect(res.body).to.haveOwnProperty("message");
                done();
            })
            .catch((err) => {
                done(err);
            });
    });

    it("should not remove user from authority at DELETE /authority/users/:userId if not authority admin", function (done) {
        agent
            .delete(`/authority/users/${userId}`)
            .set({ Authorization: `Bearer ${userToken}` })
            .set("content-type", "application/json")
            .send({})
            .end((err, res) => {
                expect(res).to.have.status(401);
                expect(res.body).to.be.an("object");
                expect(res.body).to.have.property("message");
                done();
            });
    });

    it("should get all authority reports at GET /authority/reports", function (done) {
        adminAgent
            .get("/authority/reports")
            .set({ Authorization: `Bearer ${adminToken}` })
            .end((err, res) => {
                console.log(res.body);
                res.should.have.status(200);
                expect(res.body).to.have.property("reports");
                expect(res.body.reports).to.be.an("array");
                done();
            });
    });

    it("should not get all authority reports at GET /authority/reports if no authority", function (done) {
        agent
            .get("/authority/reports")
            .set({ Authorization: `Bearer ${userToken}` })
            .end((err, res) => {
                console.log(res.body);
                res.should.have.status(401);
                done();
            });
    });

    it("should get specifc report at GET /authority/reports/:reportId", function (done) {
        adminAgent
            .get(`/authority/reports/${reportId}`)
            .set({ Authorization: `Bearer ${adminToken}` })
            .end((err, res) => {
                console.log(res.body);
                res.should.have.status(200);
                expect(res.body).to.be.an("object");
                expect(res.body).to.have.property("report");
                expect(res.body.report).to.be.an("object");
                done();
            });
    });

    it("should not get specifc report at GET /authority/reports/:reportId if no authority", function (done) {
        agent
            .get(`/authority/reports/${reportId}`)
            .set({ Authorization: `Bearer ${userToken}` })
            .end((err, res) => {
                console.log(res.body);
                res.should.have.status(401);
                expect(res.body).to.be.an("object");
                expect(res.body).to.have.property("message");
                done();
            });
    });

    it("should update specifc report at PUT /authority/reports/:reportId", function (done) {
        adminAgent
            .put(`/authority/reports/${reportId}`)
            .set({ Authorization: `Bearer ${adminToken}` })
            .set("content-type", "application/json")
            .send({ details: "new details" })
            .end((err, res) => {
                console.log(res.body);
                res.should.have.status(200);
                expect(res.body).to.be.an("object");
                expect(res.body).to.have.property("report");
                expect(res.body.report.details).to.equal("new details");
                done();
            });
    });

    it("should not update specifc report at PUT /authority/reports/:reportId if not authority admin", function (done) {
        agent
            .put(`/authority/reports/${reportId}`)
            .set({ Authorization: `Bearer ${userToken}` })
            .set("content-type", "application/json")
            .send({ details: "new details" })
            .end((err, res) => {
                console.log(res.body);
                res.should.have.status(401);
                expect(res.body).to.be.an("object");
                expect(res.body).to.property("message");
                done();
            });
    });

    it("should delete report at DELET /authority/reports/:reportId", function (done) {
        adminAgent
            .delete(`/authority/reports/${reportId}`)
            .set({ Authorization: `Bearer ${adminToken}` })
            .end((err, res) => {
                console.log(res.body);
                res.should.have.status(200);
                expect(res.body).to.be.an("object");
                expect(res.body).to.have.property("message");
                done();
            });
    });

    it("should not delete report at DELET /authority/reports/:reportId is not authority admin", function (done) {
        agent
            .delete(`/authority/reports/${reportId}`)
            .set({ Authorization: `Bearer ${userToken}` })
            .end((err, res) => {
                console.log(res.body);
                res.should.have.status(401);
                expect(res.body).to.be.an("object");
                expect(res.body).to.have.property("message");
                done();
            });
    });

    after(async function () {
        await Authority.deleteMany({});
        await Report.deleteMany({});
        await User.deleteMany({});
        return;
    });
});
