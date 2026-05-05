# VectorCross X - Complete Project Structure

## Project Overview

VectorCross X is a comprehensive cyber intelligence engine that implements cross-layer threat intelligence sharing between attack simulation and defense systems. The project consists of two main components that work together to provide unified cybersecurity protection.

## Project Architecture

```
VectorCross-X/
├── README.md                           # Main project documentation
├── PROJECT_SUMMARY.md                  # Executive summary
├── TECHNICAL_DOCS.md                   # Technical implementation details
├── INSTALLATION.md                     # Setup and installation guide
├── requirements.txt                    # Python dependencies
├── ml_ssh_attacker.py                  # Attack simulation layer
├── ML_Calculations.pdf                 # Mathematical foundations (22 pages)
├── Vector.rar                          # Complete project archive
│
└── Hybrid_SQLi_Project/                # Defense layer implementation
    ├── requirements.txt                # Defense layer dependencies
    ├── project_tree.txt               # Complete project structure
    │
    ├── src/                           # Source code directory
    │   ├── __init__.py
    │   ├── detector_service.py        # ML-based SQL injection detector
    │   ├── proxy_gateway.py           # Web interface and request proxy
    │   ├── secure_backend.py          # Safe database operations
    │   ├── train_model.py             # ML model training pipeline
    │   ├── dataset_generator.py       # Training data generation
    │   └── insert_sample_user.py      # Database setup utilities
    │
    ├── models/                        # ML models and data
    │   ├── model.joblib              # Trained ML model
    │   ├── vectorizer.joblib         # Text vectorizer
    │   ├── sqli_dataset.csv          # Training dataset
    │   ├── predictions.csv           # Detection logs
    │   ├── proxy_audit.log           # System audit logs
    │   └── test.db                   # SQLite test database
    │
    ├── templates/                     # Web interface templates
    │   └── index.html                # Main web interface
    │
    └── .venv/                        # Python virtual environment
        └── [Virtual environment files]
```

## Component Details

### 1. Attack Simulation Layer (`ml_ssh_attacker.py`)

**Purpose**: Simulates realistic SSH brute-force attacks using machine learning to generate threat intelligence.

**Key Features**:
- Machine learning-based password vulnerability prediction
- Ensemble model (Random Forest + Gradient Boosting)
- 15+ password feature extraction algorithms
- Real-time threat score generation (0-100%)
- Hydra integration for controlled attack simulation
- API communication with defense layer

**Technical Specifications**:
```python
# Model Configuration
RF_ESTIMATORS = 30              # Random Forest trees
GB_ESTIMATORS = 30              # Gradient Boosting trees
Ensemble Ratio = 60% RF + 40% GB

# Feature Engineering
- Password length and complexity
- Character type analysis (digits, special, case)
- Pattern recognition (sequences, years, common words)
- Entropy calculation and diversity metrics
```

### 2. Defense Layer (`Hybrid_SQLi_Project/`)

**Purpose**: Real-time SQL injection detection and prevention with cross-layer intelligence integration.

#### 2.1 Detector Service (`detector_service.py`)

**Core Functionality**:
- ML-based SQL injection detection
- Rule-based pattern matching
- Anomaly scoring algorithms
- Real-time threat assessment
- Decision logging and audit trails

**Detection Algorithm**:
```python
# Hybrid Detection Approach
ML_WEIGHT = 0.7                 # Machine learning component
ANOMALY_WEIGHT = 0.3            # Anomaly detection component
THRESHOLD = 0.6                 # Decision threshold

# Final Score Calculation
final_score = ML_WEIGHT * ml_prob + ANOMALY_WEIGHT * anomaly_score
decision = "block" if final_score >= THRESHOLD else "allow"
```

**Rule-Based Detection**:
- UNION SELECT attacks
- Comment-based injections (-- ; /* */)
- Boolean-based attacks (OR 1=1)
- Command execution attempts (xp_cmdshell, EXEC)

#### 2.2 Proxy Gateway (`proxy_gateway.py`)

**Functionality**:
- Web-based user interface
- Request interception and analysis
- Integration with detector service
- Safe query execution coordination
- Real-time attack blocking

**Architecture**:
```
User Input → Proxy Gateway → Detector Service → Decision → Backend/Block
```

#### 2.3 Secure Backend (`secure_backend.py`)

**Features**:
- Parameterized query execution
- SQLite database management
- Safe query processing
- Database setup and initialization

#### 2.4 ML Training Pipeline (`train_model.py`)

**Capabilities**:
- Automated model training
- Feature extraction pipeline
- TF-IDF vectorization with character n-grams
- Random Forest classifier training
- Model evaluation and metrics
- Artifact serialization (joblib)

**Training Configuration**:
```python
# Model Parameters
n_estimators = 200              # Random Forest trees
max_depth = 12                  # Tree depth limit
TF-IDF Features = 4000          # Maximum features
N-gram Range = (3, 5)           # Character n-grams
Test Split = 25%                # Validation split
```

### 3. Cross-Layer Intelligence Bridge

**Communication Protocol**:
```python
# Threat Score API Payload
{
    "threat_score": int,        # 0-100% threat assessment
    "source": "ssh-ml-bruteforce",
    "details": {
        "top": [                # Top predicted passwords
            ["password", score],
            ...
        ]
    }
}
```

**Integration Points**:
- Attack layer generates threat scores
- Defense layer receives and processes intelligence
- Adaptive threshold adjustment based on threat level
- Real-time cross-layer communication via REST API

## System Workflow

### 1. Attack Simulation Workflow
```
Password Dataset → Feature Extraction → ML Prediction → Threat Scoring → API Transmission → Hydra Attack
```

### 2. Defense Workflow
```
User Input → Proxy Gateway → Detector Service → ML Analysis + Rule Check → Decision → Execute/Block
```

### 3. Cross-Layer Intelligence Flow
```
SSH Attack Intelligence → Threat Score API → Defense Layer → Adaptive Security Posture
```

## Key Innovations

### 1. Hybrid Detection Approach
- Combines machine learning with rule-based detection
- Ensemble model for improved accuracy
- Multi-dimensional feature analysis

### 2. Cross-Layer Intelligence Sharing
- Real-time threat score communication
- Adaptive defense mechanisms
- Unified security posture across attack vectors

### 3. Comprehensive Feature Engineering
- 15+ password characteristics analysis
- Entropy and complexity calculations
- Pattern recognition algorithms
- Behavioral analysis metrics

## Performance Metrics

### Attack Simulation Layer
- **Prediction Accuracy**: 85%+ password vulnerability assessment
- **Feature Processing**: 15+ characteristics per password
- **Response Time**: <100ms threat score generation
- **Model Performance**: F1 Score > 0.85

### Defense Layer
- **Detection Accuracy**: 95%+ SQL injection identification
- **False Positive Rate**: <5% for legitimate queries
- **Processing Speed**: Real-time query analysis
- **Threat Blocking**: Automatic prevention before database access

## Deployment Architecture

### Development Environment
```bash
# Attack Layer
python ml_ssh_attacker.py          # Port: Attack simulation

# Defense Layer
python src/detector_service.py     # Port: 9000 (Detector API)
python src/proxy_gateway.py        # Port: 5000 (Web Interface)
```

### Production Considerations
- Containerized deployment (Docker)
- Load balancing for high availability
- Secure API communication (HTTPS/TLS)
- Database encryption and backup
- Comprehensive logging and monitoring

## Security Features

### Attack Layer Security
- Controlled environment testing only
- Ethical hacking guidelines compliance
- Responsible disclosure practices
- Limited scope and target restrictions

### Defense Layer Security
- Parameterized query execution
- Input validation and sanitization
- Comprehensive audit logging
- Real-time threat monitoring
- Automatic attack prevention

## Future Enhancements

### Planned Features
1. **Deep Learning Integration**: LSTM/GRU models for sequential analysis
2. **Behavioral Biometrics**: User behavior pattern analysis
3. **Zero-Day Detection**: Unknown attack pattern identification
4. **Cloud Integration**: Multi-cloud security orchestration
5. **Federated Learning**: Distributed threat intelligence

### Research Directions
1. **Quantum-Resistant Security**: Future-proof encryption methods
2. **AI-Powered Forensics**: Automated incident analysis
3. **Predictive Security**: Proactive threat prevention
4. **Cross-Platform Integration**: Universal security framework

---

**Academic Institution**: RV University - School of Computer Science and Engineering  
**Faculty Guidance**: Prof. Sunil Kumar J, Dr. Basavaraj Patil  
**Presentation**: Cyber Security Day, RV University  
**Repository**: https://github.com/Aryakanduri1992/VectorCross-X-Cyber-Intelligence-Engine