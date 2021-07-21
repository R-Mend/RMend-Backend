const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const AuthoritySchema = new Schema({
    name: { type: String, required: true },
    reports: [{type: Schema.Types.ObjectId, ref: "Report"}],
    users: [{ type: Schema.Types.ObjectId, ref: "User" }],
    requests: [{ userId: String, userEmail: String }]
}, {timestamps: true})

module.exports = mongoose.model("Authority", AuthoritySchema)