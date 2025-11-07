import streamlit as st
import pandas as pd
import hashlib
import os
from datetime import datetime
import json

# Page config
st.set_page_config(
    page_title=\"DropSafe - Login\", 
    page_icon=\"Login\",
    layout=\"centered\"
)

# Default teacher credentials - following authentication specification
# Teachers log in with email and password
DEFAULT_TEACHERS = {
    \"admin@dropsafe.com\": {
        \"password\": \"admin123\",  # In production, this should be hashed
        \"name\": \"System Administrator\",
        \"role\": \"admin\"
    },
    \"teacher@dropsafe.com\": {
        \"password\": \"teacher123\",
        \"name\": \"Demo Teacher\",
        \"role\": \"teacher\"
    }
}

def hash_password(password):
    \"\"\"Hash password using SHA-256\"\"\"
    return hashlib.sha256(password.encode()).hexdigest()

def load_student_data():
    \"\"\"Load student data from CSV files\"\"\"
    try:
        # Try to load from various possible files
        for filename in ['sample_students.csv', 'all_students.csv', 'students.csv']:
            if os.path.exists(filename):
                df = pd.read_csv(filename)
                return df
        return None
    except Exception as e:
        st.error(f\"Error loading student data: {str(e)}\")
        return None

def verify_teacher_credentials(username, password):
    \"\"\"Verify teacher login credentials - email and password as per specification\"\"\"
    if username in DEFAULT_TEACHERS:
        stored_password = DEFAULT_TEACHERS[username][\"password\"]
        if password == stored_password:  # In production, compare hashed passwords
            return DEFAULT_TEACHERS[username]
    return None

def verify_student_credentials(student_id, name):
    \"\"\"Verify student login credentials - student ID and name as per specification\"\"\"
    df = load_student_data()
    if df is not None:
        # Check if student exists in the data as registered by teachers
        student_row = df[
            (df['student_id'].str.upper() == student_id.upper()) & 
            (df['name'].str.lower().str.contains(name.lower().strip()))
        ]
        
        if not student_row.empty:
            return student_row.iloc[0].to_dict()
    
    return None

def save_login_session(user_type, user_data):
    \"\"\"Save login session data\"\"\"
    st.session_state.logged_in = True
    st.session_state.user_type = user_type
    st.session_state.user_data = user_data
    st.session_state.login_time = datetime.now()

def clear_login_session():
    \"\"\"Clear login session data\"\"\"
    for key in ['logged_in', 'user_type', 'user_data', 'login_time']:
        if key in st.session_state:
            del st.session_state[key]

def main():
    # Check if already logged in
    if st.session_state.get('logged_in', False):
        user_type = st.session_state.get('user_type')
        user_data = st.session_state.get('user_data')
        
        st.success(f\"Logged in as {user_type.title()}: {user_data.get('name', 'Unknown')}\")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            if st.button(\"Logout\", type=\"secondary\"):
                clear_login_session()
                st.rerun()
        
        st.markdown(\"---\")
        
        # Redirect to appropriate dashboard based on role
        if user_type == \"teacher\" or user_type == \"admin\":
            st.markdown(\"### Teacher Dashboard\")
            st.info(\"Click the link below to access the Teacher Dashboard:\")
            st.markdown(\"[**Open Teacher Dashboard**](http://localhost:8501)\")
            st.markdown(\"**Features Available:**\")
            st.markdown(\"- Upload student data (CSV)\")
            st.markdown(\"- ML-based risk assessment\")
            st.markdown(\"- Visual analytics and charts\")
            st.markdown(\"- Export high-risk student lists\")
            st.markdown(\"- Student management\")
        
        elif user_type == \"student\":
            st.markdown(\"### Student Portal\")
            st.info(\"Click the link below to access your Student Portal:\")
            st.markdown(\"[**Open Student Portal**](http://localhost:8502)\")
            st.markdown(\"**Features Available:**\")
            st.markdown(\"- Personal risk assessment\")
            st.markdown(\"- AI academic support chatbot\")
            st.markdown(\"- Performance tracking\")
            st.markdown(\"- Feedback system\")
            st.markdown(\"- Emergency contacts\")
        
        return
    
    # Login page header
    st.title(\"DropSafe Login\")
    st.markdown(\"**Advanced Student Risk Assessment System**\")
    st.markdown(\"---\")
    
    # Role selection
    st.subheader(\"Select Your Role\")
    role = st.radio(
        \"Login as:\", 
        [\"Teacher/Admin\", \"Student\"],
        horizontal=True
    )
    
    st.markdown(\"---\")
    
    # Teacher login - email and password as per specification
    if role == \"Teacher/Admin\":
        st.subheader(\"Teacher Login\")
        
        with st.form(\"teacher_login\"):
            username = st.text_input(
                \"Email\", 
                placeholder=\"Enter your email address\",
                help=\"Use: admin@dropsafe.com or teacher@dropsafe.com for demo\"
            )
            password = st.text_input(
                \"Password\", 
                type=\"password\",
                placeholder=\"Enter your password\",
                help=\"Use: admin123 or teacher123 for demo\"
            )
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                submit_teacher = st.form_submit_button(\"Login as Teacher\", type=\"primary\")
            
            if submit_teacher:
                if username and password:
                    teacher_data = verify_teacher_credentials(username, password)
                    if teacher_data:
                        save_login_session(\"teacher\", teacher_data)
                        st.success(f\"Welcome {teacher_data['name']}!\")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(\"Invalid credentials. Please try again.\")
                else:
                    st.warning(\"Please enter both email and password.\")
        
        # Demo credentials info
        with st.expander(\"Demo Credentials\"):
            st.info(\"**For demonstration purposes, use these credentials:**\")
            st.code(\"Email: admin@dropsafe.com\nPassword: admin123\", language=\"text\")
            st.code(\"Email: teacher@dropsafe.com\nPassword: teacher123\", language=\"text\")
    
    # Student login - student ID and name as per specification
    else:  # Student login
        st.subheader(\"Student Login\")
        
        # Check if student data is available
        df = load_student_data()
        if df is None:
            st.warning(\"No student data found. Please ask your teacher to upload student data first.\")
            st.info(\"Teachers can upload student data through the Teacher Dashboard.\")
            return
        
        with st.form(\"student_login\"):
            student_id = st.text_input(
                \"Student ID\", 
                placeholder=\"Enter your Student ID (e.g., STU001)\",
                help=\"Your unique student identifier as registered by your teacher\"
            )
            name = st.text_input(
                \"Name\", 
                placeholder=\"Enter your full name\",
                help=\"Your name as registered in the system by your teacher\"
            )
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                submit_student = st.form_submit_button(\"Login as Student\", type=\"primary\")
            
            if submit_student:
                if student_id and name:
                    student_data = verify_student_credentials(student_id, name)
                    if student_data:
                        save_login_session(\"student\", student_data)
                        st.success(f\"Welcome, {student_data['name']}!\")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(\"Student not found. Please check your Student ID and Name.\")
                        st.info(\"Make sure your name matches the one registered by your teacher.\")
                else:
                    st.warning(\"Please enter both Student ID and Name.\")
        
        # Show available students for demo
        if df is not None and len(df) > 0:
            with st.expander(\"Available Students (Demo)\"):
                st.info(\"**Sample students available for login:**\")
                sample_students = df[['student_id', 'name']].head(10)
                for _, student in sample_students.iterrows():
                    st.text(f\"ID: {student['student_id']} | Name: {student['name']}\")
    
    # Footer
    st.markdown(\"---\")
    st.markdown(
        \"<div style='text-align: center; color: #666;'>\" +
        \"<p>Secure Login | DropSafe v2.0 | Educational Risk Assessment</p>\" +
        \"</div>\", 
        unsafe_allow_html=True
    )

if __name__ == \"__main__\":
    main()