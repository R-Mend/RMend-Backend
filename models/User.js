const mongoose = require("mongoose");
const bcrypt = require("bcryptjs");
const Schema = mongoose.Schema;

const UserSchema = new Schema(
    {
        createatedAt: { type: Date },
        updatedAt: { type: Date },
        password: { type: String, select: false },
        username: { type: String, required: true },
        email: { type: String, required: true, match: /.+\@.+\..+/, unique: true },
        reports: [{ type: Schema.Types.ObjectId, ref: "Report" }],
        authority: { type: Schema.Types.ObjectId, ref: "Authority", required: false },
        access_level: { type: String, default: "user" },
    },
    { timestamps: { createdAt: "created_at" } }
);

UserSchema.pre("save", async function (next) {
    if (this.password) {
        var salt = await bcrypt.genSaltSync(10);
        this.password = await bcrypt.hashSync(this.password, salt);
    }
    next();
});

UserSchema.methods.comparePassword = function (password, done) {
    bcrypt.compare(password, this.password, (err, isMatch) => {
        done(err, isMatch);
    });
};

module.exports = mongoose.model("User", UserSchema);
