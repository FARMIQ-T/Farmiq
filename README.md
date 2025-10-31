# FarmIQ
AI4S - Intelligent Farming Management System

## Project Overview
FarmIQ is a comprehensive farming management system that combines web and USSD interfaces to serve both smartphone and basic feature phone users. The system integrates AI-powered credit scoring, Supabase for data persistence, and multiple access channels (Streamlit web apps and USSD) to provide inclusive access to farming management and financial services.

## System Architecture

### 1. Access Channels

#### Web Interface (Python + Streamlit)
- **Farmer Dashboard**: Self-service portal for farm management and loans
- **Admin Dashboard**: System management and credit monitoring
- **Support Dashboard**: Customer service and issue tracking
- **Agent Dashboard**: Field operations and data collection

#### USSD Interface (Node.js + Africa's Talking)
- Basic phone access to FarmIQ services
- Interactive menu system
- Multi-language support
- Offline-capable operations
- Session management for poor connectivity

### 2. Core Services

#### AI Services
- **Credit Scoring Engine**:
  - Ensemble model (Gradient Boosting, Random Forest, Logistic Regression)
  - Feature engineering for farm metrics
  - Bias mitigation and fairness
  - Regular model retraining

#### Database Layer (Supabase)
- Real-time data synchronization
- Row-level security
- Core Tables:
  - `farmers`: Profiles and demographics
  - `farms`: Farm characteristics
  - `crops`: Planning and harvests
  - `financial_records`: Transactions
  - `resources`: Equipment tracking
  - `credit_scores`: AI assessments
  - `loans`: Financial services

## Technical Stack

### Web Application (Python)
- **Framework**: Streamlit
- **Environment**: Python 3.8+
- **Key Libraries**:
  - streamlit: UI components
  - scikit-learn: ML models
  - pandas/numpy: Data processing
  - feature-engine: Feature engineering
  - shap: Model explainability

### USSD Service (Node.js)
- **Framework**: Express.js v5.1.0
- **Environment**: Node.js v16+
- **Key Dependencies**:
  - africastalking: USSD handling
  - @supabase/supabase-js: Database
  - jsonwebtoken: Authentication
  - swagger-jsdoc: API documentation

### Database & Infrastructure
- **Supabase**: PostgreSQL + Real-time
- **Extensions**:
  - pgcrypto: UUID generation
  - PostGIS: Location data

## Project Structure
```
farmiq/
├── farmiq-ussd/                # USSD Service
│   ├── index.js                # USSD entry point
│   ├── routes/                 # API routes
│   │   ├── routes.js
│   │   └── ussd.js
│   ├── services/              # Business logic
│   │   ├── aiService.js
│   │   ├── databaseService.js
│   │   └── ussdService.js
│   └── supabase/              # Database
│       └── migrations/        # Schema updates
│
├── streamlit_app.py           # Web app entry
├── services/                  # Python services
│   ├── database_service.py    # Supabase integration
│   └── ai_service.py         # ML operations
├── models/                    # AI models
│   ├── credit_scoring.py
│   └── feature_engine.py
└── views/                     # Web interfaces
    ├── farmer_dashboard.py
    ├── admin_dashboard.py
    └── support_dashboard.py
```

## Getting Started

### 1. Prerequisites
- Python 3.8+
- Node.js v16+
- Supabase CLI
- Africa's Talking account

### 2. Web Application Setup
```bash
# Python environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate   # Linux/Mac
pip install -r requirements.txt

# Start web app
streamlit run streamlit_app.py
```

### 3. USSD Service Setup
```bash
# Node.js setup
cd farmiq-ussd
npm install

# Configure environment
cp .env.example .env
# Edit .env with your keys

# Start USSD service
npm start
```

### 4. Database Setup
```bash
npx supabase start
npx supabase db reset
```

## Key Features

### Web Interface
- Interactive dashboards
- Real-time data updates
- Credit score visualization
- Resource management
- Loan application processing

### USSD Interface
- Basic phone access
- Registration and authentication
- Farm status checks
- Loan applications
- Credit score queries
- Resource requests

### AI Components
- Credit risk assessment
- Yield predictions
- Resource optimization
- Bias-aware modeling
- Regular retraining

## Documentation
- [Database Schema](database_docs.md)
- [ML Model Documentation](ml_model_docs.md)
- [API Documentation](api_docs.md)
- [USSD Flow](ussd_docs.md)

## Security
- JWT authentication
- Supabase RLS policies
- Encrypted sensitive data
- Rate limiting
- Regular security audits

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details

## Authors
- Emmanuel Keter (USSD Service)
- FarmIQ Team (Web Application & AI)
