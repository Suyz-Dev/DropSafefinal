<<<<<<< HEAD
# DROPSAFE

DROPSAFE is an AI-powered educational analytics platform designed to identify students at risk of dropping out and provide actionable insights for timely interventions.

## Overview

This application leverages machine learning algorithms to analyze student data including attendance, test scores, and fee status to predict dropout risk. It provides specialized dashboards for different user roles: Students, Teachers, and Counselors.

## Features

- Multi-role dashboard system with tailored analytics for each user type
- AI-powered risk assessment using machine learning models
- Real-time student performance monitoring
- Interactive data visualization and reporting
- Comprehensive intervention recommendations
- User authentication and role-based access control

## Technology Stack

- Python 3.8+
- Streamlit for web interface
- Pandas for data manipulation
- Scikit-learn for machine learning
- Plotly for interactive visualizations
- NumPy for numerical computing
- Joblib for model serialization

## Installation

1. Clone the repository:
```
git clone https://github.com/Suyz-Dev/DROPSAFE.git
cd DROPSAFE
```

2. Create a virtual environment:
```
python -m venv venv
```

3. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
```
pip install -r requirements.txt
```

## Usage

1. Generate sample data (optional):
```
python create_data.py
```

2. Train the machine learning model:
```
python train_model.py
```

3. Run the application:
```
streamlit run app_new.py
```

4. Open your web browser and navigate to `http://localhost:8502`

## File Structure

- `app_new.py` - Main Streamlit application
- `create_data.py` - Data generation script
- `create_model.py` - Model creation script
- `train_model.py` - Model training script
- `test_simple.py` - Simple testing utilities
- `requirements.txt` - Python dependencies
- `users_data.json` - User authentication data

## User Roles

### Student Dashboard
- Personal risk assessment
- Academic performance tracking
- Attendance monitoring
- Personalized recommendations

### Teacher Dashboard
- Classroom analytics
- At-risk student identification
- Performance distribution analysis
- Class overview metrics

### Counselor Dashboard
- Institution-wide analytics
- Advanced risk analysis
- Intervention planning tools
- Comprehensive reporting

## Data Requirements

The system analyzes three main data types:
- Attendance records (percentage)
- Test scores (numerical)
- Fee status (Paid/Pending/Overdue)

## Model Information

The application uses a Random Forest classifier to predict dropout risk based on:
- Student attendance patterns
- Academic performance metrics
- Financial status indicators

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is developed for educational purposes.

## Support

For questions or support, please contact the development team.
=======
# DropSafe - Advanced Student Risk Assessment System 🚀

A comprehensive **Machine Learning-powered platform** for identifying at-risk students and providing intelligent guidance through interactive dashboards and AI-driven insights.

![DropSafe](https://img.shields.io/badge/Version-2.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)
![ML](https://img.shields.io/badge/ML-XGBoost%20%7C%20LightGBM%20%7C%20ScikitLearn-orange.svg)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red.svg)
![Deployment](https://img.shields.io/badge/Deployment-Docker%20%7C%20Cloud%20%7C%20Local-blue.svg)

## 🌟 Key Features

### 🧠 **Advanced Machine Learning**
- **Multiple ML Algorithms**: Logistic Regression, Random Forest, XGBoost, LightGBM, Gradient Boosting
- **Automatic Model Selection**: Finds the best performing algorithm for your data
- **Advanced Feature Engineering**: 26+ engineered features for better predictions
- **Model Interpretability**: SHAP explanations for prediction insights
- **Cross-Validation**: Robust model evaluation with stratified K-fold

### 📊 **Comprehensive Analytics**
- **Risk Classification**: 3-tier system (Safe 🟢, Medium Risk 🟠, High Risk 🔴)
- **Interactive Visualizations**: Plotly-powered charts and graphs
- **Performance Tracking**: Attendance, marks, and fees monitoring
- **Trend Analysis**: Historical patterns and risk evolution
- **Export Capabilities**: CSV downloads for further analysis

### 🔍 **Data Validation & Quality**
- **Comprehensive Validation**: Schema validation, data type checking, range validation
- **Quality Assessment**: Data completeness, validity scores, outlier detection
- **Missing Data Handling**: Smart imputation strategies
- **Business Rules**: Domain-specific validation rules
- **Quality Reports**: Detailed JSON reports with actionable insights

### 👨‍🏫 **Teacher Dashboard**
- **Bulk Data Upload**: CSV file processing with validation
- **Real-time Risk Assessment**: Instant ML-powered predictions
- **Visual Analytics**: Charts, scatter plots, distribution analysis
- **Filtering & Sorting**: Advanced data exploration tools
- **Action Recommendations**: Guided intervention strategies
- **Export Options**: Download student lists by risk level

### 🎓 **Student Portal**
- **Personalized Dashboard**: Individual risk assessment and metrics
- **AI Chatbot**: Intelligent guidance system with contextual responses
- **Performance Tracking**: Visual representation of academic standing
- **Quick Actions**: Fast access to help and resources
- **Feedback System**: Student satisfaction tracking
- **Emergency Contacts**: Quick access to support resources
- **Google Gemini Integration**: Advanced AI counseling powered by Google's Gemini model

### 🔧 **System Administration**
- **Health Monitoring**: System status and dependency checks
- **Model Management**: Training, evaluation, and deployment tools
- **Configuration**: Environment-specific settings
- **Logging**: Comprehensive activity tracking
- **Performance Metrics**: System and model performance monitoring

## 🤖 Google Gemini Integration

DropSafe now supports advanced AI counseling through Google Gemini! This integration enhances the student counseling experience with more sophisticated and contextual responses.

### Setup Instructions

1. **Get Google API Key**:
   - Visit [Google AI Studio](https://aistudio.google.com/)
   - Sign in with your Google account
   - Create a new API key
   - Copy the API key for later use

2. **Configure the Application**:
   - Set the `GOOGLE_API_KEY` environment variable
   - Or run the setup script: `streamlit run setup_gemini.py`

3. **Restart the Application**:
   - The AI counselor will automatically use Gemini when the API key is configured

### Features

- **Enhanced Counseling Responses**: More natural and contextual conversations
- **Personalized Support**: Tailored advice based on student concerns
- **Fallback Mechanism**: Automatic fallback to local responses if Gemini is unavailable
- **Privacy Focused**: All conversations are processed securely through Google's API

### Benefits

- More empathetic and human-like responses
- Better understanding of complex student concerns
- Improved mental health support quality
- Seamless integration with existing counselor features

## 🚀 Deployment Options

### Local Deployment
Follow the manual setup instructions above for local development and testing.

### Docker Deployment (Recommended for Production)

1. **Prerequisites**:
   - Docker Engine 20.10+
   - Docker Compose 1.29+

2. **Deployment**:
   ```bash
   # Clone the repository
   git clone https://github.com/Suyz-Dev/DropSafe-.git
   cd DropSafe-
   
   # Build and run with Docker Compose
   docker-compose up -d
   
   # Check service status
   docker-compose ps
   ```

3. **Access Services**:
   - Main Page: http://localhost:8499
   - Teacher Dashboard: http://localhost:8501
   - Student Dashboard: http://localhost:8502
   - Counsellor Dashboard: http://localhost:8504

4. **Management**:
   ```bash
   # View logs
   docker-compose logs -f
   
   # Stop services
   docker-compose down
   
   # Update and restart
   git pull origin main
   docker-compose up -d --build
   ```

### Cloud Deployment

#### Streamlit Cloud (Easiest Option)
1. Fork this repository to your GitHub account
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Create a new app and connect it to your forked repository
4. Set the main file to `streamlit_main.py` (for simplified version) or `main_page.py` (for full version)
5. Use `requirements-streamlit.txt` as the requirements file
6. Deploy and share your app!

**Note**: The full version (`main_page.py`) includes redirects to localhost services that won't work on Streamlit Cloud. For a complete experience, use the simplified version (`streamlit_main.py`) or deploy locally.

#### Heroku
1. Install Heroku CLI
2. Create separate Heroku apps for each service
3. Deploy using Heroku Git deployment

#### AWS EC2
1. Launch Ubuntu 20.04+ instance
2. Install Docker and Docker Compose
3. Clone repository and run `docker-compose up -d`

#### Google Cloud Platform
1. Create Compute Engine instance
2. Install Docker and Docker Compose
3. Deploy using docker-compose

### Reverse Proxy Configuration (Production)

For production deployments with HTTPS, configure Nginx or Apache as a reverse proxy:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8499;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /teacher/ {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /student/ {
        proxy_pass http://localhost:8502;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /counsellor/ {
        proxy_pass http://localhost:8504;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🛡️ Security Considerations

1. **Authentication**: The application includes basic role-based authentication
2. **Data Protection**: Student data should be encrypted at rest
3. **Network Security**: Use HTTPS in production
4. **Access Control**: Restrict access to dashboards based on user roles
5. **Regular Updates**: Keep dependencies updated

## 📊 Monitoring and Maintenance

### Health Checks
- Check service status: Access `/healthz` endpoint on main page
- Monitor logs in `shared_data/` directory
- Set up alerts for high-risk student identification

### Backup Strategy
1. Regular backups of:
   - Student data files
   - Chat history
   - Risk assessment models
2. Store backups in secure, encrypted storage

### Performance Optimization
- Use a production WSGI server for high-traffic deployments
- Implement caching for frequently accessed data
- Monitor memory usage and optimize data loading

#### Prerequisites
- **Python 3.8 or higher** ([Download](https://www.python.org/downloads/))
- **Git** (optional, for cloning)
- **4GB RAM minimum** (8GB recommended for large datasets)

#### 1. Clone or Download
```bash
git clone <repository-url>
cd dropsafe
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv dropsafe_env
dropsafe_env\Scripts\activate

# Linux/Mac
python3 -m venv dropsafe_env
source dropsafe_env/bin/activate
```

#### 3. Install Dependencies
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install core dependencies
pip install -r requirements.txt

# For advanced ML features (optional)
pip install xgboost lightgbm imbalanced-learn shap

# For enhanced data validation (optional)
pip install pydantic pandera
```

#### 4. Generate Sample Data
```bash
python risk_model.py
```

#### 5. Launch the System
```bash
# Windows - Run individual dashboards or all at once
run.bat
# OR to run all dashboards simultaneously
run_all.bat

# Linux/Mac
./run.sh
# OR to run all dashboards simultaneously
./run_all.sh
```

## 🎯 Usage Guide

### Run All Dashboards
To run all dashboards simultaneously:
- **Windows**: Double-click `run_all.bat` or run `python run_all_dashboards.py`
- **Linux/Mac**: Run `./run_all.sh`

This will start all dashboards on their respective ports:
- Main Landing Page: http://localhost:8499
- Login Portal: http://localhost:8500
- Teacher Dashboard: http://localhost:8501
- Enhanced Student Portal: http://localhost:8502
- Original Student Portal: http://localhost:8503
- Counsellor Dashboard: http://localhost:8504

### Teacher Dashboard
1. **Launch**: Run `streamlit run teacher_dashboard.py` or use the launcher
2. **Access**: Open http://localhost:8501 in your browser
3. **Upload Data**: Use the CSV upload feature or generate sample data
4. **Analyze**: Review risk distributions, performance charts, and student lists
5. **Export**: Download filtered student data for interventions

### Student Portal
1. **Launch**: Run `streamlit run student_dashboard.py` or use the launcher
2. **Access**: Open http://localhost:8502 in your browser
3. **Login**: Use student ID (e.g., STU001 from sample data)
4. **Explore**: View personal dashboard and interact with AI chatbot
5. **Get Help**: Use quick action buttons for common queries

### Data Requirements

Your CSV file must contain these columns:

| Column | Type | Description | Example |
|--------|------|-------------|----------|
| `student_id` | String | Unique identifier | STU001 |
| `name` | String | Student name | John Doe |
| `attendance_percentage` | Float | Attendance (0-100) | 85.5 |
| `marks_percentage` | Float | Marks (0-100) | 72.3 |
| `fees_status` | String | Payment status | paid/pending |

**Optional columns**: email, phone, department, year, gender

## 🧠 Machine Learning Details

### Algorithms Implemented

1. **Logistic Regression**: Fast, interpretable baseline model
2. **Random Forest**: Ensemble method with feature importance
3. **Gradient Boosting**: Powerful sequential learning
4. **XGBoost**: Industry-standard gradient boosting
5. **LightGBM**: Fast, memory-efficient gradient boosting

### Feature Engineering

The system creates 26+ features including:
- **Risk Factors**: Attendance risk, marks risk, fees risk
- **Performance Metrics**: Academic risk, overall risk score
- **Interaction Features**: Attendance × marks, ratios
- **Categorical Encoding**: Performance categories
- **Derived Features**: Distance from ideal, consistency measures
- **Binary Flags**: High performer, at-risk indicators

### Model Selection
- **Automatic**: Trains all algorithms and selects the best performer
- **Cross-Validation**: 5-fold stratified validation
- **Metrics**: F1-weighted score, AUC-ROC, accuracy
- **Hyperparameter Tuning**: Grid search for optimal parameters

### Risk Classification

**Weighted Scoring System:**
- **Attendance (40%)**: < 60% = High Risk, < 75% = Medium Risk
- **Marks (40%)**: < 40% = High Risk, < 60% = Medium Risk  
- **Fees (20%)**: Pending = Additional Risk

**Final Classification:**
- **High Risk (🔴)**: Score ≥ 0.6 (Immediate intervention needed)
- **Medium Risk (🟠)**: Score ≥ 0.3 (Monitor closely)
- **Safe (🟢)**: Score < 0.3 (Performing well)

## 📁 File Structure

```
dropsafe/
├── 📄 README.md                    # This documentation
├── 📄 requirements.txt             # Python dependencies
├── 🐍 risk_model.py               # Advanced ML models and training
├── 🐍 data_validator.py           # Data validation and quality checks
├── 🎨 teacher_dashboard.py        # Main teacher interface
├── 🎨 student_dashboard.py        # Student portal
├── 📄 teacher_dashboard_demo.html # Demo interface
├── 🚀 run.bat                     # Windows launcher
├── 🚀 run.sh                      # Linux/Mac launcher
├── 🚀 run_all.bat                 # Windows - Run all dashboards
├── 🚀 run_all.sh                  # Linux/Mac - Run all dashboards
├── ⚙️ setup.bat                   # Windows automated setup
├── ⚙️ setup.sh                    # Linux/Mac automated setup
├── 📊 sample_students.csv         # Generated sample data
├── 🤖 advanced_risk_model.pkl     # Trained ML model
├── 📈 student_risk_predictions.csv # Model predictions
└── 📁 dropsafe_env/               # Virtual environment
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file for custom configuration:

```env
# Database settings (future enhancement)
DATABASE_URL=sqlite:///dropsafe.db

# ML Model settings
MODEL_ALGORITHM=auto  # auto, logistic, xgboost, lightgbm
CROSS_VALIDATION_FOLDS=5
TEST_SIZE=0.2

# Application settings
STREAMLIT_THEME=light
LOG_LEVEL=INFO
MAX_UPLOAD_SIZE=200MB

# Risk thresholds
HIGH_RISK_THRESHOLD=0.6
MEDIUM_RISK_THRESHOLD=0.3

# Feature engineering
USE_ADVANCED_FEATURES=true
HANDLE_CLASS_IMBALANCE=true
```

### Customization Options

1. **Risk Thresholds**: Modify classification boundaries
2. **Feature Selection**: Enable/disable specific features
3. **Model Choice**: Force specific algorithm usage
4. **Validation Rules**: Customize data validation criteria
5. **UI Themes**: Change dashboard appearance

## 📊 Performance Benchmarks

### Model Performance (Sample Data)
| Algorithm | CV Score | AUC | Training Time |
|-----------|----------|-----|---------------|
| Logistic Regression | 95.1% | 99.7% | ~1s |
| LightGBM | 95.0% | 97.2% | ~2s |
| XGBoost | 94.7% | 97.5% | ~3s |
| Random Forest | 92.4% | 98.4% | ~2s |
| Gradient Boosting | 89.6% | 98.1% | ~4s |

### System Performance
- **Dashboard Load Time**: < 3 seconds
- **Prediction Speed**: 1000+ students/second
- **Memory Usage**: ~500MB (base), ~1GB (with advanced ML)
- **Supported Data Size**: Up to 100,000 students

## 🛠️ Development

### Adding Custom Features

1. **New ML Algorithm**:
```python
# In risk_model.py, add to AdvancedRiskPredictor
self.available_algorithms['custom_algo'] = CustomClassifier()
```

2. **Custom Feature**:
```python
# In create_advanced_features method
features['custom_feature'] = your_calculation(df)
```

3. **New Validation Rule**:
```python
# In data_validator.py
self.validation_rules['custom_field'] = {
    'type': str,
    'required': True,
    'custom_check': your_validation_function
}
```

### Testing

```bash
# Run system health check
python -c "from risk_model import *; from data_validator import *; print('All imports successful')"

# Test with sample data
python risk_model.py
python data_validator.py

# Test dashboards
streamlit run teacher_dashboard.py --server.headless true
```

### Debugging

1. **Enable Debug Logging**:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. **Check Dependencies**:
```bash
pip list | grep -E "streamlit|pandas|sklearn|xgboost"
```

3. **Validate Data**:
```python
from data_validator import validate_csv_file
df_clean, report = validate_csv_file('your_data.csv')
```

## 🚨 Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Solution: Ensure virtual environment is activated
source dropsafe_env/bin/activate  # Linux/Mac
dropsafe_env\Scripts\activate     # Windows
```

**2. Streamlit Port Already in Use**
```bash
# Solution: Use different port
streamlit run teacher_dashboard.py --server.port 8503
```

**3. Memory Issues with Large Datasets**
```python
# Solution: Process data in chunks
chunk_size = 1000
for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    process_chunk(chunk)
```

**4. Model Training Fails**
```python
# Solution: Use simpler algorithm
predictor = AdvancedRiskPredictor(algorithm='logistic')
```

**5. CSV Upload Issues**
- Ensure CSV has required columns
- Check for special characters in data
- Verify file encoding (should be UTF-8)

### Getting Help

1. **Check Logs**: Look for error messages in the console
2. **Validate Data**: Use the data validation tool
3. **System Health**: Run the health check option
4. **Minimal Example**: Test with sample data first
5. **Dependencies**: Ensure all required packages are installed

## 📈 Roadmap

### Version 2.1 (Planned)
- [ ] Database integration (PostgreSQL, MySQL)
- [ ] REST API endpoints
- [ ] Email notifications for high-risk students
- [ ] Advanced time-series analysis
- [ ] Multi-language support

### Version 2.2 (Future)
- [ ] Mobile app interface
- [ ] Integration with LMS systems
- [ ] Real-time data streaming
- [ ] Advanced NLP for student feedback analysis
- [ ] Predictive interventions

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Include unit tests for new features
- Update documentation for changes

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Streamlit Team** for the amazing dashboard framework
- **Scikit-learn Contributors** for robust ML tools
- **XGBoost & LightGBM Teams** for advanced gradient boosting
- **Plotly Team** for interactive visualizations
- **Educational Institutions** for real-world feedback and requirements

## 📞 Support

For support, please:
1. Check this README for common solutions
2. Run the system health check
3. Review the troubleshooting section
4. Create an issue with:
   - System details (OS, Python version)
   - Error messages or logs
   - Steps to reproduce the problem
   - Sample data (if relevant)

---

**Made with ❤️ for educators and students worldwide**

*DropSafe v2.0 - Empowering Education Through Intelligent Analytics*
>>>>>>> c1ea61ba00576379f6f9ab293d6404d006a0762b
