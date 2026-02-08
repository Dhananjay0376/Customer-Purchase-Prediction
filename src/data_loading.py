"""
Data Loading Module
Handles downloading and initial loading of raw data
"""

import os
import pandas as pd
import yaml
import urllib.request
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_params(params_path='params.yaml'):
    """Load parameters from yaml file"""
    with open(params_path, 'r') as f:
        params = yaml.safe_load(f)
    return params


def download_data(url, output_path):
    """Download data from URL"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    if os.path.exists(output_path):
        logger.info(f"Data already exists at {output_path}")
        return
    
    logger.info(f"Downloading data from {url}")
    urllib.request.urlretrieve(url, output_path.replace('.csv', '.xlsx'))
    logger.info(f"Data downloaded successfully")


def load_raw_data(params):
    """Load raw data and perform initial checks"""
    raw_path = params['data']['raw_data_path']
    dataset_url = params['data']['dataset_url']
    
    # Create directory if not exists
    os.makedirs(os.path.dirname(raw_path), exist_ok=True)
    
    # Download if not exists
    xlsx_path = raw_path.replace('.csv', '.xlsx')
    if not os.path.exists(xlsx_path) and not os.path.exists(raw_path):
        download_data(dataset_url, raw_path)
    
    # Load data
    try:
        if os.path.exists(xlsx_path):
            logger.info(f"Loading data from {xlsx_path}")
            df = pd.read_excel(xlsx_path, engine='openpyxl')
            # Save as CSV for easier processing
            df.to_csv(raw_path, index=False)
            logger.info(f"Converted to CSV: {raw_path}")
        else:
            logger.info(f"Loading data from {raw_path}")
            df = pd.read_csv(raw_path)
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise
    
    logger.info(f"Data loaded successfully. Shape: {df.shape}")
    logger.info(f"Columns: {df.columns.tolist()}")
    logger.info(f"\nFirst few rows:\n{df.head()}")
    logger.info(f"\nData types:\n{df.dtypes}")
    logger.info(f"\nMissing values:\n{df.isnull().sum()}")
    
    return df


def main():
    """Main execution function"""
    logger.info("Starting data loading stage...")
    
    # Load parameters
    params = load_params()
    
    # Load raw data
    df = load_raw_data(params)
    
    # Save raw data
    raw_path = params['data']['raw_data_path']
    os.makedirs(os.path.dirname(raw_path), exist_ok=True)
    df.to_csv(raw_path, index=False)
    
    logger.info(f"Data loading completed. Data saved to {raw_path}")
    logger.info(f"Total records: {len(df)}")


if __name__ == "__main__":
    main()
