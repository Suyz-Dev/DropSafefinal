import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os
from risk_model import AdvancedRiskPredictor
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="DropSafe - Student Portal", 
    page_icon="🎓",
    layout="wide"
)

# Chatbot responses
CHATBOT_RESPONSES = {
    "greeting": [
        "Hello! I'm here to help you improve your academic performance. How can I assist you today?",
        "Hi there! I'm your academic support assistant. What would you like to discuss?",
        "Welcome! I'm here to help you succeed in your studies. What's on your mind?"
    ],
    "attendance": [
        "📅 **Attendance Improvement Tips:**\n- Set daily alarms for classes\n- Find a study buddy for accountability\n- Talk to your teacher about any challenges\n- Use a calendar app to track your schedule\n- Remember: Every class matters for your success!",
        "📚 **Attendance is crucial for your success!**\n- Aim for 85%+ attendance\n- If you miss a class, get notes from classmates\n- Schedule make-up sessions with teachers\n- Identify and address barriers to attendance\n- Contact the counseling office if you need support"
    ],
    "marks": [
        "📊 **Academic Performance Tips:**\n- Create a study schedule and stick to it\n- Form study groups with classmates\n- Seek help from teachers during office hours\n- Use online resources for extra practice\n- Take regular breaks while studying",
        "📈 **Boost Your Grades:**\n- Review class notes daily\n- Practice past papers and assignments\n- Ask questions during class\n- Get a tutor if needed\n- Stay organized with folders and planners"
    ],
    "fees": [
        "💰 **Fee Payment Assistance:**\n- Contact the financial aid office immediately\n- Ask about payment plans or extensions\n- Look into scholarship opportunities\n- Consider part-time work options\n- Don't let financial stress affect your studies - we're here to help!",
        "🏦 **Financial Support Options:**\n- Emergency financial aid programs\n- Work-study opportunities\n- External scholarship databases\n- Payment installment plans\n- Contact: finance@college.edu or call (555) 123-4567"
    ],
    "stress": [
        "🧘 **Managing Academic Stress:**\n- Take regular breaks and exercise\n- Practice deep breathing or meditation\n- Talk to friends, family, or counselors\n- Maintain a healthy sleep schedule\n- Remember: It's okay to ask for help!",
        "💪 **Stress Management Resources:**\n- Counseling services: counseling@college.edu\n- Peer support groups every Tuesday 3-4 PM\n- Mental health apps: Headspace, Calm\n- Campus wellness center: Room 201, Student Center\n- 24/7 Crisis helpline: (555) 999-8888"
    ],
    "general": [
        "🎯 **General Academic Success Tips:**\n- Set clear, achievable goals\n- Stay organized with planners and calendars\n- Build good relationships with teachers\n- Join study groups and academic clubs\n- Take care of your physical and mental health",
        "📚 **Academic Resources Available:**\n- Library study rooms and tutoring center\n- Writing center for essay help\n- Math lab for problem-solving support\n- Career counseling services\n- Academic advisor meetings"
    ]
}

def load_student_data():
    """Load student data from CSV files"""
    try:
        # Try to load from various possible files
        for filename in ['sample_students.csv', 'all_students.csv', 'students.csv', 'student_risk_predictions.csv']:
            if os.path.exists(filename):
                df = pd.read_csv(filename)
                return df
        return None
    except:
        return None

def verify_student_login(student_id, name):
    """Verify student login credentials against uploaded data"""
    df = load_student_data()
    if df is not None:
        # Check if student exists in the data
        student_row = df[
            (df['student_id'].str.upper() == student_id.upper()) & 
            (df['name'].str.lower().str.contains(name.lower().strip()))
        ]
        
        if not student_row.empty:
            return student_row.iloc[0].to_dict()
    
    return None

def get_student_risk_assessment(student_data):
    """Get comprehensive risk assessment for student"""
    try:
        # Load the trained model if available
        if os.path.exists('advanced_risk_model.pkl'):
            predictor = AdvancedRiskPredictor()
            predictor.load_model('advanced_risk_model.pkl')
            
            # Create dataframe with student data
            student_df = pd.DataFrame([student_data])
            
            # Get risk prediction
            risk_scores = predictor.predict_risk(student_df)
            risk_probabilities = predictor.predict_risk_proba(student_df)
            
            risk_score = risk_scores[0]
            risk_category, risk_emoji = predictor.get_risk_category(risk_score)
            
            return {
                'risk_score': risk_score,
                'risk_category': risk_category,
                'risk_emoji': risk_emoji,
                'probabilities': risk_probabilities[0] if risk_probabilities is not None else None
            }
        else:
            # Fallback to rule-based assessment
            risk_score = calculate_rule_based_risk(student_data)
            if risk_score >= 2:
                return {'risk_score': risk_score, 'risk_category': "High Risk", 'risk_emoji': "🔴", 'probabilities': None}
            elif risk_score >= 1:
                return {'risk_score': risk_score, 'risk_category': "Medium Risk", 'risk_emoji': "🟠", 'probabilities': None}
            else:
                return {'risk_score': risk_score, 'risk_category': "Safe", 'risk_emoji': "🟢", 'probabilities': None}
    except Exception as e:
        st.error(f"Error in risk assessment: {str(e)}")
        return {'risk_score': 0, 'risk_category': "Unknown", 'risk_emoji': "❓", 'probabilities': None}

def calculate_rule_based_risk(student_data):
    """Calculate risk using simple rules as fallback"""
    risk_score = 0
    
    attendance = float(student_data.get('attendance_percentage', 100))
    marks = float(student_data.get('marks_percentage', 100))
    fees_status = student_data.get('fees_status', 'paid')
    
    # Attendance factor
    if attendance < 60:
        risk_score += 1
    elif attendance < 75:
        risk_score += 0.5
    
    # Marks factor
    if marks < 40:
        risk_score += 1
    elif marks < 60:
        risk_score += 0.5
    
    # Fees factor
    if fees_status == 'pending':
        risk_score += 0.5
    
    return int(risk_score)

def show_risk_alerts(risk_assessment, student_data):
    """Display risk-based alerts and recommendations"""
    risk_category = risk_assessment['risk_category']
    risk_emoji = risk_assessment['risk_emoji']
    
    attendance = float(student_data.get('attendance_percentage', 100))
    marks = float(student_data.get('marks_percentage', 100))
    fees_status = student_data.get('fees_status', 'paid')
    
    # Main risk alert
    if risk_category == "High Risk":
        st.error(f"🚨 **URGENT ATTENTION REQUIRED** {risk_emoji}")
        st.error("Your academic performance indicates immediate intervention is needed!")
        
        # Specific alerts
        alerts = []
        if attendance < 60:
            alerts.append("📅 **Critical Attendance Issue**: Your attendance is critically low")
        if marks < 40:
            alerts.append("📊 **Academic Emergency**: Your marks need immediate improvement")
        if fees_status == 'pending':
            alerts.append("💰 **Fee Payment Urgent**: Please clear your pending fees immediately")
        
        for alert in alerts:
            st.error(alert)
        
        # Immediate action items
        st.markdown("### 🎯 Immediate Action Required:")
        st.markdown("🗓️ Schedule meeting with academic advisor TODAY")
        st.markdown("📞 Contact counseling services: (555) 123-4570")
        st.markdown("📚 Join remedial classes immediately")
        st.markdown("👥 Meet with your teachers for extra support")
        
    elif risk_category == "Medium Risk":
        st.warning(f"⚠️ **Attention Needed** {risk_emoji}")
        st.warning("Your academic performance shows some concerning trends. Let's address them now!")
        
        # Specific warnings
        warnings = []
        if attendance < 75:
            warnings.append("📅 **Attendance Concern**: Improve your class attendance")
        if marks < 60:
            warnings.append("📊 **Academic Warning**: Your marks need improvement")
        if fees_status == 'pending':
            warnings.append("💰 **Fee Reminder**: Please clear your pending fees soon")
        
        for warning in warnings:
            st.warning(warning)
        
        # Recommended actions
        st.markdown("### 📈 Recommended Actions:")
        st.markdown("🗓️ Schedule weekly check-ins with teachers")
        st.markdown("📚 Join study groups for better understanding")
        st.markdown("🕰️ Create a study schedule and stick to it")
        st.markdown("📞 Contact tutoring center: (555) 123-4567")
        
    else:
        st.success(f"✅ **Excellent Performance!** {risk_emoji}")
        st.success("Keep up the great work! Your academic performance is on track.")
        
        # Encouragement and maintenance tips
        st.markdown("### 🎆 Keep It Up:")
        st.markdown("🎯 Continue your excellent attendance record")
        st.markdown("💪 Maintain your strong academic performance")
        st.markdown("🌟 Consider helping peers who might be struggling")
        st.markdown("📈 Explore advanced learning opportunities")
    
    return risk_category

def create_performance_visualization(student_data, risk_assessment):
    """Create visual representation of student performance"""
    attendance = float(student_data.get('attendance_percentage', 0))
    marks = float(student_data.get('marks_percentage', 0))
    
    # Gauge charts for performance metrics
    col1, col2 = st.columns(2)
    
    with col1:
        # Attendance gauge
        fig_attendance = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = attendance,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Attendance %"},
            delta = {'reference': 85, 'position': "top"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 60], 'color': "lightcoral"},
                    {'range': [60, 75], 'color': "lightyellow"},
                    {'range': [75, 85], 'color': "lightgreen"},
                    {'range': [85, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 85
                }
            }
        ))
        fig_attendance.update_layout(height=300)
        st.plotly_chart(fig_attendance, use_container_width=True)
    
    with col2:
        # Marks gauge
        fig_marks = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = marks,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Marks %"},
            delta = {'reference': 75, 'position': "top"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkgreen"},
                'steps': [
                    {'range': [0, 40], 'color': "lightcoral"},
                    {'range': [40, 60], 'color': "lightyellow"},
                    {'range': [60, 75], 'color': "lightgreen"},
                    {'range': [75, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 75
                }
            }
        ))
        fig_marks.update_layout(height=300)
        st.plotly_chart(fig_marks, use_container_width=True)
    
    # Risk probability chart if available
    if risk_assessment.get('probabilities') is not None:
        st.subheader("📈 Risk Assessment Breakdown")
        probs = risk_assessment['probabilities']
        
        fig_risk = go.Figure(data=[
            go.Bar(
                x=['Safe', 'Medium Risk', 'High Risk'],
                y=[probs[0], probs[1], probs[2]],
                marker_color=['green', 'orange', 'red']
            )
        ])
        fig_risk.update_layout(
            title="AI Risk Assessment Probabilities",
            yaxis_title="Probability",
            xaxis_title="Risk Level",
            height=400
        )
        st.plotly_chart(fig_risk, use_container_width=True)

def get_chatbot_response(user_input, risk_level):
    """Generate chatbot response based on user input and risk level"""
    user_input = user_input.lower()
    
    # Determine response category
    if any(word in user_input for word in ['hello', 'hi', 'hey', 'start']):
        response_type = "greeting"
    elif any(word in user_input for word in ['attendance', 'absent', 'miss class', 'bunk']):
        response_type = "attendance"
    elif any(word in user_input for word in ['marks', 'grades', 'exam', 'test', 'study', 'score']):
        response_type = "marks"
    elif any(word in user_input for word in ['fees', 'payment', 'money', 'financial', 'pay']):
        response_type = "fees"
    elif any(word in user_input for word in ['stress', 'worried', 'anxious', 'help', 'problem']):
        response_type = "stress"
    else:
        response_type = "general"
    
    # Get response based on type
    import random
    base_response = random.choice(CHATBOT_RESPONSES[response_type])
    
    # Add risk-specific advice
    if risk_level == "High Risk":
        risk_advice = "\n\n🚨 **Urgent Action Needed:** Please schedule a meeting with your academic advisor immediately. We're here to support you!"
    elif risk_level == "Medium Risk":
        risk_advice = "\n\n⚠️ **Important:** Consider implementing these suggestions soon to improve your academic standing."
    else:
        risk_advice = "\n\n✅ **Good Job:** Keep up the great work! These tips can help you maintain your excellent performance."
    
    return base_response + risk_advice

def save_feedback(student_id, satisfaction, feedback_text=""):
    """Save student feedback to CSV"""
    try:
        feedback_data = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'student_id': student_id,
            'satisfaction': satisfaction,
            'feedback': feedback_text
        }
        
        # Load existing feedback or create new
        feedback_file = 'student_feedback.csv'
        if os.path.exists(feedback_file):
            df = pd.read_csv(feedback_file)
            df = pd.concat([df, pd.DataFrame([feedback_data])], ignore_index=True)
        else:
            df = pd.DataFrame([feedback_data])
        
        df.to_csv(feedback_file, index=False)
        
        # Save unsatisfied feedback separately
        if satisfaction == 'Unsatisfied':
            unsatisfied_file = 'unsatisfied_feedback.csv'
            unsatisfied_data = df[df['satisfaction'] == 'Unsatisfied']
            unsatisfied_data.to_csv(unsatisfied_file, index=False)
        
        return True
    except Exception as e:
        st.error(f"Error saving feedback: {str(e)}")
        return False

def main():
    # Initialize session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'student_id' not in st.session_state:
        st.session_state.student_id = None
    if 'student_data' not in st.session_state:
        st.session_state.student_data = None
    
    # Header
    st.title("🎓 DropSafe - Student Portal")
    st.markdown("**Your Academic Success & Risk Assessment Dashboard**")
    
    # Authentication check
    if st.session_state.student_id is None:
        st.subheader("🔐 Student Authentication")
        
        # Check if student data is available
        df = load_student_data()
        if df is None:
            st.error("❌ No student data found!")
            st.info("📊 Please ask your teacher to upload student data through the Teacher Dashboard first.")
            st.markdown("---")
            st.markdown("### 👨‍🏫 Teacher Instructions:")
            st.markdown("1. Go to Teacher Dashboard")
            st.markdown("2. Upload CSV file with student data")
            st.markdown("3. Students can then login using their ID and Name")
            return
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("student_login_form"):
                student_id = st.text_input(
                    "🆔 Student ID", 
                    placeholder="Enter your Student ID (e.g., STU001)",
                    help="Your unique student identifier as provided by your institution"
                )
                name = st.text_input(
                    "👤 Full Name", 
                    placeholder="Enter your full name",
                    help="Your name as registered in the system (partial matches allowed)"
                )
                
                col_a, col_b, col_c = st.columns([1, 2, 1])
                with col_b:
                    login_button = st.form_submit_button("🚀 Login to Portal", type="primary")
                
                if login_button:
                    if student_id and name:
                        student_data = verify_student_login(student_id, name)
                        if student_data:
                            st.session_state.student_id = student_id
                            st.session_state.student_data = student_data
                            st.success(f"✅ Welcome, {student_data['name']}!")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("❌ Student not found. Please check your Student ID and Name.")
                            st.info("💡 Make sure your name matches the one registered by your teacher.")
                    else:
                        st.warning("⚠️ Please enter both Student ID and Name.")
        
        with col2:
            st.info("📄 **Login Help**")
            st.markdown("- Use your official Student ID")
            st.markdown("- Enter your full registered name")
            st.markdown("- Names are case-insensitive")
            st.markdown("- Partial name matches work")
        
        # Show available students for demo
        if df is not None and len(df) > 0:
            with st.expander("🎭 Demo Students (Testing Purpose)"):
                st.info("🎯 **Sample students available for testing:**")
                sample_students = df[['student_id', 'name']].head(10)
                
                st.markdown("| Student ID | Name |")
                st.markdown("|------------|------|")
                for _, student in sample_students.iterrows():
                    st.markdown(f"| {student['student_id']} | {student['name']} |")
                
                st.markdown("📝 **How to test:** Copy any Student ID and Name from above")
        
        return
    
    # Student is logged in - show dashboard
    student = st.session_state.student_data
    
    # Logout button in sidebar
    with st.sidebar:
        st.markdown(f"### 👋 Welcome, {student['name']}!")
        st.markdown(f"**ID:** {student['student_id']}")
        st.markdown("---")
        
        if st.button("🚺 Logout", type="secondary"):
            st.session_state.student_id = None
            st.session_state.student_data = None
            st.session_state.chat_history = []
            st.rerun()
        
        st.markdown("---")
        st.markdown("📞 **Emergency Contacts**")
        st.markdown("🏫 Academic Advisor: (555) 123-4567")
        st.markdown("🧑‍⚕️ Counseling: (555) 123-4570")
        st.markdown("💰 Finance Office: (555) 123-4569")
        st.markdown("🏥 IT Support: (555) 123-4571")
    
    # Get comprehensive risk assessment
    risk_assessment = get_student_risk_assessment(student)
    
    # Main dashboard content
    st.markdown(f"## 🎯 Personal Dashboard - {student['name']} {risk_assessment['risk_emoji']}")
    
    # Risk Alert Section (Most Important)
    st.markdown("### 🚨 Risk Assessment & Alerts")
    current_risk = show_risk_alerts(risk_assessment, student)
    
    st.markdown("---")
    
    # Performance metrics section
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        attendance = float(student.get('attendance_percentage', 0))
        target_attendance = 85
        delta_att = attendance - target_attendance
        st.metric(
            "📅 Attendance", 
            f"{attendance:.1f}%", 
            delta=f"{delta_att:+.1f}% vs target",
            delta_color="normal" if delta_att >= 0 else "inverse"
        )
    
    with col2:
        marks = float(student.get('marks_percentage', 0))
        target_marks = 75
        delta_marks = marks - target_marks
        st.metric(
            "📊 Marks", 
            f"{marks:.1f}%",
            delta=f"{delta_marks:+.1f}% vs target",
            delta_color="normal" if delta_marks >= 0 else "inverse"
        )
    
    with col3:
        fee_status = student.get('fees_status', 'unknown')
        fee_display = "✅ Paid" if fee_status == 'paid' else "⏳ Pending"
        st.metric("💰 Fees", fee_display)
    
    with col4:
        st.metric(
            "🎯 Risk Level", 
            f"{risk_assessment['risk_emoji']} {risk_assessment['risk_category']}"
        )
    
    # Performance visualization
    st.markdown("### 📈 Performance Visualization")
    create_performance_visualization(student, risk_assessment)
    
    st.markdown("---")
    
    # Quick Action Buttons (Context-aware based on risk)
    st.markdown("### 🎯 Quick Actions")
    
    if current_risk == "High Risk":
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("🆘 Schedule Counseling", type="primary"):
                response = "\n🆘 **URGENT COUNSELING SCHEDULING**\n\nI've prioritized your request for immediate counseling. Here's what you need to do RIGHT NOW:\n\n🗓️ **Immediate Steps:**\n1. Call counseling services: (555) 123-4570\n2. Request URGENT appointment\n3. Mention your high-risk academic status\n\n👥 **Available Counselors:**\n- Dr. Sarah Johnson (Academic Crisis Specialist)\n- Prof. Mike Chen (Student Success Coordinator)\n- Ms. Emily Davis (Mental Health Counselor)\n\n📞 **24/7 Crisis Support:** (555) 999-8888\n\n⏰ **Office Hours:** Mon-Fri 8 AM - 6 PM\n📍 **Location:** Student Center, Room 201\n\n👍 Remember: Seeking help is a sign of strength, not weakness!"
                st.session_state.chat_history.append(("I need urgent counseling help", response))
                st.rerun()
        
        with col2:
            if st.button("📚 Emergency Tutoring"):
                response = "\n📚 **EMERGENCY TUTORING ACTIVATED**\n\nYour academic situation requires immediate intervention. Here's your emergency tutoring plan:\n\n🆘 **URGENT TUTORING OPTIONS:**\n\n1. **Crash Course Recovery Program**\n   - Intensive 2-week program\n   - Daily 3-hour sessions\n   - Covers all weak subjects\n   - Starts immediately\n\n2. **One-on-One Emergency Sessions**\n   - Available today/tomorrow\n   - Subject-specific experts\n   - Flexible timing\n\n3. **Peer Emergency Study Groups**\n   - High-performing students\n   - Immediate availability\n   - Study room access\n\n📞 **Emergency Tutoring Hotline:** (555) 123-HELP\n📋 **Online Booking:** emergency.tutoring.edu\n📍 **Walk-in Center:** Library, 3rd Floor\n\n⏰ **Available NOW:** 24/7 emergency academic support"
                st.session_state.chat_history.append(("I need emergency tutoring", response))
                st.rerun()
        
        with col3:
            if st.button("👥 Contact Family"):
                response = "\n👥 **FAMILY NOTIFICATION ASSISTANCE**\n\nI understand this is a difficult situation. Here's how to involve your family constructively:\n\n📞 **Conversation Starters:**\n\n🗺️ **What to Say:**\n\"I'm facing some academic challenges and want to be proactive about addressing them. The school has resources to help, and I'd like your support.\"\n\n📈 **Focus on Solutions:**\n- Mention the support systems available\n- Emphasize your commitment to improvement\n- Ask for their encouragement and understanding\n\n👍 **Family Support Strategies:**\n- Regular check-ins (not overwhelming)\n- Celebration of small improvements\n- Help with creating a study environment\n- Understanding of stress and pressure\n\n🏫 **School-Family Partnership:**\n- Family counseling sessions available\n- Parent-teacher conferences\n- Progress update systems\n\n📞 **Family Support Hotline:** (555) 123-4572"
                st.session_state.chat_history.append(("Help me talk to my family about my academic struggles", response))
                st.rerun()
        
        with col4:
            if st.button("💰 Financial Aid"):
                response = "\n💰 **EMERGENCY FINANCIAL AID**\n\nDon't let financial stress add to your academic challenges. Help is available:\n\n🆘 **IMMEDIATE FINANCIAL SUPPORT:**\n\n1. **Emergency Student Fund**\n   - Up to $2,000 immediate assistance\n   - No repayment required\n   - 24-48 hour approval\n\n2. **Academic Crisis Scholarship**\n   - Covers tuition/fees for struggling students\n   - Merit + need based\n   - Available this semester\n\n3. **Payment Plan Extensions**\n   - Extended deadlines\n   - Reduced late fees\n   - Flexible arrangements\n\n📞 **Emergency Financial Aid:** (555) 123-4569\n📋 **Online Application:** emergency.aid.edu\n📍 **Office:** Administration Building, Room 105\n\n🕰️ **Office Hours:** Mon-Fri 8 AM - 5 PM\n🆘 **Emergency Line:** Available 24/7\n\n📄 **Required Documents:** Student ID, current financial situation summary"
                st.session_state.chat_history.append(("I need emergency financial aid", response))
                st.rerun()
    
    elif current_risk == "Medium Risk":
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📚 Study Tips"):
                response = get_chatbot_response("study tips", current_risk)
                st.session_state.chat_history.append(("I need study tips", response))
                st.rerun()
        
        with col2:
            if st.button("📅 Attendance Help"):
                response = get_chatbot_response("attendance help", current_risk)
                st.session_state.chat_history.append(("Help with attendance", response))
                st.rerun()
        
        with col3:
            if st.button("👥 Study Groups"):
                response = "\n👥 **STUDY GROUP OPPORTUNITIES**\n\nJoin collaborative learning sessions to improve your performance:\n\n📚 **Available Study Groups:**\n\n1. **Subject-Specific Groups**\n   - Math & Science: Tuesdays 4-6 PM\n   - Literature & Writing: Wednesdays 3-5 PM\n   - History & Social Studies: Thursdays 4-6 PM\n\n2. **Exam Preparation Groups**\n   - Midterm prep sessions\n   - Final exam boot camps\n   - Test-taking strategies\n\n3. **Peer Tutoring Circles**\n   - Students helping students\n   - Friendly, supportive environment\n   - Various skill levels welcome\n\n📍 **Location:** Library Study Rooms\n📋 **Sign-up:** study.groups.edu\n📞 **Coordinator:** (555) 123-4567\n\n🎆 **Benefits:** Better understanding, new friendships, improved grades!"
                st.session_state.chat_history.append(("I want to join study groups", response))
                st.rerun()
        
        with col4:
            if st.button("💰 Fee Assistance"):
                response = get_chatbot_response("fee payment help", current_risk)
                st.session_state.chat_history.append(("I need fee assistance", response))
                st.rerun()
    
    else:  # Safe/Good performance
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("🎆 Advanced Learning"):
                response = "\n🎆 **ADVANCED LEARNING OPPORTUNITIES**\n\nSince you're performing excellently, here are ways to challenge yourself further:\n\n🎓 **Academic Excellence Programs:**\n\n1. **Honors Courses**\n   - Advanced curriculum\n   - Smaller class sizes\n   - Research opportunities\n\n2. **Independent Study Projects**\n   - Choose your own research topic\n   - Faculty mentorship\n   - Present findings at conferences\n\n3. **Leadership Opportunities**\n   - Student government\n   - Academic clubs president\n   - Peer tutoring coordinator\n\n4. **Scholarship Applications**\n   - Merit-based scholarships\n   - Research grants\n   - Study abroad programs\n\n📞 **Academic Excellence Office:** (555) 123-4580\n📋 **Applications:** excellence.portal.edu\n\n🌟 Keep pushing your boundaries!"
                st.session_state.chat_history.append(("I want advanced learning opportunities", response))
                st.rerun()
        
        with col2:
            if st.button("👥 Peer Mentoring"):
                response = "\n👥 **PEER MENTORING PROGRAM**\n\nShare your success and help others while developing leadership skills:\n\n🎯 **Mentoring Opportunities:**\n\n1. **Academic Peer Tutor**\n   - Help struggling students\n   - Flexible schedule\n   - Paid position available\n\n2. **Study Group Leader**\n   - Lead study sessions\n   - Develop teaching skills\n   - Build leadership experience\n\n3. **New Student Mentor**\n   - Guide incoming students\n   - Orientation assistance\n   - Long-term relationship building\n\n4. **Subject Specialist**\n   - Focus on your strongest subjects\n   - Create learning materials\n   - Conduct workshops\n\n📞 **Peer Mentoring Coordinator:** (555) 123-4575\n📋 **Application:** mentor.program.edu\n\n🎆 **Benefits:** Leadership skills, resume building, giving back!"
                st.session_state.chat_history.append(("I want to become a peer mentor", response))
                st.rerun()
        
        with col3:
            if st.button("🎓 Career Planning"):
                response = "\n🎓 **CAREER PLANNING & DEVELOPMENT**\n\nPlan your future with your strong academic foundation:\n\n🗺️ **Career Development Services:**\n\n1. **Career Assessment**\n   - Personality and interest tests\n   - Skill evaluation\n   - Career matching\n\n2. **Internship Opportunities**\n   - Summer internships\n   - Part-time positions\n   - Research assistantships\n\n3. **Graduate School Preparation**\n   - Application guidance\n   - Test preparation (GRE, GMAT, etc.)\n   - Personal statement writing\n\n4. **Professional Networking**\n   - Alumni connections\n   - Industry events\n   - LinkedIn optimization\n\n📞 **Career Services:** (555) 123-4590\n📋 **Online Portal:** careers.edu\n📍 **Office:** Student Center, 2nd Floor\n\n🎆 Start planning your amazing future!"
                st.session_state.chat_history.append(("I want career planning help", response))
                st.rerun()
        
        with col4:
            if st.button("🎆 Extra Credit"):
                response = "\n🎆 **EXTRA CREDIT & ENRICHMENT**\n\nMaximize your academic potential with additional opportunities:\n\n📚 **Extra Credit Options:**\n\n1. **Research Projects**\n   - Faculty-supervised research\n   - Original investigations\n   - Publication opportunities\n\n2. **Community Service Learning**\n   - Volunteer with academic credit\n   - Real-world application\n   - Social impact projects\n\n3. **Academic Competitions**\n   - Math olympiads\n   - Debate tournaments\n   - Science fairs\n\n4. **Creative Projects**\n   - Art exhibitions\n   - Writing contests\n   - Innovation challenges\n\n📞 **Academic Enhancement:** (555) 123-4585\n📋 **Project Portal:** projects.edu\n\n🌟 Turn your excellence into extraordinary achievements!"
                st.session_state.chat_history.append(("I want extra credit opportunities", response))
                st.rerun()("🎓 DropSafe - Student Portal")
    st.markdown("**Your Academic Success Companion**")
    
    # Student login section
    if st.session_state.student_id is None:
        st.subheader("🔐 Student Login")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            student_id = st.text_input("Enter your Student ID", placeholder="e.g., STU001")
            
        with col2:
            if st.button("Login", type="primary"):
                if student_id:
                    # Load student data
                    df = load_student_data()
                    if df is not None:
                        student_row = df[df['student_id'] == student_id]
                        if not student_row.empty:
                            st.session_state.student_id = student_id
                            st.session_state.student_data = student_row.iloc[0]
                            st.success(f"Welcome, {st.session_state.student_data['name']}!")
                            st.rerun()
                        else:
                            st.error("Student ID not found. Please check your ID or contact the administration.")
                    else:
                        st.error("No student data available. Please contact the administration.")
                else:
                    st.error("Please enter your Student ID")
        
        # Demo/Guest access
        with st.expander("🎲 Demo Access"):
            st.info("For demonstration purposes, you can use these sample Student IDs:")
            
            # Generate sample data to show available IDs
            if st.button("Generate Sample IDs"):
                from risk_model import generate_sample_data
                sample_df = generate_sample_data(10)
                st.dataframe(sample_df[['student_id', 'name']], use_container_width=True)
                
                # Save sample data for login
                sample_df.to_csv('sample_students.csv', index=False)
                st.success("Sample data generated! Use any Student ID above to login.")
    
    else:
        # Student is logged in
        student = st.session_state.student_data
        
        # Determine risk level (you might need to recompute this)
        risk_score = 0
        if student['attendance_percentage'] < 75:
            risk_score += 1
        if student['marks_percentage'] < 60:
            risk_score += 1
        if student['fees_status'] == 'pending':
            risk_score += 1
        
        if risk_score >= 2:
            risk_level = "High Risk"
            risk_color = "🔴"
        elif risk_score == 1:
            risk_level = "Medium Risk"
            risk_color = "🟠"
        else:
            risk_level = "Safe"
            risk_color = "🟢"
        
        # Logout button
        if st.button("Logout", type="secondary"):
            st.session_state.student_id = None
            st.session_state.student_data = None
            st.session_state.chat_history = []
            st.rerun()
        
        # Student dashboard
        st.header(f"Welcome, {student['name']}! {risk_color}")
        
        # Risk alert
        if risk_level == "High Risk":
            st.error(f"🚨 **URGENT ATTENTION NEEDED** - Your academic status is at {risk_level}. Please take immediate action!")
        elif risk_level == "Medium Risk":
            st.warning(f"⚠️ **Attention Required** - Your academic status is at {risk_level}. Let's work together to improve!")
        else:
            st.success(f"✅ **Great Job!** - Your academic status is {risk_level}. Keep up the excellent work!")
        
        # Student metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📅 Attendance", f"{student['attendance_percentage']:.1f}%", 
                     delta=f"Target: 85%", delta_color="inverse" if student['attendance_percentage'] < 85 else "normal")
        
        with col2:
            st.metric("📊 Marks", f"{student['marks_percentage']:.1f}%",
                     delta=f"Target: 70%", delta_color="inverse" if student['marks_percentage'] < 70 else "normal")
        
        with col3:
            fee_status = "✅ Paid" if student['fees_status'] == 'paid' else "⏳ Pending"
            st.metric("💰 Fees", fee_status)
        
        with col4:
            st.metric("🎯 Risk Level", f"{risk_color} {risk_level}")
        
        # Chatbot section
        st.header("🤖 Academic Support Chatbot")
        
        # Chat interface
        with st.container():
            # Display chat history
            for i, (user_msg, bot_msg) in enumerate(st.session_state.chat_history):
                with st.chat_message("user"):
                    st.write(user_msg)
                with st.chat_message("assistant"):
                    st.write(bot_msg)
            
            # Chat input
            user_input = st.chat_input("Ask me anything about improving your academic performance...")
            
            if user_input:
                # Generate bot response
                bot_response = get_chatbot_response(user_input, risk_level)
                
                # Add to chat history
                st.session_state.chat_history.append((user_input, bot_response))
                
                # Display new messages
                with st.chat_message("user"):
                    st.write(user_input)
                with st.chat_message("assistant"):
                    st.write(bot_response)
                
                st.rerun()
        
        # Quick action buttons
        st.subheader("🚀 Quick Actions")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📚 Study Tips"):
                response = get_chatbot_response("study tips", risk_level)
                st.session_state.chat_history.append(("I need study tips", response))
                st.rerun()
        
        with col2:
            if st.button("📅 Attendance Help"):
                response = get_chatbot_response("attendance help", risk_level)
                st.session_state.chat_history.append(("Help with attendance", response))
                st.rerun()
        
        with col3:
            if st.button("💰 Fee Assistance"):
                response = get_chatbot_response("fee payment help", risk_level)
                st.session_state.chat_history.append(("I need fee assistance", response))
                st.rerun()
        
        with col4:
            if st.button("🧘 Stress Management"):
                response = get_chatbot_response("stress management", risk_level)
                st.session_state.chat_history.append(("Help with stress", response))
                st.rerun()
        
        # Feedback section
        st.header("📝 Feedback")
        
        with st.form("feedback_form"):
            st.subheader("How satisfied are you with the guidance provided?")
            
            satisfaction = st.radio(
                "Satisfaction Level:",
                ["Satisfied", "Unsatisfied"],
                horizontal=True
            )
            
            feedback_text = st.text_area(
                "Additional Comments (Optional):",
                placeholder="Tell us how we can improve our support..."
            )
            
            submitted = st.form_submit_button("Submit Feedback", type="primary")
            
            if submitted:
                if save_feedback(st.session_state.student_id, satisfaction, feedback_text):
                    st.success("Thank you for your feedback! 🙏")
                    
                    if satisfaction == "Unsatisfied":
                        st.info("We've noted your concern. A counselor will reach out to you soon.")
        
        # Emergency contacts
        with st.expander("🆘 Emergency Contacts & Resources"):
            st.markdown("""
            **Academic Support:**
            - Academic Advisor: advisor@college.edu
            - Tutoring Center: (555) 123-4567
            - Library Help Desk: (555) 123-4568
            
            **Financial Aid:**
            - Financial Aid Office: finaid@college.edu
            - Emergency Fund: (555) 123-4569
            
            **Mental Health:**
            - Counseling Services: (555) 123-4570
            - Crisis Hotline: (555) 999-8888 (24/7)
            - Wellness Center: Room 201, Student Center
            
            **Technical Support:**
            - IT Help Desk: (555) 123-4571
            - Online Learning Support: online@college.edu
            """)

if __name__ == "__main__":
    main()