const mongoose = require('mongoose');

const metalTypeSchema = new mongoose.Schema({
  name: { type: String, required: true }
});

module.exports = mongoose.model('MetalType', metalTypeSchema);
