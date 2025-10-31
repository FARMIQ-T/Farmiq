const supabase = require('../config/supabase');

class DatabaseService {
    // Session Management
    async createOrUpdateSession(sessionId, phoneNumber, sessionData) {
        const { data: existingSession } = await supabase
            .from('ussd_sessions')
            .select('id')
            .eq('session_id', sessionId)
            .single();

        if (existingSession) {
            const { data, error } = await supabase
                .from('ussd_sessions')
                .update({
                    session_data: sessionData,
                    updated_at: new Date().toISOString()
                })
                .eq('session_id', sessionId)
                .select()
                .single();

            if (error) throw error;
            return data;
        }

        const { data, error } = await supabase
            .from('ussd_sessions')
            .insert([{
                session_id: sessionId,
                phone_number: phoneNumber,
                session_data: sessionData
            }])
            .select()
            .single();

        if (error) throw error;
        return data;
    }

    // Farmer Management
    async getOrCreateFarmer(phoneNumber) {
        const { data: existingFarmer } = await supabase
            .from('farmers')
            .select('*')
            .eq('phone_number', phoneNumber)
            .single();

        if (existingFarmer) return existingFarmer;

        const { data, error } = await supabase
            .from('farmers')
            .insert([{
                phone_number: phoneNumber,
                // Set default values
                farm_size_acres: 0,
                years_farming: 0
            }])
            .select()
            .single();

        if (error) throw error;
        return data;
    }

    async updateFarmerProfile(farmerId, updates) {
        const { data, error } = await supabase
            .from('farmers')
            .update(updates)
            .eq('id', farmerId)
            .select()
            .single();

        if (error) throw error;
        return data;
    }

    // Credit Score Management
    async getLatestCreditScore(farmerId) {
        const { data, error } = await supabase
            .from('credit_scores')
            .select('*')
            .eq('farmer_id', farmerId)
            .order('created_at', { ascending: false })
            .limit(1)
            .single();

        if (error && error.code !== 'PGRST116') throw error;
        return data;
    }

    async createCreditScore(farmerId, score, riskAssessment) {
        const { data, error } = await supabase
            .from('credit_scores')
            .insert([{
                farmer_id: farmerId,
                score,
                risk_assessment: riskAssessment,
                model_version: '1.0'
            }])
            .select()
            .single();

        if (error) throw error;
        return data;
    }

    // Loan Management
    async getActiveLoan(farmerId) {
        const { data, error } = await supabase
            .from('loans')
            .select('*')
            .eq('farmer_id', farmerId)
            .eq('status', 'active')
            .single();

        if (error && error.code !== 'PGRST116') throw error;
        return data;
    }

    async createLoanApplication(farmerId, amount, termMonths, creditScoreId) {
        const { data, error } = await supabase
            .from('loans')
            .insert([{
                farmer_id: farmerId,
                amount,
                term_months: termMonths,
                interest_rate: 15, // Example fixed rate
                monthly_payment: amount * (1.15 / termMonths), // Simple calculation
                status: 'pending',
                credit_score_id: creditScoreId
            }])
            .select()
            .single();

        if (error) throw error;
        return data;
    }

    async recordLoanPayment(loanId, amount, paymentMethod, transactionRef) {
        const { data, error } = await supabase
            .from('loan_payments')
            .insert([{
                loan_id: loanId,
                amount,
                payment_method: paymentMethod,
                transaction_reference: transactionRef,
                payment_date: new Date().toISOString()
            }])
            .select()
            .single();

        if (error) throw error;
        return data;
    }

    // Farm Details Management
    async updateFarmDetails(farmerId, details) {
        const { data: existing } = await supabase
            .from('farm_details')
            .select('farmer_id')
            .eq('farmer_id', farmerId)
            .single();

        if (existing) {
            const { data, error } = await supabase
                .from('farm_details')
                .update(details)
                .eq('farmer_id', farmerId)
                .select()
                .single();

            if (error) throw error;
            return data;
        }

        const { data, error } = await supabase
            .from('farm_details')
            .insert([{ farmer_id: farmerId, ...details }])
            .select()
            .single();

        if (error) throw error;
        return data;
    }
}

module.exports = new DatabaseService();