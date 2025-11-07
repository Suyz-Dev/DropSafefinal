"""
Shared Data Management System
Handles risk alerts and student data sharing between dashboards
"""

import pandas as pd
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class SharedDataManager:
    def __init__(self):
        self.data_dir = "shared_data"
        self.risk_alerts_file = os.path.join(self.data_dir, "risk_alerts.json")
        self.student_lists_file = os.path.join(self.data_dir, "student_lists.json")
        self.chat_history_file = os.path.join(self.data_dir, "chat_history.json")
        self.feedback_file = os.path.join(self.data_dir, "counselor_feedback.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize files if they don't exist
        self._init_files()
    
    def _init_files(self):
        """Initialize data files with empty structures"""
        if not os.path.exists(self.risk_alerts_file):
            self._save_json(self.risk_alerts_file, {})
        
        if not os.path.exists(self.student_lists_file):
            self._save_json(self.student_lists_file, {
                "high_risk": [],
                "medium_risk": [],
                "low_risk": [],
                "last_updated": None
            })
        
        if not os.path.exists(self.chat_history_file):
            self._save_json(self.chat_history_file, {})
            
        if not os.path.exists(self.feedback_file):
            self._save_json(self.feedback_file, {})
    
    def _load_json(self, filepath: str) -> dict:
        """Load JSON data from file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_json(self, filepath: str, data: dict):
        """Save JSON data to file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def update_risk_alerts(self, student_data: pd.DataFrame):
        """Update risk alerts based on student data from teacher dashboard"""
        alerts = {}
        current_time = datetime.now().isoformat()
        
        for _, student in student_data.iterrows():
            student_id = str(student.get('Student_ID', ''))
            risk_level = student.get('Risk_Level', 'Unknown').lower()
            
            # Create personalized alert message
            alert_msg = self._generate_alert_message(student, risk_level)
            
            alerts[student_id] = {
                "student_name": student.get('Name', 'Unknown'),
                "risk_level": risk_level,
                "alert_message": alert_msg,
                "last_updated": current_time,
                "counselor_assigned": risk_level in ['high', 'medium']
            }
        
        self._save_json(self.risk_alerts_file, alerts)
        return True
    
    def _generate_alert_message(self, student: pd.Series, risk_level: str) -> str:
        """Generate personalized alert message based on risk level"""
        name = student.get('Name', 'Student')
        
        if risk_level == 'high':
            return f"🚨 HIGH ALERT: {name}, immediate attention required! Please contact your counselor or visit the counseling center. Your safety is our priority."
        elif risk_level == 'medium':
            return f"⚠️ MEDIUM ALERT: {name}, we've noticed some concerns. Please consider speaking with a counselor. Support is available when you need it."
        else:
            return f"✅ SAFE STATUS: {name}, you're doing well! Keep up the positive momentum. Remember, support is always available if needed."
    
    def get_student_alert(self, student_id: str) -> Optional[dict]:
        """Get alert for specific student"""
        alerts = self._load_json(self.risk_alerts_file)
        return alerts.get(str(student_id))
    
    def update_student_lists(self, high_risk: List[dict], medium_risk: List[dict], low_risk: List[dict] = None):
        """Update student lists for counselor dashboard"""
        data = {
            "high_risk": high_risk,
            "medium_risk": medium_risk,
            "low_risk": low_risk or [],
            "last_updated": datetime.now().isoformat()
        }
        self._save_json(self.student_lists_file, data)
        return True
    
    def get_student_lists(self) -> dict:
        """Get student lists for counselor dashboard"""
        return self._load_json(self.student_lists_file)
    
    def save_chat_message(self, student_id: str, message: str, response: str):
        """Save chat conversation for AI counselor"""
        chat_data = self._load_json(self.chat_history_file)
        
        if student_id not in chat_data:
            chat_data[student_id] = []
        
        chat_data[student_id].append({
            "timestamp": datetime.now().isoformat(),
            "student_message": message,
            "counselor_response": response
        })
        
        # Keep only last 50 messages per student
        if len(chat_data[student_id]) > 50:
            chat_data[student_id] = chat_data[student_id][-50:]
        
        self._save_json(self.chat_history_file, chat_data)
    
    def get_chat_history(self, student_id: str) -> List[dict]:
        """Get chat history for student"""
        chat_data = self._load_json(self.chat_history_file)
        return chat_data.get(student_id, [])
        
    def save_counselor_feedback(self, student_id: str, student_name: str, satisfaction: str):
        """Save student satisfaction feedback for counselor dashboard"""
        feedback_data = self._load_json(self.feedback_file)
        
        # Create or update feedback entry
        feedback_data[student_id] = {
            "student_name": student_name,
            "satisfaction": satisfaction,  # "satisfied" or "unsatisfied"
            "timestamp": datetime.now().isoformat()
        }
        
        self._save_json(self.feedback_file, feedback_data)
        
    def get_counselor_feedback(self) -> dict:
        """Get all counselor feedback for counselor dashboard"""
        return self._load_json(self.feedback_file)
        
    def get_student_feedback(self, student_id: str) -> Optional[dict]:
        """Get feedback for specific student"""
        feedback_data = self._load_json(self.feedback_file)
        return feedback_data.get(str(student_id))

# Global instance
shared_data_manager = SharedDataManager()