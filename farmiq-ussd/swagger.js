const swaggerUi = require("swagger-ui-express");
const swaggerJsdoc = require("swagger-jsdoc");

const swaggerOptions = {
    definition: {
        openapi: "3.0.0",
        info: {
            title: "FarmIQ USSD & Payment API",
            version: "1.0.0",
            description: "API documentation for FarmIQ USSD, SMS, and M-Pesa integration",
        },
        servers: [{
                url: "http://localhost:83/",
                description: "Local development server",
            },
            {
                url: "https://ngrok-url/",
                description: "Locally deployed API",
            },
        ],
        components: {
            securitySchemes: {
                apiKey: {
                    type: 'apiKey',
                    in: 'header',
                    name: 'apiKey',
                    description: "Africa's Talking API Key"
                }
            }
        },
        tags: [{
                name: 'USSD',
                description: 'USSD session management endpoints'
            },
            {
                name: 'SMS',
                description: 'SMS messaging endpoints'
            },
            {
                name: 'M-Pesa',
                description: 'M-Pesa payment integration endpoints'
            }
        ]
    },
    apis: ["./routes/*.js"],
};

const swaggerDocs = swaggerJsdoc(swaggerOptions);

module.exports = (app) => {
    app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerDocs));
};