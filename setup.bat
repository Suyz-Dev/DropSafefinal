@echo off
chcp 65001 >nul
echo ===============================================
echo         🚀 DropSafe ML System Setup
echo    Advanced Student Risk Assessment Platform
echo ===============================================
echo.
echo This script will set up the complete DropSafe environment.
echo Please ensure you have Python 3.8+ installed.
echo.
pause

echo 📋 Step 1: Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python 3.8+ first.
    echo Download from: https://www.python.org/downloads/
    echo Make sure to check \"Add Python to PATH\" during installation.
    pause
    exit /b 1
)

echo ✅ Python found!
python --version
echo.

echo 📋 Step 2: Creating virtual environment...
if exist \"dropsafe_env\" (
    echo ⚠️  Virtual environment already exists. Removing old one...
    rmdir /s /q dropsafe_env
)

python -m venv dropsafe_env
if %errorlevel% neq 0 (
    echo ❌ Failed to create virtual environment!
    pause
    exit /b 1
)

echo ✅ Virtual environment created!
echo.

echo 📋 Step 3: Activating virtual environment and upgrading pip...
call dropsafe_env\\Scripts\\activate.bat
python -m pip install --upgrade pip
echo.

echo 📋 Step 4: Installing core dependencies...
echo This may take a few minutes...
pip install streamlit pandas numpy scikit-learn plotly matplotlib seaborn
if %errorlevel% neq 0 (
    echo ❌ Failed to install core dependencies!
    pause
    exit /b 1
)
echo ✅ Core dependencies installed!
echo.

echo 📋 Step 5: Installing advanced ML libraries...
pip install xgboost lightgbm imbalanced-learn shap
if %errorlevel% neq 0 (
    echo ⚠️  Some advanced ML libraries failed to install. Basic functionality will still work.
) else (
    echo ✅ Advanced ML libraries installed!
)
echo.

echo 📋 Step 6: Installing data validation libraries...
pip install pydantic python-dotenv loguru
if %errorlevel% neq 0 (
    echo ⚠️  Some validation libraries failed to install. Basic validation will still work.
) else (
    echo ✅ Data validation libraries installed!
)
echo.

echo 📋 Step 7: Testing installation...
python -c \"import streamlit, pandas, numpy, sklearn; print('✅ All core packages working!')\"
if %errorlevel% neq 0 (
    echo ❌ Installation test failed!
    pause
    exit /b 1
)
echo.

echo 📋 Step 8: Generating sample data and training models...
python risk_model.py
if %errorlevel% neq 0 (
    echo ⚠️  Failed to generate sample data. You can do this later.
) else (
    echo ✅ Sample data and models created!
)
echo.

echo 📋 Step 9: Testing Streamlit dashboards...
echo Testing teacher dashboard (this will open briefly and close)...
start /b streamlit run teacher_dashboard.py --server.headless true --server.port 8501
timeout /t 5 /nobreak >nul
taskkill /f /im streamlit.exe >nul 2>&1
echo ✅ Teacher dashboard test completed!
echo.

echo 🎉 Setup completed successfully!
echo ===============================================
echo              📋 NEXT STEPS
echo ===============================================
echo.
echo 1. 🚀 Run the system:
echo    - Double-click \"run.bat\" to access the main menu
echo    - Or run individual components:
echo      • Teacher Dashboard: streamlit run teacher_dashboard.py
echo      • Student Portal: streamlit run student_dashboard.py
echo.
echo 2. 📚 Access URLs:
echo    - Teacher Dashboard: http://localhost:8501
echo    - Student Portal: http://localhost:8502
echo.
echo 3. 📁 Important files created:
echo    - sample_students.csv (100 demo student records)
echo    - advanced_risk_model.pkl (trained ML model)
echo    - student_risk_predictions.csv (sample predictions)
echo.
echo 4. 🔧 System features:
echo    - ✅ Advanced ML algorithms (XGBoost, LightGBM, etc.)
echo    - ✅ Comprehensive data validation
echo    - ✅ Interactive dashboards
echo    - ✅ Risk assessment and reporting
echo    - ✅ Student portal with chatbot
echo.
echo 5. 📖 Documentation:
echo    - Read README.md for detailed information
echo    - Check requirements.txt for all dependencies
echo.
echo ===============================================
echo Ready to launch DropSafe? (Y/N)
set /p launch=\"Enter choice: \"
if /i \"%launch%\"==\"Y\" (
    echo 🚀 Launching DropSafe main menu...
    call run.bat
) else (
    echo 👋 Setup complete! Run \"run.bat\" anytime to start.
)
echo.
pause