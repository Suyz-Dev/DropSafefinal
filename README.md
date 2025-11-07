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