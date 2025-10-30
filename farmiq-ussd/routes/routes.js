require("dotenv").config();
// ✅ Import necessary modules
const express = require("express");
const router = express.Router();
const jwt = require("jsonwebtoken");
const path = require("path");
const axios = require("axios");
const crypto = require("crypto");
// 🔐 Config — replace with env vars in production
const config = {
    africa_callbackURL: process.env.AFRICAS_TALKING_CALLBACK_URL,
    consumerKey: process.env.MPESA_CONSUMER_KEY,
    consumerSecret: process.env.MPESA_CONSUMER_SECRET,
    shortcode: process.env.MPESA_SHORTCODE,
    passkey: process.env.MPESA_PASSKEY,
    callbackURL: process.env.MPESA_CALLBACK_URL,
    accountRef: "FARMIQ"
};

// 🔄 Utility: Get OAuth Token
async function getAccessToken() {
    const credentials = Buffer.from(`${config.consumerKey}:${config.consumerSecret}`).toString("base64");
    const res = await axios.get("https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials", {
        headers: { Authorization: `Basic ${credentials}` }
    });
    return res.data.access_token;
}

// 🔧 Utility: Timestamp & Password
function getTimestamp() {
    const date = new Date();
    return date.toISOString().replace(/[-:T.]/g, "").substring(0, 14);
}

function getPassword(timestamp) {
    return Buffer.from(config.shortcode + config.passkey + timestamp).toString("base64");
}

//
// 🚀 INITIATE PAYMENT
//
router.post("/mpesa/stkpush", async(req, res) => {
    try {
        const { fineId, phone } = req.body;
        const fine = await Fine.findById(fineId);
        if (!fine) return res.status(404).json({ error: "Fine not found" });

        const timestamp = getTimestamp();
        const password = getPassword(timestamp);
        const accessToken = await getAccessToken();
        const amount = fine.amount + 5;

        const stkRes = await axios.post("https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest", {
            BusinessShortCode: config.shortcode,
            Password: password,
            Timestamp: timestamp,
            TransactionType: "CustomerPayBillOnline",
            Amount: amount,
            PartyA: phone,
            PartyB: config.shortcode,
            PhoneNumber: phone,
            CallBackURL: config.callbackURL,
            AccountReference: config.accountRef,
            TransactionDesc: fine.violationName
        }, {
            headers: { Authorization: `Bearer ${accessToken}` }
        });

        await Payment.create({
            fine: fine._id,
            phone,
            amount,
            checkoutRequestID: stkRes.data.CheckoutRequestID,
            status: "Pending"
        });

        res.json({ success: true, checkoutRequestID: stkRes.data.CheckoutRequestID });
    } catch (err) {
        console.error("❌ STK INIT ERROR:", err.message);
        res.status(500).json({ error: "STK initiation failed" });
    }
});



//
// 🔍 QUERY STATUS
//


const resultMessages = {
    0: "✅ Payment successful",
    1: "⏱️ Timeout",
    1032: "❌ Cancelled by user",
    2001: "💸 Insufficient balance",
    1001: "🔐 Invalid credentials"
};

router.post("/mpesa/stkquery", async(req, res) => {
    try {
        const { checkoutRequestID } = req.body;
        const timestamp = getTimestamp();
        const password = getPassword(timestamp);
        const accessToken = await getAccessToken();

        const queryRes = await axios.post("https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query", {
            BusinessShortCode: config.shortcode,
            Password: password,
            Timestamp: timestamp,
            CheckoutRequestID: checkoutRequestID
        }, {
            headers: { Authorization: `Bearer ${accessToken}` }
        });

        const result = queryRes.data;
        const userMessage = resultMessages[result.ResultCode] || "🤷 Unrecognized result";

        const payment = await Payment.findOne({ checkoutRequestID });
        if (payment) {
            if (result.ResultCode === 0) payment.status = "Paid";
            else if ([1, 1032, 2001].includes(result.ResultCode)) payment.status = "Failed";
            await payment.save();
        }

        res.json({ success: true, result, userMessage });
    } catch (err) {
        console.error("❌ STK QUERY ERROR:", err.response.data || err.message);
        res.status(500).json({
            error: "Query failed",
            details: err.response.data || err.message
        });

    }
});

// 🧾 GENERATE QR CODE
//
router.post("/mpesa/generate-qr", async(req, res) => {
    try {
        const { MerchantName, RefNo, Amount, TrxCode, CPI, Size } = req.body;
        const accessToken = await getAccessToken();

        const qrRes = await axios.post("https://sandbox.safaricom.co.ke/mpesa/qrcode/v1/generate", {
            MerchantName,
            RefNo,
            Amount,
            TrxCode,
            CPI,
            Size
        }, {
            headers: {
                Authorization: `Bearer ${accessToken}`,
                "Content-Type": "application/json"
            }
        });

        res.json(qrRes.data);
    } catch (err) {
        console.error("❌ QR GENERATION ERROR:", err.message);
        res.status(500).json({ error: "QR generation failed" });
    }
});


//
// 📲 CALLBACK RECEIVER
//
router.post("/mpesa/stkcallback", async(req, res) => {
    const result = req.body.Body.stkCallback;
    if (!result) return res.status(400).json({ error: "Invalid callback format" });

    const { CheckoutRequestID, ResultCode, ResultDesc, CallbackMetadata } = result;

    try {
        const payment = await Payment.findOne({ checkoutRequestID: CheckoutRequestID });
        if (!payment) return res.status(404).json({ error: "Payment not found" });

        if (ResultCode === 0) {
            const items = CallbackMetadata.Item || [];
            const mpesaCode = items.find(i => i.Name === "MpesaReceiptNumber").Value;
            const amount = items.find(i => i.Name === "Amount").Value;

            payment.status = "Success";
            payment.mpesaCode = mpesaCode;
            payment.metadata = result;
            await payment.save();

            await Fine.findByIdAndUpdate(payment.fine, { status: "Paid" });
        } else {
            payment.status = "Failed";
            payment.metadata = result;
            await payment.save();
        }

        res.status(200).json({ received: true });
    } catch (err) {
        console.error("❌ CALLBACK ERROR:", err.message);
        res.status(500).json({ error: "Callback handling failed" });
    }
});
module.exports = router;