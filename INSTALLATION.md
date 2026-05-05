# VectorCross X - Installation Guide

## Prerequisites

### System Requirements
- **Operating System**: Linux (Ubuntu 18.04+), macOS, or Windows with WSL
- **Python Version**: 3.8 or higher
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: 2GB free space for datasets and dependencies
- **Network**: Internet connection for package installation

### Required Tools
- **Python Package Manager**: pip or conda
- **Version Control**: Git
- **Security Tools**: Hydra (for attack simulation)
- **Text Editor**: Any preferred IDE or text editor

## Installation Steps

### 1. Clone the Repository
```bash
git clone https://github.com/Aryakanduri1992/VectorCross-X-Cyber-Intelligence-Engine.git
cd VectorCross-X-Cyber-Intelligence-Engine
```

### 2. Create Virtual Environment (Recommended)
```bash
# Using venv
python3 -m venv vectorcross_env
source vectorcross_env/bin/activate  # On Windows: vectorcross_env\Scripts\activate

# Using conda
conda create -n vectorcross python=3.8
conda activate vectorcross
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Security Tools

#### For Ubuntu/Debian:
```bash
sudo apt update
sudo apt install hydra
```

#### For macOS:
```bash
brew install hydra
```

#### For Windows (WSL):
```bash
sudo apt update
sudo apt install hydra
```

### 5. Download Password Datasets

#### RockYou Dataset (Required)
```bash
# Download RockYou wordlist
wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt
mv rockyou.txt rockyou_2025_00.txt
```

#### Create Custom Password List
```bash
# Create a sample passwords.txt file
cat > passwords.txt << EOF
admin
password
123456
password123
admin123
root
test
user
guest
welcome
EOF
```

## Configuration

### 1. Network Configuration
Edit the target configuration in `ml_ssh_attacker.py`:
```python
# Update these values for your test environment
TARGET_IP = "192.168.64.3"      # Your test server IP
USERNAME = "ubuntu"              # Test username
```

### 2. API Configuration
Ensure the Flask API endpoint is configured:
```python
# Default API endpoint
API_ENDPOINT = "http://localhost:5000/api/threat_score"
```

### 3. Test Environment Setup

#### SSH Server Setup (For Testing)
```bash
# Install SSH server (Ubuntu)
sudo apt install openssh-server
sudo systemctl start ssh
sudo systemctl enable ssh

# Create test user
sudo useradd -m testuser
echo "testuser:weakpassword" | sudo chpasswd
```

#### Defense Layer API (Mock Setup)
```python
# Simple Flask API for testing (save as api_server.py)
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/threat_score', methods=['POST'])
def receive_threat_score():
    data = request.json
    print(f"Received threat score: {data}")
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
```

## Verification

### 1. Test Python Environment
```bash
python3 -c "import numpy, pandas, sklearn, requests; print('All dependencies installed successfully')"
```

### 2. Test Security Tools
```bash
hydra -h | head -5
```

### 3. Test Dataset Loading
```bash
python3 -c "
with open('rockyou_2025_00.txt', 'r', encoding='utf-8', errors='ignore') as f:
    lines = sum(1 for _ in f)
    print(f'Dataset loaded: {lines} passwords')
"
```

## Running the System

### 1. Start Defense Layer API (Terminal 1)
```bash
python3 api_server.py
```

### 2. Run VectorCross X (Terminal 2)
```bash
python3 ml_ssh_attacker.py
```

### Expected Output
```
[*] Training ML model...

MODEL METRICS
Accuracy: 0.85
Precision: 0.82
Recall: 0.88
F1: 0.85

Top 10 Password Predictions:

1. admin -> 89%
2. password -> 85%
3. 123456 -> 82%
...

[+] Threat score sent: 200
[*] Running Hydra...
```

## Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# If sklearn import fails
pip install --upgrade scikit-learn

# If pandas import fails
pip install --upgrade pandas
```

#### 2. Hydra Not Found
```bash
# Check if hydra is in PATH
which hydra

# If not found, install using package manager
sudo apt install hydra  # Ubuntu
brew install hydra      # macOS
```

#### 3. Permission Denied (SSH)
```bash
# Check SSH service status
sudo systemctl status ssh

# Restart SSH service
sudo systemctl restart ssh
```

#### 4. API Connection Failed
```bash
# Check if Flask API is running
curl -X POST http://localhost:5000/api/threat_score \
  -H "Content-Type: application/json" \
  -d '{"threat_score": 50, "source": "test"}'
```

### Dataset Issues

#### Large Dataset Memory Error
```python
# Reduce sample size in ml_ssh_attacker.py
sample_size = min(100, len(COMMON_PASSWORDS))  # Reduce from 300 to 100
```

#### Encoding Errors
```python
# The system handles multiple encodings automatically
# If issues persist, convert dataset to UTF-8:
iconv -f iso-8859-1 -t utf-8 rockyou.txt > rockyou_utf8.txt
```

## Security Considerations

### Ethical Usage
- **Test Environment Only**: Never run against production systems
- **Authorized Testing**: Ensure proper authorization for all testing
- **Responsible Disclosure**: Follow responsible disclosure practices

### Network Isolation
```bash
# Recommended: Use isolated test network
# Configure firewall rules to limit scope
sudo ufw enable
sudo ufw allow from 192.168.64.0/24 to any port 22
```

## Performance Tuning

### Memory Optimization
```python
# Adjust sample sizes based on available memory
RF_ESTIMATORS = 20      # Reduce from 30 if memory limited
GB_ESTIMATORS = 20      # Reduce from 30 if memory limited
```

### Processing Speed
```python
# Enable parallel processing
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(n_estimators=30, n_jobs=-1)  # Use all CPU cores
```

## Development Setup

### IDE Configuration
```bash
# VS Code with Python extension
code .

# PyCharm
pycharm-community .
```

### Debugging
```python
# Enable verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Next Steps

After successful installation:
1. Review the [Technical Documentation](TECHNICAL_DOCS.md)
2. Read the [Project Summary](PROJECT_SUMMARY.md)
3. Explore the ML model implementation
4. Customize for your specific use case
5. Contribute improvements to the project

## Support

For installation issues or technical questions:
- Check the troubleshooting section above
- Review the technical documentation
- Submit issues on the GitHub repository
- Contact the development team at RV University

---

**Installation Guide Version**: 1.0  
**Last Updated**: Cyber Security Day 2024  
**Maintained by**: RV University CSE Team