"""
Project Initialization and Validation Script
Checks dependencies and validates project structure
"""

import sys
import subprocess
import os
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.8 or higher"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor} detected. Requires 3.8+")
        return False


def check_package(package_name):
    """Check if a Python package is installed"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False


def check_dependencies():
    """Check if required packages are installed"""
    print("\nChecking required packages...")
    
    required_packages = [
        'pandas', 'numpy', 'sklearn', 'xgboost', 
        'mlflow', 'dvc', 'yaml', 'joblib'
    ]
    
    missing_packages = []
    for package in required_packages:
        if package == 'yaml':
            package_import = 'yaml'
        elif package == 'sklearn':
            package_import = 'sklearn'
        else:
            package_import = package
        
        if check_package(package_import):
            print(f"✓ {package}")
        else:
            print(f"✗ {package} not installed")
            missing_packages.append(package)
    
    return len(missing_packages) == 0, missing_packages


def check_directory_structure():
    """Check if required directories exist"""
    print("\nChecking directory structure...")
    
    required_dirs = [
        'src',
        'data',
        'data/raw',
        'data/processed',
        'models'
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✓ {dir_path}/")
        else:
            print(f"✗ {dir_path}/ not found")
            all_exist = False
            # Create missing directories
            os.makedirs(dir_path, exist_ok=True)
            print(f"  → Created {dir_path}/")
    
    return all_exist


def check_required_files():
    """Check if required files exist"""
    print("\nChecking required files...")
    
    required_files = [
        'params.yaml',
        'dvc.yaml',
        'requirements.txt',
        'README.md',
        'src/data_loading.py',
        'src/data_preprocessing.py',
        'src/feature_engineering.py',
        'src/model_training.py',
        'src/model_evaluation.py'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} not found")
            all_exist = False
    
    return all_exist


def check_git():
    """Check if Git is initialized"""
    print("\nChecking Git...")
    
    if os.path.exists('.git'):
        print("✓ Git repository initialized")
        return True
    else:
        print("✗ Git repository not initialized")
        print("  Run: git init")
        return False


def check_dvc():
    """Check if DVC is initialized"""
    print("\nChecking DVC...")
    
    if os.path.exists('.dvc'):
        print("✓ DVC initialized")
        return True
    else:
        print("✗ DVC not initialized")
        print("  Run: dvc init")
        return False


def validate_params_yaml():
    """Validate params.yaml structure"""
    print("\nValidating params.yaml...")
    
    try:
        import yaml
        with open('params.yaml', 'r') as f:
            params = yaml.safe_load(f)
        
        required_sections = ['data', 'preprocessing', 'feature_engineering', 'model', 'evaluation', 'mlflow']
        
        all_present = True
        for section in required_sections:
            if section in params:
                print(f"✓ Section '{section}' found")
            else:
                print(f"✗ Section '{section}' missing")
                all_present = False
        
        return all_present
    except Exception as e:
        print(f"✗ Error reading params.yaml: {e}")
        return False


def print_summary(checks):
    """Print validation summary"""
    print("\n" + "="*50)
    print("VALIDATION SUMMARY")
    print("="*50)
    
    passed = sum(checks.values())
    total = len(checks)
    
    for check_name, result in checks.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {check_name}")
    
    print("="*50)
    print(f"Result: {passed}/{total} checks passed")
    print("="*50)
    
    if passed == total:
        print("\n🎉 All checks passed! Project is ready to use.")
        print("\nNext steps:")
        print("1. Activate virtual environment:")
        print("   - Windows: venv\\Scripts\\activate")
        print("   - macOS/Linux: source venv/bin/activate")
        print("2. Run pipeline: dvc repro")
        print("3. View results: mlflow ui")
        return True
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\nTo install missing packages:")
        print("  pip install -r requirements.txt")
        return False


def main():
    """Main validation function"""
    print("="*50)
    print("PROJECT VALIDATION SCRIPT")
    print("Customer Purchase Prediction Pipeline")
    print("="*50)
    
    checks = {
        'Python Version (3.8+)': check_python_version(),
        'Required Packages': check_dependencies()[0],
        'Directory Structure': check_directory_structure(),
        'Required Files': check_required_files(),
        'Git Repository': check_git(),
        'DVC Initialization': check_dvc(),
        'Configuration File': validate_params_yaml()
    }
    
    success = print_summary(checks)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
