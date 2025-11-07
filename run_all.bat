@echo off
chcp 65001 >nul
echo ========================================
echo    DropSafe - All Dashboards Launcher
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "dropsafe_env\Scripts\activate.bat" (
    echo ⚠️  Virtual environment not found!
    echo 💡 Please run setup.bat first to create the environment.
    pause
    exit /b
)

echo 🚀 Starting all DropSafe dashboards...
echo.

echo 🏠 1/6 Starting Main Landing Page (port 8499)...
start "Main Landing Page" /min cmd /c "dropsafe_env\Scripts\activate.bat && streamlit run main_page.py --server.port 8499"

timeout /t 3 /nobreak >nul

echo 🔐 2/6 Starting Unified Login Portal (port 8500)...
start "Login Portal" /min cmd /c "dropsafe_env\Scripts\activate.bat && streamlit run login_page.py --server.port 8500"

timeout /t 3 /nobreak >nul

echo 👨‍🏫 3/6 Starting Teacher Dashboard (port 8501)...
start "Teacher Dashboard" /min cmd /c "dropsafe_env\Scripts\activate.bat && streamlit run teacher_dashboard.py --server.port 8501"

timeout /t 3 /nobreak >nul

echo 🎓 4/6 Starting Enhanced Student Portal (port 8502)...
start "Enhanced Student Portal" /min cmd /c "dropsafe_env\Scripts\activate.bat && streamlit run enhanced_student_dashboard.py --server.port 8502"

timeout /t 3 /nobreak >nul

echo 📚 5/6 Starting Original Student Portal (port 8503)...
start "Original Student Portal" /min cmd /c "dropsafe_env\Scripts\activate.bat && streamlit run student_dashboard.py --server.port 8503"

timeout /t 3 /nobreak >nul

echo 🧠 6/6 Starting Counsellor Dashboard (port 8504)...
start "Counsellor Dashboard" /min cmd /c "dropsafe_env\Scripts\activate.bat && streamlit run counsellor_dashboard.py --server.port 8504"

echo.
echo ========================================
echo 🎉 All Dashboards Started Successfully!
echo ========================================
echo.
echo Available Dashboards:
echo   🌐 Main Landing Page: http://localhost:8499
echo   🌐 Login Portal: http://localhost:8500
echo   🌐 Teacher Dashboard: http://localhost:8501
echo   🌐 Enhanced Student Portal: http://localhost:8502
echo   🌐 Original Student Portal: http://localhost:8503
echo   🌐 Counsellor Dashboard: http://localhost:8504
echo.
echo 📝 Notes:
echo   - Dashboards are running in separate windows
echo   - Close each window individually to stop specific dashboards
echo   - Close this window to return to command prompt
echo.
pause