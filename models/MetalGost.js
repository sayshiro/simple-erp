const mongoose = require('mongoose');

const metalGostSchema = new mongoose.Schema({
  number: { type: String, required: true },
  name: { type: String, required: true }
});

module.exports = mongoose.model('MetalGost', metalGostSchema);
