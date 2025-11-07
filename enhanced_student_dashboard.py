import streamlit as st
import pandas as pd
import os
from datetime import datetime
from risk_model import AdvancedRiskPredictor
import plotly.graph_objects as go
from shared_data import shared_data_manager
from ai_counselor import ai_counselor

# Page config
st.set_page_config(
    page_title="DropSafe - Student Portal", 
    page_icon="🎓",
    layout="wide"
)

# Professional color scheme CSS
st.markdown("""
<style>
    /* Color Variables - Professional Student Dashboard Colors */
    :root {
        --deep-blue: #1E3A8A;
        --sky-blue: #3B82F6;
        --safe-green: #10B981;
        --warning-amber: #F59E0B;
        --danger-red: #EF4444;
        --light-gray-bg: #F9FAFB;
        --white: #FFFFFF;
        --dark-gray: #374151;
        --medium-gray: #6B7280;
        --purple-accent: #8B5CF6;
    }
    
    /* Main App Background */
    .main {
        background-color: var(--light-gray-bg);
    }
    
    /* Student-specific styling */
    .student-header {
        background: linear-gradient(135deg, var(--sky-blue) 0%, var(--deep-blue) 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: var(--white);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
    }
    
    .alert-card {
        background: var(--white);
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid var(--sky-blue);
    }
    
    .high-risk-alert {
        background: #FEF2F2 !important;
        border-left-color: var(--danger-red) !important;
    }
    
    .medium-risk-alert {
        background: #FFFBEB !important;
        border-left-color: var(--warning-amber) !important;
    }
    
    .safe-alert {
        background: #F0FDF4 !important;
        border-left-color: var(--safe-green) !important;
    }
    
    .performance-card {
        background: var(--white);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
        border: 1px solid #E5E7EB;
    }
    
    .ai-counselor-section {
        background: linear-gradient(45deg, var(--purple-accent), #7C3AED);
        color: var(--white);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.3);
    }
    
    /* Streamlit Button Styling */
    .stButton > button {
        background: linear-gradient(45deg, var(--sky-blue), #2563EB) !important;
        color: var(--white) !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #2563EB, var(--deep-blue)) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Metrics styling */
    .metric {
        background: var(--white);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid #E5E7EB;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: var(--dark-gray) !important;
    }
    
    /* Success, Warning, Error styling with professional colors */
    .stSuccess {
        background-color: #F0FDF4 !important;
        border: 1px solid var(--safe-green) !important;
        color: #14532D !important;
    }
    
    .stWarning {
        background-color: #FFFBEB !important;
        border: 1px solid var(--warning-amber) !important;
        color: #92400E !important;
    }
    
    .stError {
        background-color: #FEF2F2 !important;
        border: 1px solid var(--danger-red) !important;
        color: #991B1B !important;
    }
    
    .stInfo {
        background-color: #EFF6FF !important;
        border: 1px solid var(--sky-blue) !important;
        color: #1E40AF !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--white) !important;
    }
</style>
""", unsafe_allow_html=True)

# Add navigation header with new professional colors
st.markdown("""
<div style="background: linear-gradient(90deg, #1E3A8A, #3B82F6); padding: 0.5rem; border-radius: 5px; margin-bottom: 1rem;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h3 style="color: white; margin: 0;">🎓 Student Portal</h3>
        <a href="http://localhost:8499" style="color: white; text-decoration: none; background: rgba(255,255,255,0.2); padding: 0.3rem 0.8rem; border-radius: 3px;">
            🏠 Back to Main
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize session state early
if 'student_logged_in' not in st.session_state:
    st.session_state.student_logged_in = False
if 'student_data' not in st.session_state:
    st.session_state.student_data = None

def load_student_data():
    """Load student data from CSV files"""
    try:
        for filename in ['sample_students.csv', 'student_risk_predictions.csv', 'all_students.csv']:
            if os.path.exists(filename):
                return pd.read_csv(filename)
        return None
    except:
        return None

def verify_student_login(student_id, name):
    """Verify student login credentials"""
    df = load_student_data()
    if df is not None:
        student_row = df[
            (df['student_id'].str.upper() == student_id.upper()) & 
            (df['name'].str.lower().str.contains(name.lower().strip()))
        ]
        if not student_row.empty:
            return student_row.iloc[0].to_dict()
    return None

def get_risk_assessment(student_data):
    """Get risk assessment for student"""
    try:
        if os.path.exists('advanced_risk_model.pkl'):
            predictor = AdvancedRiskPredictor()
            predictor.load_model('advanced_risk_model.pkl')
            student_df = pd.DataFrame([student_data])
            risk_scores = predictor.predict_risk(student_df)
            risk_category, risk_emoji = predictor.get_risk_category(risk_scores[0])
            return {'category': risk_category, 'emoji': risk_emoji, 'score': risk_scores[0]}
        else:
            # Fallback calculation
            attendance = float(student_data.get('attendance_percentage', 100))
            marks = float(student_data.get('marks_percentage', 100))
            fees_status = student_data.get('fees_status', 'paid')
            
            risk_score = 0
            if attendance < 60: risk_score += 1
            if marks < 40: risk_score += 1
            if fees_status == 'pending': risk_score += 0.5
            
            if risk_score >= 1.5:
                return {'category': "High Risk", 'emoji': "🔴", 'score': 2}
            elif risk_score >= 0.5:
                return {'category': "Medium Risk", 'emoji': "🟠", 'score': 1}
            else:
                return {'category': "Safe", 'emoji': "🟢", 'score': 0}
    except:
        return {'category': "Unknown", 'emoji': "❓", 'score': -1}

def show_personalized_alerts(student_data):
    """Display personalized alerts from teacher dashboard data"""
    student_id = str(student_data.get('student_id', ''))
    alert_data = shared_data_manager.get_student_alert(student_id)
    
    if alert_data:
        risk_level = alert_data['risk_level']
        alert_message = alert_data['alert_message']
        last_updated = alert_data['last_updated']
        
        # Display alert based on risk level with new professional color coding
        if risk_level == 'high':
            st.error("🚨 HIGH PRIORITY ALERT")
            st.markdown(f"<div style='background: #FEF2F2; border-left: 5px solid #EF4444; padding: 15px; margin: 10px 0; border-radius: 5px;'><strong style='color: #991B1B;'>{alert_message}</strong></div>", unsafe_allow_html=True)
        elif risk_level == 'medium':
            st.warning("⚠️ ATTENTION REQUIRED")
            st.markdown(f"<div style='background: #FFFBEB; border-left: 5px solid #F59E0B; padding: 15px; margin: 10px 0; border-radius: 5px;'><strong style='color: #92400E;'>{alert_message}</strong></div>", unsafe_allow_html=True)
        else:
            st.success("✅ POSITIVE STATUS")
            st.markdown(f"<div style='background: #F0FDF4; border-left: 5px solid #10B981; padding: 15px; margin: 10px 0; border-radius: 5px;'><strong style='color: #14532D;'>{alert_message}</strong></div>", unsafe_allow_html=True)
        
        # Show when alert was last updated
        if last_updated:
            try:
                update_time = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
                st.caption(f"Last updated: {update_time.strftime('%Y-%m-%d %H:%M')}")
            except:
                st.caption(f"Last updated: {last_updated}")
        
        # Show counselor assignment status
        if alert_data.get('counselor_assigned', False):
            st.info("💼 A counselor has been assigned to support you. Check the AI Chat Counselor below!")
    
    else:
        # Fallback to original risk assessment if no personalized alert
        st.info("💙 Welcome! Your personalized alerts will appear here once your teacher updates your risk assessment.")

def show_risk_alerts(risk_assessment, student_data):
    """Display risk-based alerts following project specifications"""
    risk_category = risk_assessment['category']
    attendance = float(student_data.get('attendance_percentage', 100))
    marks = float(student_data.get('marks_percentage', 100))
    fees_status = student_data.get('fees_status', 'paid')
    
    # High Risk - Red color coding as per specifications
    if risk_category == "High Risk":
        st.error("URGENT ATTENTION REQUIRED")
        st.error("Your academic performance needs immediate intervention!")
        
        # Specific risk indicators
        if attendance < 60:
            st.error("Critical Attendance Issue: Your attendance is dangerously low")
        if marks < 40:
            st.error("Academic Emergency: Your marks need immediate improvement")
        if fees_status == 'pending':
            st.error("Fee Payment Urgent: Please clear pending fees immediately")
        
        # Actionable recommendations for high risk
        st.markdown("### Immediate Actions Required:")
        st.markdown("• Contact Academic Advisor: (555) 123-4567")
        st.markdown("• Visit Counseling Services: (555) 123-4570")
        st.markdown("• Start Emergency Tutoring: (555) 123-HELP")
        st.markdown("• Apply for Financial Aid: (555) 123-4569")
        
    # Medium Risk - Orange color coding as per specifications
    elif risk_category == "Medium Risk":
        st.warning("Attention Needed")
        st.warning("Your academic performance shows concerning trends.")
        
        # Specific warnings
        if attendance < 75:
            st.warning("Attendance Concern: Improve your class attendance")
        if marks < 60:
            st.warning("Academic Warning: Your marks need improvement")
        if fees_status == 'pending':
            st.warning("Fee Reminder: Please clear pending fees soon")
        
        # Actionable recommendations for medium risk
        st.markdown("### Recommended Actions:")
        st.markdown("• Join study groups")
        st.markdown("• Meet with teachers weekly")
        st.markdown("• Contact Tutoring Center: (555) 123-4567")
        st.markdown("• Create a study schedule")
        
    # Safe - Green color coding as per specifications
    else:
        st.success("Excellent Performance!")
        st.success("Keep up the great work! You're on track for success.")
        
        # Maintenance recommendations for safe students
        st.markdown("### Keep It Up:")
        st.markdown("• Maintain your excellent performance")
        st.markdown("• Consider helping peers")
        st.markdown("• Explore advanced opportunities")
        st.markdown("• Apply for honors programs")

def create_performance_charts(student_data):
    """Create performance visualization with color coding"""
    attendance = float(student_data.get('attendance_percentage', 0))
    marks = float(student_data.get('marks_percentage', 0))
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Attendance gauge with new professional risk color coding
        fig_attendance = go.Figure(go.Indicator(
            mode="gauge+number",
            value=attendance,
            title={'text': "Attendance %"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#3B82F6"},  # Sky Blue
                'steps': [
                    {'range': [0, 60], 'color': "#EF4444"},      # Danger Red
                    {'range': [60, 75], 'color': "#F59E0B"},     # Warning Amber
                    {'range': [75, 85], 'color': "#84CC16"},     # Light Green
                    {'range': [85, 100], 'color': "#10B981"}    # Safe Green
                ],
                'threshold': {
                    'line': {'color': "#EF4444", 'width': 4},
                    'thickness': 0.75,
                    'value': 75
                }
            }
        ))
        fig_attendance.update_layout(height=250)
        st.plotly_chart(fig_attendance, use_container_width=True)
    
    with col2:
        # Marks gauge with new professional risk color coding
        fig_marks = go.Figure(go.Indicator(
            mode="gauge+number",
            value=marks,
            title={'text': "Marks %"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#10B981"},  # Safe Green
                'steps': [
                    {'range': [0, 40], 'color': "#EF4444"},      # Danger Red
                    {'range': [40, 60], 'color': "#F59E0B"},     # Warning Amber
                    {'range': [60, 75], 'color': "#84CC16"},     # Light Green
                    {'range': [75, 100], 'color': "#10B981"}    # Safe Green
                ],
                'threshold': {
                    'line': {'color': "#EF4444", 'width': 4},
                    'thickness': 0.75,
                    'value': 60
                }
            }
        ))
        fig_marks.update_layout(height=250)
        st.plotly_chart(fig_marks, use_container_width=True)

def main():
    # Initialize session state FIRST
    if 'student_logged_in' not in st.session_state:
        st.session_state.student_logged_in = False
    if 'student_data' not in st.session_state:
        st.session_state.student_data = None
    
    st.title("DropSafe - Student Portal")
    st.markdown("**Secure Student Authentication & Risk Assessment**")
    
    # Authentication check
    if not st.session_state.student_logged_in:
        st.subheader("Student Login")
        
        # Check if data exists
        df = load_student_data()
        if df is None:
            st.error("No student data found!")
            st.info("Please ask your teacher to upload student data first.")
            return
        
        # Login form
        with st.form("student_login"):
            col1, col2 = st.columns(2)
            
            with col1:
                student_id = st.text_input(
                    "Student ID", 
                    placeholder="Enter your Student ID (e.g., STU001)"
                )
            
            with col2:
                name = st.text_input(
                    "Full Name", 
                    placeholder="Enter your name"
                )
            
            login_btn = st.form_submit_button("Login", type="primary")
            
            if login_btn:
                if student_id and name:
                    student_data = verify_student_login(student_id, name)
                    if student_data:
                        st.session_state.student_logged_in = True
                        st.session_state.student_data = student_data
                        st.success(f"Welcome, {student_data['name']}!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Please check your Student ID and Name.")
                else:
                    st.warning("Please enter both Student ID and Name.")
        
        # Demo students
        with st.expander("Demo Students (For Testing)"):
            if df is not None:
                st.markdown("**Available students for testing:**")
                demo_df = df[['student_id', 'name']].head(10)
                st.dataframe(demo_df, use_container_width=True)
        
        return
    
    # Student is logged in - show dashboard
    student = st.session_state.student_data
    
    # Sidebar with logout and emergency contacts
    with st.sidebar:
        st.markdown(f"### Welcome {student['name']}")
        st.markdown(f"**ID:** {student['student_id']}")
        
        if st.button("Logout"):
            st.session_state.student_logged_in = False
            st.session_state.student_data = None
            st.rerun()
        
        st.markdown("---")
        st.markdown("### Emergency Contacts")
        st.markdown("Academic: (555) 123-4567")
        st.markdown("Counseling: (555) 123-4570")
        st.markdown("Finance: (555) 123-4569")
        st.markdown("Crisis: (555) 999-8888")
    
    # Get risk assessment
    risk_assessment = get_risk_assessment(student)
    
    # Main dashboard
    st.markdown(f"## Dashboard - {student['name']} {risk_assessment['emoji']}")
    
    # Personalized alerts section (PRIORITY: from teacher dashboard data)
    st.markdown("### 🎯 Personalized Alerts from Your Teachers")
    show_personalized_alerts(student)
    
    st.markdown("---")
    
    # Risk assessment section (fallback/additional info)
    st.markdown("### 📊 Risk Assessment & Recommendations")
    show_risk_alerts(risk_assessment, student)
    
    st.markdown("---")
    
    # Performance metrics with color coding
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        attendance_val = student['attendance_percentage']
        st.metric("Attendance", f"{attendance_val:.1f}%")
    
    with col2:
        marks_val = student['marks_percentage']
        st.metric("Marks", f"{marks_val:.1f}%")
    
    with col3:
        fee_status = "Paid" if student['fees_status'] == 'paid' else "Pending"
        st.metric("Fees", fee_status)
    
    with col4:
        st.metric("Risk Level", f"{risk_assessment['emoji']} {risk_assessment['category']}")
    
    # Performance charts with risk color coding
    st.markdown("### Performance Visualization")
    create_performance_charts(student)
    
    # Risk-tailored quick actions
    st.markdown("### Quick Actions")
    
    if risk_assessment['category'] == "High Risk":
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Emergency Help", type="primary"):
                st.info("Connecting you to emergency academic support...")
                st.markdown("**Call NOW:** (555) 123-4567")
        with col2:
            if st.button("Urgent Tutoring"):
                st.info("Emergency tutoring requested.")
                st.markdown("**Tutor Hotline:** (555) 123-HELP")
        with col3:
            if st.button("Financial Aid"):
                st.info("Financial aid application initiated.")
                st.markdown("**Aid Office:** (555) 123-4569")
    
    elif risk_assessment['category'] == "Medium Risk":
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Study Groups"):
                st.info("Study group information sent to your email.")
        with col2:
            if st.button("Study Plan"):
                st.info("Personalized study plan created.")
        with col3:
            if st.button("Teacher Meeting"):
                st.info("Teacher meeting scheduled.")
    
    else:  # Safe students
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Advanced Courses"):
                st.info("Advanced course recommendations sent.")
        with col2:
            if st.button("Peer Mentoring"):
                st.info("Peer mentoring opportunities available.")
        with col3:
            if st.button("Honors Program"):
                st.info("Honors program application available.")
    
    st.markdown("---")
    
    # AI Chat Counselor Section
    st.markdown("### 🤖 AI Chat Counselor")
    st.markdown("Need someone to talk to? Our AI counselor is here 24/7 to provide support and guidance.")
    
    # Create tabs for better organization
    tab1, tab2 = st.tabs(["💬 Chat with Counselor", "📊 Your Wellness Summary"])
    
    with tab1:
        # Render AI chat interface
        ai_counselor.render_chat_interface(
            student_id=str(student['student_id']), 
            student_name=student['name']
        )
    
    with tab2:
        # Wellness summary based on chat history and risk level
        st.markdown("#### 🌟 Your Wellness Journey")
        
        chat_history = shared_data_manager.get_chat_history(str(student['student_id']))
        if chat_history:
            st.metric("Chat Sessions", len(chat_history))
            
            # Show recent activity
            if len(chat_history) > 0:
                latest_chat = chat_history[-1]
                try:
                    latest_time = datetime.fromisoformat(latest_chat['timestamp'])
                    st.metric("Last Session", latest_time.strftime('%Y-%m-%d %H:%M'))
                except:
                    st.metric("Last Session", "Recent")
            
            # Wellness tips based on risk level
            st.markdown("#### 💚 Wellness Tips for You")
            if risk_assessment['category'] == "High Risk":
                st.markdown("""
                - 🌱 **Daily Check-ins**: Try to chat with the counselor daily
                - 📞 **Connect**: Reach out to friends and family regularly
                - 🏃 **Move**: Even 10 minutes of walking can help
                - 📚 **Focus**: Break study tasks into smaller chunks
                """)
            elif risk_assessment['category'] == "Medium Risk":
                st.markdown("""
                - ⏰ **Schedule**: Create a balanced daily routine
                - 📝 **Plan**: Use the counselor to discuss study strategies
                - 👥 **Social**: Maintain connections with classmates
                - 🎯 **Goals**: Set small, achievable daily goals
                """)
            else:
                st.markdown("""
                - 🎆 **Celebrate**: Acknowledge your achievements
                - 🔄 **Maintain**: Keep up your good habits
                - 🤝 **Help Others**: Consider peer mentoring
                - 📈 **Grow**: Explore new challenges and opportunities
                """)
        else:
            st.info("🎉 Welcome! Start a conversation with the AI counselor to begin your wellness journey.")
            st.markdown("""
            **The AI Counselor can help you with:**
            - 😌 Stress management
            - 📚 Study strategies  
            - 😰 Anxiety support
            - 💬 Someone to listen
            - 🎯 Goal setting
            """)

if __name__ == "__main__":
    main()