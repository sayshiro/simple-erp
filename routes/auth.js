const express = require('express');
const router = express.Router();
const authController = require('../controllers/authController');

// Login route
router.get('/login', authController.loginPage);

// Register route
router.get('/register', authController.registerPage);

// Login action
router.post('/login', authController.login);

// Register action
router.post('/register', authController.register);

module.exports = router;
