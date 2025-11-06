const express = require('express');
const router = express.Router();

router.post('/register', async (req, res) => {
  res.json({ success: true, message: 'User registered' });
});

router.post('/login', async (req, res) => {
  res.json({ success: true, token: 'sample-jwt-token' });
});

module.exports = router;
