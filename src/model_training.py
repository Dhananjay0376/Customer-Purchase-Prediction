"""
Model Training Module
Handles model training with MLflow tracking
"""

import pandas as pd
import numpy as np
import yaml
import logging
import os
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
import joblib

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_params(params_path='params.yaml'):
    """Load parameters from yaml file"""
    with open(params_path, 'r') as f:
        params = yaml.safe_load(f)
    return params


def get_model(params):
    """Get model based on configuration"""
    algorithm = params['model']['algorithm']
    logger.info(f"Selected algorithm: {algorithm}")
    
    if algorithm == 'random_forest':
        model_params = params['model']['random_forest']
        model = RandomForestClassifier(**model_params)
    elif algorithm == 'xgboost':
        model_params = params['model']['xgboost']
        model = XGBClassifier(**model_params)
    elif algorithm == 'logistic_regression':
        model_params = params['model']['logistic_regression']
        model = LogisticRegression(**model_params)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")
    
    return model, model_params


def train_model(X_train, y_train, params):
    """Train the model with MLflow tracking"""
    logger.info("Starting model training...")
    
    # Setup MLflow
    experiment_name = params['mlflow']['experiment_name']
    mlflow.set_experiment(experiment_name)
    
    # Get model
    model, model_params = get_model(params)
    
    # Start MLflow run
    with mlflow.start_run():
        # Log parameters
        mlflow.log_params(model_params)
        mlflow.log_param("algorithm", params['model']['algorithm'])
        mlflow.log_param("n_features", X_train.shape[1])
        mlflow.log_param("n_samples", X_train.shape[0])
        
        # Log feature names
        mlflow.log_param("features", list(X_train.columns))
        
        # Train model
        logger.info("Training model...")
        model.fit(X_train, y_train)
        logger.info("Model training completed")
        
        # Log model
        mlflow.sklearn.log_model(model, "model")
        
        # Save model locally
        os.makedirs('models', exist_ok=True)
        model_path = 'models/model.pkl'
        joblib.dump(model, model_path)
        logger.info(f"Model saved to {model_path}")
        
        # Log feature importances if available
        if hasattr(model, 'feature_importances_'):
            feature_importance = pd.DataFrame({
                'feature': X_train.columns,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            logger.info(f"\nFeature Importances:\n{feature_importance}")
            
            # Save feature importance
            importance_path = 'models/feature_importance.csv'
            feature_importance.to_csv(importance_path, index=False)
            mlflow.log_artifact(importance_path)
        
        mlflow.log_artifact(model_path)
        
        run_id = mlflow.active_run().info.run_id
        logger.info(f"MLflow run ID: {run_id}")
    
    return model


def main():
    """Main execution function"""
    logger.info("Starting model training stage...")
    
    # Load parameters
    params = load_params()
    
    # Load training data
    train_path = params['data']['train_data_path']
    logger.info(f"Loading training data from {train_path}")
    train_data = pd.read_csv(train_path)
    
    # Separate features and target
    target_col = params['feature_engineering']['target_column']
    X_train = train_data.drop(target_col, axis=1)
    y_train = train_data[target_col]
    
    logger.info(f"Training data shape: X={X_train.shape}, y={y_train.shape}")
    
    # Train model
    model = train_model(X_train, y_train, params)
    
    logger.info("Model training completed successfully!")


if __name__ == "__main__":
    main()
