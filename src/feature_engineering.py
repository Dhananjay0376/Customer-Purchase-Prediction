"""
Feature Engineering Module
Handles feature selection, transformation, and train-test split
"""

import pandas as pd
import numpy as np
import yaml
import logging
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_params(params_path='params.yaml'):
    """Load parameters from yaml file"""
    with open(params_path, 'r') as f:
        params = yaml.safe_load(f)
    return params


def select_features(df, params):
    """Select relevant features for modeling"""
    logger.info("Selecting features...")
    
    features = params['feature_engineering']['features']
    target = params['feature_engineering']['target_column']
    
    # Ensure all features exist
    available_features = [f for f in features if f in df.columns]
    missing_features = [f for f in features if f not in df.columns]
    
    if missing_features:
        logger.warning(f"Missing features: {missing_features}")
    
    logger.info(f"Selected features: {available_features}")
    
    X = df[available_features]
    y = df[target]
    
    logger.info(f"Feature matrix shape: {X.shape}")
    logger.info(f"Target shape: {y.shape}")
    logger.info(f"Target distribution:\n{y.value_counts()}")
    
    return X, y


def handle_missing_values(X):
    """Handle any missing values in features"""
    logger.info("Handling missing values...")
    
    missing_counts = X.isnull().sum()
    if missing_counts.sum() > 0:
        logger.warning(f"Found missing values:\n{missing_counts[missing_counts > 0]}")
        # Fill with median for numerical columns
        X = X.fillna(X.median())
        logger.info("Missing values filled with median")
    else:
        logger.info("No missing values found")
    
    return X


def scale_features(X_train, X_test, params):
    """Scale features using StandardScaler"""
    logger.info("Scaling features...")
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Convert back to DataFrame
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns, index=X_train.index)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns, index=X_test.index)
    
    # Save scaler
    os.makedirs('models', exist_ok=True)
    scaler_path = 'models/scaler.pkl'
    joblib.dump(scaler, scaler_path)
    logger.info(f"Scaler saved to {scaler_path}")
    
    logger.info("Feature scaling completed")
    
    return X_train_scaled, X_test_scaled, scaler


def split_data(X, y, params):
    """Split data into train and test sets"""
    logger.info("Splitting data into train and test sets...")
    
    test_size = params['data']['test_size']
    random_state = params['data']['random_state']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    logger.info(f"Train set shape: X={X_train.shape}, y={y_train.shape}")
    logger.info(f"Test set shape: X={X_test.shape}, y={y_test.shape}")
    logger.info(f"Train target distribution:\n{y_train.value_counts()}")
    logger.info(f"Test target distribution:\n{y_test.value_counts()}")
    
    return X_train, X_test, y_train, y_test


def save_train_test_data(X_train, X_test, y_train, y_test, params):
    """Save train and test data"""
    logger.info("Saving train and test data...")
    
    # Combine features and target
    train_data = pd.concat([X_train, y_train], axis=1)
    test_data = pd.concat([X_test, y_test], axis=1)
    
    # Save
    train_path = params['data']['train_data_path']
    test_path = params['data']['test_data_path']
    
    os.makedirs(os.path.dirname(train_path), exist_ok=True)
    
    train_data.to_csv(train_path, index=False)
    test_data.to_csv(test_path, index=False)
    
    logger.info(f"Train data saved to {train_path}")
    logger.info(f"Test data saved to {test_path}")


def main():
    """Main execution function"""
    logger.info("Starting feature engineering stage...")
    
    # Load parameters
    params = load_params()
    
    # Load processed data
    processed_path = params['data']['processed_data_path']
    logger.info(f"Loading processed data from {processed_path}")
    df = pd.read_csv(processed_path)
    
    # Select features
    X, y = select_features(df, params)
    
    # Handle missing values
    X = handle_missing_values(X)
    
    # Split data
    X_train, X_test, y_train, y_test = split_data(X, y, params)
    
    # Scale features
    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test, params)
    
    # Save train and test data
    save_train_test_data(X_train_scaled, X_test_scaled, y_train, y_test, params)
    
    logger.info("Feature engineering completed successfully!")


if __name__ == "__main__":
    main()
