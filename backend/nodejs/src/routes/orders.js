const express = require('express');
const router = express.Router();

router.get('/', async (req, res) => {
  res.json({ success: true, orders: [] });
});

router.post('/', async (req, res) => {
  res.json({ success: true, message: 'Order created' });
});

module.exports = router;
