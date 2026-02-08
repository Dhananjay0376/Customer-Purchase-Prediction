"""
Data Preprocessing Module
Handles data cleaning, transformation, and preparation
"""

import pandas as pd
import numpy as np
import yaml
import logging
import os
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_params(params_path='params.yaml'):
    """Load parameters from yaml file"""
    with open(params_path, 'r') as f:
        params = yaml.safe_load(f)
    return params


def clean_data(df, params):
    """Clean and prepare data"""
    logger.info("Starting data cleaning...")
    
    initial_shape = df.shape
    logger.info(f"Initial shape: {initial_shape}")
    
    # Make a copy
    df = df.copy()
    
    # Handle column names - standardize them
    df.columns = df.columns.str.strip()
    
    # Remove rows with missing CustomerID
    df = df.dropna(subset=['CustomerID'])
    logger.info(f"After removing missing CustomerID: {df.shape}")
    
    # Remove cancelled orders (InvoiceNo starting with 'C')
    df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
    logger.info(f"After removing cancelled orders: {df.shape}")
    
    # Remove negative or zero quantities
    min_quantity = params['preprocessing']['min_quantity']
    df = df[df['Quantity'] > min_quantity]
    logger.info(f"After removing invalid quantities: {df.shape}")
    
    # Remove negative or zero prices
    min_price = params['preprocessing']['min_price']
    max_price = params['preprocessing']['max_price']
    df = df[(df['UnitPrice'] > min_price) & (df['UnitPrice'] < max_price)]
    logger.info(f"After removing invalid prices: {df.shape}")
    
    # Convert InvoiceDate to datetime
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    # Create TotalPrice
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    
    # Remove invalid CustomerIDs
    df['CustomerID'] = df['CustomerID'].astype(int)
    
    logger.info(f"Final shape after cleaning: {df.shape}")
    logger.info(f"Removed {initial_shape[0] - df.shape[0]} rows ({((initial_shape[0] - df.shape[0]) / initial_shape[0] * 100):.2f}%)")
    
    return df


def create_customer_features(df, params):
    """Create customer-level features for prediction"""
    logger.info("Creating customer features...")
    
    # Get the reference date (latest date in dataset)
    reference_date = df['InvoiceDate'].max()
    logger.info(f"Reference date: {reference_date}")
    
    # Calculate RFM metrics per customer
    customer_features = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (reference_date - x.max()).days,  # Recency
        'InvoiceNo': 'nunique',  # Frequency (unique invoices)
        'TotalPrice': 'sum',  # Monetary
    }).reset_index()
    
    customer_features.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']
    
    # Additional features
    additional_features = df.groupby('CustomerID').agg({
        'TotalPrice': 'mean',  # Average purchase value
        'InvoiceDate': ['min', 'max'],  # First and last purchase
        'StockCode': 'nunique',  # Unique products
        'Quantity': 'sum'  # Total quantity
    }).reset_index()
    
    additional_features.columns = ['CustomerID', 'AvgPurchaseValue', 'FirstPurchase', 'LastPurchase', 'UniqueProducts', 'TotalQuantity']
    
    # Merge features
    customer_features = customer_features.merge(additional_features, on='CustomerID')
    
    # Calculate days since first purchase
    customer_features['DaysSinceFirstPurchase'] = (reference_date - customer_features['FirstPurchase']).dt.days
    
    # Calculate average quantity per order
    customer_features['QuantityPerOrder'] = customer_features['TotalQuantity'] / customer_features['Frequency']
    
    # Drop intermediate columns
    customer_features = customer_features.drop(['FirstPurchase', 'LastPurchase', 'TotalQuantity'], axis=1)
    
    # Create target variable: Will the customer purchase in the future?
    # We'll use a simple heuristic: customers with recent purchases (< 90 days) are likely to purchase again
    customer_features['WillPurchase'] = (customer_features['Recency'] < 90).astype(int)
    
    logger.info(f"Created features for {len(customer_features)} customers")
    logger.info(f"Feature columns: {customer_features.columns.tolist()}")
    logger.info(f"\nTarget distribution:\n{customer_features['WillPurchase'].value_counts()}")
    logger.info(f"\nFeature statistics:\n{customer_features.describe()}")
    
    return customer_features


def save_processed_data(df, params):
    """Save processed data"""
    processed_path = params['data']['processed_data_path']
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    df.to_csv(processed_path, index=False)
    logger.info(f"Processed data saved to {processed_path}")


def main():
    """Main execution function"""
    logger.info("Starting data preprocessing stage...")
    
    # Load parameters
    params = load_params()
    
    # Load raw data
    raw_path = params['data']['raw_data_path']
    logger.info(f"Loading raw data from {raw_path}")
    df = pd.read_csv(raw_path)
    
    # Clean data
    df_clean = clean_data(df, params)
    
    # Create customer features
    customer_features = create_customer_features(df_clean, params)
    
    # Save processed data
    save_processed_data(customer_features, params)
    
    logger.info("Data preprocessing completed successfully!")


if __name__ == "__main__":
    main()
