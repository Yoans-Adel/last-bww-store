const express = require('express');
const router = express.Router();

router.post('/message', async (req, res) => {
  res.json({ success: true, response: 'مرحباً! كيف يمكنني مساعدتك؟' });
});

module.exports = router;
