import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import os
from shared_data import shared_data_manager

# Configure page
st.set_page_config(
    page_title="DropSafe - Counsellor Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for counsellor theme with purple accent
st.markdown("""
<style>
    /* Color Variables - Professional Counsellor Colors with Purple Accent */
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
        --purple-light: #A78BFA;
        --purple-dark: #7C3AED;
    }
    
    /* Main App Background */
    .main {
        background-color: var(--light-gray-bg);
    }
    
    .main-header {
        background: linear-gradient(90deg, var(--purple-accent), var(--purple-dark));
        padding: 1rem;
        border-radius: 10px;
        color: var(--white);
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.3);
    }
    
    .counsellor-card {
        background: var(--white);
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid var(--purple-accent);
        transition: transform 0.2s ease, box-shadow 0.3s ease;
    }
    
    .counsellor-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(139, 92, 246, 0.15);
    }
    
    .high-priority {
        border-left-color: var(--danger-red) !important;
        background: #FEF2F2 !important;
    }
    
    .medium-priority {
        border-left-color: var(--warning-amber) !important;
        background: #FFFBEB !important;
    }
    
    .low-priority {
        border-left-color: var(--safe-green) !important;
        background: #F0FDF4 !important;
    }
    
    .intervention-tracker {
        background: var(--white);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 2px solid var(--purple-light);
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .mental-health-section {
        background: linear-gradient(135deg, var(--purple-accent) 0%, var(--purple-dark) 100%);
        color: var(--white);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.3);
    }
    
    .live-monitoring {
        background: linear-gradient(45deg, var(--purple-light), var(--purple-accent));
        color: var(--white);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.25);
    }
    
    /* Streamlit Button Styling for Counsellor */
    .stButton > button {
        background: linear-gradient(45deg, var(--purple-accent), var(--purple-dark)) !important;
        color: var(--white) !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, var(--purple-dark), #6B21A8) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(139, 92, 246, 0.4) !important;
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
        background-color: #F3E8FF !important;
        border: 1px solid var(--purple-accent) !important;
        color: #581C87 !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--white) !important;
    }
    
    /* Metrics with purple accent */
    .metric {
        background: var(--white);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid #E5E7EB;
        border-top: 3px solid var(--purple-accent);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_counsellor_data():
    """Load student data from shared system and fallback to generated data"""
    try:
        # First, try to load from shared data system
        student_lists = shared_data_manager.get_student_lists()
        
        if student_lists and (student_lists.get('high_risk') or student_lists.get('medium_risk')):
            # Combine all student data from shared system
            all_students = []
            
            for risk_level, students in [('High Risk', student_lists.get('high_risk', [])), 
                                        ('Medium Risk', student_lists.get('medium_risk', [])),
                                        ('Safe', student_lists.get('low_risk', []))]:
                for student in students:
                    # Convert shared data format to counsellor dashboard format
                    counsellor_student = {
                        'student_id': student.get('Student_ID', student.get('student_id', 'Unknown')),
                        'name': student.get('Name', student.get('name', 'Unknown')),
                        'grade': student.get('Grade', student.get('grade', 10)),
                        'attendance_rate': float(student.get('Attendance_Percentage', student.get('attendance_percentage', 85))),
                        'gpa': float(student.get('Marks_Percentage', student.get('marks_percentage', 75))) / 25,  # Convert to 4.0 scale
                        'family_income': student.get('Family_Income', student.get('family_income', 'Medium')),
                        'risk_level': risk_level,
                        'fees_status': student.get('Fees_Status', student.get('fees_status', 'paid')),
                        # Add counsellor-specific fields
                        'mental_health_score': np.random.normal(70 if risk_level == 'Safe' else (40 if risk_level == 'High Risk' else 55), 15),
                        'social_engagement': np.random.normal(65 if risk_level == 'Safe' else (35 if risk_level == 'High Risk' else 50), 20),
                        'counselling_sessions': np.random.poisson(1 if risk_level == 'Safe' else (5 if risk_level == 'High Risk' else 3)),
                        'last_intervention': (datetime.now() - timedelta(days=np.random.randint(1, 30))).strftime('%Y-%m-%d'),
                        'intervention_type': np.random.choice([
                            'Academic Support', 'Mental Health', 'Family Outreach', 
                            'Peer Mentoring', 'Career Guidance'
                        ])
                    }
                    # Ensure mental health score is within valid range
                    counsellor_student['mental_health_score'] = max(0, min(100, counsellor_student['mental_health_score']))
                    counsellor_student['social_engagement'] = max(0, min(100, counsellor_student['social_engagement']))
                    
                    all_students.append(counsellor_student)
            
            if all_students:
                df = pd.DataFrame(all_students)
                st.info(f"📊 Updated with latest data from Teacher Dashboard! Last updated: {student_lists.get('last_updated', 'Unknown')}")
                return df
        
        # Fallback: Check for existing CSV files
        if os.path.exists('student_data.csv'):
            df = pd.read_csv('student_data.csv')
            return df
        else:
            # Generate sample data for counsellor dashboard
            np.random.seed(42)
            n_students = 50
            
            df = pd.DataFrame({
                'student_id': [f'STU{str(i+1).zfill(3)}' for i in range(n_students)],
                'name': [f'Student {i+1}' for i in range(n_students)],
                'grade': np.random.choice([9, 10, 11, 12], n_students),
                'attendance_rate': np.random.normal(85, 15, n_students).clip(0, 100),
                'gpa': np.random.normal(2.8, 0.8, n_students).clip(0, 4),
                'family_income': np.random.choice(['Low', 'Medium', 'High'], n_students, p=[0.3, 0.5, 0.2]),
                'mental_health_score': np.random.normal(70, 20, n_students).clip(0, 100),
                'social_engagement': np.random.normal(60, 25, n_students).clip(0, 100),
                'counselling_sessions': np.random.poisson(3, n_students),
                'risk_level': np.random.choice(['Low', 'Medium', 'High'], n_students, p=[0.5, 0.3, 0.2])
            })
            
            # Add intervention data
            df['last_intervention'] = pd.date_range(
                start=datetime.now() - timedelta(days=30),
                end=datetime.now(),
                periods=n_students
            ).strftime('%Y-%m-%d')
            
            df['intervention_type'] = np.random.choice([
                'Academic Support', 'Mental Health', 'Family Outreach', 
                'Peer Mentoring', 'Career Guidance'
            ], n_students)
            
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

def counsellor_sidebar():
    """Counsellor dashboard sidebar"""
    # Back to Main Page button with enhanced styling
    st.sidebar.markdown("## 🏠 Navigation")
    
    # Enhanced back button with success styling
    if st.sidebar.button("🎅 Back to Main Page", type="primary", use_container_width=True, help="Return to DropSafe main page"):
        st.sidebar.success("Returning to main page...")
        st.markdown("""
        <script>
            window.location.href = 'http://localhost:8499';
        </script>
        """, unsafe_allow_html=True)
        st.markdown("""<meta http-equiv="refresh" content="0; url=http://localhost:8499" />""", unsafe_allow_html=True)
    
    # Add direct link as backup with purple theme
    st.sidebar.markdown("""
    <div style="text-align: center; margin: 0.5rem 0;">
        <a href="http://localhost:8499" style="
            background: linear-gradient(45deg, #8B5CF6, #7C3AED);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            text-decoration: none;
            font-weight: bold;
            display: block;
        ">
            🏠 Direct Link to Main
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    st.sidebar.markdown("## 🧠 Counsellor Tools")
    
    # Quick actions
    st.sidebar.markdown("### Quick Actions")
    if st.sidebar.button("📝 Schedule Intervention"):
        st.sidebar.success("Intervention scheduling opened!")
    
    if st.sidebar.button("📞 Emergency Contact"):
        st.sidebar.error("Emergency protocol activated!")
    
    if st.sidebar.button("📋 Generate Report"):
        st.sidebar.info("Report generation started...")
    
    # Filters
    st.sidebar.markdown("### Filters")
    
    risk_filter = st.sidebar.multiselect(
        "Risk Level",
        ['Safe', 'Medium Risk', 'High Risk'],
        default=['Medium Risk', 'High Risk']
    )
    
    grade_filter = st.sidebar.multiselect(
        "Grade Level",
        [9, 10, 11, 12],
        default=[9, 10, 11, 12]
    )
    
    intervention_filter = st.sidebar.selectbox(
        "Intervention Type",
        ['All', 'Academic Support', 'Mental Health', 'Family Outreach', 'Peer Mentoring', 'Career Guidance']
    )
    
    return risk_filter, grade_filter, intervention_filter

def mental_health_overview(df):
    """Mental health overview section"""
    st.markdown("""
    <div class="mental-health-section">
        <h3>🧠 Mental Health Overview</h3>
        <p>Comprehensive mental health monitoring and intervention tracking</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_mental_health = df['mental_health_score'].mean()
        st.metric(
            "Average Mental Health Score",
            f"{avg_mental_health:.1f}/100",
            delta=f"{np.random.uniform(-2, 2):.1f}" # Simulated change
        )
    
    with col2:
        at_risk_mental = len(df[df['mental_health_score'] < 50])
        st.metric(
            "Students At Risk",
            at_risk_mental,
            delta=-2  # Improvement
        )
    
    with col3:
        total_sessions = df['counselling_sessions'].sum()
        st.metric(
            "Total Counselling Sessions",
            total_sessions,
            delta=15  # This month
        )
    
    with col4:
        avg_engagement = df['social_engagement'].mean()
        st.metric(
            "Social Engagement Score",
            f"{avg_engagement:.1f}/100",
            delta=f"{np.random.uniform(-1, 3):.1f}"
        )

def live_risk_monitoring():
    """Real-time risk monitoring from teacher dashboard"""
    st.markdown("## 📡 Live Risk Monitoring")
    st.markdown("Real-time updates from Teacher Dashboard risk assessments")
    
    # Get latest data from shared system
    student_lists = shared_data_manager.get_student_lists()
    
    if student_lists and student_lists.get('last_updated'):
        try:
            last_update = datetime.fromisoformat(student_lists['last_updated'])
            time_diff = datetime.now() - last_update
            
            if time_diff.total_seconds() < 300:  # Less than 5 minutes
                status_color = "green"
                status_text = "🟢 Live"
            elif time_diff.total_seconds() < 3600:  # Less than 1 hour
                status_color = "orange"
                status_text = "🟡 Recent"
            else:
                status_color = "red"
                status_text = "🔴 Stale"
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"**Data Status:** <span style='color: {status_color}'>{status_text}</span>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"**Last Update:** {last_update.strftime('%H:%M:%S')}")
            
            with col3:
                high_risk_count = len(student_lists.get('high_risk', []))
                st.markdown(f"**High Risk:** 🔴 {high_risk_count}")
            
            with col4:
                medium_risk_count = len(student_lists.get('medium_risk', []))
                st.markdown(f"**Medium Risk:** 🟠 {medium_risk_count}")
            
            # Quick action buttons for immediate interventions
            if high_risk_count > 0:
                st.error(f"🚨 {high_risk_count} students require immediate intervention!")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📞 Emergency Contact Protocol", type="primary"):
                        st.success("Emergency contact protocol initiated for high-risk students")
                with col2:
                    if st.button("💰 Schedule Crisis Interventions"):
                        st.success("Crisis intervention sessions scheduled")
            
            if medium_risk_count > 0:
                st.warning(f"⚠️ {medium_risk_count} students need scheduled support")
                
                if st.button("📅 Schedule Support Sessions"):
                    st.success("Support sessions scheduled for medium-risk students")
                    
        except Exception as e:
            st.error(f"Error processing update time: {e}")
    else:
        st.info("📊 Waiting for data from Teacher Dashboard...")
        st.markdown("Risk monitoring will activate once teachers upload and assess student data.")

def student_satisfaction_feedback():
    """Display student satisfaction feedback from AI counselor"""
    st.markdown("## 📊 Student Satisfaction Feedback")
    st.markdown("Feedback from students about their AI counseling sessions")
    
    # Get feedback data
    feedback_data = shared_data_manager.get_counselor_feedback()
    
    if not feedback_data:
        st.info("No feedback received yet. Students will be able to provide feedback after their AI counseling sessions.")
        return
    
    # Convert to DataFrame for easier handling
    feedback_list = []
    for student_id, feedback in feedback_data.items():
        feedback_list.append({
            'student_id': student_id,
            'student_name': feedback.get('student_name', 'Unknown'),
            'satisfaction': feedback.get('satisfaction', 'Unknown'),
            'timestamp': feedback.get('timestamp', '')
        })
    
    feedback_df = pd.DataFrame(feedback_list)
    
    # Summary metrics
    total_feedback = len(feedback_df)
    satisfied_count = len(feedback_df[feedback_df['satisfaction'] == 'satisfied'])
    unsatisfied_count = len(feedback_df[feedback_df['satisfaction'] == 'unsatisfied'])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Feedback", total_feedback)
    
    with col2:
        st.metric("Satisfied", satisfied_count, 
                 delta=f"{(satisfied_count/total_feedback)*100:.1f}%" if total_feedback > 0 else "0%",
                 delta_color="normal")
    
    with col3:
        st.metric("Unsatisfied", unsatisfied_count,
                 delta=f"{(unsatisfied_count/total_feedback)*100:.1f}%" if total_feedback > 0 else "0%",
                 delta_color="inverse")
    
    # Satisfaction trend chart
    if not feedback_df.empty:
        feedback_df['date'] = pd.to_datetime(feedback_df['timestamp']).dt.date
        daily_feedback = feedback_df.groupby(['date', 'satisfaction']).size().reset_index(name='count')
        
        fig = px.bar(daily_feedback, 
                     x='date', 
                     y='count', 
                     color='satisfaction',
                     title="Daily Feedback Trend",
                     color_discrete_map={'satisfied': '#10B981', 'unsatisfied': '#EF4444'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed feedback table
    st.markdown("### Detailed Feedback")
    
    # Prepare data for display
    display_df = feedback_df[['student_name', 'satisfaction', 'timestamp']].copy()
    display_df['satisfaction'] = display_df['satisfaction'].apply(
        lambda x: "👍 Satisfied" if x == "satisfied" else "👎 Unsatisfied" if x == "unsatisfied" else x
    )
    display_df['timestamp'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
    
    # Sort by timestamp (newest first)
    display_df = display_df.sort_values('timestamp', ascending=False)
    
    st.dataframe(display_df.rename(columns={
        'student_name': 'Student Name',
        'satisfaction': 'Feedback',
        'timestamp': 'Session Time'
    }), use_container_width=True)

def priority_students(df, risk_filter):
    """Display priority students requiring immediate attention"""
    st.markdown("## 🚨 Priority Students")
    
    # Filter high-risk students
    priority_df = df[df['risk_level'].isin(risk_filter)].copy()
    priority_df = priority_df.sort_values(['risk_level', 'mental_health_score'])
    
    for idx, student in priority_df.head(5).iterrows():
        risk_class = f"{student['risk_level'].lower()}-priority"
        
        st.markdown(f"""
        <div class="counsellor-card {risk_class}">
            <h4>{student['name']} (ID: {student['student_id']})</h4>
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <strong>Risk Level:</strong> {student['risk_level']}<br>
                    <strong>Mental Health Score:</strong> {student['mental_health_score']:.1f}/100<br>
                    <strong>Grade:</strong> {student['grade']}
                </div>
                <div>
                    <strong>Attendance:</strong> {student['attendance_rate']:.1f}%<br>
                    <strong>GPA:</strong> {student['gpa']:.2f}<br>
                    <strong>Sessions:</strong> {student['counselling_sessions']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons for each student
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button(f"📅 Schedule Session", key=f"schedule_{student['student_id']}"):
                st.success(f"Session scheduled for {student['name']}")
        with col2:
            if st.button(f"📞 Contact Family", key=f"contact_{student['student_id']}"):
                st.info(f"Family contact initiated for {student['name']}")
        with col3:
            if st.button(f"📋 View Full Profile", key=f"profile_{student['student_id']}"):
                st.info(f"Opening full profile for {student['name']}")
        with col4:
            if st.button(f"🎯 Create Intervention", key=f"intervention_{student['student_id']}"):
                st.success(f"Intervention plan created for {student['name']}")

def intervention_tracking(df):
    """Track ongoing interventions"""
    st.markdown("## 📊 Intervention Tracking")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Intervention type distribution
        intervention_counts = df['intervention_type'].value_counts()
        fig_interventions = px.bar(
            x=intervention_counts.index,
            y=intervention_counts.values,
            title="Active Interventions by Type",
            color=intervention_counts.values,
            color_continuous_scale="Viridis"
        )
        fig_interventions.update_layout(
            xaxis_title="Intervention Type",
            yaxis_title="Number of Students",
            showlegend=False
        )
        st.plotly_chart(fig_interventions, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="intervention-tracker">
            <h4>📈 Intervention Success Rate</h4>
            <div style="font-size: 2rem; color: #4CAF50; text-align: center;">78%</div>
            <p style="text-align: center;">Students showing improvement</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="intervention-tracker">
            <h4>🎯 This Week's Goals</h4>
            <ul>
                <li>✅ Complete 15 assessments</li>
                <li>⏳ Schedule 8 family meetings</li>
                <li>📋 Review 12 intervention plans</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def risk_analytics(df):
    """Detailed risk analytics for counsellors"""
    st.markdown("## 📈 Risk Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Risk level distribution with professional colors - handle both formats
        risk_counts = df['risk_level'].value_counts()
        
        # Create color mapping that handles both old and new formats
        color_map = {}
        for risk_level in risk_counts.index:
            if risk_level in ['Low', 'Safe']:
                color_map[risk_level] = '#10B981'  # Safe Green
            elif risk_level in ['Medium', 'Medium Risk']:
                color_map[risk_level] = '#F59E0B'  # Warning Amber
            elif risk_level in ['High', 'High Risk']:
                color_map[risk_level] = '#EF4444'  # Danger Red
            else:
                color_map[risk_level] = '#6B7280'  # Default gray
        
        fig_risk = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            title="Student Risk Distribution",
            color_discrete_map=color_map
        )
        st.plotly_chart(fig_risk, use_container_width=True)
    
    with col2:
        # Mental health vs academic performance with professional colors - handle both formats
        # Create color mapping that handles both old and new formats
        color_map = {}
        for risk_level in df['risk_level'].unique():
            if risk_level in ['Low', 'Safe']:
                color_map[risk_level] = '#10B981'  # Safe Green
            elif risk_level in ['Medium', 'Medium Risk']:
                color_map[risk_level] = '#F59E0B'  # Warning Amber
            elif risk_level in ['High', 'High Risk']:
                color_map[risk_level] = '#EF4444'  # Danger Red
            else:
                color_map[risk_level] = '#6B7280'  # Default gray
        
        fig_scatter = px.scatter(
            df,
            x='mental_health_score',
            y='gpa',
            color='risk_level',
            size='counselling_sessions',
            title="Mental Health vs Academic Performance",
            color_discrete_map=color_map
        )
        fig_scatter.update_layout(
            xaxis_title="Mental Health Score",
            yaxis_title="GPA"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

def student_profiles(df, grade_filter, intervention_filter):
    """Detailed student profiles view"""
    st.markdown("## 👥 Student Profiles")
    
    # Apply filters
    filtered_df = df[df['grade'].isin(grade_filter)].copy()
    if intervention_filter != 'All':
        filtered_df = filtered_df[filtered_df['intervention_type'] == intervention_filter]
    
    # Search functionality
    search_term = st.text_input("🔍 Search students by name or ID")
    if search_term:
        filtered_df = filtered_df[
            filtered_df['name'].str.contains(search_term, case=False) |
            filtered_df['student_id'].str.contains(search_term, case=False)
        ]
    
    # Display students in expandable cards
    for idx, student in filtered_df.iterrows():
        with st.expander(f"{student['name']} - {student['risk_level']} Risk"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Academic Information**")
                st.write(f"Student ID: {student['student_id']}")
                st.write(f"Grade: {student['grade']}")
                st.write(f"GPA: {student['gpa']:.2f}")
                st.write(f"Attendance: {student['attendance_rate']:.1f}%")
            
            with col2:
                st.markdown("**Counselling Data**")
                st.write(f"Mental Health Score: {student['mental_health_score']:.1f}/100")
                st.write(f"Social Engagement: {student['social_engagement']:.1f}/100")
                st.write(f"Sessions Completed: {student['counselling_sessions']}")
                st.write(f"Last Intervention: {student['last_intervention']}")
            
            with col3:
                st.markdown("**Risk Assessment**")
                # Fix risk level mapping to handle both formats
                risk_level = student['risk_level']
                if risk_level == 'High Risk':
                    risk_color = '🔴'
                    risk_display = 'High'
                elif risk_level == 'Medium Risk':
                    risk_color = '🟡'
                    risk_display = 'Medium'
                elif risk_level == 'Safe':
                    risk_color = '🟢'
                    risk_display = 'Safe'
                else:
                    # Fallback for other formats
                    risk_color = {'Low': '🟢', 'Medium': '🟡', 'High': '🔴'}.get(risk_level, '❓')
                    risk_display = risk_level
                
                st.write(f"Risk Level: {risk_color} {risk_display}")
                st.write(f"Family Income: {student['family_income']}")
                st.write(f"Current Intervention: {student['intervention_type']}")
            
            # Action buttons
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.button(f"📅 Schedule", key=f"sched_{student['student_id']}")
            with col2:
                st.button(f"📝 Add Note", key=f"note_{student['student_id']}")
            with col3:
                st.button(f"📊 View History", key=f"history_{student['student_id']}")
            with col4:
                st.button(f"📧 Contact", key=f"contact2_{student['student_id']}")

def main():
    """Main counsellor dashboard function"""
    # Add header navigation bar with purple theme
    st.markdown("""
    <div style="background: linear-gradient(90deg, #8B5CF6, #7C3AED); padding: 0.5rem; border-radius: 5px; margin-bottom: 1rem;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h3 style="color: white; margin: 0;">🧠 Counsellor Dashboard</h3>
            <a href="http://localhost:8499" style="color: white; text-decoration: none; background: rgba(255,255,255,0.2); padding: 0.3rem 0.8rem; border-radius: 3px; font-weight: bold;">
                🏠 Back to Main
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🧠 DropSafe Counsellor Dashboard</h1>
        <p>Comprehensive student support and intervention management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    df = load_counsellor_data()
    
    if df.empty:
        st.error("No student data available. Please ensure data is uploaded through the Teacher Dashboard.")
        return
    
    # Sidebar filters
    risk_filter, grade_filter, intervention_filter = counsellor_sidebar()
    
    # Main dashboard sections
    mental_health_overview(df)
    
    st.markdown("---")
    
    # Live risk monitoring section (NEW)
    live_risk_monitoring()
    
    st.markdown("---")
    
    # Student satisfaction feedback section
    student_satisfaction_feedback()
    
    st.markdown("---")
    
    # Priority students section
    if risk_filter:
        priority_students(df, risk_filter)
    
    st.markdown("---")
    
    # Intervention tracking
    intervention_tracking(df)
    
    st.markdown("---")
    
    # Risk analytics
    risk_analytics(df)
    
    st.markdown("---")
    
    # Student profiles
    if grade_filter:
        student_profiles(df, grade_filter, intervention_filter)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>🧠 DropSafe Counsellor Dashboard | Student Support & Intervention Management</p>
        <p>For technical support or emergency protocols, contact: support@dropsafe.edu</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()