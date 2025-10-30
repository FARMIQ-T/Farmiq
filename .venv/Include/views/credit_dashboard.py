# views/credit_dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import shap
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

def simulate_weather_impact(base_score, irrigation_score, drought_resistant_crops, soil_quality):
    """Simulate impact of weather conditions on credit score."""
    drought_impact = 1.0 - (irrigation_score * 0.4 + (drought_resistant_crops/5) * 0.4 + soil_quality * 0.2)
    return max(0, min(1, base_score * (1 - drought_impact * st.session_state.weather_severity)))

def simulate_market_impact(base_score, market_access, value_chain_participation, seasonal_variation):
    """Simulate impact of market conditions on credit score."""
    market_shock = st.session_state.market_shock_severity * (
        0.5 * (1 - market_access) +
        0.3 * (1 - value_chain_participation) +
        0.2 * seasonal_variation
    )
    return max(0, min(1, base_score * (1 - market_shock)))

def calculate_loan_recommendation(credit_score, monthly_revenue, expense_ratio):
    """Calculate loan recommendations based on credit score and financial health."""
    max_monthly_payment = monthly_revenue * (1 - expense_ratio) * 0.5  # 50% of disposable income
    
    # Base calculations
    max_loan_amount = max_monthly_payment * 24  # 2-year term as baseline
    recommended_term = 24
    base_interest_rate = 0.15  # 15% base rate
    
    # Adjust based on credit score
    if credit_score >= 0.8:
        max_loan_amount *= 1.5
        base_interest_rate *= 0.8
    elif credit_score >= 0.6:
        max_loan_amount *= 1.2
        base_interest_rate *= 0.9
    else:
        max_loan_amount *= 0.8
        base_interest_rate *= 1.2
    
    return {
        'max_loan_amount': max_loan_amount,
        'recommended_term': recommended_term,
        'interest_rate': base_interest_rate,
        'monthly_payment': max_monthly_payment
    }

def render():
    """Render the Credit Scoring Dashboard with dynamic risk simulation."""
    
    # Initialize session state for simulation parameters
    if 'weather_severity' not in st.session_state:
        st.session_state.weather_severity = 0.0
    if 'market_shock_severity' not in st.session_state:
        st.session_state.market_shock_severity = 0.0

    # Resolve model path relative to this file (models are in .venv/Include/ai-models/models)
    base_dir = os.path.dirname(os.path.abspath(__file__))  # views directory
    ai_models_dir = os.path.join(os.path.dirname(base_dir), 'ai-models')  # Include/ai-models
    models_dir = os.path.join(ai_models_dir, 'models')  # Include/ai-models/models
    
    # Construct paths for model components
    model_path = os.path.join(models_dir, 'ensemble_latest.pkl')
    scaler_path = os.path.join(models_dir, 'scaler_latest.pkl')
    
    try:
        if not os.path.exists(models_dir):
            st.error(f"Models directory not found at: {models_dir}")
            st.info("Please run the model training script first: python ai-models/enhanced_credit_scoring.py")
            return
            
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
    except Exception as e:
        st.error(f"Failed to load model components from {models_dir}: {e}")
        st.info("Make sure you have trained the model and the files exist in ai-models/models/")
        return

    # Create tabs for different sections
    tabs = st.tabs(["Basic Assessment", "Risk Simulation", "Loan Recommendation"])
    
    with tabs[0]:
        st.subheader("Farmer Profile")
        col1, col2 = st.columns(2)
        
        with col1:
            # Farm characteristics
            farm_size = st.number_input("Farm Size (acres)", 0.1, 100.0, 5.0)
            years_farming = st.number_input("Years Farming", 0, 50, 5)
            crop_diversity = st.slider("Number of Crops", 1, 10, 3)
            
            # Production metrics
            yield_kg = st.number_input("Average Yield (kg/acre)", 100, 10000, 4000)
            yield_consistency = st.slider("Yield Consistency", 0.0, 1.0, 0.8)
            
        with col2:
            # Financial indicators
            monthly_revenue = st.number_input("Monthly Revenue (KES)", 1000, 1000000, 50000)
            expense_ratio = st.slider("Expense Ratio", 0.0, 1.0, 0.6)
            existing_loans = st.number_input("Existing Loans", 0, 5, 0)
            
            # Support network
            training_hours = st.slider("Training Hours", 0, 100, 20)
            coop_years = st.slider("Years in Cooperative", 0, 20, 2)
    
    with tabs[1]:
        st.subheader("Risk Simulation")
        
        # Weather risk factors
        st.write("Weather Risk Factors")
        weather_col1, weather_col2 = st.columns(2)
        with weather_col1:
            irrigation_score = st.slider("Irrigation Coverage", 0.0, 1.0, 0.5)
            drought_resistant = st.slider("Drought-Resistant Crops", 0, crop_diversity, 1)
        with weather_col2:
            soil_quality = st.slider("Soil Quality", 0.0, 1.0, 0.7)
            st.session_state.weather_severity = st.slider("Simulate Drought Severity", 0.0, 1.0, 0.0)
        
        # Market risk factors
        st.write("Market Risk Factors")
        market_col1, market_col2 = st.columns(2)
        with market_col1:
            market_access = st.slider("Market Access Score", 0.0, 1.0, 0.6)
            value_chain = st.slider("Value Chain Integration", 0.0, 1.0, 0.4)
        with market_col2:
            seasonal_variation = st.slider("Seasonal Revenue Variation", 0.0, 1.0, 0.3)
            st.session_state.market_shock_severity = st.slider("Simulate Market Shock", 0.0, 1.0, 0.0)
    
    # Prepare raw feature vector
    raw_data = pd.DataFrame([{
        'farm_size_acres': farm_size,
        'years_farming': years_farming,
        'crop_diversity': crop_diversity,
        'yield_kg_per_acre': yield_kg,
        'yield_consistency': yield_consistency,
        'advisory_visits': 10,  # Default value since not collected in UI
        'monthly_revenue': monthly_revenue,
        'expense_ratio': expense_ratio,
        'training_hours': training_hours,
        'coop_membership_years': coop_years
    }])
    
    # Engineer features to match training data
    X = pd.DataFrame()
    
    # Basic features
    X['farm_size_acres'] = raw_data['farm_size_acres']
    X['years_farming'] = raw_data['years_farming']
    X['crop_diversity'] = raw_data['crop_diversity']
    X['monthly_revenue'] = raw_data['monthly_revenue']
    X['expense_ratio'] = raw_data['expense_ratio']
    X['training_hours'] = raw_data['training_hours']
    X['coop_membership_years'] = raw_data['coop_membership_years']
    
    # Engineered features
    X['revenue_per_acre'] = raw_data['monthly_revenue'] / raw_data['farm_size_acres']
    X['yield_value'] = raw_data['yield_kg_per_acre'] * raw_data['yield_consistency']
    
    # Knowledge score
    X['knowledge_score'] = (
        0.4 * raw_data['years_farming'] / raw_data['years_farming'].max() +
        0.3 * raw_data['training_hours'] / raw_data['training_hours'].max() +
        0.3 * raw_data['advisory_visits'] / raw_data['advisory_visits'].max()
    )
    
    # Risk assessment
    X['revenue_stability'] = raw_data['yield_consistency'] * (1 - raw_data['expense_ratio'])
    X['debt_service_ratio'] = np.minimum(
        raw_data['monthly_revenue'] * 0.5,
        raw_data['monthly_revenue'] - raw_data['expense_ratio'] * raw_data['monthly_revenue']
    )
    
    # Support network score
    X['support_score'] = (
        raw_data['coop_membership_years'] / raw_data['coop_membership_years'].max() +
        raw_data['advisory_visits'] / raw_data['advisory_visits'].max()
    ) / 2

    try:
        # Get base credit score with proper feature names
        X_scaled = pd.DataFrame(
            scaler.transform(X),
            columns=X.columns,
            index=X.index
        )
        base_score = model.predict_proba(X_scaled)[0][1]
        
        # Apply risk simulations
        weather_adjusted_score = simulate_weather_impact(
            base_score, irrigation_score, drought_resistant, soil_quality)
        final_score = simulate_market_impact(
            weather_adjusted_score, market_access, value_chain, seasonal_variation)
        
        # Display scores
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Base Credit Score", f"{base_score:.2f}")
        with col2:
            st.metric("Weather-Adjusted Score", f"{weather_adjusted_score:.2f}", 
                     f"{(weather_adjusted_score - base_score):.3f}")
        with col3:
            st.metric("Final Score (with Market Impact)", f"{final_score:.2f}", 
                     f"{(final_score - weather_adjusted_score):.3f}")
        
        # Loan recommendations
        with tabs[2]:
            st.subheader("Loan Recommendations")
            loan_rec = calculate_loan_recommendation(final_score, monthly_revenue, expense_ratio)
            
            loan_col1, loan_col2 = st.columns(2)
            with loan_col1:
                st.metric("Maximum Loan Amount", f"KES {loan_rec['max_loan_amount']:,.0f}")
                st.metric("Recommended Term", f"{loan_rec['recommended_term']} months")
            with loan_col2:
                st.metric("Interest Rate", f"{loan_rec['interest_rate']:.1%}")
                st.metric("Maximum Monthly Payment", f"KES {loan_rec['monthly_payment']:,.0f}")
            
            # Loan simulation
            st.subheader("Loan Simulation")
            loan_amount = st.slider("Loan Amount", 0, int(loan_rec['max_loan_amount']), 
                                 int(loan_rec['max_loan_amount']/2))
            loan_term = st.slider("Loan Term (months)", 6, 36, loan_rec['recommended_term'])
            
            # Calculate payment schedule
            payment_schedule = []
            monthly_payment = (loan_amount * (1 + loan_rec['interest_rate'])) / loan_term
            
            for month in range(1, loan_term + 1):
                payment_schedule.append({
                    'Month': month,
                    'Payment': monthly_payment,
                    'Remaining Balance': max(0, loan_amount - (monthly_payment * month))
                })
            
            df_schedule = pd.DataFrame(payment_schedule)
            
            # Plot payment schedule
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_schedule['Month'], y=df_schedule['Remaining Balance'],
                                   name='Remaining Balance'))
            fig.add_trace(go.Bar(x=df_schedule['Month'], y=df_schedule['Payment'],
                               name='Monthly Payment'))
            fig.update_layout(title='Loan Amortization Schedule',
                            xaxis_title='Month',
                            yaxis_title='Amount (KES)')
            st.plotly_chart(fig, width="stretch")  # Updated from use_container_width
            
        # SHAP explanation
        if st.checkbox("Show Feature Impact Analysis"):
            try:
                # Use the Gradient Boosting model directly for SHAP explanations
                base_model = model.named_estimators_['gb']
                explainer = shap.TreeExplainer(base_model)
                
                # Ensure feature names are preserved for SHAP analysis
                shap_values = explainer.shap_values(X_scaled)
                
                st.subheader("Feature Impact")
                
                # Create and display a bar plot of feature importances
                importance_df = pd.DataFrame({
                    'Feature': X.columns,
                    'Importance': np.abs(shap_values).mean(axis=0)
                }).sort_values('Importance', ascending=True)
                
                fig = go.Figure(go.Bar(
                    x=importance_df['Importance'],
                    y=importance_df['Feature'],
                    orientation='h'
                ))
                fig.update_layout(
                    title='Feature Importance (SHAP values)',
                    xaxis_title='SHAP Value (absolute)',
                    yaxis_title='Feature'
                )
                st.plotly_chart(fig, width="stretch")
            except Exception as e:
                st.warning(f"SHAP explanation unavailable: {e}")
                
    except Exception as e:
        st.error(f"Prediction failed: {e}")
        st.info("Please check the input values and try again.")


if __name__ == "__main__":
    render()
