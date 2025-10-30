"""
Enhanced Credit Scoring Model for Smallholder Farmers

Features:
- Farm Characteristics: size, years active, crop diversity
- Production: yields, consistency, seasonal variation
- Financial Health: revenue, expenses, savings
- Risk Factors: weather impact, market access
- Social Factors: cooperative membership, training participation
- Historical Performance: past loans, repayment history

Models:
- Gradient Boosting: Main model for non-linear relationships
- Random Forest: Robust to outliers, handles missing data
- Logistic Regression: Interpretable baseline
- Voting Ensemble: Combines all models for stability

Evaluation:
- ROC-AUC: Overall discriminative ability
- Precision/Recall: Balance between risk and accessibility
- F1 Score: Harmonic mean of precision and recall
- Calibration: Reliability of probability estimates
"""

try:
    import pandas as pd
    import numpy as np
    from sklearn.model_selection import train_test_split, cross_val_score, KFold
    from sklearn.preprocessing import StandardScaler
    from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier, VotingClassifier
    from sklearn.linear_model import LogisticRegression
except ImportError as e:
    if "sklearn" in str(e):
        print("Error: scikit-learn is not installed. Please install required packages using:")
        print("pip install scikit-learn pandas numpy matplotlib seaborn joblib shap")
        print("\nNote: While we install using 'scikit-learn', we import using 'sklearn'")
        exit(1)
    raise e
from sklearn.metrics import (roc_auc_score, precision_score, recall_score,
                           f1_score, confusion_matrix, classification_report,
                           precision_recall_curve, average_precision_score)
from sklearn.calibration import calibration_curve
import shap
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

class EnhancedCreditScorer:
    def __init__(self, random_state=42):
        """Initialize the credit scoring system with multiple models."""
        self.random_state = random_state
        self.scaler = StandardScaler()
        
        # Initialize individual models
        self.gb = GradientBoostingClassifier(
            n_estimators=200,
            learning_rate=0.1,
            max_depth=4,
            min_samples_leaf=10,
            random_state=random_state
        )
        
        self.rf = RandomForestClassifier(
            n_estimators=200,
            max_depth=6,
            min_samples_leaf=10,
            random_state=random_state
        )
        
        self.lr = LogisticRegression(
            C=0.1,
            max_iter=1000,
            random_state=random_state
        )
        
        # Create voting ensemble
        self.ensemble = VotingClassifier(
            estimators=[
                ('gb', self.gb),
                ('rf', self.rf),
                ('lr', self.lr)
            ],
            voting='soft'
        )
        
        self.feature_names = None
        self.feature_importance = None
        self.shap_explainer = None

    def prepare_features(self, df):
        """
        Engineer features from raw farmer data.
        Returns both basic and engineered features.
        """
        # Basic features (direct from input)
        basic_features = [
            'farm_size_acres', 'years_farming', 'crop_diversity',
            'monthly_revenue', 'expense_ratio', 'training_hours',
            'coop_membership_years'
        ]
        
        # Engineer new features
        df = df.copy()
        
        # Handle missing columns with defaults
        if 'advisory_visits' not in df.columns:
            df['advisory_visits'] = 0
        if 'yield_kg_per_acre' not in df.columns:
            df['yield_kg_per_acre'] = df['monthly_revenue'] / (df['farm_size_acres'] * 50)  # Rough estimate
        if 'yield_consistency' not in df.columns:
            df['yield_consistency'] = 0.7  # Default moderate consistency
        
        # Production efficiency
        df['revenue_per_acre'] = df['monthly_revenue'] / df['farm_size_acres']
        df['yield_value'] = df['yield_kg_per_acre'] * df['yield_consistency']
        
        # Experience and training impact
        df['knowledge_score'] = (
            0.4 * df['years_farming'] / max(df['years_farming'].max(), 1) +
            0.3 * df['training_hours'] / max(df['training_hours'].max(), 1) +
            0.3 * df['advisory_visits'] / max(df['advisory_visits'].max(), 1)
        )
        
        # Risk assessment
        df['revenue_stability'] = df['yield_consistency'] * (1 - df['expense_ratio'])
        df['debt_service_ratio'] = np.minimum(
            df['monthly_revenue'] * 0.5,  # Max 50% of revenue for debt service
            df['monthly_revenue'] - df['expense_ratio'] * df['monthly_revenue']
        )
        
        # Cooperation and support network
        df['support_score'] = (
            df['coop_membership_years'] / max(df['coop_membership_years'].max(), 1) +
            df['advisory_visits'] / max(df['advisory_visits'].max(), 1)
        ) / 2
        
        # Combine all features
        engineered_features = [
            'revenue_per_acre', 'yield_value', 'knowledge_score',
            'revenue_stability', 'debt_service_ratio', 'support_score'
        ]
        
        self.feature_names = basic_features + engineered_features
        return df[self.feature_names]

    def train(self, X, y):
        """Train the model ensemble and compute feature importance."""
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        X_scaled = pd.DataFrame(X_scaled, columns=self.feature_names)
        
        # Train ensemble
        self.ensemble.fit(X_scaled, y)
        
        # Compute feature importance (from Gradient Boosting)
        self.feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.ensemble.named_estimators_['gb'].feature_importances_
        }).sort_values('importance', ascending=False)
        
        # Initialize SHAP explainer
        self.shap_explainer = shap.TreeExplainer(self.ensemble.named_estimators_['gb'])
        
        return self

    def evaluate(self, X, y):
        """Comprehensive model evaluation."""
        X_scaled = self.scaler.transform(X)
        X_scaled = pd.DataFrame(X_scaled, columns=self.feature_names)  # Add feature names
        predictions = self.ensemble.predict(X_scaled)
        probabilities = self.ensemble.predict_proba(X_scaled)[:, 1]
        
        # Basic metrics
        metrics = {
            'roc_auc': roc_auc_score(y, probabilities),
            'precision': precision_score(y, predictions),
            'recall': recall_score(y, predictions),
            'f1': f1_score(y, predictions),
            'avg_precision': average_precision_score(y, probabilities)
        }
        
        # Store latest evaluation results
        self.latest_evaluation = {
            'metrics': metrics.copy()
        }
        
        # Confusion matrix
        cm = confusion_matrix(y, predictions)
        
        # Calibration curve
        prob_true, prob_pred = calibration_curve(y, probabilities, n_bins=10)
        
        # SHAP values for global feature importance
        shap_values = self.shap_explainer.shap_values(X_scaled)
        
        return {
            'metrics': metrics,
            'confusion_matrix': cm,
            'calibration': (prob_true, prob_pred),
            'shap_values': shap_values,
            'feature_importance': self.feature_importance
        }

    def predict(self, X):
        """Make predictions with uncertainty estimates."""
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame([X])
        
        X = self.prepare_features(X)
        X_scaled = self.scaler.transform(X)
        X_scaled = pd.DataFrame(X_scaled, columns=self.feature_names)  # Add feature names
        
        # Get predictions from all models
        probabilities = []
        for name, model in self.ensemble.named_estimators_.items():
            prob = model.predict_proba(X_scaled)[:, 1]
            probabilities.append(prob)
        
        # Calculate mean and std of probabilities
        prob_array = np.array(probabilities)
        mean_prob = prob_array.mean(axis=0)
        std_prob = prob_array.std(axis=0)
        
        # Get SHAP values for explanation
        shap_values = self.shap_explainer.shap_values(X_scaled)
        
        return {
            'probability': mean_prob,
            'uncertainty': std_prob,
            'approved': mean_prob >= 0.7,  # Threshold can be adjusted
            'shap_values': shap_values,
            'feature_names': self.feature_names
        }

    def simulate_loan_terms(self, credit_score, monthly_revenue, expense_ratio):
        """Simulate loan terms based on credit score and financial metrics."""
        max_monthly_payment = monthly_revenue * (1 - expense_ratio) * 0.5  # 50% of disposable income
        
        # Base calculations
        max_loan_amount = max_monthly_payment * 24  # 2-year term as baseline
        recommended_term = 24
        base_interest_rate = 0.15  # 15% base rate
        
        # Adjust based on credit score
        if credit_score >= 0.8:
            max_loan_amount *= 1.5
            base_interest_rate *= 0.8
            recommended_term = 36  # Offer longer terms to high-score clients
        elif credit_score >= 0.6:
            max_loan_amount *= 1.2
            base_interest_rate *= 0.9
        else:
            max_loan_amount *= 0.8
            base_interest_rate *= 1.2
            recommended_term = 18  # Shorter terms for higher risk
        
        # Calculate payment schedules for different terms
        terms = [12, 18, 24, 36]
        payment_schedules = {}
        
        for term in terms:
            monthly_payment = (max_loan_amount * (1 + base_interest_rate)) / term
            schedule = []
            
            for month in range(1, term + 1):
                schedule.append({
                    'month': month,
                    'payment': monthly_payment,
                    'remaining_balance': max(0, max_loan_amount - (monthly_payment * month))
                })
            
            payment_schedules[term] = {
                'monthly_payment': monthly_payment,
                'total_interest': (monthly_payment * term) - max_loan_amount,
                'schedule': schedule
            }
        
        return {
            'max_loan_amount': max_loan_amount,
            'base_interest_rate': base_interest_rate,
            'recommended_term': recommended_term,
            'max_monthly_payment': max_monthly_payment,
            'payment_schedules': payment_schedules
        }

    def save(self, model_dir=None):
        """Save the model and associated transformers."""
        if model_dir is None:
            # Get the ai-models directory (where the model folder should be)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            model_dir = os.path.join(current_dir, 'models')
        
        os.makedirs(model_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save model components with timestamp
        model_components = {
            'ensemble': self.ensemble,
            'scaler': self.scaler,
            'feature_info': {
                'names': self.feature_names,
                'importance': self.feature_importance.to_dict() if self.feature_importance is not None else None
            }
        }
        # Save all components with timestamp and latest version
        for name, component in model_components.items():
            # Save timestamped version
            timestamped_path = os.path.join(model_dir, f'{name}_{timestamp}.pkl')
            joblib.dump(component, timestamped_path)
            
            # Save/update latest version
            latest_path = os.path.join(model_dir, f'{name}_latest.pkl')
            if os.path.exists(latest_path):
                os.remove(latest_path)
            import shutil
            shutil.copy2(timestamped_path, latest_path)
        
        # Save evaluation metrics if available
        if hasattr(self, 'latest_evaluation'):
            eval_path = os.path.join(model_dir, f'evaluation_{timestamp}.json')
            import json
            with open(eval_path, 'w') as f:
                # Convert numpy values to Python native types
                eval_dict = {}
                for k, v in self.latest_evaluation['metrics'].items():
                    eval_dict[k] = float(v)
                json.dump(eval_dict, f, indent=2)
        
        print(f"\nModel artifacts saved in {model_dir}:")
        print(f"- Timestamped versions: *_{timestamp}.pkl")
        print(f"- Latest versions: *_latest.pkl")
        if hasattr(self, 'latest_evaluation'):
            print(f"- Evaluation metrics: evaluation_{timestamp}.json")

    @classmethod
    def load(cls, model_dir=None):
        """Load the latest model version."""
        if model_dir is None:
            # Get the ai-models directory (where the model folder should be)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            model_dir = os.path.join(current_dir, 'models')
        
        try:
            scorer = cls()
            # Load model components
            model_files = {
                'ensemble': 'ensemble_latest.pkl',
                'scaler': 'scaler_latest.pkl',
                'feature_info': 'feature_info_latest.pkl'
            }
            
            for component, filename in model_files.items():
                file_path = os.path.join(model_dir, filename)
                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"Model component not found: {file_path}")
                
                data = joblib.load(file_path)
                if component == 'ensemble':
                    scorer.ensemble = data
                elif component == 'scaler':
                    scorer.scaler = data
                elif component == 'feature_info':
                    scorer.feature_names = data['names']
                    if data['importance'] is not None:
                        scorer.feature_importance = pd.DataFrame.from_dict(data['importance'])
            
            # Initialize SHAP explainer
            if scorer.ensemble is not None:
                scorer.shap_explainer = shap.TreeExplainer(scorer.ensemble.named_estimators_['gb'])
            
            # Try to load latest evaluation metrics
            eval_files = [f for f in os.listdir(model_dir) if f.startswith('evaluation_')]
            if eval_files:
                latest_eval = sorted(eval_files)[-1]
                import json
                with open(os.path.join(model_dir, latest_eval), 'r') as f:
                    scorer.latest_evaluation = {'metrics': json.load(f)}
            
            print(f"\nSuccessfully loaded model from {model_dir}")
            return scorer
        except Exception as e:
            print(f"\nError loading model: {str(e)}")
            print(f"Please ensure all required model files exist in {model_dir}/")
            raise

def plot_evaluation_results(evaluation_results, save_dir='models'):
    """Plot and save evaluation visualizations."""
    metrics = evaluation_results['metrics']
    cm = evaluation_results['confusion_matrix']
    prob_true, prob_pred = evaluation_results['calibration']
    shap_values = evaluation_results['shap_values']
    feature_importance = evaluation_results['feature_importance']
    
    # Create evaluation directory
    os.makedirs(save_dir, exist_ok=True)
    
    # 1. Confusion Matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.savefig(f'{save_dir}/confusion_matrix.png')
    plt.close()
    
    # 2. Calibration Plot
    plt.figure(figsize=(8, 6))
    plt.plot(prob_pred, prob_true, marker='o')
    plt.plot([0, 1], [0, 1], linestyle='--')
    plt.xlabel('Mean Predicted Probability')
    plt.ylabel('True Probability')
    plt.title('Calibration Plot')
    plt.savefig(f'{save_dir}/calibration.png')
    plt.close()
    
    # 3. Feature Importance
    plt.figure(figsize=(10, 6))
    sns.barplot(x='importance', y='feature', data=feature_importance)
    plt.title('Feature Importance')
    plt.tight_layout()
    plt.savefig(f'{save_dir}/feature_importance.png')
    plt.close()
    
    # 4. SHAP Summary Plot
    plt.figure(figsize=(10, 8))
    shap.summary_plot(shap_values, feature_importance.feature.values, show=False)
    plt.tight_layout()
    plt.savefig(f'{save_dir}/shap_summary.png', bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    # Setup paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    models_dir = os.path.join(current_dir, 'models')
    
    # Create necessary directories
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)
    
    # Check if we have real data, otherwise use synthetic
    data_file = os.path.join(data_dir, 'farmer_profiles.csv')
    try:
        df = pd.read_csv(data_file)
        print(f"Loaded existing data from {data_file}")
    except FileNotFoundError:
        print("No real data found, generating synthetic data...")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        import sys
        sys.path.append(current_dir)
        from data_generator import generate_synthetic_farmer_data
        df = generate_synthetic_farmer_data(n_samples=1000)
        df.to_csv(data_file, index=False)
        print(f"Generated synthetic data saved to {data_file}")
    
    # Prepare data
    X = df.drop('creditworthy', axis=1)
    y = df['creditworthy']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    print("\nTraining credit scoring model...")
    scorer = EnhancedCreditScorer()
    X_train_features = scorer.prepare_features(X_train)
    scorer.train(X_train_features, y_train)
    
    # Evaluate
    print("\nEvaluating model performance...")
    X_test_features = scorer.prepare_features(X_test)
    evaluation = scorer.evaluate(X_test_features, y_test)
    
    # Print results
    print("\nModel Evaluation Results:")
    print("-" * 50)
    for metric, value in evaluation['metrics'].items():
        print(f"{metric}: {value:.3f}")
    
    # Plot and save visualizations
    print("\nGenerating performance visualizations...")
    plot_evaluation_results(evaluation, save_dir=models_dir)
    
    # Save model
    print("\nSaving model artifacts...")
    scorer.save(models_dir)
    
    # Test loan simulation
    print("\nTesting loan simulation functionality...")
    sample_profile = X_test.iloc[0].to_dict()
    sample_features = scorer.prepare_features(pd.DataFrame([sample_profile]))
    prediction = scorer.predict(sample_features)
    
    loan_simulation = scorer.simulate_loan_terms(
        credit_score=prediction['probability'][0],
        monthly_revenue=sample_profile.get('monthly_revenue', 50000),
        expense_ratio=sample_profile.get('expense_ratio', 0.6)
    )
    
    print("\nSample Loan Simulation Results:")
    print("-" * 50)
    print(f"Credit Score: {prediction['probability'][0]:.2f}")
    print(f"Maximum Loan Amount: KES {loan_simulation['max_loan_amount']:,.2f}")
    print(f"Interest Rate: {loan_simulation['base_interest_rate']:.1%}")
    print(f"Recommended Term: {loan_simulation['recommended_term']} months")
    print(f"Maximum Monthly Payment: KES {loan_simulation['max_monthly_payment']:,.2f}")
    
    print("\nModel training and validation completed successfully!")
    print(f"All files saved in {models_dir} directory.")