const express = require('express');
const router = express.Router();

router.get('/', async (req, res) => {
  res.json({ success: true, products: [] });
});

router.get('/:id', async (req, res) => {
  res.json({ success: true, product: {} });
});

router.post('/', async (req, res) => {
  res.json({ success: true, message: 'Product created' });
});

module.exports = router;
