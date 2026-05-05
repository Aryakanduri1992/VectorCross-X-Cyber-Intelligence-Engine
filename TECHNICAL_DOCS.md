# VectorCross X - Technical Documentation

## System Architecture Overview

VectorCross X implements a novel cross-layer cyber intelligence architecture that bridges the gap between attack simulation and defense mechanisms through real-time threat intelligence sharing.

## Core Components

### 1. Machine Learning Attack Simulator (`ml_ssh_attacker.py`)

#### Purpose
Simulates realistic SSH brute-force attacks using machine learning to predict password vulnerability and generate threat intelligence.

#### Technical Specifications
```python
# Model Architecture
Random Forest Regressor: 30 estimators, max_depth=8
Gradient Boosting Regressor: 30 estimators, max_depth=4
Ensemble Combination: 60% RF + 40% GB predictions
Feature Scaling: StandardScaler normalization
```

#### Feature Engineering Pipeline
The system extracts 15+ features from each password:

1. **Basic Metrics**
   - Password length
   - Character type counts (digits, uppercase, lowercase, special)
   - Character type presence flags

2. **Pattern Analysis**
   - Mixed case detection
   - Common word identification (admin, pass, user, test, root)
   - Year pattern matching (19xx, 20xx)
   - Sequential character detection

3. **Complexity Measures**
   - Character diversity ratio
   - Entropy calculation
   - Uniqueness assessment

#### ML Model Training Process
```python
def train_password_model():
    # 1. Sample password dataset (300 samples for efficiency)
    # 2. Extract features for each password
    # 3. Generate synthetic labels based on complexity
    # 4. Train ensemble models (RF + GB)
    # 5. Validate performance metrics
    # 6. Return trained models and preprocessing pipeline
```

#### Threat Score Generation
- **Input**: Password candidates from wordlists
- **Processing**: Feature extraction → ML prediction → Ensemble scoring
- **Output**: Ranked list of passwords with threat scores (0-100%)
- **API Integration**: Automatic threat score transmission to defense layer

### 2. Cross-Layer Intelligence API

#### Communication Protocol
```python
# Threat Score Payload Structure
{
    "threat_score": int,        # 0-100% threat assessment
    "source": "ssh-ml-bruteforce",
    "details": {
        "top": [                # Top 5 predicted passwords
            ["password", score],
            ...
        ]
    }
}
```

#### API Endpoint
- **URL**: `http://localhost:5000/api/threat_score`
- **Method**: POST
- **Content-Type**: application/json
- **Response**: HTTP status code confirmation

### 3. Defense Layer Integration

#### SQL Injection Detection System
The defense layer (developed under Dr. Basavaraj Patil's guidance) implements:

1. **Real-Time Query Analysis**
   - Pattern-based SQL injection detection
   - Behavioral analysis of login attempts
   - Source IP monitoring and profiling

2. **Threat Intelligence Integration**
   - Receives threat scores from attack simulation layer
   - Adjusts detection thresholds based on current threat level
   - Implements adaptive security posture

3. **Automated Response Mechanisms**
   - Automatic IP blocking for suspicious sources
   - Query termination before database execution
   - Real-time alert generation

## Implementation Details

### Password Dataset Processing
```python
def load_common_passwords(file_path):
    # Multi-encoding support for various password files
    encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
    # Robust file loading with fallback encoding detection
```

### Attack Simulation Workflow
1. **Model Training**: Train ML models on password datasets
2. **Password Analysis**: Extract features and predict vulnerability
3. **Threat Scoring**: Generate ranked threat assessments
4. **Intelligence Sharing**: Transmit scores to defense layer
5. **Attack Execution**: Controlled Hydra-based SSH attacks

### Security Considerations

#### Ethical Implementation
- **Controlled Environment**: Attacks limited to designated test systems
- **Educational Purpose**: Designed for security research and training
- **Responsible Disclosure**: Academic presentation and documentation

#### Safety Mechanisms
- **Target Limitation**: Hardcoded target IP restrictions
- **Credential Scope**: Limited to test credentials only
- **Rate Limiting**: Controlled attack frequency (1 thread)

## Performance Optimization

### Model Efficiency
- **Sample Size Optimization**: 300-sample training for speed/accuracy balance
- **Feature Selection**: 15 most predictive password characteristics
- **Ensemble Weighting**: Optimized RF/GB combination ratios

### Scalability Features
- **Concurrent Processing**: Multi-threaded threat assessment capability
- **Memory Management**: Efficient dataset handling and processing
- **API Responsiveness**: <100ms threat score generation

## Integration Architecture

### System Flow
```
Password Input → Feature Extraction → ML Prediction → Threat Scoring → API Transmission → Defense Layer → Automated Response
```

### Cross-Layer Communication
1. **Attack Layer**: Generates threat intelligence
2. **Intelligence Bridge**: RESTful API communication
3. **Defense Layer**: Receives and acts on threat data
4. **Feedback Loop**: Continuous learning and adaptation

## Deployment Configuration

### Environment Requirements
```bash
# Python Environment
Python 3.8+
Virtual environment recommended

# Core Dependencies
numpy>=1.21.0
pandas>=1.3.0
scikit-learn>=1.0.0
requests>=2.25.0

# Security Tools
hydra (for attack simulation)
SSH client/server setup
```

### Configuration Parameters
```python
# Target Configuration
TARGET_IP = "192.168.64.3"      # Test environment IP
USERNAME = "ubuntu"              # Test username
PASSWORD_FILE = "passwords.txt"  # Custom password list
COMMON_PASSWORDS_FILE = "rockyou_2025_00.txt"  # Large dataset

# Model Parameters
RF_ESTIMATORS = 30               # Random Forest trees
GB_ESTIMATORS = 30               # Gradient Boosting trees
```

## Monitoring and Metrics

### Performance Indicators
- **Prediction Accuracy**: Model performance on test datasets
- **Threat Score Distribution**: Range and variance of generated scores
- **API Response Time**: Intelligence transmission latency
- **Defense Activation Rate**: Frequency of automated responses

### Logging and Debugging
```python
# Threat Score Transmission Logging
print(f"[+] Threat score sent: {response.status_code}")
print(f"[!] Failed to send threat score: {e}")

# Model Performance Metrics
print("Accuracy:", accuracy_score(y_test_clf, preds_bin))
print("Precision:", precision_score(y_test_clf, preds_bin))
print("Recall:", recall_score(y_test_clf, preds_bin))
print("F1:", f1_score(y_test_clf, preds_bin))
```

## Future Technical Enhancements

### Advanced ML Integration
- **Deep Learning Models**: LSTM/GRU for sequential pattern analysis
- **Transfer Learning**: Pre-trained models for enhanced accuracy
- **Federated Learning**: Distributed training across multiple environments

### Enhanced Security Features
- **Behavioral Biometrics**: User behavior pattern analysis
- **Zero-Day Detection**: Unknown attack pattern identification
- **Quantum-Resistant Algorithms**: Future-proof security measures

### Scalability Improvements
- **Microservices Architecture**: Containerized deployment
- **Cloud Integration**: Multi-cloud security orchestration
- **Real-Time Processing**: Stream processing for continuous analysis

---

**Technical Lead**: Prof. Sunil Kumar J  
**Defense System Lead**: Dr. Basavaraj Patil  
**Institution**: RV University - School of Computer Science and Engineering