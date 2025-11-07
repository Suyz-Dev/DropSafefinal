#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo "===================================="
echo "        DropSafe ML System v2.0"
echo "   Advanced Student Risk Assessment"
echo "===================================="
echo
echo "🚀 Available Options:"
echo "1. Teacher Dashboard (Main Interface)"
echo "2. Student Portal (Student Access)"
echo "3. Generate Sample Data (Demo)"
echo "4. Validate Data (Quality Check)"
echo "5. Train ML Model (Advanced)"
echo "6. System Health Check"
echo "7. View Documentation"
echo "8. Setup Virtual Environment"
echo "9. Exit"
echo
read -p "Enter your choice (1-9): " choice

case $choice in
    1)
        echo "🎯 Starting Teacher Dashboard..."
        echo "📊 URL: http://localhost:8501"
        if [ -d "dropsafe_env" ]; then
            source dropsafe_env/bin/activate
        fi
        streamlit run teacher_dashboard.py --server.port 8501
        ;;
    2)
        echo "🎓 Starting Student Portal..."
        echo "📊 URL: http://localhost:8502"
        if [ -d "dropsafe_env" ]; then
            source dropsafe_env/bin/activate
        fi
        streamlit run student_dashboard.py --server.port 8502
        ;;
    3)
        echo "📊 Generating sample data and training models..."
        if [ -d "dropsafe_env" ]; then
            source dropsafe_env/bin/activate
        fi
        python risk_model.py
        echo
        echo "✅ Sample data generated successfully!"
        echo "📁 Files created:"
        echo "    - sample_students.csv (100 student records)"
        echo "    - advanced_risk_model.pkl (trained ML model)"
        echo "    - student_risk_predictions.csv (predictions)"
        read -p "Press Enter to continue..."
        ;;
    4)
        echo "🔍 Running data validation..."
        if [ -d "dropsafe_env" ]; then
            source dropsafe_env/bin/activate
        fi
        python data_validator.py
        echo
        echo "✅ Data validation completed!"
        read -p "Press Enter to continue..."
        ;;
    5)
        echo "🤖 Training advanced ML models..."
        if [ -d "dropsafe_env" ]; then
            source dropsafe_env/bin/activate
        fi
        python -c "from risk_model import AdvancedRiskPredictor, generate_sample_data; import pandas as pd; import os; df = pd.read_csv('sample_students.csv') if os.path.exists('sample_students.csv') else generate_sample_data(100); predictor = AdvancedRiskPredictor(); predictor.train(df); predictor.save_model(); print('✅ Model training completed!')"
        read -p "Press Enter to continue..."
        ;;
    6)
        echo "🏥 Checking system health..."
        if [ -d "dropsafe_env" ]; then
            source dropsafe_env/bin/activate
        fi
        python -c "import streamlit, pandas, numpy, sklearn, sys; print('✅ All core packages working!'); print(f'Python: {sys.version}'); import os; print(f'Current directory: {os.getcwd()}'); files = ['risk_model.py', 'teacher_dashboard.py', 'student_dashboard.py', 'data_validator.py']; missing = [f for f in files if not os.path.exists(f)]; print(f'Missing files: {missing}' if missing else '✅ All files present')"
        read -p "Press Enter to continue..."
        ;;
    7)
        echo "📚 Opening documentation..."
        if command -v xdg-open > /dev/null; then
            xdg-open README.md
        elif command -v open > /dev/null; then
            open README.md
        else
            echo "Please open README.md manually"
        fi
        read -p "Press Enter to continue..."
        ;;
    8)
        echo "🔧 Setting up virtual environment..."
        python3 -m venv dropsafe_env
        source dropsafe_env/bin/activate
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        echo "✅ Virtual environment setup completed!"
        read -p "Press Enter to continue..."
        ;;
    9)
        echo "👋 Goodbye! Thank you for using DropSafe!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Please try again."
        read -p "Press Enter to continue..."
        exec $0
        ;;
esac