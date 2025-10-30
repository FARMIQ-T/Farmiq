import pytest
import pandas as pd
import numpy as np
from train_credit_model import DynamicCreditScorer
import os
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_supabase_data():
    """Create mock data for testing"""
    farmers = pd.DataFrame({
        'farmer_id': range(1, 101),
        'age': np.random.randint(18, 80, 100),
        'location': np.random.choice(['Nyeri', 'Kiambu', 'Thika'], 100),
        'years_farming': np.random.randint(1, 30, 100)
    })
    
    loans = pd.DataFrame({
        'farmer_id': range(1, 101),
        'loan_amount': np.random.uniform(1000, 50000, 100),
        'repayment_period': np.random.randint(6, 24, 100),
        'purpose': np.random.choice(['Equipment', 'Seeds', 'Fertilizer'], 100)
    })
    
    transactions = pd.DataFrame({
        'farmer_id': range(1, 101),
        'amount': np.random.uniform(100, 5000, 100),
        'type': np.random.choice(['Deposit', 'Withdrawal'], 100),
        'status': np.random.choice(['Completed', 'Pending'], 100)
    })
    
    credit_scores = pd.DataFrame({
        'farmer_id': range(1, 101),
        'credit_score': np.random.randint(300, 850, 100),
        'risk_level': np.random.choice(['Low', 'Medium', 'High'], 100)
    })
    
    return {
        'farmers': farmers,
        'loans': loans,
        'transactions': transactions,
        'credit_scores': credit_scores
    }

@pytest.fixture
def mock_scorer(mock_supabase_data):
    """Create a mock DynamicCreditScorer instance"""
    with patch('train_credit_model.create_client') as mock_client:
        # Mock Supabase responses
        mock_response = MagicMock()
        for table_name, data in mock_supabase_data.items():
            mock_response.table(table_name).select('*').execute.return_value.data = data.to_dict('records')
        
        mock_client.return_value = mock_response
        
        scorer = DynamicCreditScorer(
            supabase_url='mock_url',
            supabase_key='mock_key'
        )
        return scorer

def test_fetch_data(mock_scorer, mock_supabase_data):
    """Test data fetching from Supabase"""
    df = mock_scorer.fetch_data()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 100
    assert 'farmer_id' in df.columns

def test_preprocess_features(mock_scorer, mock_supabase_data):
    """Test feature preprocessing"""
    df = pd.DataFrame(mock_supabase_data['farmers'])
    processed_df = mock_scorer.preprocess_features(df)
    assert isinstance(processed_df, pd.DataFrame)
    assert len(processed_df) == len(df)

def test_model_training(mock_scorer):
    """Test model training pipeline"""
    mock_scorer.train_model(force_retrain=True)
    assert mock_scorer.model is not None
    assert os.path.exists('models/credit_model.pkl')
    assert os.path.exists('models/feature_processors.pkl')
    assert os.path.exists('models/model_metadata.json')

def test_prediction(mock_scorer):
    """Test model prediction"""
    # Train the model first
    mock_scorer.train_model(force_retrain=True)
    
    # Test prediction
    test_features = {
        'age': 35,
        'location': 'Nyeri',
        'years_farming': 10,
        'loan_amount': 25000,
        'repayment_period': 12,
        'purpose': 'Equipment'
    }
    
    prediction = mock_scorer.predict(test_features)
    assert isinstance(prediction, dict)
    assert 'prediction' in prediction
    assert 'confidence' in prediction
    assert isinstance(prediction['prediction'], int)
    assert isinstance(prediction['confidence'], float)

def test_config_loading(mock_scorer):
    """Test configuration loading"""
    assert mock_scorer.config is not None
    assert 'target_column' in mock_scorer.config
    assert 'model_params' in mock_scorer.config
    assert 'feature_engineering' in mock_scorer.config

def test_feature_engineering(mock_scorer, mock_supabase_data):
    """Test feature engineering components"""
    df = mock_scorer.fetch_data()
    processed_df = mock_scorer.preprocess_features(df)
    
    # Check if feature engineering was applied
    assert len(processed_df.columns) >= len(df.columns)
    assert mock_scorer.feature_processors != {}
    assert 'feature_stats' in dir(mock_scorer)

def test_model_persistence(mock_scorer):
    """Test model saving and loading"""
    mock_scorer.train_model(force_retrain=True)
    
    # Check if model files exist
    assert os.path.exists('models/credit_model.pkl')
    assert os.path.exists('models/feature_processors.pkl')
    assert os.path.exists('models/model_metadata.json')
    
    # Try loading the model
    import joblib
    loaded_model = joblib.load('models/credit_model.pkl')
    assert loaded_model is not None