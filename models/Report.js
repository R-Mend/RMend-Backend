const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const ReportSchema = new Schema({
  title: { type: String, required: true },
  details: { type: String, required: true},
  author: { type: Schema.Types.ObjectId, ref: "User", required: true},
  organization: { type: Schema.Types.ObjectId, ref: "Organization", required: true }
}, {timestamps: true})

module.exports = mongoose.model("Report", ReportSchema);