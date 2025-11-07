#!/usr/bin/env python3
"""
DropSafe System Status Checker
==============================

This script performs comprehensive health checks on the DropSafe system
to ensure all components are working correctly.

Usage: python system_status.py
"""

import sys
import os
import importlib
from datetime import datetime


def check_system_status():
    print("=" * 60)
    print("         DROPSAFE SYSTEM STATUS CHECK")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Platform: {sys.platform}")
    print(f"Working Directory: {os.getcwd()}")
    print("=" * 60)
    
    checks_passed = 0
    checks_failed = 0
    warnings = []
    
    # Check Python version
    print("\nChecking Python Version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"   [OK] Python {version.major}.{version.minor}.{version.micro} - Compatible")
        checks_passed += 1
    else:
        print(f"   [FAIL] Python {version.major}.{version.minor}.{version.micro} - Requires 3.8+")
        checks_failed += 1
    
    # Check required files
    print("\nChecking Required Files...")
    required_files = [
        'risk_model.py',
        'teacher_dashboard.py', 
        'student_dashboard.py',
        'data_validator.py',
        'requirements.txt',
        'README.md'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file) / 1024  # KB
            print(f"   [OK] {file} ({size:.1f}KB)")
            checks_passed += 1
        else:
            print(f"   [FAIL] {file} - Missing")
            checks_failed += 1
    
    # Check generated files
    print("\nChecking Generated Files...")
    generated_files = {
        'sample_students.csv': 'Sample student data',
        'advanced_risk_model.pkl': 'Trained ML model',
        'student_risk_predictions.csv': 'Model predictions'
    }
    
    for file, description in generated_files.items():
        if os.path.exists(file):
            size = os.path.getsize(file) / 1024  # KB
            print(f"   [OK] {file} ({size:.1f}KB) - {description}")
            checks_passed += 1
        else:
            print(f"   [WARN] {file} - Missing ({description})")
            warnings.append(f"Generate {description} by running: python risk_model.py")
    
    # Check virtual environment
    print("\nChecking Virtual Environment...")
    if os.path.exists('dropsafe_env'):
        print("   [OK] Virtual environment exists")
        checks_passed += 1
        
        # Check if we're in the virtual environment
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            print("   [OK] Virtual environment is activated")
            checks_passed += 1
        else:
            print("   [WARN] Virtual environment not activated")
            warnings.append("Activate with: dropsafe_env\\\\Scripts\\\\activate (Windows) or source dropsafe_env/bin/activate (Linux/Mac)")
    else:
        print("   [FAIL] Virtual environment not found")
        checks_failed += 1
        warnings.append("Create with: python -m venv dropsafe_env")
    
    # Check core dependencies
    print("\nChecking Core Dependencies...")
    core_packages = {
        'streamlit': 'Web framework',
        'pandas': 'Data manipulation',
        'numpy': 'Numerical computing',
        'sklearn': 'Machine learning',
        'plotly': 'Interactive plots'
    }
    
    for package, description in core_packages.items():
        try:
            module = importlib.import_module(package)
            version = getattr(module, '__version__', 'Unknown')
            print(f"   [OK] {package} {version} - {description}")
            checks_passed += 1
        except ImportError:
            print(f"   [FAIL] {package} - Missing ({description})")
            checks_failed += 1
    
    # Test model functionality
    print("\nTesting ML Model Functionality...")
    try:
        from risk_model import AdvancedRiskPredictor, generate_sample_data
        
        # Test model creation
        predictor = AdvancedRiskPredictor()
        print("   [OK] Model class instantiation")
        
        # Test data generation
        test_data = generate_sample_data(5)
        print("   [OK] Sample data generation")
        
        # Test model training
        predictor.train(test_data)
        print("   [OK] Model training")
        
        # Test predictions
        predictions = predictor.predict_risk(test_data)
        print(f"   [OK] Risk predictions ({len(predictions)} samples)")
        
        checks_passed += 1
        
    except Exception as e:
        print(f"   [FAIL] Model functionality test failed: {str(e)}")
        checks_failed += 1
    
    # Print summary
    print("\n" + "=" * 60)
    print("                    SUMMARY")
    print("=" * 60)
    
    total_checks = checks_passed + checks_failed
    success_rate = (checks_passed / total_checks * 100) if total_checks > 0 else 0
    
    print(f"Total Checks: {total_checks}")
    print(f"Passed: {checks_passed}")
    print(f"Failed: {checks_failed}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    if warnings:
        print(f"\nWarnings ({len(warnings)}):")
        for i, warning in enumerate(warnings, 1):
            print(f"   {i}. {warning}")
    
    print("\n" + "=" * 60)
    
    if success_rate >= 90:
        print("EXCELLENT! DropSafe is fully operational.")
        print("Ready to launch with: run.bat (Windows) or ./run.sh (Linux/Mac)")
    elif success_rate >= 70:
        print("GOOD! DropSafe is mostly functional.")
        print("Address warnings for optimal performance.")
    else:
        print("ISSUES DETECTED! DropSafe may not work properly.")
        print("Please resolve failed checks before using.")
    
    print("\nNext Steps:")
    print("   1. Teacher Dashboard: streamlit run teacher_dashboard.py")
    print("   2. Student Portal: streamlit run student_dashboard.py")
    print("   3. Generate Data: python risk_model.py")
    print("   4. Main Menu: run.bat (Windows) or ./run.sh (Linux/Mac)")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    check_system_status()
