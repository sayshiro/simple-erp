const mongoose = require('mongoose');

const metalGradeSchema = new mongoose.Schema({
  name: { type: String, required: true },
  description: { type: String }
});

module.exports = mongoose.model('MetalGrade', metalGradeSchema);
