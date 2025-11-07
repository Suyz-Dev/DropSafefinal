"""
DropSafe - Streamlit Cloud Version
Simplified main page for Streamlit Cloud deployment
"""

import streamlit as st

# Configure page
st.set_page_config(
    page_title="DropSafe - Student Risk Assessment Platform",
    page_icon="🛡️",
    layout="wide"
)

# Simple styling for Streamlit Cloud
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    }
    
    .dashboard-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #3B82F6;
        transition: transform 0.2s ease;
    }
    
    .dashboard-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.15);
    }
    
    .feature-item {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🛡️ DropSafe</h1>
    <h3>Advanced Student Risk Assessment Platform</h3>
    <p>Empowering educators with AI-driven insights to identify at-risk students early</p>
</div>
""", unsafe_allow_html=True)

# Introduction
st.markdown("## 🎓 Welcome to DropSafe")
st.markdown("""
DropSafe is a comprehensive machine learning-powered platform designed to help educational 
institutions identify at-risk students early and provide targeted interventions.
""")

# Features
st.markdown("## ✨ Key Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-item">
        <h4>🤖 AI-Powered Risk Assessment</h4>
        <p>Advanced ML algorithms analyze multiple factors to predict student dropout risk</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-item">
        <h4>📊 Real-time Analytics</h4>
        <p>Interactive dashboards provide instant insights into student performance</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-item">
        <h4>🎯 Personalized Interventions</h4>
        <p>Tailored recommendations based on individual student risk profiles</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-item">
        <h4>🔒 Secure & Private</h4>
        <p>Role-based access control ensures student data privacy</p>
    </div>
    """, unsafe_allow_html=True)

# Dashboard Access
st.markdown("## 🚀 Access Dashboards")

st.info("ℹ️ **Note for Streamlit Cloud Deployment**")
st.markdown("""
This simplified version is designed for Streamlit Cloud deployment. 
For the full multi-dashboard experience with separate services, 
please deploy locally or use Docker.
""")

st.markdown("### Available Components:")

# Teacher Dashboard Simulation
with st.expander("👨‍🏫 Teacher Dashboard (Simulation)"):
    st.markdown("**Key Features:**")
    st.markdown("- Upload student data (CSV)")
    st.markdown("- View risk analytics and visualizations")
    st.markdown("- Download risk-based student lists")
    st.markdown("- Monitor class performance")
    
    st.markdown("#### Sample Risk Distribution")
    # Sample data for demonstration
    import pandas as pd
    import plotly.express as px
    
    sample_data = pd.DataFrame({
        'Risk_Level': ['High Risk', 'Medium Risk', 'Safe'],
        'Count': [15, 30, 55]
    })
    
    fig = px.pie(sample_data, values='Count', names='Risk_Level', 
                 color='Risk_Level',
                 color_discrete_map={'High Risk': '#EF4444', 
                                   'Medium Risk': '#F59E0B', 
                                   'Safe': '#10B981'})
    st.plotly_chart(fig, use_container_width=True)

# Student Dashboard Simulation
with st.expander("🎓 Student Portal (Simulation)"):
    st.markdown("**Key Features:**")
    st.markdown("- Personalized risk assessment")
    st.markdown("- Performance tracking")
    st.markdown("- AI chat counselor")
    st.markdown("- Quick action recommendations")
    
    st.markdown("#### Sample Student Profile")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Attendance", "85%")
    with col2:
        st.metric("Marks", "78%")
    with col3:
        st.metric("Risk Level", "Safe 🟢")

# Counsellor Dashboard Simulation
with st.expander("🧠 Counsellor Dashboard (Simulation)"):
    st.markdown("**Key Features:**")
    st.markdown("- Student mental health monitoring")
    st.markdown("- Intervention tracking")
    st.markdown("- Priority student lists")
    st.markdown("- Wellness analytics")
    
    st.markdown("#### Sample Intervention Tracking")
    intervention_data = pd.DataFrame({
        'Type': ['Academic Support', 'Mental Health', 'Family Outreach', 'Peer Mentoring'],
        'Students': [25, 18, 12, 30]
    })
    
    fig2 = px.bar(intervention_data, x='Type', y='Students',
                  color='Type',
                  color_discrete_sequence=['#1E3A8A', '#3B82F6', '#8B5CF6', '#10B981'])
    st.plotly_chart(fig2, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "<h4>🛡️ DropSafe - Advanced Student Risk Assessment Platform</h4>"
    "<p>Empowering educators with AI-driven insights for student success</p>"
    "<p>For full deployment options, see our <a href='https://github.com/Suyz-Dev/DropSafe-' target='_blank'>GitHub repository</a></p>"
    "</div>",
    unsafe_allow_html=True
)