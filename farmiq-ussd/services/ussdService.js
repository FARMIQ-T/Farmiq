const AfricasTalking = require('africastalking');
const crypto = require('crypto');
const db = require('./databaseService');

// Initialize Africa's Talking
const africasTalking = AfricasTalking({
    apiKey: process.env.AFRICAS_TALKING_API_KEY,
    username: process.env.AFRICAS_TALKING_USERNAME
});

class USSDService {
    constructor() {
        this.sms = africasTalking.SMS;
    }

    async handleUSSDSession(sessionId, phoneNumber, text) {
        try {
            // Get or create farmer profile
            const farmer = await db.getOrCreateFarmer(phoneNumber);

            // Get or update session
            const session = await db.createOrUpdateSession(sessionId, phoneNumber, {
                farmerId: farmer.id,
                level: 1,
                data: {}
            });

            if (!text) {
                return this.showMainMenu();
            }

            // Split input text into array of responses
            const inputs = text.split('*');
            const lastInput = inputs[inputs.length - 1];

            // Handle menu levels
            switch (session.session_data.level) {
                case 1:
                    return await this.handleMainMenuInput(lastInput, farmer, session);
                case 2:
                    return await this.handleSecondLevelMenu(lastInput, farmer, session);
                default:
                    return this.showMainMenu();
            }
        } catch (error) {
            console.error('USSD Error:', error);
            return 'END An error occurred. Please try again.';
        }
    }

    showMainMenu() {
        return `CON Welcome to FarmIQ
1. Check Credit Score
2. Apply for Loan
3. Make Payment
4. Check Loan Status
5. Update Farm Profile`;
    }

    async handleMainMenuInput(text, farmer, session) {
        try {
            switch (text) {
                case "1":
                    const creditScore = await db.getLatestCreditScore(farmer.id);
                    if (!creditScore) {
                        return `END Credit score not available yet. 
                        We'll assess your profile soon.
                        
                        Call support: 0700000000`;
                    }
                    return `END Your Credit Score: ${creditScore.score}
                    Risk Level: ${this.getRiskLevel(creditScore.score)}
                    Last Updated: ${new Date(creditScore.created_at).toLocaleDateString()}
                    
                    Need help? Call 0700000000`;

                case "2":
                    session.session_data.level = 2;
                    session.session_data.menu = "loan";
                    await db.createOrUpdateSession(session.session_id, farmer.phone_number, session.session_data);

                    return `CON Select Loan Type:
1. Farm Input Loan (Up to 50,000)
2. Equipment Loan (Up to 200,000)
3. Emergency Loan (Up to 20,000)`;

                case "3":
                    const activeLoan = await db.getActiveLoan(farmer.id);
                    if (!activeLoan) {
                        return `END No active loan found.
                        
                        Apply for a loan from the main menu.`;
                    }

                    return `CON Your loan balance: KES ${activeLoan.amount}
1. Pay via M-PESA
2. Payment History
3. Back to Main Menu`;

                case "4":
                    const loans = await db.getActiveLoan(farmer.id);
                    if (!loans) {
                        return `END No active loans found.
                        
                        Apply for a loan from the main menu.`;
                    }

                    return `END Loan Status:
Amount: KES ${loans.amount}
Status: ${loans.status}
Next Payment: KES ${loans.monthly_payment}
Due Date: ${new Date(loans.updated_at).toLocaleDateString()}`;

                case "5":
                    session.session_data.level = 2;
                    session.session_data.menu = "profile";
                    await db.createOrUpdateSession(session.session_id, farmer.phone_number, session.session_data);

                    return `CON Update Farm Profile:
1. Farm Size
2. Years Farming
3. Main Crops
4. Back to Main Menu`;

                default:
                    return this.showMainMenu();
            }
        } catch (error) {
            console.error('Menu Error:', error);
            return 'END An error occurred. Please try again.';
        }
    }

    async handleSecondLevelMenu(text, farmer, session) {
        try {
            switch (session.session_data.menu) {
                case "loan":
                    return await this.handleLoanApplication(text, farmer, session);

                case "profile":
                    return await this.handleProfileUpdate(text, farmer, session);

                default:
                    return this.showMainMenu();
            }
        } catch (error) {
            console.error('Menu Error:', error);
            return 'END An error occurred. Please try again.';
        }
    }

    async handleLoanApplication(text, farmer, session) {
        const loanTypes = {
            "1": { name: "Farm Input Loan", max: 50000 },
            "2": { name: "Equipment Loan", max: 200000 },
            "3": { name: "Emergency Loan", max: 20000 }
        };

        const loanType = loanTypes[text];
        if (!loanType) return this.showMainMenu();

        try {
            const creditScore = await db.getLatestCreditScore(farmer.id);
            const loan = await db.createLoanApplication(
                farmer.id,
                loanType.max * 0.5, // Start with 50% of max amount
                12, // 12 months term
                creditScore.id
            );

            // Send SMS notification
            await this.sendSMS(farmer.phone_number,
                `Your FarmIQ ${loanType.name} application is being processed. Ref: ${loan.id}. Our agent will contact you within 24hrs.`);

            return `END Loan Application Submitted!
Type: ${loanType.name}
Reference: ${loan.id}
Maximum Amount: KES ${loanType.max}

We will contact you shortly.`;
        } catch (error) {
            console.error('Loan Application Error:', error);
            return 'END Loan application failed. Please try again later.';
        }
    }

    async handleProfileUpdate(text, farmer, session) {
        switch (text) {
            case "1":
                session.session_data.updating = 'farm_size';
                await db.createOrUpdateSession(session.session_id, farmer.phone_number, session.session_data);
                return `CON Enter farm size in acres:`;

            case "2":
                session.session_data.updating = 'years';
                await db.createOrUpdateSession(session.session_id, farmer.phone_number, session.session_data);
                return `CON Enter years of farming experience:`;

            case "3":
                return `CON Select main crop:
1. Maize
2. Coffee
3. Tea
4. Other`;

            case "4":
                return this.showMainMenu();

            default:
                // Handle actual updates
                if (session.session_data.updating) {
                    try {
                        const updates = {};
                        switch (session.session_data.updating) {
                            case 'farm_size':
                                updates.farm_size_acres = parseFloat(text);
                                break;
                            case 'years':
                                updates.years_farming = parseInt(text);
                                break;
                        }

                        await db.updateFarmerProfile(farmer.id, updates);

                        // Also update farm details
                        await db.updateFarmDetails(farmer.id, updates);

                        // Clear the updating flag
                        session.session_data.updating = null;
                        await db.createOrUpdateSession(session.session_id, farmer.phone_number, session.session_data);

                        return `END Profile updated successfully!`;
                    } catch (error) {
                        console.error('Profile Update Error:', error);
                        return 'END Update failed. Please try again.';
                    }
                }
                return this.showMainMenu();
        }
    }

    getRiskLevel(score) {
        if (score >= 700) return 'Low Risk';
        if (score >= 500) return 'Medium Risk';
        return 'High Risk';
    }

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