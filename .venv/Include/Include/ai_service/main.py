from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np
from typing import Dict, Optional
import os
from enhanced_credit_scoring import CreditScoringModel

app = FastAPI(title="FarmIQ Credit Scoring API")

# Load models
model_path = "models/credit_ensemble.pkl"
scaler_path = "models/scaler.pkl"

try:
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
except Exception as e:
    print(f"Error loading models: {e}")
    print("Models will be loaded when available.")
    model = None
    scaler = None

class FarmerProfile(BaseModel):
    farm_size_acres: float = Field(..., gt=0, description="Farm size in acres")
    years_farming: int = Field(..., ge=0, description="Years of farming experience")
    crop_diversity: int = Field(..., ge=1, le=10, description="Number of different crops")
    yield_kg_per_acre: float = Field(..., gt=0, description="Average yield in kg per acre")
    yield_consistency: float = Field(..., ge=0, le=1, description="Consistency of yields")
    monthly_revenue: float = Field(..., ge=0, description="Monthly revenue")
    expense_ratio: float = Field(..., ge=0, le=1, description="Ratio of expenses to revenue")
    existing_loans: int = Field(..., ge=0, description="Number of existing loans")
    repayment_history: float = Field(..., ge=0, le=1, description="Loan repayment history score")
    training_hours: int = Field(..., ge=0, description="Hours of agricultural training")
    coop_membership_years: int = Field(..., ge=0, description="Years as cooperative member")
    advisory_visits: int = Field(..., ge=0, description="Number of advisory visits received")

class LoanRequest(BaseModel):
    farmer: FarmerProfile
    loan_amount: float = Field(..., gt=0, description="Requested loan amount")
    loan_term_months: int = Field(..., gt=0, description="Requested loan term in months")

class CreditDecision(BaseModel):
    approved: bool
    credit_score: float
    max_loan_amount: Optional[float]
    recommended_term_months: Optional[int]
    risk_assessment: Dict[str, float]
    explanation: Dict[str, float]

@app.post("/predict/credit-score", response_model=CreditDecision)
async def predict_credit_score(farmer: FarmerProfile):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Create feature vector
    farmer_dict = farmer.dict()
    credit_model = CreditScoringModel()
    prediction = credit_model.predict(farmer_dict)
    
    # Calculate max loan amount based on monthly revenue and credit score
    max_loan = (
        farmer.monthly_revenue * 12 * prediction['probability'] 
        if prediction['probability'] >= 0.7 else 0
    )
    
    # Risk assessment based on key factors
    risk_assessment = {
        "revenue_risk": 1 - farmer.yield_consistency,
        "debt_risk": 0.2 * farmer.existing_loans,
        "experience_risk": np.exp(-farmer.years_farming/10),
        "diversification_risk": 1 - (farmer.crop_diversity / 10)
    }
    
    # Get feature importance for explanation
    feature_importance = dict(zip(
        prediction['feature_names'],
        np.abs(prediction['shap_values'][0]) / sum(np.abs(prediction['shap_values'][0]))
    ))
    
    return CreditDecision(
        approved=prediction['approved'],
        credit_score=prediction['probability'],
        max_loan_amount=max_loan if prediction['approved'] else 0,
        recommended_term_months=24 if prediction['approved'] else None,
        risk_assessment=risk_assessment,
        explanation=feature_importance
    )

@app.post("/simulate/loan")
async def simulate_loan(request: LoanRequest):
    """Simulate loan scenarios and provide recommendations."""
    farmer_score = await predict_credit_score(request.farmer)
    
    if not farmer_score.approved:
        return {
            "approved": False,
            "reason": "Credit score below threshold",
            "recommendations": [
                "Consider increasing crop diversity",
                "Participate in more training sessions",
                "Build positive repayment history with smaller loans"
            ]
        }
    
    # Calculate monthly payment
    interest_rate = 0.15  # 15% annual interest rate
    monthly_rate = interest_rate / 12
    monthly_payment = (
        request.loan_amount * monthly_rate * (1 + monthly_rate)**request.loan_term_months
    ) / ((1 + monthly_rate)**request.loan_term_months - 1)
    
    # Check if monthly payment is sustainable
    payment_to_revenue_ratio = monthly_payment / request.farmer.monthly_revenue
    
    if payment_to_revenue_ratio > 0.5:
        return {
            "approved": False,
            "reason": "Monthly payment too high relative to revenue",
            "recommendations": [
                f"Consider a smaller loan amount (max: {farmer_score.max_loan_amount})",
                f"Consider a longer term (recommend: {farmer_score.recommended_term_months} months)",
                "Work on increasing monthly revenue"
            ]
        }
    
    return {
        "approved": True,
        "loan_details": {
            "amount": request.loan_amount,
            "term_months": request.loan_term_months,
            "monthly_payment": monthly_payment,
            "total_repayment": monthly_payment * request.loan_term_months,
            "payment_to_revenue_ratio": payment_to_revenue_ratio
        },
        "risk_assessment": farmer_score.risk_assessment
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)