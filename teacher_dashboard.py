import streamlit as st
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
from risk_model import RiskPredictor, generate_sample_data
from shared_data import shared_data_manager

# Page config
st.set_page_config(
    page_title="DropSafe - Teacher Dashboard", 
    page_icon="👨‍🏫",
    layout="wide"
)

# Custom CSS for new professional color scheme
st.markdown("""
<style>
    /* Color Variables - Professional Color System */
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
    
    .main-header {
        background: linear-gradient(135deg, var(--deep-blue) 0%, var(--sky-blue) 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: var(--white);
        box-shadow: 0 8px 25px rgba(30, 58, 138, 0.3);
    }
    
    .welcome-section {
        background: var(--white);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        border-left: 5px solid var(--sky-blue);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .feature-card {
        background: var(--white);
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid var(--sky-blue);
        transition: transform 0.2s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.15);
    }
    
    .csv-format-card {
        background: #F0FDF4;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid var(--safe-green);
    }
    
    .metric-card {
        background: linear-gradient(45deg, var(--sky-blue), var(--deep-blue));
        color: var(--white);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    .upload-section {
        background: var(--white);
        padding: 2rem;
        border-radius: 15px;
        border: 2px dashed var(--sky-blue);
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .action-button {
        background: linear-gradient(45deg, var(--sky-blue), var(--deep-blue));
        color: var(--white);
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: bold;
        margin: 0.2rem;
    }
    
    /* Risk Level Specific Colors */
    .high-risk {
        background-color: #FEF2F2 !important;
        border-left-color: var(--danger-red) !important;
        color: #991B1B;
    }
    
    .medium-risk {
        background-color: #FFFBEB !important;
        border-left-color: var(--warning-amber) !important;
        color: #92400E;
    }
    
    .safe-risk {
        background-color: #F0FDF4 !important;
        border-left-color: var(--safe-green) !important;
        color: #14532D;
    }
    
    /* Streamlit Elements Styling */
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
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: var(--dark-gray) !important;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        background: var(--white);
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    /* Success, Warning, Error styling */
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
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'students_data' not in st.session_state:
    st.session_state.students_data = None
if 'risk_predictor' not in st.session_state:
    st.session_state.risk_predictor = RiskPredictor()

def load_and_process_data(df):
    """Load data and predict risks"""
    try:
        # Validate required columns
        required_cols = ['student_id', 'name', 'attendance_percentage', 'marks_percentage', 'fees_status']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            st.error(f"Missing required columns: {', '.join(missing_cols)}")
            return None
        
        # Clean and validate data
        df = df.copy()
        df['attendance_percentage'] = pd.to_numeric(df['attendance_percentage'], errors='coerce')
        df['marks_percentage'] = pd.to_numeric(df['marks_percentage'], errors='coerce')
        
        # Remove rows with invalid data
        df = df.dropna(subset=['attendance_percentage', 'marks_percentage'])
        
        # Ensure valid ranges
        df['attendance_percentage'] = df['attendance_percentage'].clip(0, 100)
        df['marks_percentage'] = df['marks_percentage'].clip(0, 100)
        
        # Predict risks
        predictor = st.session_state.risk_predictor
        predictor.train(df)
        risk_scores = predictor.predict_risk(df)
        
        # Add risk information
        df['risk_score'] = risk_scores
        df['risk_category'] = [predictor.get_risk_category(score)[0] for score in risk_scores]
        df['risk_emoji'] = [predictor.get_risk_category(score)[1] for score in risk_scores]
        
        # Update shared data system for student alerts
        shared_data_manager.update_risk_alerts(df)
        
        # Update student lists for counselor dashboard
        high_risk_students = df[df['risk_category'] == 'High Risk'].to_dict('records')
        medium_risk_students = df[df['risk_category'] == 'Medium Risk'].to_dict('records')
        low_risk_students = df[df['risk_category'] == 'Safe'].to_dict('records')
        
        shared_data_manager.update_student_lists(
            high_risk=high_risk_students,
            medium_risk=medium_risk_students,
            low_risk=low_risk_students
        )
        
        return df
        
    except Exception as e:
        st.error(f"Error processing data: {str(e)}")
        return None

def create_charts(df):
    """Create visualization charts"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Risk Distribution")
        
        # Risk distribution pie chart with professional colors
        risk_counts = df['risk_category'].value_counts()
        # Updated colors to match professional color scheme
        colors = {
            'High Risk': '#EF4444',    # Danger Red
            'Medium Risk': '#F59E0B',  # Warning Amber  
            'Safe': '#10B981'          # Safe Green
        }
        
        fig_pie = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            title="Student Risk Distribution",
            color=risk_counts.index,
            color_discrete_map=colors
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Risk statistics
        total_students = len(df)
        high_risk = len(df[df['risk_category'] == 'High Risk'])
        medium_risk = len(df[df['risk_category'] == 'Medium Risk'])
        safe = len(df[df['risk_category'] == 'Safe'])
        
        st.metric("Total Students", total_students)
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("🔴 High Risk", high_risk, f"{high_risk/total_students*100:.1f}%")
        with col_b:
            st.metric("🟠 Medium Risk", medium_risk, f"{medium_risk/total_students*100:.1f}%")
        with col_c:
            st.metric("🟢 Safe", safe, f"{safe/total_students*100:.1f}%")
    
    with col2:
        st.subheader("📈 Performance Analysis")
        
        # Scatter plot: Attendance vs Marks colored by risk
        fig_scatter = px.scatter(
            df, 
            x='attendance_percentage', 
            y='marks_percentage',
            color='risk_category',
            color_discrete_map=colors,
            title="Attendance vs Marks by Risk Level",
            hover_data=['name', 'fees_status'],
            labels={
                'attendance_percentage': 'Attendance %',
                'marks_percentage': 'Marks %'
            }
        )
        fig_scatter.update_layout(xaxis_range=[0, 100], yaxis_range=[0, 100])
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Bar chart: Average performance by risk category
        avg_performance = df.groupby('risk_category')[['attendance_percentage', 'marks_percentage']].mean()
        
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(name='Attendance %', x=avg_performance.index, y=avg_performance['attendance_percentage']))
        fig_bar.add_trace(go.Bar(name='Marks %', x=avg_performance.index, y=avg_performance['marks_percentage']))
        fig_bar.update_layout(barmode='group', title='Average Performance by Risk Category')
        st.plotly_chart(fig_bar, use_container_width=True)

def main():
    # Enhanced header with new professional navigation colors
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1E3A8A, #3B82F6); padding: 0.5rem; border-radius: 5px; margin-bottom: 1rem;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h3 style="color: white; margin: 0;">👨‍🏫 Teacher Dashboard</h3>
            <a href="http://localhost:8499" style="color: white; text-decoration: none; background: rgba(255,255,255,0.2); padding: 0.3rem 0.8rem; border-radius: 3px; font-weight: bold;">
                🏠 Back to Main
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Attractive main header
    st.markdown("""
    <div class="main-header">
        <h1>👨‍🏫 DropSafe Teacher Dashboard</h1>
        <h3>Identify at-risk students and take proactive measures</h3>
        <p style="font-size: 1.1rem; opacity: 0.9;">Powered by Advanced AI & Machine Learning</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if data exists, show appropriate welcome message
    if st.session_state.students_data is None:
        # Enhanced welcome section for new users
        st.markdown("""
        <div class="welcome-section">
            <h2>👋 Welcome to DropSafe!</h2>
            <p style="font-size: 1.1rem; margin-bottom: 1.5rem;">Please upload a CSV file or use sample data to get started with student risk assessment.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # CSV Format Requirements in attractive card
        st.markdown("""
        <div class="csv-format-card">
            <h3>📋 Required CSV Format:</h3>
            <p>Your CSV file should contain these columns:</p>
            <ul style="font-size: 1rem; line-height: 1.6;">
                <li><strong>student_id:</strong> Unique identifier (e.g., STU001)</li>
                <li><strong>name:</strong> Student name</li>
                <li><strong>attendance_percentage:</strong> Attendance percentage (0-100)</li>
                <li><strong>marks_percentage:</strong> Marks percentage (0-100)</li>
                <li><strong>fees_status:</strong> Either 'paid' or 'pending'</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Features section with cards
        st.markdown("### 🎆 Features:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h4>🎯 Risk Assessment</h4>
                <p>Automatic classification into High/Medium/Low risk categories using advanced ML algorithms</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <h4>📥 Export Options</h4>
                <p>Download filtered student lists and detailed reports for further analysis</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h4>📈 Visual Analytics</h4>
                <p>Interactive charts and graphs for better insights into student performance</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <h4>⏱️ Real-time Updates</h4>
                <p>Add students manually or via CSV upload with instant risk calculations</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Enhanced sidebar with better styling - SINGLE INSTANCE
    with st.sidebar:
        # Sidebar header with new professional colors
        st.markdown("""
        <div style="background: linear-gradient(45deg, #1E3A8A, #3B82F6); padding: 1rem; border-radius: 10px; margin-bottom: 1rem; color: white; text-align: center;">
            <h3 style="margin: 0;">📁 Data Management</h3>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">Upload & Manage Student Data</p>
        </div>
        """, unsafe_allow_html=True)
        
        # File uploader with enhanced styling
        st.markdown("""
        <div class="upload-section">
            <h4>📄 Upload Student Data</h4>
            <p>Choose your CSV file to get started</p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose CSV file", 
            type=['csv'],
            key="main_csv_uploader",
            help="Upload CSV with required columns: student_id, name, attendance_percentage, marks_percentage, fees_status"
        )
        
        # Sample data section with enhanced button
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: #f0f8f0; border-radius: 10px; margin: 1rem 0;">
            <h4>🎲 Try Sample Data</h4>
            <p>Generate 30 sample student records for demonstration</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎲 Load Sample Data", type="primary", use_container_width=True):
            sample_df = generate_sample_data(30)
            st.session_state.students_data = load_and_process_data(sample_df)
            st.success("✅ Sample data loaded successfully!")
            st.rerun()
        
        # Manual data entry section
        st.markdown("---")
        with st.expander("➕ Add Single Student", expanded=False):
            st.markdown("""
            <div style="background: #e8f5e8; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;">
                <strong>📝 Quick Add:</strong> Manually add a single student record
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("add_student"):
                student_id = st.text_input("🆔 Student ID", placeholder="e.g., STU001")
                name = st.text_input("👤 Name", placeholder="Enter student name")
                
                col1, col2 = st.columns(2)
                with col1:
                    attendance = st.slider("📅 Attendance %", 0, 100, 75)
                with col2:
                    marks = st.slider("📈 Marks %", 0, 100, 70)
                
                fees_status = st.selectbox("💳 Fees Status", ["paid", "pending"])
                
                if st.form_submit_button("➕ Add Student", type="primary", use_container_width=True):
                    if student_id and name:
                        new_student = pd.DataFrame([{
                            'student_id': student_id,
                            'name': name,
                            'attendance_percentage': attendance,
                            'marks_percentage': marks,
                            'fees_status': fees_status
                        }])
                        
                        if st.session_state.students_data is not None:
                            combined_df = pd.concat([st.session_state.students_data, new_student], ignore_index=True)
                        else:
                            combined_df = new_student
                            
                        st.session_state.students_data = load_and_process_data(combined_df)
                        st.success(f"✅ Added {name} successfully!")
                        st.rerun()
                    else:
                        st.error("⚠️ Please fill in Student ID and Name")
        
        # Additional sidebar information
        if st.session_state.students_data is not None:
            st.markdown("---")
            st.markdown("""
            <div style="background: linear-gradient(45deg, #4CAF50, #45a049); padding: 1rem; border-radius: 10px; color: white; text-align: center;">
                <h4 style="margin: 0;">📊 Quick Stats</h4>
                <p style="margin: 0.5rem 0 0 0;">Current Dataset Overview</p>
            </div>
            """, unsafe_allow_html=True)
            
            df = st.session_state.students_data
            total_students = len(df)
            high_risk = len(df[df['risk_category'] == 'High Risk'])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("👥 Total", total_students)
            with col2:
                st.metric("🔴 High Risk", high_risk)
    
    # Process uploaded file
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.students_data = load_and_process_data(df)
            if st.session_state.students_data is not None:
                st.success(f"✅ Loaded {len(st.session_state.students_data)} students successfully!")
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
    
    # Main content
    if st.session_state.students_data is not None:
        df = st.session_state.students_data
        
        # Success message with stats
        st.markdown("""
        <div style="background: linear-gradient(45deg, #4CAF50, #45a049); color: white; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; text-align: center;">
            <h3 style="margin: 0;">✅ Data Successfully Loaded!</h3>
            <p style="margin: 0.5rem 0 0 0;">Ready for analysis and risk assessment</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick Action Buttons for Risk Management
        st.markdown("""
        <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
            <h4>🎯 Quick Actions</h4>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📊 Generate Risk Report", use_container_width=True):
                st.success("Risk report generated!")
        with col2:
            if st.button("📧 Email High Risk List", use_container_width=True):
                st.success("High risk list prepared for email!")
        with col3:
            if st.button("📅 Schedule Interventions", use_container_width=True):
                st.success("Intervention scheduling opened!")
        with col4:
            if st.button("📊 Export All Data", use_container_width=True):
                all_data_csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Complete Dataset",
                    data=all_data_csv,
                    file_name=f"complete_student_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )
        
        # Charts section
        create_charts(df)
        
        # Enhanced student list section - MOVED BEFORE RISK SPREADSHEETS
        st.markdown("""
        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border-left: 5px solid #4CAF50;">
            <h2>👥 Student Risk Management</h2>
            <p>Filter, sort, and manage student data with advanced analytics</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced filters section
        st.markdown("""
        <div style="background: #e8f5e8; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
            <h4>🔍 Filter & Sort Options</h4>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            risk_filter = st.selectbox("🎯 Filter by Risk", ["All", "High Risk", "Medium Risk", "Safe"])
        with col2:
            fees_filter = st.selectbox("💳 Filter by Fees", ["All", "paid", "pending"])
        with col3:
            sort_by = st.selectbox("🔄 Sort by", ["name", "attendance_percentage", "marks_percentage", "risk_score"])
        with col4:
            show_count = st.selectbox("📄 Show Records", [10, 25, 50, "All"])
        
        # Apply filters
        filtered_df = df.copy()
        if risk_filter != "All":
            filtered_df = filtered_df[filtered_df['risk_category'] == risk_filter]
        if fees_filter != "All":
            filtered_df = filtered_df[filtered_df['fees_status'] == fees_filter]
        
        # Sort data
        filtered_df = filtered_df.sort_values(sort_by)
        
        # Limit display
        if show_count != "All":
            filtered_df = filtered_df.head(show_count)
        
        # Display student table with styling
        if not filtered_df.empty:
            st.markdown(f"**Showing {len(filtered_df)} students**")
            
            # Add download button for filtered data
            col1, col2, col3 = st.columns([2, 1, 1])
            with col2:
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"students_{risk_filter.lower().replace(' ', '_')}.csv",
                    mime="text/csv"
                )
            with col3:
                if st.button("📊 Refresh Data"):
                    st.rerun()
            
            # Display the data
            st.dataframe(
                filtered_df[['student_id', 'name', 'attendance_percentage', 'marks_percentage', 'fees_status', 'risk_category', 'risk_emoji']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No students match the selected filters.")
        
        # Risk-based Student Spreadsheets Section
        st.markdown("""
        <div style="background: linear-gradient(45deg, #ff4444, #cc0000); color: white; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; text-align: center;">
            <h2 style="margin: 0;">🚨 Risk-Based Student Analysis</h2>
            <p style="margin: 0.5rem 0 0 0;">Separate spreadsheets for high-risk and medium-risk students</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create risk-based dataframes
        high_risk_df = df[df['risk_category'] == 'High Risk'].copy()
        medium_risk_df = df[df['risk_category'] == 'Medium Risk'].copy()
        safe_df = df[df['risk_category'] == 'Safe'].copy()
        
        # Risk Summary Cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: #ffebee; border: 2px solid #f44336; padding: 1rem; border-radius: 10px; text-align: center;">
                <h3 style="color: #d32f2f; margin: 0;">🔴 High Risk Students</h3>
                <h2 style="color: #d32f2f; margin: 0.5rem 0;">{}</h2>
                <p style="color: #666; margin: 0;">Immediate Attention Required</p>
            </div>
            """.format(len(high_risk_df)), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: #fff3e0; border: 2px solid #ff9800; padding: 1rem; border-radius: 10px; text-align: center;">
                <h3 style="color: #f57c00; margin: 0;">🟠 Medium Risk Students</h3>
                <h2 style="color: #f57c00; margin: 0.5rem 0;">{}</h2>
                <p style="color: #666; margin: 0;">Monitor Closely</p>
            </div>
            """.format(len(medium_risk_df)), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: #e8f5e8; border: 2px solid #4CAF50; padding: 1rem; border-radius: 10px; text-align: center;">
                <h3 style="color: #388e3c; margin: 0;">🟢 Safe Students</h3>
                <h2 style="color: #388e3c; margin: 0.5rem 0;">{}</h2>
                <p style="color: #666; margin: 0;">Performing Well</p>
            </div>
            """.format(len(safe_df)), unsafe_allow_html=True)
        
        # High Risk Students Spreadsheet
        if not high_risk_df.empty:
            st.markdown("""
            <div style="background: #ffebee; padding: 1.5rem; border-radius: 10px; margin: 1.5rem 0; border-left: 5px solid #f44336;">
                <h3 style="color: #d32f2f; margin: 0 0 1rem 0;">🚨 High Risk Students - Detailed Spreadsheet</h3>
                <p style="color: #666;">Students requiring immediate intervention and support</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Download button for high risk students
            col1, col2, col3 = st.columns([2, 1, 1])
            with col2:
                high_risk_csv = high_risk_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download High Risk CSV",
                    data=high_risk_csv,
                    file_name=f"high_risk_students_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    type="secondary"
                )
            with col3:
                if st.button("📊 Analyze High Risk", key="analyze_high"):
                    st.success("High risk analysis initiated!")
            
            # Display high risk students table
            st.dataframe(
                high_risk_df[['student_id', 'name', 'attendance_percentage', 'marks_percentage', 'fees_status', 'risk_score', 'risk_emoji']],
                use_container_width=True,
                hide_index=True
            )
            
            # High risk insights
            st.markdown("""
            <div style="background: #fff; border: 1px solid #f44336; padding: 1rem; border-radius: 5px; margin: 1rem 0;">
                <h4 style="color: #d32f2f;">📊 High Risk Insights:</h4>
                <ul>
                    <li><strong>Average Attendance:</strong> {:.1f}%</li>
                    <li><strong>Average Marks:</strong> {:.1f}%</li>
                    <li><strong>Pending Fees:</strong> {} students</li>
                    <li><strong>Recommended Action:</strong> Immediate counseling and intervention required</li>
                </ul>
            </div>
            """.format(
                high_risk_df['attendance_percentage'].mean(),
                high_risk_df['marks_percentage'].mean(),
                len(high_risk_df[high_risk_df['fees_status'] == 'pending'])
            ), unsafe_allow_html=True)
        else:
            st.success("🎉 Excellent! No high-risk students found.")
        
        # Medium Risk Students Spreadsheet
        if not medium_risk_df.empty:
            st.markdown("""
            <div style="background: #fff3e0; padding: 1.5rem; border-radius: 10px; margin: 1.5rem 0; border-left: 5px solid #ff9800;">
                <h3 style="color: #f57c00; margin: 0 0 1rem 0;">⚠️ Medium Risk Students - Detailed Spreadsheet</h3>
                <p style="color: #666;">Students who need monitoring and preventive measures</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Download button for medium risk students
            col1, col2, col3 = st.columns([2, 1, 1])
            with col2:
                medium_risk_csv = medium_risk_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Medium Risk CSV",
                    data=medium_risk_csv,
                    file_name=f"medium_risk_students_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    type="secondary"
                )
            with col3:
                if st.button("📊 Analyze Medium Risk", key="analyze_medium"):
                    st.success("Medium risk analysis initiated!")
            
            # Display medium risk students table
            st.dataframe(
                medium_risk_df[['student_id', 'name', 'attendance_percentage', 'marks_percentage', 'fees_status', 'risk_score', 'risk_emoji']],
                use_container_width=True,
                hide_index=True
            )
            
            # Medium risk insights
            st.markdown("""
            <div style="background: #fff; border: 1px solid #ff9800; padding: 1rem; border-radius: 5px; margin: 1rem 0;">
                <h4 style="color: #f57c00;">📊 Medium Risk Insights:</h4>
                <ul>
                    <li><strong>Average Attendance:</strong> {:.1f}%</li>
                    <li><strong>Average Marks:</strong> {:.1f}%</li>
                    <li><strong>Pending Fees:</strong> {} students</li>
                    <li><strong>Recommended Action:</strong> Regular monitoring and support sessions</li>
                </ul>
            </div>
            """.format(
                medium_risk_df['attendance_percentage'].mean(),
                medium_risk_df['marks_percentage'].mean(),
                len(medium_risk_df[medium_risk_df['fees_status'] == 'pending'])
            ), unsafe_allow_html=True)
        else:
            st.info("📊 No medium-risk students found. Great progress!")


if __name__ == "__main__":
    main()