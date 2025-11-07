@echo off
chcp 65001 >nul
echo ====================================
echo        DropSafe ML System v2.0
echo   Advanced Student Risk Assessment
echo ====================================
echo.
echo 🚀 Available Options:
echo 0. Main Landing Page (Hero + Dashboard Selection)
echo 1. Unified Login Portal (Authentication)
echo 2. Teacher Dashboard (Direct Access)
echo 3. Student Portal (Enhanced with Auth)
echo 4. Counsellor Dashboard (New!)
echo 5. Original Student Portal (Legacy)
echo 6. Generate Sample Data (Demo)
echo 7. Validate Data (Quality Check)
echo 8. Train ML Model (Advanced)
echo 9. System Health Check
echo x. Exit
echo.
set /p choice="Enter your choice (0-9, x): "

if "%choice%"=="0" (
    echo 🏠 Starting Main Landing Page...
    echo 🌐 URL: http://localhost:8499
    dropsafe_env\Scripts\activate.ps1 && streamlit run main_page.py --server.port 8499
) else if "%choice%"=="1" (
    echo 🔐 Starting Unified Login Portal...
    echo 🌐 URL: http://localhost:8500
    dropsafe_env\Scripts\activate.ps1 && streamlit run login_page.py --server.port 8500
) else if "%choice%"=="2" (
    echo 👨‍🏫 Starting Teacher Dashboard...
    echo 📊 URL: http://localhost:8501
    dropsafe_env\Scripts\activate.ps1 && streamlit run teacher_dashboard.py --server.port 8501
) else if "%choice%"=="3" (
    echo 🎓 Starting Enhanced Student Portal...
    echo 🔐 URL: http://localhost:8502
    dropsafe_env\Scripts\activate.ps1 && streamlit run enhanced_student_dashboard.py --server.port 8502
) else if "%choice%"=="4" (
    echo 🧠 Starting Counsellor Dashboard...
    echo 💙 URL: http://localhost:8504
    dropsafe_env\Scripts\activate.ps1 && streamlit run counsellor_dashboard.py --server.port 8504
) else if "%choice%"=="5" (
    echo 🎓 Starting Original Student Portal...
    echo 📚 URL: http://localhost:8503
    dropsafe_env\Scripts\activate.ps1 && streamlit run student_dashboard.py --server.port 8503
) else if "%choice%"=="6" (
    echo 📊 Generating sample data and training models...
    dropsafe_env\Scripts\activate.ps1 && python risk_model.py
    echo.
    echo ✅ Sample data generated successfully!
    echo 📁 Files created:
    echo    - sample_students.csv (100 student records)
    echo    - advanced_risk_model.pkl (trained ML model)
    echo    - student_risk_predictions.csv (predictions)
    pause
) else if "%choice%"=="7" (
    echo 🔍 Running data validation...
    dropsafe_env\Scripts\activate.ps1 && python data_validator.py
    echo.
    echo ✅ Data validation completed!
    pause
) else if "%choice%"=="8" (
    echo 🤖 Training advanced ML models...
    dropsafe_env\Scripts\activate.ps1 && python -c "from risk_model import AdvancedRiskPredictor, generate_sample_data; import pandas as pd; df = pd.read_csv('sample_students.csv') if __import__('os').path.exists('sample_students.csv') else generate_sample_data(100); predictor = AdvancedRiskPredictor(); predictor.train(df); predictor.save_model(); print('✅ Model training completed!')"
    pause
) else if "%choice%"=="9" (
    echo 🏥 Checking system health...
    dropsafe_env\Scripts\activate.ps1 && python system_status.py
    pause
) else if "%choice%"=="x" (
    echo 👋 Goodbye! Thank you for using DropSafe!
    exit
) else (
    echo ❌ Invalid choice. Please try again.
    pause
    cls
    goto :eof
)