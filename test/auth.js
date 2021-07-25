const chai = require("chai");
const chaiHttp = require("chai-http");
const app = require("../server");

chai.should();
chai.use(chaiHttp);

// Agent that will keep track of our cookies
const expect = chai.expect;
const agent = chai.request.agent(app);

const User = require("../models/User.js");

describe("User", function () {
    after(function () {
        agent.close();
    });

    it("should not be able to login if they have not registered", function (done) {
        agent
            .post("/login")
            .set("content-type", "application/json")
            .send({ email: "wrong@wrong.com", password: "nope" })
            .end(function (err, res) {
                res.status.should.be.equal(401);
                done();
            });
    });

    // signup
    it("should be able to signup", function (done) {
        User.findOneAndRemove({ email: "test@email.com" }, function () {
            agent
                .post("/sign-up")
                .set({ "content-type": "application/json" })
                .send({ username: "user", email: "test@email.com", password: "password" })
                .end(function (err, res) {
                    res.should.have.status(200);
                    expect(res.body).to.be.an("object");
                    expect(res.body).to.have.property("user");
                    expect(res.body.user).to.have.property("token");
                    done();
                });
        });
    });

    // login
    it("should be able to login", function (done) {
        agent
            .post("/login")
            .set({ "content-type": "application/json" })
            .send({ email: "test@email.com", password: "password" })
            .end(function (err, res) {
                res.should.have.status(200);
                expect(res.body).to.be.an("object");
                expect(res.body).to.have.property("user");
                expect(res.body.user).to.have.property("token");
                done();
            });
    });

    // logout
    //   it('should be able to logout', function(done) {
    //     agent
    //     .get('/logout')
    //     .end((err, res) => {
    //       res.should.have.status(200);
    //       agent.should.not.have.cookie('nToken');
    //       done();
    //     });
    //   });

    after(async function () {
        await User.deleteMany({});
        return;
    });
});
