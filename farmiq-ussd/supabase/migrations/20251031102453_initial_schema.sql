-- Use pgcrypto for UUID generation (gen_random_uuid)
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS farmers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone_number TEXT,
    location TEXT,
    years_farming INTEGER,
    education_level TEXT,
    training_hours INTEGER DEFAULT 0,
    coop_member BOOLEAN DEFAULT false,
    coop_membership_years INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS farms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    farmer_id UUID REFERENCES farmers(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    farm_size DECIMAL NOT NULL,
    soil_type TEXT,
    irrigation_score DECIMAL DEFAULT 0,
    soil_quality_score DECIMAL DEFAULT 0,
    location TEXT,
    land_ownership TEXT,
    certification TEXT[]
);

CREATE TABLE IF NOT EXISTS crops (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    farm_id UUID REFERENCES farms(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    crop_name TEXT NOT NULL,
    variety TEXT,
    planting_date DATE,
    expected_harvest_date DATE,
    actual_harvest_date DATE,
    expected_yield DECIMAL,
    actual_yield DECIMAL,
    area_planted DECIMAL,
    season TEXT,
    drought_resistant BOOLEAN DEFAULT false,
    status TEXT
);

CREATE TABLE IF NOT EXISTS financial_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    farmer_id UUID REFERENCES farmers(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    record_date DATE NOT NULL,
    transaction_type TEXT NOT NULL,
    amount DECIMAL NOT NULL,
    description TEXT,
    category TEXT,
    payment_method TEXT,
    related_crop_id UUID REFERENCES crops(id)
);

CREATE TABLE IF NOT EXISTS resources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    farm_id UUID REFERENCES farms(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    resource_type TEXT NOT NULL,
    name TEXT NOT NULL,
    quantity DECIMAL,
    unit TEXT,
    status TEXT,
    purchase_date DATE,
    purchase_price DECIMAL,
    current_value DECIMAL
);

CREATE TABLE IF NOT EXISTS credit_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    farmer_id UUID REFERENCES farmers(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    score DECIMAL NOT NULL,
    risk_score DECIMAL,
    credit_limit DECIMAL,
    score_date DATE NOT NULL,
    model_version TEXT,
    factors JSONB,
    status TEXT
);

CREATE TABLE IF NOT EXISTS loans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    farmer_id UUID REFERENCES farmers(id),
    credit_score_id UUID REFERENCES credit_scores(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    amount DECIMAL NOT NULL,
    interest_rate DECIMAL NOT NULL,
    term_months INTEGER NOT NULL,
    status TEXT NOT NULL,
    purpose TEXT,
    disbursement_date DATE,
    last_payment_date DATE,
    next_payment_date DATE,
    remaining_balance DECIMAL
);

-- Create triggers for updating timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = TIMEZONE('utc'::text, NOW());
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add triggers to all tables
CREATE TRIGGER update_farmers_updated_at
    BEFORE UPDATE ON farmers
    FOR EACH ROW
    EXECUTE PROCEDURE update_updated_at_column();

CREATE TRIGGER update_farms_updated_at
    BEFORE UPDATE ON farms
    FOR EACH ROW
    EXECUTE PROCEDURE update_updated_at_column();

CREATE TRIGGER update_crops_updated_at
    BEFORE UPDATE ON crops
    FOR EACH ROW
    EXECUTE PROCEDURE update_updated_at_column();

CREATE TRIGGER update_financial_records_updated_at
    BEFORE UPDATE ON financial_records
    FOR EACH ROW
    EXECUTE PROCEDURE update_updated_at_column();

CREATE TRIGGER update_resources_updated_at
    BEFORE UPDATE ON resources
    FOR EACH ROW
    EXECUTE PROCEDURE update_updated_at_column();

CREATE TRIGGER update_credit_scores_updated_at
    BEFORE UPDATE ON credit_scores
    FOR EACH ROW
    EXECUTE PROCEDURE update_updated_at_column();

CREATE TRIGGER update_loans_updated_at
    BEFORE UPDATE ON loans
    FOR EACH ROW
    EXECUTE PROCEDURE update_updated_at_column();

-- Create indices for better query performance
CREATE INDEX idx_farmers_id ON farmers(id);
CREATE INDEX idx_farms_farmer_id ON farms(farmer_id);
CREATE INDEX idx_crops_farm_id ON crops(farm_id);
CREATE INDEX idx_financial_records_farmer_id ON financial_records(farmer_id);
CREATE INDEX idx_resources_farm_id ON resources(farm_id);
CREATE INDEX idx_credit_scores_farmer_id ON credit_scores(farmer_id);
CREATE INDEX idx_loans_farmer_id ON loans(farmer_id);