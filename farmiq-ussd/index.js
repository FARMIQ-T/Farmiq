const os = require("os");
const http = require("http");
const express = require("express");
const path = require("path");
const cors = require("cors");
const routes = require("./routes/routes");
const swagger = require("./swagger");


// Initialize Express app
const app = express();

// Middleware Setup
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));


// Swagger Documentation
swagger(app);

// Serve static files
app.use("/images", express.static(path.join(__dirname, "images")));
app.use(express.static(path.join(__dirname, "public")));

// Import routes
const ussdRoutes = require("./routes/ussd");
const mpesaRoutes = require("./routes/routes");

// API Routes
app.use("/", mpesaRoutes); // M-Pesa routes
app.use("/", ussdRoutes); // USSD and SMS routes



// Error Handling Middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ message: "Something went wrong!", error: err.message });
});

// Get Local Network IP
const getNetworkIp = () => {
    const networkInterfaces = os.networkInterfaces();
    for (const iface of Object.values(networkInterfaces).flat()) {
        if (iface.family === "IPv4" && !iface.internal) {
            return iface.address;
        }
    }
    return "localhost";
};

// Start the Server
const PORT = process.env.PORT || 83;
http.createServer(app).listen(PORT, () => {
    const networkIp = getNetworkIp();
    console.log(`Server running at:\n- Local:    http://localhost:${PORT}/\n- Network:  http://${networkIp}:${PORT}/`);
    console.log(`Swagger Docs available at http://${networkIp}:${PORT}/api-docs`);
});