const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
const Schema = mongoose.Schema;

const UserSchema = new Schema({
  createatedAt: { type: Date },
  updatedAt: { type: Date },
  password: { type: String, select: false},
  username: { type: String, required: true },
  reports : [{ type: Schema.Types.ObjectId, ref: "Report" }]
},
  {timestamps: {createdAt: 'created_at'}}
);

UserSchema.methods.comparePassword = function(password, done) {
  bcrypt.compare(password, this.password, (err, isMatch) => {
      done(err, isMatch);
  });
};

module.exports = mongoose.model('User', UserSchema);