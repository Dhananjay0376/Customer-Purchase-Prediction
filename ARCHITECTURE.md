# System Architecture Documentation

## 🏗️ Architecture Overview

This document describes the architecture and design principles of the Customer Purchase Prediction ML Pipeline.

## 📐 High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     User Interface                       │
│                  (Command Line + MLflow UI)              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  DVC Pipeline Controller                 │
│            (Orchestration & Automation)                  │
└────┬────────────┬────────────┬──────────┬──────────────┘
     │            │            │          │
     ▼            ▼            ▼          ▼
┌─────────┐  ┌─────────┐  ┌──────────┐  ┌──────────┐
│  Data   │  │Feature  │  │  Model   │  │  Model   │
│ Loading │→ │Engineer │→ │ Training │→ │Evaluation│
│         │  │   ing   │  │          │  │          │
└─────────┘  └─────────┘  └──────────┘  └──────────┘
     │            │            │              │
     ▼            ▼            ▼              ▼
┌─────────────────────────────────────────────────┐
│              Data & Model Storage                │
│         (DVC Tracked + Version Control)          │
└─────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│            MLflow Tracking Server                │
│     (Experiments, Metrics, Model Registry)       │
└─────────────────────────────────────────────────┘
```

## 🔄 Pipeline Flow

### Stage 1: Data Loading
```
Input:  Dataset URL (params.yaml)
        ↓
Process: Download → Validate → Convert to CSV
        ↓
Output: data/raw/online_retail.csv
```

### Stage 2: Data Preprocessing
```
Input:  data/raw/online_retail.csv
        ↓
Process: Clean → Remove Invalids → Create Features
        ↓
Output: data/processed/processed_data.csv
```

### Stage 3: Feature Engineering
```
Input:  data/processed/processed_data.csv
        ↓
Process: Select → Scale → Split (Train/Test)
        ↓
Output: data/processed/train.csv
        data/processed/test.csv
        models/scaler.pkl
```

### Stage 4: Model Training
```
Input:  data/processed/train.csv
        ↓
Process: Initialize Model → Train → Save
        ↓
Output: models/model.pkl
        MLflow: Parameters + Model
```

### Stage 5: Model Evaluation
```
Input:  data/processed/test.csv
        models/model.pkl
        ↓
Process: Predict → Calculate Metrics → Visualize
        ↓
Output: models/metrics.json
        models/confusion_matrix.png
        models/roc_curve.png
        MLflow: Metrics + Artifacts
```

## 🧩 Component Design

### 1. Configuration Layer (`params.yaml`)
**Purpose**: Centralized configuration management

**Sections**:
- `data`: Dataset paths and split configuration
- `preprocessing`: Data cleaning parameters
- `feature_engineering`: Feature selection and transformation
- `model`: Algorithm selection and hyperparameters
- `evaluation`: Metrics and validation settings
- `mlflow`: Experiment tracking configuration

**Design Principle**: Separation of configuration from code

### 2. Data Processing Layer

#### a. Data Loading Module (`data_loading.py`)
**Responsibilities**:
- Download dataset from source
- Perform initial validation
- Save raw data

**Dependencies**: None (Entry point)

#### b. Data Preprocessing Module (`data_preprocessing.py`)
**Responsibilities**:
- Data cleaning and validation
- Feature creation (RFM analysis)
- Customer-level aggregation

**Dependencies**: Raw data

#### c. Feature Engineering Module (`feature_engineering.py`)
**Responsibilities**:
- Feature selection
- Data scaling
- Train-test splitting

**Dependencies**: Processed data

### 3. Machine Learning Layer

#### a. Model Training Module (`model_training.py`)
**Responsibilities**:
- Model initialization based on config
- Model training
- MLflow tracking
- Model persistence

**Supported Algorithms**:
- Random Forest Classifier
- XGBoost Classifier
- Logistic Regression

**Design Pattern**: Strategy Pattern (algorithm selection)

#### b. Model Evaluation Module (`model_evaluation.py`)
**Responsibilities**:
- Model prediction
- Metrics calculation
- Visualization generation
- Cross-validation
- MLflow logging

**Metrics**:
- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC

### 4. Orchestration Layer (DVC)

**Pipeline Definition** (`dvc.yaml`):
```yaml
stages:
  stage_name:
    cmd: Command to execute
    deps: Dependencies (files/data)
    params: Parameters from params.yaml
    outs: Output artifacts
    metrics: Metric files (optional)
```

**DVC Features Used**:
- Pipeline DAG management
- Automatic dependency tracking
- Incremental execution
- Data versioning
- Reproducibility

### 5. Experiment Tracking Layer (MLflow)

**Tracking Components**:
- **Experiments**: Named containers for runs
- **Runs**: Individual training executions
- **Parameters**: Hyperparameters and config
- **Metrics**: Performance measurements
- **Artifacts**: Models, plots, files
- **Models**: Versioned model registry

## 🔐 Data Flow and Dependencies

```
params.yaml
    ├── data_loading.py
    ├── data_preprocessing.py
    ├── feature_engineering.py
    ├── model_training.py
    └── model_evaluation.py

data/raw/
    └── data_preprocessing.py

data/processed/
    ├── feature_engineering.py
    └── model_evaluation.py

models/
    ├── model_training.py (writes)
    └── model_evaluation.py (reads)
```

## 🎯 Design Principles

### 1. Modularity
- Each stage is a separate Python module
- Clear interfaces between stages
- Single Responsibility Principle

### 2. Configuration-Driven
- All parameters in `params.yaml`
- No hardcoded values in code
- Easy experimentation

### 3. Reproducibility
- DVC for pipeline versioning
- Fixed random seeds
- Deterministic execution

### 4. Automation
- Single command execution (`dvc repro`)
- Automatic dependency resolution
- Incremental updates

### 5. Observability
- Comprehensive logging
- MLflow experiment tracking
- Visualization generation

### 6. Scalability
- Modular architecture allows easy extensions
- Support for multiple algorithms
- Parameterized pipeline

## 🔧 Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Language | Python 3.8+ | Core implementation |
| ML Framework | scikit-learn, XGBoost | Model training |
| Experiment Tracking | MLflow | Experiment management |
| Pipeline Orchestration | DVC | Workflow automation |
| Data Processing | pandas, numpy | Data manipulation |
| Visualization | matplotlib, seaborn | Plotting |
| Model Persistence | joblib | Model serialization |
| Configuration | PyYAML | Config management |

## 📊 Data Model

### Customer Features (After Preprocessing)

| Feature | Type | Description |
|---------|------|-------------|
| CustomerID | int | Unique customer identifier |
| Recency | int | Days since last purchase |
| Frequency | int | Number of unique purchases |
| Monetary | float | Total spend amount |
| AvgPurchaseValue | float | Average transaction value |
| DaysSinceFirstPurchase | int | Customer lifetime |
| UniqueProducts | int | Product diversity |
| QuantityPerOrder | float | Average items per order |
| WillPurchase | int | Target (0/1) |

## 🚀 Extensibility Points

### Adding New Features
1. Modify `data_preprocessing.py`
2. Update `params.yaml` feature list
3. Run `dvc repro`

### Adding New Algorithms
1. Add algorithm config in `params.yaml`
2. Extend `get_model()` in `model_training.py`
3. Run with new algorithm parameter

### Adding New Metrics
1. Add metric calculation in `model_evaluation.py`
2. Update `params.yaml` evaluation section
3. Ensure MLflow logging

### Adding New Data Sources
1. Update `data_loading.py`
2. Adjust preprocessing as needed
3. Update DVC dependencies

## 🔍 Quality Assurance

### Code Quality
- Modular design
- Comprehensive logging
- Error handling
- Type hints (where applicable)

### Data Quality
- Validation at each stage
- Missing value handling
- Outlier detection
- Data type consistency

### Model Quality
- Cross-validation
- Multiple metrics
- Visualization
- Feature importance analysis

## 📝 Future Enhancements

### Planned Features
- Automated hyperparameter tuning
- Model monitoring and drift detection
- A/B testing framework
- Real-time prediction API
- Docker containerization
- Cloud deployment support
- Unit and integration tests
- CI/CD pipeline

### Scalability Improvements
- Distributed training support
- Batch prediction pipeline
- Feature store integration
- Model serving infrastructure

---

**Last Updated**: 2024
**Version**: 1.0.0
