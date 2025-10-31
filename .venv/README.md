# Farm Intelligent Farming Management System

## Overview
FarmIQ is an integrated farming management system that combines Streamlit for the user interface, Supabase for data persistence, and AI models for credit scoring and risk assessment. The system helps farmers manage their operations, track resources, and access financial services through data-driven decisions.

## Architecture Components

### 1. Database Layer (Supabase)
- **Core Tables**:
  - `farmers`: Farmer profiles and demographics
  - `farms`: Farm details and soil characteristics
  - `crops`: Crop planning and harvest tracking
  - `financial_records`: Transaction history
  - `resources`: Farm equipment and resources
  - `credit_scores`: AI-generated credit assessments
  - `loans`: Loan management and tracking

### 2. Streamlit Applications
- **Farmer Dashboard**: Self-service portal for farmers
  - Farm management
  - Crop tracking
  - Financial record keeping
  - Loan applications
- **Admin Dashboard**: System management interface
  - User management
  - Credit score monitoring
  - Loan approval workflow
- **Support Dashboard**: Customer service interface
  - Farmer assistance
  - Issue tracking
  - Resource allocation
- **Agent Dashboard**: Field agent interface
  - Farm visits
  - Data collection
  - Resource distribution

### 3. AI Model Integration
- **Credit Scoring Engine**:
  - Ensemble model combining:
    - Gradient Boosting
    - Random Forest
    - Logistic Regression
  - Feature engineering for:
    - Farm performance metrics
    - Financial behavior patterns
    - Resource utilization
    - Crop yield predictions
- **Bias Mitigation**:
  - Fairness-aware model training
  - Regular bias audits
  - Diverse training data representation

## Technical Stack

### Python Environment
- Python 3.8+
- Key Dependencies:
  - `streamlit`: Web interface
  - `supabase`: Database operations
  - `scikit-learn`: ML models
  - `pandas`: Data processing
  - `numpy`: Numerical operations
  - `feature-engine`: Feature engineering
  - `shap`: Model explainability

### Database
- Supabase (PostgreSQL)
- Extensions:
  - pgcrypto (UUID generation)
  - PostGIS (location data)

### ML Pipeline
- Automated feature engineering
- Model versioning
- Regular retraining via cron jobs
- Performance monitoring

## Getting Started

1. **Environment Setup**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\Activate.ps1 # Windows
pip install -r requirements.txt
```

2. **Database Initialization**
```bash
npx supabase start
npx supabase db reset
```

3. **Running the Application**
```bash
streamlit run streamlit_app.py
```

## Project Structure
```
farmiq/
├── streamlit_app.py         # Main Streamlit entry
├── services/
│   ├── database_service.py  # Supabase integration
│   └── ai_service.py        # ML model operations
├── models/
│   ├── credit_scoring.py    # Credit score prediction
│   └── feature_engine.py    # Feature engineering
├── views/
│   ├── farmer_dashboard.py  # Farmer interface
│   ├── admin_dashboard.py   # Admin interface
│   └── support_dashboard.py # Support interface
└── utils/
    ├── data_validation.py   # Input validation
    └── metrics.py          # Performance tracking
```

## Documentation
- [Database Schema](database_docs.md)
- [ML Model Documentation](ml_model_docs.md)
- [API Documentation](api_docs.md)

## Security
- Supabase authentication
- Row-level security policies
- Encrypted sensitive data
- Regular security audits

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details
