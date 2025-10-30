const swaggerUi = require("swagger-ui-express");
const swaggerJsdoc = require("swagger-jsdoc");

const swaggerOptions = {
    definition: {
        openapi: "3.0.0",
        info: {
            title: "My API",
            version: "1.0.0",
            description: "API documentation for my web app",
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
    },
    apis: ["./routes/*.js"], // Specify where route docs are stored
};

const swaggerDocs = swaggerJsdoc(swaggerOptions);

module.exports = (app) => {
    app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerDocs));
};