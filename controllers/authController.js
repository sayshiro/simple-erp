// Controller for handling authentication logic

const bcrypt = require('bcrypt');
const User = require('../models/user');

exports.loginPage = (req, res) => {
  res.sendFile('login.html', { root: './views' });
};

exports.registerPage = (req, res) => {
  res.sendFile('register.html', { root: './views' });
};

exports.login = async (req, res) => {
  try {
    const { username, password } = req.body;
    const user = await User.findOne({ username });
    if (!user) {
      return res.status(400).send('User not found');
    }
    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) {
      return res.status(400).send('Invalid credentials');
    }
    res.send('Logged in successfully');
  } catch (error) {
    res.status(500).send('Error logging in');
  }
};

exports.register = async (req, res) => {
  try {
    const { username, password, email } = req.body;
    const hashedPassword = await bcrypt.hash(password, 10);
    const user = new User({ username, password: hashedPassword, email });
    await user.save();
    res.send('User registered successfully');
  } catch (error) {
    res.status(500).send('Error registering user');
  }
};
