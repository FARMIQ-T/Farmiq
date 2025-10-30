import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
from datetime import datetime
import os
import json
from supabase import create_client, Client
from typing import List, Dict, Any
import logging
from feature_engine.selection import DropConstantFeatures
from feature_engine.creation import CombineWithReferenceFeature
from feature_engine.encoding import RareLabelEncoder
import yaml

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DynamicCreditScorer:
    def __init__(self, supabase_url: str, supabase_key: str, config_path: str = "model_config.yaml"):
        """
        Initialize the credit scorer with Supabase credentials and configuration.
        
        Args:
            supabase_url: Supabase project URL
            supabase_key: Supabase project API key
            config_path: Path to the model configuration YAML file
        """
        self.supabase: Client = create_client(supabase_url, supabase_key)
        self.config_path = config_path
        self.load_config()
        self.model = None
        self.feature_processors = {}
        self.feature_stats = {}
        
    def load_config(self):
        """Load model configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            logger.info(f"Loaded configuration from {self.config_path}")
        except FileNotFoundError:
            logger.warning("Config file not found, using default configuration")
            self.config = {
                'target_column': 'credit_score',
                'model_params': {
                    'n_estimators': 100,
                    'max_depth': 10,
                    'random_state': 42
                },
                'feature_engineering': {
                    'combine_features': True,
                    'drop_constant': True,
                    'encode_categorical': True,
                    'rare_label_threshold': 0.01
                },
                'training': {
                    'test_size': 0.2,
                    'random_state': 42
                }
            }
            
    def fetch_data(self) -> pd.DataFrame:
        """
        Fetch training data from Supabase tables.
        Returns:
            DataFrame containing the merged data
        """
        try:
            # Fetch data from different tables and merge
            farmers = self.supabase.table('farmers').select('*').execute()
            loans = self.supabase.table('loans').select('*').execute()
            transactions = self.supabase.table('transactions').select('*').execute()
            credit_scores = self.supabase.table('credit_scores').select('*').execute()
            
            # Convert to DataFrames
            df_farmers = pd.DataFrame(farmers.data)
            df_loans = pd.DataFrame(loans.data)
            df_transactions = pd.DataFrame(transactions.data)
            df_scores = pd.DataFrame(credit_scores.data)
            
            # Merge dataframes
            merged_df = df_farmers.merge(df_loans, on='farmer_id', how='left')\
                                .merge(df_transactions, on='farmer_id', how='left')\
                                .merge(df_scores, on='farmer_id', how='left')
            
            logger.info(f"Fetched {len(merged_df)} records from Supabase")
            return merged_df
            
        except Exception as e:
            logger.error(f"Error fetching data from Supabase: {str(e)}")
            raise
            
    def preprocess_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Dynamically preprocess features based on their data types and statistics.
        
        Args:
            df: Input DataFrame
        Returns:
            Preprocessed DataFrame
        """
        processed_df = df.copy()
        
        # Drop constant features
        if self.config['feature_engineering']['drop_constant']:
            constant_dropper = DropConstantFeatures(tol=0.98)
            processed_df = constant_dropper.fit_transform(processed_df)
            self.feature_processors['constant_dropper'] = constant_dropper
        
        # Handle categorical features
        categorical_columns = processed_df.select_dtypes(include=['object']).columns
        if self.config['feature_engineering']['encode_categorical']:
            for col in categorical_columns:
                if col != self.config['target_column']:
                    # Use Rare Label Encoding for categorical features
                    rare_encoder = RareLabelEncoder(
                        tol=self.config['feature_engineering']['rare_label_threshold'],
                        n_categories=10
                    )
                    processed_df[col] = rare_encoder.fit_transform(processed_df[[col]])
                    self.feature_processors[f'rare_encoder_{col}'] = rare_encoder
        
        # Feature combination for numerical columns
        if self.config['feature_engineering']['combine_features']:
            numerical_columns = processed_df.select_dtypes(include=['int64', 'float64']).columns
            combiner = CombineWithReferenceFeature(
                variables_to_combine=list(numerical_columns[:5]),
                reference_variables=list(numerical_columns[5:7]),
                operations=['sum', 'prod']
            )
            processed_df = combiner.fit_transform(processed_df)
            self.feature_processors['feature_combiner'] = combiner
        
        # Scale numerical features
        scaler = StandardScaler()
        numerical_columns = processed_df.select_dtypes(include=['int64', 'float64']).columns
        processed_df[numerical_columns] = scaler.fit_transform(processed_df[numerical_columns])
        self.feature_processors['scaler'] = scaler
        
        # Store feature statistics
        self.feature_stats = {
            'n_features': len(processed_df.columns),
            'feature_names': list(processed_df.columns),
            'categorical_features': list(categorical_columns),
            'numerical_features': list(numerical_columns)
        }
        
        return processed_df
        
    def train_model(self, force_retrain: bool = False) -> None:
        """
        Train the credit scoring model with current data.
        
        Args:
            force_retrain: Whether to force retraining even if recent model exists
        """
        try:
            # Check if we need to retrain
            if not force_retrain and self._check_recent_model():
                logger.info("Recent model found, skipping training")
                return
            
            # Fetch and preprocess data
            df = self.fetch_data()
            processed_df = self.preprocess_features(df)
            
            # Prepare features and target
            X = processed_df.drop(columns=[self.config['target_column']])
            y = processed_df[self.config['target_column']]
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y,
                test_size=self.config['training']['test_size'],
                random_state=self.config['training']['random_state']
            )
            
            # Train model
            self.model = RandomForestClassifier(**self.config['model_params'])
            self.model.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = self.model.predict(X_test)
            report = classification_report(y_test, y_pred, output_dict=True)
            
            # Save model and metadata
            self._save_model(report)
            
            logger.info("Model training completed successfully")
            logger.info(f"Model Score: {self.model.score(X_test, y_test):.4f}")
            
        except Exception as e:
            logger.error(f"Error during model training: {str(e)}")
            raise
            
    def _check_recent_model(self) -> bool:
        """Check if a recent model exists (less than 24 hours old)."""
        try:
            model_path = os.path.join('models', 'credit_model.pkl')
            if not os.path.exists(model_path):
                return False
            
            model_time = datetime.fromtimestamp(os.path.getmtime(model_path))
            time_diff = datetime.now() - model_time
            
            return time_diff.days < 1
        except Exception:
            return False
            
    def _save_model(self, metrics: Dict[str, Any]) -> None:
        """
        Save the model and its metadata.
        
        Args:
            metrics: Model evaluation metrics
        """
        # Create models directory if it doesn't exist
        os.makedirs('models', exist_ok=True)
        
        # Save model
        model_path = os.path.join('models', 'credit_model.pkl')
        joblib.dump(self.model, model_path)
        
        # Save feature processors
        processors_path = os.path.join('models', 'feature_processors.pkl')
        joblib.dump(self.feature_processors, processors_path)
        
        # Save metadata
        metadata = {
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics,
            'feature_stats': self.feature_stats,
            'config': self.config
        }
        metadata_path = os.path.join('models', 'model_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
            
    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make predictions using the trained model.
        
        Args:
            features: Dictionary of feature names and values
        Returns:
            Dictionary containing prediction and confidence
        """
        try:
            # Convert features to DataFrame
            df = pd.DataFrame([features])
            
            # Apply feature processing
            for processor_name, processor in self.feature_processors.items():
                if processor_name.startswith('rare_encoder_'):
                    col = processor_name.replace('rare_encoder_', '')
                    df[col] = processor.transform(df[[col]])
                elif hasattr(processor, 'transform'):
                    df = processor.transform(df)
            
            # Make prediction
            prediction = self.model.predict(df)[0]
            probabilities = self.model.predict_proba(df)[0]
            confidence = float(max(probabilities))
            
            return {
                'prediction': int(prediction),
                'confidence': confidence,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            raise

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Initialize scorer
    scorer = DynamicCreditScorer(
        supabase_url=os.getenv('SUPABASE_URL'),
        supabase_key=os.getenv('SUPABASE_KEY')
    )
    
    # Train model
    scorer.train_model(force_retrain=True)