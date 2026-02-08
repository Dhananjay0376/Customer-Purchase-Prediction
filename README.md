# Customer Purchase Prediction - Automated ML Pipeline

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![DVC](https://img.shields.io/badge/DVC-Pipeline-orange.svg)](https://dvc.org/)
[![MLflow](https://img.shields.io/badge/MLflow-Tracking-blue.svg)](https://mlflow.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An end-to-end automated machine learning pipeline for predicting customer purchase behavior, built with MLOps best practices using DVC for pipeline orchestration and MLflow for experiment tracking.

![Pipeline Architecture](https://img.shields.io/badge/Architecture-Modular-brightgreen)
![Automation](https://img.shields.io/badge/Automation-DVC-orange)
![Tracking](https://img.shields.io/badge/Tracking-MLflow-blue)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Pipeline Stages](#pipeline-stages)
- [Configuration](#configuration)
- [MLflow Tracking](#mlflow-tracking)
- [DVC Pipeline](#dvc-pipeline)
- [Results](#results)
- [Customization](#customization)

## 🎯 Overview

This project implements a complete MLOps pipeline for customer purchase prediction using the Online Retail dataset. The pipeline is designed to be:

- **Automated**: Single command execution using DVC
- **Reproducible**: Version-controlled data and models
- **Configurable**: Parameter-driven pipeline via YAML
- **Tracked**: Complete experiment tracking with MLflow
- **Modular**: Separate Python files for each pipeline stage

## ✨ Features

- **Automated Data Pipeline**: End-to-end automation from data loading to model evaluation
- **DVC Integration**: Complete pipeline orchestration and data versioning
- **MLflow Tracking**: Comprehensive experiment tracking and model registry
- **Modular Architecture**: Clean separation of concerns with individual Python modules
- **Parameter Configuration**: YAML-based configuration for easy experimentation
- **Multiple Algorithms**: Support for Random Forest, XGBoost, and Logistic Regression
- **Comprehensive Metrics**: Accuracy, Precision, Recall, F1-Score, ROC-AUC
- **Visualizations**: Confusion matrix and ROC curve plots
- **Cross-Validation**: K-fold cross-validation for robust evaluation

## 📁 Project Structure

```
customer-purchase-prediction/
│
├── data/
│   ├── raw/                    # Raw data (DVC tracked)
│   └── processed/              # Processed data (DVC tracked)
│
├── src/
│   ├── data_loading.py         # Stage 1: Data loading
│   ├── data_preprocessing.py   # Stage 2: Data cleaning & preprocessing
│   ├── feature_engineering.py  # Stage 3: Feature engineering & splitting
│   ├── model_training.py       # Stage 4: Model training
│   └── model_evaluation.py     # Stage 5: Model evaluation
│
├── models/                     # Trained models and artifacts (DVC tracked)
│   ├── model.pkl
│   ├── scaler.pkl
│   ├── metrics.json
│   ├── confusion_matrix.png
│   ├── roc_curve.png
│   └── feature_importance.csv
│
├── mlruns/                     # MLflow tracking directory
│
├── params.yaml                 # Pipeline configuration parameters
├── dvc.yaml                    # DVC pipeline definition
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
├── .dvcignore                  # DVC ignore rules
└── README.md                   # This file
```

## 🔧 Requirements

- Python 3.8+
- Git
- DVC
- MLflow

## 📦 Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd customer-purchase-prediction
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize DVC

```bash
dvc init
```

## 🚀 Usage

### Run Complete Pipeline

Execute the entire ML pipeline with a single command:

```bash
dvc repro
```

This will:
1. Download and load the dataset
2. Clean and preprocess the data
3. Engineer features and split data
4. Train the model
5. Evaluate and track metrics

### Run Specific Stage

To run only a specific stage:

```bash
dvc repro <stage_name>
```

Examples:
```bash
dvc repro data_loading
dvc repro model_training
dvc repro model_evaluation
```

### View Pipeline DAG

Visualize the pipeline structure:

```bash
dvc dag
```

### Check Pipeline Status

```bash
dvc status
```

## 🔄 Pipeline Stages

### 1. Data Loading (`data_loading.py`)

- Downloads the Online Retail dataset from UCI repository
- Performs initial data validation
- Saves raw data for processing

**Output**: `data/raw/online_retail.csv`

### 2. Data Preprocessing (`data_preprocessing.py`)

- Removes cancelled orders and invalid transactions
- Handles missing values
- Creates customer-level aggregations
- Generates RFM (Recency, Frequency, Monetary) features

**Output**: `data/processed/processed_data.csv`

### 3. Feature Engineering (`feature_engineering.py`)

- Selects relevant features
- Handles missing values
- Scales features using StandardScaler
- Splits data into train/test sets (80/20)

**Outputs**: 
- `data/processed/train.csv`
- `data/processed/test.csv`
- `models/scaler.pkl`

### 4. Model Training (`model_training.py`)

- Trains selected ML algorithm
- Logs parameters to MLflow
- Saves trained model
- Tracks feature importances

**Output**: `models/model.pkl`

### 5. Model Evaluation (`model_evaluation.py`)

- Evaluates model on test set
- Performs cross-validation
- Generates confusion matrix and ROC curve
- Logs all metrics to MLflow

**Outputs**:
- `models/metrics.json`
- `models/confusion_matrix.png`
- `models/roc_curve.png`

## ⚙️ Configuration

All pipeline parameters are defined in `params.yaml`. You can modify this file to change pipeline behavior without touching the code.

### Key Parameters

#### Data Configuration
```yaml
data:
  test_size: 0.2          # Train-test split ratio
  random_state: 42        # Reproducibility seed
```

#### Model Selection
```yaml
model:
  algorithm: random_forest  # Options: random_forest, xgboost, logistic_regression
```

#### Model Hyperparameters
```yaml
model:
  random_forest:
    n_estimators: 100
    max_depth: 10
    min_samples_split: 5
```

### Changing Configuration

1. Edit `params.yaml`
2. Run `dvc repro` to execute pipeline with new parameters
3. MLflow will track the new experiment automatically

## 📊 MLflow Tracking

### View MLflow UI

```bash
mlflow ui
```

Then open http://localhost:5000 in your browser.

### Tracked Information

- **Parameters**: All model hyperparameters and configuration
- **Metrics**: Accuracy, Precision, Recall, F1-Score, ROC-AUC
- **Artifacts**: Model files, plots, feature importances
- **Models**: Versioned model registry

### Compare Experiments

Use the MLflow UI to:
- Compare different algorithm performances
- Analyze hyperparameter effects
- Track model evolution over time
- Download best models

## 🔍 DVC Pipeline

### Pipeline Benefits

- **Reproducibility**: Exact pipeline recreation
- **Efficiency**: Only runs changed stages
- **Data Versioning**: Track data changes like code
- **Collaboration**: Share pipelines with team

### DVC Commands

```bash
# Run pipeline
dvc repro

# Show pipeline structure
dvc dag

# Check what changed
dvc status

# Push data to remote storage
dvc push

# Pull data from remote storage
dvc pull
```

## 📈 Results

After running the pipeline, you'll find:

### Metrics (`models/metrics.json`)
```json
{
    "accuracy": 0.85,
    "precision": 0.82,
    "recall": 0.88,
    "f1_score": 0.85,
    "roc_auc": 0.91,
    "cv_accuracy_mean": 0.84,
    "cv_accuracy_std": 0.02
}
```

### Visualizations
- **Confusion Matrix**: `models/confusion_matrix.png`
- **ROC Curve**: `models/roc_curve.png`

### Feature Importances
- **CSV File**: `models/feature_importance.csv`

## 🎨 Customization

### Use Different Dataset

1. Update `params.yaml` with new dataset URL or path
2. Modify `data_loading.py` to handle new data format
3. Adjust `data_preprocessing.py` for different features
4. Run `dvc repro`

### Add New Features

1. Edit `data_preprocessing.py` to create new features
2. Update `params.yaml` to include new features
3. Run `dvc repro feature_engineering`

### Try Different Algorithm

1. Edit `params.yaml` to change `model.algorithm`
2. Adjust hyperparameters if needed
3. Run `dvc repro model_training`

### Add New Metrics

1. Edit `model_evaluation.py` to calculate new metrics
2. Update `params.yaml` evaluation section
3. Run `dvc repro model_evaluation`

## 🐛 Troubleshooting

### Issue: DVC pipeline fails

**Solution**: Check `dvc status` and ensure all dependencies are met

### Issue: MLflow tracking not working

**Solution**: Ensure MLflow is installed and `mlflow ui` is accessible

### Issue: Data download fails

**Solution**: Check internet connection and dataset URL in `params.yaml`

### Issue: Module import errors

**Solution**: Ensure you're in the project directory and virtual environment is activated

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 👥 Authors

- Your Name - MLOps Engineer

## 🙏 Acknowledgments

- Dataset: [UCI Machine Learning Repository - Online Retail](https://archive.ics.uci.edu/ml/datasets/online+retail)
- Tools: DVC, MLflow, scikit-learn, XGBoost

## 📞 Contact

For questions or feedback, please open an issue on GitHub.

---

**Note**: This project is designed for educational and demonstration purposes, showcasing MLOps best practices for building automated, reproducible ML pipelines.
