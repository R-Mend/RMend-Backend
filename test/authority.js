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
                done();
            });
    });

    before(function (done) {
        const report = new Report({
            _id: reportId,
            title: "report",
            details: "report details",
            author: userId,
        });
        report.save();
        done();
    });

    it("should create join authority join request at POST /authority/send-request", function (done) {
        agent
            .post("/authority/send-request")
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
            .set("content-type", "application/json")
            .send({})
            .end((err, res) => {
                expect(res).to.have.status(401);
                expect(res.body).to.have.property("message");
                done();
            });
    });

    it("should get specifc user at GET /authority/:userId", function (done) {
        adminAgent.get(`/authority/${userId}`).end((err, res) => {
            console.log(res.body);
            expect(res).to.have.status(200);
            expect(res.body).to.be.an("object");
            done();
        });
    });

    it("should not get specifc user at GET /authority/:userId is not authority admin", function (done) {
        agent.get(`/authority/${userId}`).end((err, res) => {
            console.log(res.body);
            expect(res).to.have.status(401);
            expect(res.body).to.be.an("object");
            expect(res.body).to.have.property("message");
            done();
        });
    });

    it("should update specifc user access_level at PUT /authority/:userId", function (done) {
        adminAgent
            .put(`/authority/${userId}`)
            .set("content-type", "application/json")
            .send({ access_level: "employee" })
            .end((err, res) => {
                console.log(res.body);
                expect(res).to.have.status(200);
                done();
            });
    });

    it("should not update specifc user access_level at PUT /authority/:userId if not authority admin", function (done) {
        agent
            .put(`/authority/${userId}`)
            .set("content-type", "application/json")
            .send({ access_level: "employee" })
            .end((err, res) => {
                console.log(res.body);
                expect(res).to.have.status(401);
                done();
            });
    });

    it("should remove user from authority at DELETE /authority/:userId", function (done) {
        adminAgent
            .delete(`/authority/${userId}`)
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

    it("should not remove user from authority at DELETE /authority/:userId if not authority admin", function (done) {
        agent
            .delete(`/authority/${userId}`)
            .set("content-type", "application/json")
            .send({})
            .end((err, res) => {
                expect(res).to.have.status(401);
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
