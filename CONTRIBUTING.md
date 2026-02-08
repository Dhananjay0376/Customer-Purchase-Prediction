# Contributing to Customer Purchase Prediction Pipeline

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## 🎯 Project Goals

This project aims to demonstrate MLOps best practices for building automated, reproducible machine learning pipelines. Contributions should align with these goals:

- Maintain clean, modular code architecture
- Preserve pipeline automation and reproducibility
- Follow ML engineering best practices
- Keep documentation up-to-date

## 🚀 Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/your-username/customer-purchase-prediction.git
   cd customer-purchase-prediction
   ```
3. **Set up development environment**
   ```bash
   ./setup.sh
   ```

## 🔧 Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

Follow these principles:
- Keep each module focused on a single responsibility
- Add logging for important operations
- Update `params.yaml` for new configurable parameters
- Maintain DVC pipeline dependencies

### 3. Test Your Changes

```bash
# Run the complete pipeline
dvc repro

# Verify all stages complete successfully
dvc status
```

### 4. Update Documentation

- Update README.md if you add new features
- Add docstrings to new functions
- Update params.yaml comments

### 5. Commit Your Changes

```bash
git add .
git commit -m "feat: add your feature description"
```

Follow conventional commit messages:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation updates
- `refactor:` Code refactoring
- `test:` Test additions

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## 📋 Contribution Ideas

### New Features
- Add support for more ML algorithms
- Implement automated hyperparameter tuning
- Add more feature engineering techniques
- Create data drift detection
- Add model monitoring capabilities

### Improvements
- Optimize data loading for large datasets
- Add more comprehensive error handling
- Improve visualization quality
- Add unit tests and integration tests
- Create Docker containerization

### Documentation
- Add usage examples
- Create tutorials for specific scenarios
- Improve code comments
- Add architecture diagrams

## 🧪 Code Standards

### Python Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Keep functions focused and small
- Add type hints where appropriate

### Module Structure
Each pipeline stage should:
- Have a main() function
- Load parameters using load_params()
- Include comprehensive logging
- Handle errors gracefully

### Configuration
- Add new parameters to params.yaml
- Provide sensible defaults
- Document parameter purposes

## 📝 Pull Request Guidelines

Your PR should:
- Have a clear title and description
- Reference any related issues
- Include updated documentation
- Pass all pipeline stages
- Be focused on a single feature/fix

## 🐛 Reporting Issues

When reporting issues, include:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)
- Relevant logs or error messages

## 💡 Questions?

Feel free to:
- Open an issue for questions
- Start a discussion for ideas
- Reach out to maintainers

## 📜 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Focus on what's best for the project

## 🙏 Thank You!

Every contribution, no matter how small, is valued and appreciated!
