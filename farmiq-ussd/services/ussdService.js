const AfricasTalking = require('africastalking');
const crypto = require('crypto');

// Initialize Africa's Talking
const africasTalking = AfricasTalking({
    apiKey: process.env.AFRICAS_TALKING_API_KEY,
    username: process.env.AFRICAS_TALKING_USERNAME
});

// Initialize session storage (in production, use Redis or a database)
const sessions = new Map();

class USSDService {
    constructor() {
        this.sms = africasTalking.SMS;
    }

    // Handle USSD session
    async handleUSSDSession(sessionId, phoneNumber, text) {
        let response = '';
        let currentSession = sessions.get(sessionId);

        if (!currentSession) {
            // New session
            currentSession = {
                phoneNumber,
                level: 1,
                data: {}
            };
            sessions.set(sessionId, currentSession);
            return this.showMainMenu();
        }

        // Handle menu levels
        switch (currentSession.level) {
            case 1:
                response = await this.handleMainMenuInput(text, currentSession);
                break;
            case 2:
                response = await this.handleSecondLevelMenu(text, currentSession);
                break;
            default:
                response = this.showMainMenu();
                currentSession.level = 1;
        }

        return response;
    }

    // Show main menu
    showMainMenu() {
        return `CON Welcome to FarmIQ
1. Check Credit Score
2. Apply for Loan
3. Make Payment
4. Check Loan Status
5. Get Support`;
    }

    // Handle main menu input
    async handleMainMenuInput(text, session) {
        switch (text) {
            case "1":
                session.level = 2;
                session.menu = "credit";
                return `CON Enter your ID Number to check credit score:`;

            case "2":
                session.level = 2;
                session.menu = "loan";
                return `CON Select Loan Type:
1. Farm Input Loan
2. Equipment Loan
3. Emergency Loan`;

            case "3":
                session.level = 2;
                session.menu = "payment";
                return `CON Enter Loan Reference Number:`;

            case "4":
                session.level = 2;
                session.menu = "status";
                return `CON Enter Loan Reference Number:`;

            case "5":
                return `END Thank you for using FarmIQ. Please call our support line: 0700000000`;

            default:
                return this.showMainMenu();
        }
    }

    // Handle second level menu
    async handleSecondLevelMenu(text, session) {
        switch (session.menu) {
            case "credit":
                // Simulate credit score check
                const score = Math.floor(Math.random() * 300) + 500;
                return `END Your credit score is: ${score}
                
Need help improving your score? 
Call our support: 0700000000`;

            case "loan":
                session.data.loanType = text;
                // Initialize loan application
                return `END Loan application initiated! 
                
Our agent will call you on ${session.phoneNumber} within 24 hours.
                
Reference: ${Date.now().toString().slice(-8)}`;

            case "payment":
                // Initiate M-Pesa payment
                return `END Payment initiated! 
                
Please check your phone for the M-PESA prompt.`;

            case "status":
                // Simulate loan status check
                const statuses = ['Active', 'Pending', 'Completed'];
                const randomStatus = statuses[Math.floor(Math.random() * statuses.length)];
                return `END Loan Status: ${randomStatus}
                
Need help? Call: 0700000000`;

            default:
                return this.showMainMenu();
        }
    }

    // Send SMS notification
    async sendSMS(to, message) {
        try {
            const result = await this.sms.send({
                to,
                message,
                from: 'FARMIQ'
            });
            return result;
        } catch (error) {
            console.error('SMS Error:', error);
            throw error;
        }
    }
}

module.exports = new USSDService();