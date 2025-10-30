const express = require("express");
const router = express.Router();
const ussdService = require("../services/ussdService");
const { validateAPIKey } = require("../middleware/auth");

/**
 * @swagger
 * /ussd:
 *   post:
 *     summary: Handle USSD sessions
 *     tags: [USSD]
 *     security:
 *       - apiKey: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/x-www-form-urlencoded:
 *           schema:
 *             type: object
 *             properties:
 *               sessionId:
 *                 type: string
 *                 description: The USSD session ID
 *               phoneNumber:
 *                 type: string
 *                 description: The user's phone number
 *               text:
 *                 type: string
 *                 description: The user's input text
 *     responses:
 *       200:
 *         description: USSD response
 *         content:
 *           text/plain:
 *             schema:
 *               type: string
 */
router.post("/ussd", validateAPIKey, async(req, res) => {
    try {
        const { sessionId, phoneNumber, text } = req.body;
        const response = await ussdService.handleUSSDSession(sessionId, phoneNumber, text);
        res.set('Content-Type', 'text/plain');
        res.send(response);
    } catch (error) {
        console.error("USSD Error:", error);
        res.status(500).send("END An error occurred. Please try again.");
    }
});

/**
 * @swagger
 * /sms/send:
 *   post:
 *     summary: Send SMS message
 *     tags: [SMS]
 *     security:
 *       - apiKey: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               to:
 *                 type: array
 *                 items:
 *                   type: string
 *                 description: Array of phone numbers
 *               message:
 *                 type: string
 *                 description: Message content
 *     responses:
 *       200:
 *         description: SMS sent successfully
 */
router.post("/sms/send", validateAPIKey, async(req, res) => {
    try {
        const { to, message } = req.body;
        const result = await ussdService.sendSMS(to, message);
        res.json(result);
    } catch (error) {
        console.error("SMS Error:", error);
        res.status(500).json({ error: "Failed to send SMS" });
    }
});

module.exports = router;