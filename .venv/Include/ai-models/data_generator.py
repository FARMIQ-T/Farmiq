try:
    import numpy as np
    import pandas as pd
    from sklearn.preprocessing import StandardScaler
except ImportError as e:
    if "sklearn" in str(e):
        print("Error: scikit-learn is not installed. Please install it using:")
        print("pip install scikit-learn")
        print("\nNote: While we install using 'scikit-learn', we import using 'sklearn'")
        exit(1)
    raise e

def generate_synthetic_farmer_data(n_samples=1000, random_state=42):
    """Generate synthetic farmer data for model training with enhanced risk factors."""
    np.random.seed(random_state)
    
    # Basic farm characteristics
    farm_size = np.random.lognormal(2, 1, n_samples)  # in acres
    years_farming = np.random.randint(1, 30, n_samples)
    
    # Crop and yield information
    n_crops = np.random.randint(1, 6, n_samples)  # number of different crops
    avg_yield = np.random.normal(4000, 1000, n_samples)  # kg per acre
    yield_consistency = np.random.uniform(0.6, 1.0, n_samples)
    
    # Weather resilience factors
    irrigation_score = np.random.uniform(0, 1, n_samples)
    drought_resistant_crops = np.random.randint(0, n_crops + 1, n_samples)
    soil_quality = np.random.uniform(0.3, 1.0, n_samples)
    
    # Financial indicators
    monthly_revenue = np.random.lognormal(10, 1, n_samples)
    expense_ratio = np.random.uniform(0.4, 0.9, n_samples)
    savings = np.random.lognormal(8, 2, n_samples)
    existing_loans = np.random.randint(0, 3, n_samples)
    repayment_history = np.random.uniform(0.7, 1.0, n_samples)
    seasonal_revenue_variation = np.random.uniform(0.1, 0.5, n_samples)
    market_access_score = np.random.uniform(0.3, 1.0, n_samples)
    value_chain_participation = np.random.uniform(0, 1, n_samples)
    
    # Training and support
    training_hours = np.random.randint(0, 100, n_samples)
    coop_membership_years = np.random.randint(0, 10, n_samples)
    advisory_visits = np.random.randint(0, 24, n_samples)
    
    # Create risk factors that influence creditworthiness
    risk_score = (
        0.2 * (farm_size / farm_size.max()) +
        0.15 * (years_farming / 30) +
        0.1 * (n_crops / 5) +
        0.1 * yield_consistency +
        0.1 * (1 - expense_ratio) +
        0.15 * repayment_history +
        0.1 * (training_hours / 100) +
        0.1 * (coop_membership_years / 10)
    )
    
    # Generate target variable (creditworthy) based on risk score
    creditworthy = (risk_score > np.percentile(risk_score, 70)).astype(int)
    
    # Combine into DataFrame
    df = pd.DataFrame({
        # Basic farm characteristics
        'farm_size_acres': farm_size,
        'years_farming': years_farming,
        'crop_diversity': n_crops,
        'yield_kg_per_acre': avg_yield,
        'yield_consistency': yield_consistency,
        
        # Weather resilience
        'irrigation_score': irrigation_score,
        'drought_resistant_crops': drought_resistant_crops,
        'soil_quality': soil_quality,
        
        # Financial health
        'monthly_revenue': monthly_revenue,
        'expense_ratio': expense_ratio,
        'savings_amount': savings,
        'existing_loans': existing_loans,
        'repayment_history': repayment_history,
        'seasonal_revenue_variation': seasonal_revenue_variation,
        
        # Market factors
        'market_access_score': market_access_score,
        'value_chain_participation': value_chain_participation,
        
        # Support network
        'training_hours': training_hours,
        'coop_membership_years': coop_membership_years,
        'advisory_visits': advisory_visits,
        
        'creditworthy': creditworthy
    })
    
    return df

if __name__ == "__main__":
    # Generate sample dataset
    df = generate_synthetic_farmer_data()
    df.to_csv("data/farmer_profiles.csv", index=False)
    print("Generated synthetic farmer profiles dataset with shape:", df.shape)