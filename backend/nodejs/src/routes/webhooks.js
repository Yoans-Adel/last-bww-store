const express = require('express');
const router = express.Router();

router.get('/facebook', (req, res) => {
  res.send('OK');
});

router.post('/facebook', (req, res) => {
  res.json({ success: true });
});

router.post('/whatsapp', (req, res) => {
  res.json({ success: true });
});

module.exports = router;
