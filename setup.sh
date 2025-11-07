#!/bin/bash

# Colors for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
PURPLE='\\033[0;35m'
CYAN='\\033[0;36m'
NC='\\033[0m' # No Color

echo -e \"${CYAN}===============================================${NC}\"
echo -e \"${CYAN}         🚀 DropSafe ML System Setup${NC}\"
echo -e \"${CYAN}    Advanced Student Risk Assessment Platform${NC}\"
echo -e \"${CYAN}===============================================${NC}\"
echo
echo \"This script will set up the complete DropSafe environment.\"
echo \"Please ensure you have Python 3.8+ installed.\"
echo
read -p \"Press Enter to continue...\"

echo -e \"\n${BLUE}📋 Step 1: Checking Python installation...${NC}\"
if command -v python3 &> /dev/null; then
    PYTHON_CMD=\"python3\"
elif command -v python &> /dev/null; then
    PYTHON_CMD=\"python\"
else
    echo -e \"${RED}❌ Python not found! Please install Python 3.8+ first.${NC}\"
    echo \"Install instructions:\"
    echo \"  Ubuntu/Debian: sudo apt-get install python3 python3-pip python3-venv\"
    echo \"  CentOS/RHEL: sudo yum install python3 python3-pip\"
    echo \"  macOS: brew install python3 (requires Homebrew)\"
    echo \"  Or download from: https://www.python.org/downloads/\"
    exit 1
fi

echo -e \"${GREEN}✅ Python found!${NC}\"
$PYTHON_CMD --version
echo

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(sys.version_info[:2])')
echo \"Python version: $PYTHON_VERSION\"

echo -e \"\n${BLUE}📋 Step 2: Creating virtual environment...${NC}\"
if [ -d \"dropsafe_env\" ]; then
    echo -e \"${YELLOW}⚠️  Virtual environment already exists. Removing old one...${NC}\"
    rm -rf dropsafe_env
fi

$PYTHON_CMD -m venv dropsafe_env
if [ $? -ne 0 ]; then
    echo -e \"${RED}❌ Failed to create virtual environment!${NC}\"
    echo \"Try installing python3-venv: sudo apt-get install python3-venv\"
    exit 1
fi

echo -e \"${GREEN}✅ Virtual environment created!${NC}\"
echo

echo -e \"${BLUE}📋 Step 3: Activating virtual environment and upgrading pip...${NC}\"
source dropsafe_env/bin/activate
python -m pip install --upgrade pip
echo

echo -e \"${BLUE}📋 Step 4: Installing core dependencies...${NC}\"
echo \"This may take a few minutes...\"
pip install streamlit pandas numpy scikit-learn plotly matplotlib seaborn
if [ $? -ne 0 ]; then
    echo -e \"${RED}❌ Failed to install core dependencies!${NC}\"
    exit 1
fi
echo -e \"${GREEN}✅ Core dependencies installed!${NC}\"
echo

echo -e \"${BLUE}📋 Step 5: Installing advanced ML libraries...${NC}\"
pip install xgboost lightgbm imbalanced-learn shap
if [ $? -ne 0 ]; then
    echo -e \"${YELLOW}⚠️  Some advanced ML libraries failed to install. Basic functionality will still work.${NC}\"
else
    echo -e \"${GREEN}✅ Advanced ML libraries installed!${NC}\"
fi
echo

echo -e \"${BLUE}📋 Step 6: Installing data validation libraries...${NC}\"
pip install pydantic python-dotenv loguru
if [ $? -ne 0 ]; then
    echo -e \"${YELLOW}⚠️  Some validation libraries failed to install. Basic validation will still work.${NC}\"
else
    echo -e \"${GREEN}✅ Data validation libraries installed!${NC}\"
fi
echo

echo -e \"${BLUE}📋 Step 7: Testing installation...${NC}\"
python -c \"import streamlit, pandas, numpy, sklearn; print('✅ All core packages working!')\"
if [ $? -ne 0 ]; then
    echo -e \"${RED}❌ Installation test failed!${NC}\"
    exit 1
fi
echo

echo -e \"${BLUE}📋 Step 8: Generating sample data and training models...${NC}\"
python risk_model.py
if [ $? -ne 0 ]; then
    echo -e \"${YELLOW}⚠️  Failed to generate sample data. You can do this later.${NC}\"
else
    echo -e \"${GREEN}✅ Sample data and models created!${NC}\"
fi
echo

echo -e \"${BLUE}📋 Step 9: Making scripts executable...${NC}\"
chmod +x run.sh
echo -e \"${GREEN}✅ Scripts are now executable!${NC}\"
echo

echo -e \"${GREEN}🎉 Setup completed successfully!${NC}\"
echo -e \"${CYAN}===============================================${NC}\"
echo -e \"${CYAN}              📋 NEXT STEPS${NC}\"
echo -e \"${CYAN}===============================================${NC}\"
echo
echo -e \"${YELLOW}1. 🚀 Run the system:${NC}\"
echo \"   - Run ./run.sh to access the main menu\"
echo \"   - Or run individual components:\"
echo \"     • Teacher Dashboard: streamlit run teacher_dashboard.py\"
echo \"     • Student Portal: streamlit run student_dashboard.py\"
echo
echo -e \"${YELLOW}2. 📚 Access URLs:${NC}\"
echo \"   - Teacher Dashboard: http://localhost:8501\"
echo \"   - Student Portal: http://localhost:8502\"
echo
echo -e \"${YELLOW}3. 📁 Important files created:${NC}\"
echo \"   - sample_students.csv (100 demo student records)\"
echo \"   - advanced_risk_model.pkl (trained ML model)\"
echo \"   - student_risk_predictions.csv (sample predictions)\"
echo
echo -e \"${YELLOW}4. 🔧 System features:${NC}\"
echo \"   - ✅ Advanced ML algorithms (XGBoost, LightGBM, etc.)\"
echo \"   - ✅ Comprehensive data validation\"
echo \"   - ✅ Interactive dashboards\"
echo \"   - ✅ Risk assessment and reporting\"
echo \"   - ✅ Student portal with chatbot\"
echo
echo -e \"${YELLOW}5. 📖 Documentation:${NC}\"
echo \"   - Read README.md for detailed information\"
echo \"   - Check requirements.txt for all dependencies\"
echo
echo -e \"${CYAN}===============================================${NC}\"
echo -n \"Ready to launch DropSafe? (y/n): \"
read launch
if [[ \"$launch\" =~ ^[Yy]$ ]]; then
    echo -e \"${GREEN}🚀 Launching DropSafe main menu...${NC}\"
    ./run.sh
else
    echo -e \"${GREEN}👋 Setup complete! Run ./run.sh anytime to start.${NC}\"
fi
echo