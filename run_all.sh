#!/bin/bash

echo "========================================"
echo "   DropSafe - All Dashboards Launcher"
echo "========================================"
echo

# Check if virtual environment exists
if [ ! -f "dropsafe_env/bin/activate" ]; then
    echo "⚠️  Virtual environment not found!"
    echo "💡 Please run setup.sh first to create the environment."
    exit 1
fi

echo "🚀 Starting all DropSafe dashboards..."
echo

echo "🏠 1/6 Starting Main Landing Page (port 8499)..."
source dropsafe_env/bin/activate && streamlit run main_page.py --server.port 8499 &
MAIN_PID=$!

sleep 3

echo "🔐 2/6 Starting Unified Login Portal (port 8500)..."
source dropsafe_env/bin/activate && streamlit run login_page.py --server.port 8500 &
LOGIN_PID=$!

sleep 3

echo "👨‍🏫 3/6 Starting Teacher Dashboard (port 8501)..."
source dropsafe_env/bin/activate && streamlit run teacher_dashboard.py --server.port 8501 &
TEACHER_PID=$!

sleep 3

echo "🎓 4/6 Starting Enhanced Student Portal (port 8502)..."
source dropsafe_env/bin/activate && streamlit run enhanced_student_dashboard.py --server.port 8502 &
STUDENT_ENHANCED_PID=$!

sleep 3

echo "📚 5/6 Starting Original Student Portal (port 8503)..."
source dropsafe_env/bin/activate && streamlit run student_dashboard.py --server.port 8503 &
STUDENT_ORIGINAL_PID=$!

sleep 3

echo "🧠 6/6 Starting Counsellor Dashboard (port 8504)..."
source dropsafe_env/bin/activate && streamlit run counsellor_dashboard.py --server.port 8504 &
COUNSELLOR_PID=$!

echo
echo "========================================"
echo "🎉 All Dashboards Started Successfully!"
echo "========================================"
echo
echo "Available Dashboards:"
echo "  🌐 Main Landing Page: http://localhost:8499"
echo "  🌐 Login Portal: http://localhost:8500"
echo "  🌐 Teacher Dashboard: http://localhost:8501"
echo "  🌐 Enhanced Student Portal: http://localhost:8502"
echo "  🌐 Original Student Portal: http://localhost:8503"
echo "  🌐 Counsellor Dashboard: http://localhost:8504"
echo
echo "📝 Notes:"
echo "  - All dashboards are running in the background"
echo "  - Use 'kill $MAIN_PID $LOGIN_PID $TEACHER_PID $STUDENT_ENHANCED_PID $STUDENT_ORIGINAL_PID $COUNSELLOR_PID' to stop all"
echo "  - Or press Ctrl+C to stop all dashboards"
echo

# Wait for all processes
wait $MAIN_PID $LOGIN_PID $TEACHER_PID $STUDENT_ENHANCED_PID $STUDENT_ORIGINAL_PID $COUNSELLOR_PID