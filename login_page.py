import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="DropSafe - Login",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add navigation header
st.markdown("""
<div style="background: linear-gradient(90deg, #9C27B0, #7B1FA2); padding: 0.5rem; border-radius: 5px; margin-bottom: 1rem;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h3 style="color: white; margin: 0;">🔐 Login Portal</h3>
        <a href="http://localhost:8499" style="color: white; text-decoration: none; background: rgba(255,255,255,0.2); padding: 0.3rem 0.8rem; border-radius: 3px;">
            🏠 Back to Main
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

# Default teacher credentials for testing
DEFAULT_TEACHERS = {
    "admin@dropsafe.com": {
        "password": "admin123",
        "name": "Administrator",
        "role": "admin"
    },
    "teacher@dropsafe.com": {
        "password": "teacher123",
        "name": "Default Teacher",
        "role": "teacher"
    }
}

def load_student_data():
    """Load student data from CSV file"""
    try:
        if os.path.exists('student_data.csv'):
            return pd.read_csv('student_data.csv')
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading student data: {str(e)}")
        return pd.DataFrame()

def verify_teacher_credentials(username, password):
    """Verify teacher login credentials - email and password as per specification"""
    if username in DEFAULT_TEACHERS:
        stored_password = DEFAULT_TEACHERS[username]["password"]
        if password == stored_password:
            return DEFAULT_TEACHERS[username]
    return None

def verify_student_credentials(student_id, student_name):
    """Verify student login credentials - student ID and name as registered by teachers"""
    df = load_student_data()
    if not df.empty:
        # Check if student exists with matching ID and name
        student_match = df[(df['student_id'].astype(str) == str(student_id)) & 
                          (df['name'].str.lower() == student_name.lower())]
        if not student_match.empty:
            return student_match.iloc[0].to_dict()
    return None

def teacher_login():
    """Teacher login interface using email and password"""
    st.subheader("🎓 Teacher Login")
    
    with st.form("teacher_login_form"):
        email = st.text_input("Email Address", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            login_btn = st.form_submit_button("Login", use_container_width=True)
        
        if login_btn:
            if email and password:
                teacher_data = verify_teacher_credentials(email, password)
                if teacher_data:
                    st.session_state.user_type = "teacher"
                    st.session_state.user_data = teacher_data
                    st.session_state.authenticated = True
                    st.success(f"Welcome, {teacher_data['name']}!")
                    st.rerun()
                else:
                    st.error("Invalid email or password. Please try again.")
            else:
                st.warning("Please enter both email and password.")

def student_login():
    """Student login interface using student ID and name as registered by teachers"""
    st.subheader("🎓 Student Login")
    
    with st.form("student_login_form"):
        student_id = st.text_input("Student ID", placeholder="Enter your student ID")
        student_name = st.text_input("Student Name", placeholder="Enter your full name")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            login_btn = st.form_submit_button("Login", use_container_width=True)
        
        if login_btn:
            if student_id and student_name:
                student_data = verify_student_credentials(student_id, student_name)
                if student_data:
                    st.session_state.user_type = "student"
                    st.session_state.user_data = student_data
                    st.session_state.authenticated = True
                    st.success(f"Welcome, {student_data['name']}!")
                    st.rerun()
                else:
                    st.error("Invalid student ID or name. Please check your details and try again.")
            else:
                st.warning("Please enter both student ID and name.")

def main():
    """Main login page"""
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_type' not in st.session_state:
        st.session_state.user_type = None
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    
    # Check if user is already authenticated
    if st.session_state.authenticated:
        user_name = st.session_state.user_data.get('name', 'User')
        user_type = st.session_state.user_type
        
        st.success(f"✅ Welcome back, {user_name}! You are logged in as {user_type.title()}.")
        
        st.markdown("---")
        
        if user_type == "teacher":
            st.markdown("### 👨‍🏫 Teacher Dashboard Access")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🚀 Open Teacher Dashboard", type="primary", use_container_width=True):
                    st.markdown("""<script>window.open('http://localhost:8501', '_blank');</script>""", unsafe_allow_html=True)
            
            st.info("📊 Teacher Dashboard Features:")
            st.markdown("""
            - 📤 Upload and manage student data
            - 🤖 AI-powered risk assessment
            - 📈 Visual analytics and reports
            - 📥 Export high-risk student lists
            - 👥 Student performance monitoring
            """)
            
            st.markdown("**Direct Link:** [Teacher Dashboard](http://localhost:8501)")
            
        elif user_type == "student":
            st.markdown("### 🎓 Student Portal Access")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🚀 Open Student Portal", type="primary", use_container_width=True):
                    st.markdown("""<script>window.open('http://localhost:8502', '_blank');</script>""", unsafe_allow_html=True)
            
            st.info("🎯 Student Portal Features:")
            st.markdown("""
            - 📊 Personal risk assessment with alerts
            - 🤖 AI academic support chatbot
            - 📈 Performance tracking and trends
            - 💬 Feedback and support system
            - 🆘 Emergency contacts and resources
            """)
            
            st.markdown("**Direct Link:** [Student Portal](http://localhost:8502)")
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚪 Logout", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.success("Successfully logged out!")
                st.rerun()
        return
    
    # Login page header
    st.title("🔐 DropSafe Authentication")
    st.markdown("---")
    
    # Login type selection
    login_type = st.radio(
        "Select your login type:",
        ["Teacher", "Student"],
        horizontal=True
    )
    
    st.markdown("---")
    
    # Show appropriate login form
    if login_type == "Teacher":
        teacher_login()
        
        # Help section for teachers
        with st.expander("📋 Teacher Login Help"):
            st.info("""
            **Default Teacher Credentials:**
            - Email: admin@dropsafe.com, Password: admin123
            - Email: teacher@dropsafe.com, Password: teacher123
            
            Teachers login using their email and password to access the main dashboard.
            """)
            
            st.markdown("**After Login, you will be redirected to:**")
            st.markdown("🔗 [Teacher Dashboard](http://localhost:8501) - Main teaching interface")
    
    else:  # Student login
        student_login()
        
        # Help section for students
        with st.expander("📋 Student Login Help"):
            st.info("""
            **Student Login:**
            - Use your Student ID and full name as registered by your teacher
            - Both fields must match exactly with the data in the system
            - Contact your teacher if you cannot access your account
            
            Students can only login if their data has been uploaded by a teacher.
            """)
            
            st.markdown("**After Login, you will be redirected to:**")
            st.markdown("🔗 [Student Portal](http://localhost:8502) - Personal dashboard with risk alerts")
    
    # Footer with navigation links
    st.markdown("---")
    
    # Quick Access Section
    st.markdown("### 🔗 Quick Access Links")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("👨‍🏫 **Teacher Dashboard**")
        st.markdown("[Access Teacher Dashboard](http://localhost:8501)")
        st.caption("Upload data, monitor students, view analytics")
    
    with col2:
        st.markdown("🎓 **Student Portal**")
        st.markdown("[Access Student Portal](http://localhost:8502)")
        st.caption("Personal dashboard, risk alerts, AI support")
    
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>DropSafe - Student Dropout Risk Assessment System</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()