const { createClient } = require('@supabase/supabase-js');

class AIService {
    constructor() {
        this.supabase = createClient(config.url, config.serviceRoleKey);
    }

    async calculateCreditScore(farmerId) {
        try {
            const response = await this.supabase.functions.invoke('farmer_analytics', {
                body: {
                    action: 'calculate_credit_score',
                    farmerId: farmerId
                }
            });

            if (response.error) throw response.error;
            return response.data;
        } catch (error) {
            console.error('Credit Score Calculation Error:', error);
            throw error;
        }
    }

    async getLoanRecommendation(farmerId) {
        try {
            const response = await this.supabase.functions.invoke('farmer_analytics', {
                body: {
                    action: 'get_loan_recommendation',
                    farmerId: farmerId
                }
            });

            if (response.error) throw response.error;
            return response.data;
        } catch (error) {
            console.error('Loan Recommendation Error:', error);
            throw error;
        }
    }

    async updateFarmerProfile(farmerId, profileData) {
        try {
            // Update farmer profile in the database
            const { data: farmerDetails, error: farmerError } = await this.supabase
                .from('farm_details')
                .upsert({
                    farmer_id: farmerId,
                    ...profileData
                })
                .single();

            if (farmerError) throw farmerError;

            // Recalculate credit score with new profile data
            const creditScore = await this.calculateCreditScore(farmerId);

            return {
                farmerDetails,
                creditScore
            };
        } catch (error) {
            console.error('Profile Update Error:', error);
            throw error;
        }
    }

    async getAIAnalytics(farmerId) {
        try {
            // Get farmer's complete profile with credit history
            const { data: farmer, error } = await this.supabase
                .from('farmers')
                .select(`
                    *,
                    farm_details (*),
                    credit_scores (
                        score,
                        risk_level,
                        created_at
                    ),
                    loans (
                        amount,
                        status,
                        created_at
                    )
                `)
                .eq('id', farmerId)
                .single();

            if (error) throw error;

            // Get latest credit score and loan recommendation
            const [creditScore, loanRec] = await Promise.all([
                this.calculateCreditScore(farmerId),
                this.getLoanRecommendation(farmerId)
            ]);

            return {
                farmer,
                currentCreditScore: creditScore,
                loanRecommendation: loanRec,
                creditHistory: farmer.credit_scores,
                loanHistory: farmer.loans
            };
        } catch (error) {
            console.error('AI Analytics Error:', error);
            throw error;
        }
    }

    formatCreditScoreMessage(creditScore) {
            const riskLevels = {
                'low_risk': 'Low Risk - Excellent qualification for loans',
                'medium_risk': 'Medium Risk - Good qualification with some conditions',
                'high_risk': 'High Risk - Limited loan options available'
            };

            return `Credit Score: ${creditScore.score}
Risk Level: ${riskLevels[creditScore.risk_level]}
Key Factors:
${creditScore.factors.slice(0, 3).map(f => `- ${f.feature}: ${Math.round(f.importance * 100)}% impact`).join('\n')}`;
    }

    formatLoanRecommendationMessage(recommendation) {
        return `Loan Recommendation:
Maximum Amount: KES ${Math.round(recommendation.max_amount).toLocaleString()}
Recommended: KES ${Math.round(recommendation.recommended_amount).toLocaleString()}
Term: ${recommendation.term_months} months
Monthly Payment: KES ${Math.round(recommendation.monthly_payment).toLocaleString()}
Interest Rate: ${(recommendation.interest_rate * 100).toFixed(1)}%

Requirements:
${recommendation.requirements.map(r => `- ${r}`).join('\n')}`;
    }
}

module.exports = new AIService();