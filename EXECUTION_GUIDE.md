# Step-by-Step Execution Guide

This guide provides detailed instructions for running the Customer Purchase Prediction ML Pipeline.

## 📋 Prerequisites

Before starting, ensure you have:
- Python 3.8 or higher installed
- Git installed
- Internet connection (for data download)
- 2GB free disk space

## 🚀 Step-by-Step Instructions

### Step 1: Get the Project

#### Option A: Clone from GitHub (Recommended)
```bash
git clone https://github.com/YOUR-USERNAME/customer-purchase-prediction.git
cd customer-purchase-prediction
```

#### Option B: Download as ZIP
1. Download the project ZIP file
2. Extract to a folder
3. Open terminal in that folder

---

### Step 2: Set Up Environment

#### Automated Setup (Recommended)
```bash
# Make setup script executable (Linux/Mac)
chmod +x setup.sh

# Run setup script
./setup.sh
```

#### Manual Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize Git and DVC
git init
dvc init

# Create directories
mkdir -p data/raw data/processed models
```

---

### Step 3: Verify Setup

```bash
# Run validation script
python validate_setup.py
```

Expected output:
```
==================================================
PROJECT VALIDATION SCRIPT
Customer Purchase Prediction Pipeline
==================================================

✓ Python Version (3.8+)
✓ Required Packages
✓ Directory Structure
✓ Required Files
✓ Git Repository
✓ DVC Initialization
✓ Configuration File

==================================================
Result: 7/7 checks passed
==================================================

🎉 All checks passed! Project is ready to use.
```

---

### Step 4: Review Configuration

Open `params.yaml` and review the settings:

```yaml
# Key parameters to check
data:
  test_size: 0.2          # 80/20 train-test split
  random_state: 42        # For reproducibility

model:
  algorithm: random_forest  # Current algorithm
  random_forest:
    n_estimators: 100
    max_depth: 10
```

You can modify these parameters before running the pipeline.

---

### Step 5: Run the Complete Pipeline

```bash
# Execute the entire pipeline
dvc repro
```

**What happens:**

1. **Data Loading** (30-60 seconds)
   - Downloads Online Retail dataset
   - Converts to CSV format
   - Saves to `data/raw/`

2. **Data Preprocessing** (10-20 seconds)
   - Cleans invalid records
   - Creates customer features
   - Performs RFM analysis
   - Saves to `data/processed/`

3. **Feature Engineering** (5-10 seconds)
   - Selects features
   - Scales data
   - Splits train/test
   - Saves to `data/processed/`

4. **Model Training** (10-30 seconds)
   - Trains Random Forest model
   - Logs to MLflow
   - Saves model to `models/`

5. **Model Evaluation** (5-10 seconds)
   - Evaluates on test set
   - Performs cross-validation
   - Generates visualizations
   - Logs metrics to MLflow

**Total Time**: 1-2 minutes

---

### Step 6: View Results

#### A. Check Pipeline Status
```bash
dvc status
```

Expected output:
```
Data and pipelines are up to date.
```

#### B. View Metrics File
```bash
cat models/metrics.json
```

Example output:
```json
{
    "accuracy": 0.8523,
    "precision": 0.8214,
    "recall": 0.8845,
    "f1_score": 0.8518,
    "roc_auc": 0.9123,
    "cv_accuracy_mean": 0.8456,
    "cv_accuracy_std": 0.0234
}
```

#### C. View Visualizations
```bash
# Open confusion matrix
open models/confusion_matrix.png    # Mac
xdg-open models/confusion_matrix.png  # Linux
start models/confusion_matrix.png   # Windows

# Open ROC curve
open models/roc_curve.png           # Mac
xdg-open models/roc_curve.png       # Linux
start models/roc_curve.png          # Windows
```

#### D. Check Feature Importance
```bash
cat models/feature_importance.csv
```

---

### Step 7: Launch MLflow UI

```bash
# Start MLflow server
mlflow ui
```

Then open your browser to: `http://localhost:5000`

**In MLflow UI you can:**
- View all experiments
- Compare different runs
- Check parameters and metrics
- Download trained models
- View artifact plots

To stop MLflow: Press `Ctrl+C` in terminal

---

### Step 8: Experiment with Different Settings

#### Experiment 1: Try XGBoost
```bash
# 1. Edit params.yaml
nano params.yaml  # or use any text editor

# Change this line:
model:
  algorithm: xgboost  # changed from random_forest

# 2. Run pipeline
dvc repro

# 3. Check results
cat models/metrics.json

# 4. Compare in MLflow
mlflow ui
```

#### Experiment 2: Adjust Hyperparameters
```bash
# Edit params.yaml
model:
  random_forest:
    n_estimators: 200  # increased from 100
    max_depth: 15      # increased from 10

# Rerun
dvc repro
```

#### Experiment 3: Change Train-Test Split
```bash
# Edit params.yaml
data:
  test_size: 0.3  # changed from 0.2

# Rerun
dvc repro
```

---

### Step 9: View Pipeline Structure

```bash
# View pipeline DAG
dvc dag
```

Output shows dependencies:
```
+------------------+
| data_loading     |
+------------------+
        *
        *
        *
+-----------------+
| data_preprocessing |
+-----------------+
        *
        *
        *
+---------------------+
| feature_engineering |
+---------------------+
    *               *
    *               *
    *               *
+----------------+   *
| model_training |   *
+----------------+   *
    *               *
    *               *
    *****************
          *
          *
          *
+-------------------+
| model_evaluation  |
+-------------------+
```

---

### Step 10: Understand Output Files

```bash
# View directory structure
tree -L 3
```

Key files:
```
├── data/
│   ├── raw/
│   │   └── online_retail.csv      # Original data
│   └── processed/
│       ├── processed_data.csv      # Cleaned data
│       ├── train.csv               # Training set
│       └── test.csv                # Test set
├── models/
│   ├── model.pkl                   # Trained model
│   ├── scaler.pkl                  # Feature scaler
│   ├── metrics.json                # All metrics
│   ├── confusion_matrix.png        # CM plot
│   ├── roc_curve.png              # ROC plot
│   └── feature_importance.csv      # Features ranked
└── mlruns/                         # MLflow tracking
```

---

## 🔍 Detailed Stage Execution

If you want to run stages individually:

### Stage 1: Data Loading Only
```bash
dvc repro data_loading
```

### Stage 2: Up to Preprocessing
```bash
dvc repro data_preprocessing
```

### Stage 3: Up to Feature Engineering
```bash
dvc repro feature_engineering
```

### Stage 4: Up to Model Training
```bash
dvc repro model_training
```

### Stage 5: Complete Pipeline
```bash
dvc repro model_evaluation
# or simply
dvc repro
```

---

## 🐛 Troubleshooting

### Issue 1: Python Package Not Found
```bash
# Solution: Reinstall requirements
pip install -r requirements.txt --break-system-packages
```

### Issue 2: DVC Command Not Found
```bash
# Solution: Activate virtual environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### Issue 3: Data Download Fails
```bash
# Solution: Check internet or download manually
# URL: https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx
# Place in: data/raw/online_retail.xlsx
```

### Issue 4: Pipeline Stages Out of Date
```bash
# Solution: Force rerun all stages
dvc repro --force
```

### Issue 5: MLflow UI Not Opening
```bash
# Solution: Specify backend explicitly
mlflow ui --backend-store-uri ./mlruns --port 5000
```

---

## 📊 Understanding the Results

### Metrics Interpretation

| Metric | Range | Good Value | Meaning |
|--------|-------|------------|---------|
| Accuracy | 0-1 | >0.80 | Overall correctness |
| Precision | 0-1 | >0.80 | True positive rate |
| Recall | 0-1 | >0.80 | Positive detection rate |
| F1-Score | 0-1 | >0.80 | Harmonic mean of P & R |
| ROC-AUC | 0-1 | >0.85 | Discrimination ability |

### Cross-Validation Interpretation
- **Mean**: Average performance across folds
- **Std**: Consistency (lower is better)

---

## 🎯 What's Next?

### Learn More
1. Read `ARCHITECTURE.md` for system design
2. Check `CONTRIBUTING.md` for contribution guide
3. Review `README.md` for complete documentation

### Customize
1. Try different algorithms (xgboost, logistic_regression)
2. Tune hyperparameters in `params.yaml`
3. Add custom features in `data_preprocessing.py`
4. Experiment with different metrics

### Share
1. Push to GitHub (see `GITHUB_SETUP.md`)
2. Set up DVC remote for collaboration
3. Deploy model as API
4. Create dashboards

---

## ✅ Success Checklist

After completing these steps, you should have:

- ✅ Pipeline running successfully
- ✅ Trained model in `models/model.pkl`
- ✅ Metrics in `models/metrics.json`
- ✅ Visualizations generated
- ✅ MLflow tracking working
- ✅ Understanding of pipeline flow
- ✅ Ability to modify parameters

---

## 📞 Getting Help

If you encounter issues:

1. **Check logs**: Each stage prints detailed logs
2. **Run validation**: `python validate_setup.py`
3. **Review docs**: Check README.md and other .md files
4. **Check DVC status**: `dvc status`
5. **Verify environment**: Ensure virtual env is activated

---

**Congratulations! 🎉** 

You now have a fully functional, automated ML pipeline with industry-standard MLOps practices!

---

**Last Updated**: 2024
