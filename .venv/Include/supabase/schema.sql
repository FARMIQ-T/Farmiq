-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Farmers table
CREATE TABLE farmers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    national_id VARCHAR(20) UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    farm_size_acres DECIMAL NOT NULL,
    years_farming INTEGER NOT NULL,
    location JSON,  -- Store coordinates or region info
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Farm details table (one-to-one with farmers)
CREATE TABLE farm_details (
    farmer_id UUID PRIMARY KEY REFERENCES farmers(id),
    crop_diversity INTEGER NOT NULL,
    yield_kg_per_acre DECIMAL,
    yield_consistency DECIMAL,
    monthly_revenue DECIMAL,
    expense_ratio DECIMAL,
    cooperative_member BOOLEAN DEFAULT FALSE,
    coop_membership_years INTEGER DEFAULT 0,
    training_hours INTEGER DEFAULT 0,
    advisory_visits INTEGER DEFAULT 0,
    last_assessment_date TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Credit scores table (historical tracking)
CREATE TABLE credit_scores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farmer_id UUID REFERENCES farmers(id),
    score DECIMAL NOT NULL,
    risk_assessment JSON,  -- Store detailed risk factors
    feature_importance JSON,  -- Store SHAP values
    model_version VARCHAR(50),  -- Track which model version made the prediction
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Loans table
CREATE TABLE loans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farmer_id UUID REFERENCES farmers(id),
    amount DECIMAL NOT NULL,
    term_months INTEGER NOT NULL,
    interest_rate DECIMAL NOT NULL,
    monthly_payment DECIMAL NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',  -- pending, active, completed, defaulted
    credit_score_id UUID REFERENCES credit_scores(id),
    approved_at TIMESTAMPTZ,
    disbursed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Loan payments tracking
CREATE TABLE loan_payments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    loan_id UUID REFERENCES loans(id),
    amount DECIMAL NOT NULL,
    payment_date TIMESTAMPTZ NOT NULL,
    payment_method VARCHAR(50),
    transaction_reference VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- USSD sessions table
CREATE TABLE ussd_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    farmer_id UUID REFERENCES farmers(id),
    session_data JSON,  -- Store session state
    last_menu_shown VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for better query performance
CREATE INDEX idx_farmers_phone ON farmers(phone_number);
CREATE INDEX idx_loans_farmer ON loans(farmer_id);
CREATE INDEX idx_loans_status ON loans(status);
CREATE INDEX idx_credit_scores_farmer ON credit_scores(farmer_id);
CREATE INDEX idx_ussd_sessions_phone ON ussd_sessions(phone_number);

-- Add triggers for updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_farmers_updated_at
    BEFORE UPDATE ON farmers
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_farm_details_updated_at
    BEFORE UPDATE ON farm_details
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_loans_updated_at
    BEFORE UPDATE ON loans
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ussd_sessions_updated_at
    BEFORE UPDATE ON ussd_sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Row Level Security (RLS) policies
ALTER TABLE farmers ENABLE ROW LEVEL SECURITY;
ALTER TABLE farm_details ENABLE ROW LEVEL SECURITY;
ALTER TABLE credit_scores ENABLE ROW LEVEL SECURITY;
ALTER TABLE loans ENABLE ROW LEVEL SECURITY;
ALTER TABLE loan_payments ENABLE ROW LEVEL SECURITY;
ALTER TABLE ussd_sessions ENABLE ROW LEVEL SECURITY;

-- Example RLS policy (customize based on your auth needs)
CREATE POLICY "Farmers are viewable by authenticated users only"
ON farmers FOR SELECT
TO authenticated
USING (true);

-- Functions for USSD integration
CREATE OR REPLACE FUNCTION get_or_create_session(
    p_session_id VARCHAR,
    p_phone_number VARCHAR
) RETURNS UUID AS $$
DECLARE
    v_session_id UUID;
BEGIN
    -- Try to find existing session
    SELECT id INTO v_session_id
    FROM ussd_sessions
    WHERE session_id = p_session_id;
    
    -- Create new session if not found
    IF v_session_id IS NULL THEN
        INSERT INTO ussd_sessions (session_id, phone_number, session_data)
        VALUES (p_session_id, p_phone_number, '{"step": "start"}')
        RETURNING id INTO v_session_id;
    END IF;
    
    RETURN v_session_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;