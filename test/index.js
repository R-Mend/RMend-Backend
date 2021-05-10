const app = require('./../server');
const chai = require('chai');
const chaiHttp = require('chai-http');
const { expect } = require('chai');

chai.use(chaiHttp);

describe("site", function () {
    it('Should load the index route', function(done) {
        chai
          .request(app)
          .get('/')
          .end(function(err, res) {
            if (err) {
                return done(err);
            }
            expect(res).to.have.status(200);
            return done();
        });
    });
});