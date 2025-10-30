/**
 * Middleware to validate Africa's Talking API key
 */
const validateAPIKey = (req, res, next) => {
    const apiKey = req.get('apiKey');

    if (!apiKey || apiKey !== process.env.AFRICAS_TALKING_API_KEY) {
        return res.status(401).json({
            status: "error",
            message: "Invalid or missing API key"
        });
    }

    // Add username to request for routes that need it
    req.username = process.env.AFRICAS_TALKING_USERNAME;
    next();
};

module.exports = {
    validateAPIKey
};