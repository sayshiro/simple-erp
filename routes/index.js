const express = require('express');
const router = express.Router();

// Basic route
router.get('/', (req, res) => {
  res.send('Welcome to the Simple ERP Home Page!');
});

module.exports = router;