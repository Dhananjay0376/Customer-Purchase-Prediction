# Quick Start Guide

Get up and running with the Customer Purchase Prediction Pipeline in 5 minutes!

## ⚡ Fast Track Installation

### Prerequisites
- Python 3.8 or higher
- Git

### Step 1: Clone and Setup (1 minute)

```bash
# Clone the repository
git clone <your-repository-url>
cd customer-purchase-prediction

# Run automated setup
chmod +x setup.sh
./setup.sh
```

### Step 2: Activate Environment (10 seconds)

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 3: Run Pipeline (2-3 minutes)

```bash
dvc repro
```

That's it! The pipeline will:
1. ✓ Download dataset
2. ✓ Clean and preprocess data
3. ✓ Engineer features
4. ✓ Train model
5. ✓ Evaluate and track results

### Step 4: View Results (30 seconds)

**Check Metrics:**
```bash
cat models/metrics.json
```

**View Visualizations:**
- Open `models/confusion_matrix.png`
- Open `models/roc_curve.png`

**Launch MLflow UI:**
```bash
mlflow ui
# Visit http://localhost:5000
```

## 🎯 What You Get

After running the pipeline, you'll have:

```
✓ Trained ML model (Random Forest by default)
✓ Evaluation metrics (Accuracy, Precision, Recall, F1, ROC-AUC)
✓ Cross-validation results
✓ Feature importance rankings
✓ Confusion matrix visualization
✓ ROC curve plot
✓ Complete experiment tracking in MLflow
```

## 🔄 Try Different Settings

### Change Algorithm

Edit `params.yaml`:
```yaml
model:
  algorithm: xgboost  # or logistic_regression
```

Run again:
```bash
dvc repro
```

### Adjust Hyperparameters

Edit `params.yaml`:
```yaml
model:
  random_forest:
    n_estimators: 200  # Change from 100
    max_depth: 15      # Change from 10
```

Run again:
```bash
dvc repro
```

MLflow will track all experiments automatically!

## 📊 Quick Commands Reference

| Command | Purpose |
|---------|---------|
| `dvc repro` | Run complete pipeline |
| `dvc status` | Check pipeline status |
| `dvc dag` | View pipeline structure |
| `mlflow ui` | Launch experiment tracking UI |
| `dvc repro <stage>` | Run specific stage only |

## 🆘 Troubleshooting

**Pipeline fails?**
```bash
dvc status  # Check what's missing
```

**Want to start fresh?**
```bash
dvc repro --force  # Rerun everything
```

**MLflow not showing experiments?**
```bash
mlflow ui --backend-store-uri ./mlruns
```

## 📚 Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Explore [params.yaml](params.yaml) for all configuration options
3. Check [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
4. Experiment with different algorithms and hyperparameters!

## 💡 Pro Tips

- Use `dvc dag` to visualize pipeline dependencies
- Compare experiments in MLflow to find best model
- Modify `params.yaml` for easy experimentation
- Check logs for detailed execution information
- Use `dvc repro <stage>` to run only changed stages

---

**Questions?** Open an issue on GitHub!

**Ready for more?** See the complete [README.md](README.md)
