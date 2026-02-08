"""
Model Evaluation Module
Handles model evaluation and metrics tracking
"""

import pandas as pd
import numpy as np
import yaml
import logging
import os
import mlflow
import mlflow.sklearn
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, roc_auc_score, confusion_matrix,
    classification_report, roc_curve
)
from sklearn.model_selection import cross_val_score
import joblib
import json
import matplotlib.pyplot as plt
import seaborn as sns

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_params(params_path='params.yaml'):
    """Load parameters from yaml file"""
    with open(params_path, 'r') as f:
        params = yaml.safe_load(f)
    return params


def load_model(model_path='models/model.pkl'):
    """Load trained model"""
    logger.info(f"Loading model from {model_path}")
    model = joblib.load(model_path)
    return model


def evaluate_model(model, X_test, y_test, params):
    """Evaluate model and calculate metrics"""
    logger.info("Evaluating model...")
    
    # Make predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    metrics = {}
    
    if 'accuracy' in params['evaluation']['metrics']:
        metrics['accuracy'] = accuracy_score(y_test, y_pred)
    
    if 'precision' in params['evaluation']['metrics']:
        metrics['precision'] = precision_score(y_test, y_pred, average='binary')
    
    if 'recall' in params['evaluation']['metrics']:
        metrics['recall'] = recall_score(y_test, y_pred, average='binary')
    
    if 'f1_score' in params['evaluation']['metrics']:
        metrics['f1_score'] = f1_score(y_test, y_pred, average='binary')
    
    if 'roc_auc' in params['evaluation']['metrics']:
        metrics['roc_auc'] = roc_auc_score(y_test, y_pred_proba)
    
    logger.info(f"\nTest Set Metrics:")
    for metric_name, metric_value in metrics.items():
        logger.info(f"{metric_name}: {metric_value:.4f}")
    
    # Classification report
    logger.info(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    logger.info(f"\nConfusion Matrix:\n{cm}")
    
    return metrics, y_pred, y_pred_proba, cm


def cross_validate_model(model, X_train, y_train, params):
    """Perform cross-validation"""
    logger.info("Performing cross-validation...")
    
    cv_folds = params['evaluation']['cv_folds']
    
    cv_scores = {}
    
    # Accuracy
    scores = cross_val_score(model, X_train, y_train, cv=cv_folds, scoring='accuracy')
    cv_scores['cv_accuracy_mean'] = scores.mean()
    cv_scores['cv_accuracy_std'] = scores.std()
    
    # Precision
    scores = cross_val_score(model, X_train, y_train, cv=cv_folds, scoring='precision')
    cv_scores['cv_precision_mean'] = scores.mean()
    cv_scores['cv_precision_std'] = scores.std()
    
    # Recall
    scores = cross_val_score(model, X_train, y_train, cv=cv_folds, scoring='recall')
    cv_scores['cv_recall_mean'] = scores.mean()
    cv_scores['cv_recall_std'] = scores.std()
    
    # F1
    scores = cross_val_score(model, X_train, y_train, cv=cv_folds, scoring='f1')
    cv_scores['cv_f1_mean'] = scores.mean()
    cv_scores['cv_f1_std'] = scores.std()
    
    logger.info(f"\nCross-Validation Results ({cv_folds} folds):")
    for metric_name, metric_value in cv_scores.items():
        logger.info(f"{metric_name}: {metric_value:.4f}")
    
    return cv_scores


def plot_confusion_matrix(cm, output_path='models/confusion_matrix.png'):
    """Plot and save confusion matrix"""
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    logger.info(f"Confusion matrix plot saved to {output_path}")


def plot_roc_curve(y_test, y_pred_proba, output_path='models/roc_curve.png'):
    """Plot and save ROC curve"""
    fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    logger.info(f"ROC curve plot saved to {output_path}")


def log_to_mlflow(metrics, cv_scores):
    """Log metrics to MLflow"""
    logger.info("Logging metrics to MLflow...")
    
    experiment_name = "customer_purchase_prediction"
    mlflow.set_experiment(experiment_name)
    
    # Get the last run
    runs = mlflow.search_runs(experiment_names=[experiment_name], order_by=["start_time DESC"], max_results=1)
    
    if len(runs) > 0:
        run_id = runs.iloc[0]['run_id']
        
        with mlflow.start_run(run_id=run_id):
            # Log test metrics
            for metric_name, metric_value in metrics.items():
                mlflow.log_metric(f"test_{metric_name}", metric_value)
            
            # Log CV metrics
            for metric_name, metric_value in cv_scores.items():
                mlflow.log_metric(metric_name, metric_value)
            
            # Log artifacts
            if os.path.exists('models/confusion_matrix.png'):
                mlflow.log_artifact('models/confusion_matrix.png')
            if os.path.exists('models/roc_curve.png'):
                mlflow.log_artifact('models/roc_curve.png')
            if os.path.exists('models/feature_importance.csv'):
                mlflow.log_artifact('models/feature_importance.csv')
            
            logger.info(f"Metrics logged to MLflow run: {run_id}")


def save_metrics(metrics, cv_scores, output_path='models/metrics.json'):
    """Save metrics to JSON file"""
    all_metrics = {**metrics, **cv_scores}
    
    with open(output_path, 'w') as f:
        json.dump(all_metrics, f, indent=4)
    
    logger.info(f"Metrics saved to {output_path}")


def main():
    """Main execution function"""
    logger.info("Starting model evaluation stage...")
    
    # Load parameters
    params = load_params()
    
    # Load test data
    test_path = params['data']['test_data_path']
    logger.info(f"Loading test data from {test_path}")
    test_data = pd.read_csv(test_path)
    
    # Load train data for cross-validation
    train_path = params['data']['train_data_path']
    logger.info(f"Loading train data from {train_path}")
    train_data = pd.read_csv(train_path)
    
    # Separate features and target
    target_col = params['feature_engineering']['target_column']
    X_test = test_data.drop(target_col, axis=1)
    y_test = test_data[target_col]
    X_train = train_data.drop(target_col, axis=1)
    y_train = train_data[target_col]
    
    # Load model
    model = load_model()
    
    # Evaluate model
    metrics, y_pred, y_pred_proba, cm = evaluate_model(model, X_test, y_test, params)
    
    # Cross-validation
    cv_scores = cross_validate_model(model, X_train, y_train, params)
    
    # Create visualizations
    os.makedirs('models', exist_ok=True)
    plot_confusion_matrix(cm)
    plot_roc_curve(y_test, y_pred_proba)
    
    # Save metrics
    save_metrics(metrics, cv_scores)
    
    # Log to MLflow
    log_to_mlflow(metrics, cv_scores)
    
    logger.info("Model evaluation completed successfully!")


if __name__ == "__main__":
    main()
