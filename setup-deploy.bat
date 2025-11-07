@echo off
chcp 65001 >nul
echo ===============================================
echo         🚀 DropSafe Deployment Setup
echo    Advanced Student Risk Assessment Platform
echo ===============================================
echo.
echo This script will set up the DropSafe environment for deployment.
echo Please ensure you have Python 3.8+ installed.
echo.
echo Deployment Options:
echo 1. Local Development Setup
echo 2. Docker Deployment Setup
echo 3. Cloud Deployment Preparation
echo.
choice /c 123 /m "Select deployment option"
if errorlevel 3 goto cloud
if errorlevel 2 goto docker
goto local

:local
echo.
echo 📋 Setting up Local Development Environment...
call setup.bat
goto finalize

:docker
echo.
echo 📋 Setting up Docker Deployment Environment...
echo Checking Docker installation...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Docker not found. Please install Docker Desktop first.
    echo Download from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)
echo ✅ Docker found!
docker --version
echo.
echo Building Docker images...
docker build -t dropsafe-main -f Dockerfile .
if %errorlevel% neq 0 (
    echo ❌ Failed to build Docker image!
    pause
    exit /b 1
)
echo ✅ Docker image built successfully!
echo.
echo To run with Docker:
echo docker run -p 8499:8499 -p 8501:8501 -p 8502:8502 -p 8504:8504 dropsafe-main
goto finalize

:cloud
echo.
echo 📋 Preparing for Cloud Deployment...
echo Creating deployment package...
if not exist "deploy" mkdir deploy
xcopy "*.py" "deploy\" /Y
xcopy "*.md" "deploy\" /Y
xcopy "*.txt" "deploy\" /Y
xcopy "*.bat" "deploy\" /Y
xcopy "*.sh" "deploy\" /Y
xcopy "Dockerfile" "deploy\" /Y
xcopy "docker-compose.yml" "deploy\" /Y
xcopy ".gitignore" "deploy\" /Y
echo.
echo Deployment package created in 'deploy' folder.
echo.
echo Cloud Deployment Options:
echo 1. Heroku Deployment
echo 2. AWS Deployment
echo 3. Google Cloud Deployment
echo.
echo For detailed cloud deployment instructions, see DEPLOYMENT.md
goto finalize

:finalize
echo.
echo 🎉 Deployment setup completed successfully!
echo ===============================================
echo              📋 NEXT STEPS
echo ===============================================
echo.
echo 1. 🚀 Run the system:
echo    - For Local: Double-click "run.bat"
echo    - For Docker: docker-compose up -d
echo    - For Cloud: Follow instructions in DEPLOYMENT.md
echo.
echo 2. 📚 Documentation:
echo    - Read DEPLOYMENT.md for detailed deployment instructions
echo    - Check README.md for general usage information
echo.
echo 3. 🔧 System features:
echo    - ✅ Advanced ML algorithms (XGBoost, LightGBM, etc.)
echo    - ✅ Comprehensive data validation
echo    - ✅ Interactive dashboards
echo    - ✅ Risk assessment and reporting
echo    - ✅ Student portal with chatbot
echo.
echo ===============================================
echo Ready to launch DropSafe? (Y/N)
set /p launch="Enter choice: "
if /i "%launch%"=="Y" (
    echo 🚀 Launching DropSafe...
    if "%launch%"=="Y" (
        if exist "run.bat" (
            call run.bat
        ) else (
            echo ⚠️  run.bat not found. Please check your installation.
        )
    )
) else (
    echo 👋 Deployment setup complete!
)
echo.
pause