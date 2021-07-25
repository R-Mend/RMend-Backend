const app = require("../server");
const chai = require("chai");
const chaiHttp = require("chai-http");

const expect = chai.expect;
const agent = chai.request.agent(app);
const otherAgent = chai.request.agent(app);

const Report = require("../models/Report.js");
const User = require("../models/User.js");
const Authority = require("../models/Authority.js");

chai.should();
chai.use(chaiHttp);

describe("Reports", function () {
    // Post that we'll use for testing purposes
    var authorityId = "5ddf784f9dbb9f1530b96033";
    var otherId = "6ddf86af01c5992ec4fa1c8c";
    var userId = "5ddf76af01c5992ec4fa1c9c";
    var reportId = "6ddf784f9dbb9f1530b96022";
    let otherToken;
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
        otherAgent
            .post("/sign-up")
            .set({ "content-type": "application/json" })
            .send({
                _id: otherId,
                username: "testother",
                email: "other@email.com",
                password: "password",
            })
            .end(function (err, res) {
                expect(res.status).to.equal(200);
                expect(res.body).to.be.an("object");
                expect(res.body).to.have.property("user");
                expect(res.body.user).to.have.property("token");
                otherToken = res.body.user.token;
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

    before(async function () {
        const report = new Report({
            _id: reportId,
            title: "report",
            details: "report details",
            author: userId,
            authority: authorityId,
        });
        await report.save();
        return;
    });

    it("should get all reports at GET /reports", function (done) {
        agent
            .get("/reports")
            .set({ Authorization: `Bearer ${userToken}` })
            .end((err, res) => {
                console.log(res.body);
                res.should.have.status(200);
                expect(res.body).to.have.property("reports");
                expect(res.body.reports).to.be.an("array");
                done();
            });
    });

    it("should create with valid attributes at POST /report/new", async function () {
        const initialDocCount = await Report.estimatedDocumentCount();

        agent
            .post("/report/new")
            .set({ Authorization: `Bearer ${userToken}` })
            .set("content-type", "application/json")
            .send({ title: "report", details: "detials", authority: authorityId })
            .end(async (err, res) => {
                console.log(res.body);
                expect(res).to.have.status(200);
                const newDocCount = await Report.estimatedDocumentCount();
                expect(newDocCount).to.be.equal(initialDocCount + 1);
                return;
            });
    });

    it("should get all user reports at GET /my/reports", function (done) {
        agent
            .get("/my/reports")
            .set({ Authorization: `Bearer ${userToken}` })
            .end((err, res) => {
                console.log(res.body);
                res.should.have.status(200);
                expect(res.body).to.have.property("reports");
                expect(res.body.reports).to.be.an("array");
                done();
            });
    });

    it("should get specifc report at GET /reports/:reportId", function (done) {
        agent
            .get(`/reports/${reportId}`)
            .set({ Authorization: `Bearer ${userToken}` })
            .end((err, res) => {
                console.log(res.body);
                res.should.have.status(200);
                expect(res.body).to.be.an("object");
                expect(res.body).to.have.property("report");
                expect(res.body.report).to.be.an("object");
                done();
            });
    });

    it("should update specifc report at PUT /reports/:reportId", function (done) {
        agent
            .put(`/reports/${reportId}`)
            .set({ Authorization: `Bearer ${userToken}` })
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

    it("should not update specifc report at PUT /reports/:reportId if not report author", function (done) {
        otherAgent
            .put(`/reports/${reportId}`)
            .set({ Authorization: `Bearer ${otherToken}` })
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

    it("should not delete report at DELETE /reports/:reportId is not report author", function (done) {
        otherAgent
            .delete(`/reports/${reportId}`)
            .set({ Authorization: `Bearer ${otherToken}` })
            .end((err, res) => {
                console.log(res.body);
                res.should.have.status(401);
                expect(res.body).to.be.an("object");
                expect(res.body).to.have.property("message");
                done();
            });
    });

    it("should delete report at DELETE /reports/:reportId", function (done) {
        agent
            .delete(`/reports/${reportId}`)
            .set({ Authorization: `Bearer ${userToken}` })
            .end((err, res) => {
                console.log(res.body);
                res.should.have.status(200);
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
