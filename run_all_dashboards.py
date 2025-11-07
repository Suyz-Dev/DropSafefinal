#!/usr/bin/env python3
"""
Script to run all DropSafe dashboards simultaneously
"""
import subprocess
import sys
import os
import time

def run_dashboard(command, name, port):
    """Run a dashboard in the background"""
    try:
        print(f"🚀 Starting {name} on port {port}...")
        # Use shell=True to handle the activation script properly
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"✅ {name} started successfully!")
        return process
    except Exception as e:
        print(f"❌ Failed to start {name}: {e}")
        return None

def main():
    print("=" * 50)
    print("       DropSafe - All Dashboards Launcher")
    print("=" * 50)
    
    # Check if virtual environment exists
    venv_path = "dropsafe_env"
    if not os.path.exists(venv_path):
        print("⚠️  Virtual environment not found. Please run setup first.")
        print("💡 Run 'setup.bat' or 'setup.sh' to create the environment.")
        return
    
    # Commands to start each dashboard
    dashboards = [
        ("Main Landing Page", "main_page.py", 8499),
        ("Unified Login Portal", "login_page.py", 8500),
        ("Teacher Dashboard", "teacher_dashboard.py", 8501),
        ("Enhanced Student Portal", "enhanced_student_dashboard.py", 8502),
        ("Original Student Portal", "student_dashboard.py", 8503),
        ("Counsellor Dashboard", "counsellor_dashboard.py", 8504),
    ]
    
    processes = []
    
    # Activate virtual environment and run each dashboard
    for name, script, port in dashboards:
        # Construct the command
        if sys.platform.startswith("win"):
            activate_cmd = f"{venv_path}\\Scripts\\activate && "
        else:
            activate_cmd = f"source {venv_path}/bin/activate && "
            
        cmd = f"{activate_cmd}streamlit run {script} --server.port {port}"
        process = run_dashboard(cmd, name, port)
        if process:
            processes.append((process, name, port))
        time.sleep(2)  # Small delay between starting processes
    
    if processes:
        print("\n" + "=" * 50)
        print("🎉 All Dashboards Started Successfully!")
        print("=" * 50)
        print("Available Dashboards:")
        for _, name, port in processes:
            print(f"  🌐 {name}: http://localhost:{port}")
        
        print("\n📝 Notes:")
        print("  - Press Ctrl+C to stop all dashboards")
        print("  - Check your browser to access each dashboard")
        print("  - Initial loading may take a few seconds")
        
        try:
            # Wait for all processes
            print("\n⏳ Waiting for dashboards... (Press Ctrl+C to stop)")
            for process, name, _ in processes:
                process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping all dashboards...")
            for process, name, _ in processes:
                try:
                    process.terminate()
                    process.wait(timeout=5)
                    print(f"✅ {name} stopped")
                except subprocess.TimeoutExpired:
                    process.kill()
                    print(f"⚠️  {name} force killed")
            print("👋 All dashboards stopped. Goodbye!")
    else:
        print("❌ No dashboards were started successfully.")

if __name__ == "__main__":
    main()