import streamlit as st
import time
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="DropSafe - Student Risk Assessment Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add meta tag to set as homepage
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="cache-control" content="no-cache">
<meta http-equiv="expires" content="0">
<meta http-equiv="pragma" content="no-cache">
<meta name="cache-control" content="no-cache, no-store, must-revalidate">
""", unsafe_allow_html=True)

# Health check endpoint
if st.query_params.get("healthz"):
    st.json({"status": "healthy", "timestamp": datetime.now().isoformat()})
    st.stop()

# Force refresh if needed
if 'page_refresh' not in st.session_state:
    st.session_state.page_refresh = True
    st.rerun()

# Custom CSS for new professional color scheme
st.markdown("""
<style>
    /* Color Variables */
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
    
    .hero-section {
        background: linear-gradient(135deg, var(--deep-blue) 0%, var(--sky-blue) 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 3rem;
        color: var(--white);
        box-shadow: 0 8px 25px rgba(30, 58, 138, 0.3);
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        color: var(--white);
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        margin-bottom: 2rem;
        opacity: 0.95;
        color: var(--white);
    }
    
    .hero-description {
        font-size: 1.1rem;
        max-width: 800px;
        margin: 0 auto 2rem;
        line-height: 1.6;
        opacity: 0.9;
        color: var(--white);
    }
    
    .dashboard-card {
        background: var(--white);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 2px solid #E5E7EB;
        margin-bottom: 1.5rem;
    }
    
    .dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.15);
        border-color: var(--sky-blue);
    }
    
    .card-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .card-title {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: var(--dark-gray);
    }
    
    .card-description {
        color: var(--medium-gray);
        margin-bottom: 1.5rem;
        line-height: 1.5;
    }
    
    .features-section {
        margin: 3rem 0;
        text-align: center;
    }
    
    .feature-item {
        background: var(--white);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid #E5E7EB;
    }
    
    .stats-container {
        background: linear-gradient(45deg, var(--deep-blue), var(--sky-blue));
        color: var(--white);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(30, 58, 138, 0.2);
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: var(--white);
    }
    
    .stat-label {
        font-size: 1rem;
        opacity: 0.9;
        color: var(--white);
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
    
    /* Section Headers */
    h1, h2, h3 {
        color: var(--dark-gray) !important;
    }
    
    /* Success/Info Messages */
    .stSuccess {
        background-color: #ECFDF5 !important;
        border: 1px solid var(--safe-green) !important;
        color: #065F46 !important;
    }
</style>
""", unsafe_allow_html=True)

def hero_section():
    """Create the hero section"""
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">🛡️ DropSafe</div>
        <div class="hero-subtitle">Advanced Student Risk Assessment Platform</div>
        <div class="hero-description">
            Empowering educators with AI-driven insights to identify at-risk students early, 
            provide targeted interventions, and ensure every student has the support they need to succeed.
        </div>
    </div>
    """, unsafe_allow_html=True)

def dashboard_cards():
    """Create dashboard selection cards"""
    st.markdown("## 🚀 Choose Your Dashboard")
    st.markdown("Select the appropriate dashboard based on your role:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="dashboard-card">
            <div class="card-icon">🎓</div>
            <div class="card-title">Student Dashboard</div>
            <div class="card-description">
                Access your personal academic profile, view risk assessments, 
                get personalized recommendations, and connect with support resources.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎓 Open Student Dashboard", key="student", use_container_width=True, type="primary"):
            st.success("🎓 Opening Student Dashboard...")
            st.markdown("""<meta http-equiv="refresh" content="0; url=http://localhost:8502" />""", unsafe_allow_html=True)
            st.markdown("""<script>window.location.href = 'http://localhost:8502';</script>""", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="dashboard-card">
            <div class="card-icon">👨‍🏫</div>
            <div class="card-title">Teacher Dashboard</div>
            <div class="card-description">
                Upload student data, monitor class performance, view risk analytics, 
                generate reports, and manage student interventions.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("👨‍🏫 Open Teacher Dashboard", key="teacher", use_container_width=True, type="primary"):
            st.success("👨‍🏫 Opening Teacher Dashboard...")
            st.markdown("""<meta http-equiv="refresh" content="0; url=http://localhost:8501" />""", unsafe_allow_html=True)
            st.markdown("""<script>window.location.href = 'http://localhost:8501';</script>""", unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="dashboard-card">
            <div class="card-icon">🧠</div>
            <div class="card-title">Counsellor Dashboard</div>
            <div class="card-description">
                Access comprehensive student profiles, intervention tracking, 
                mental health assessments, and coordination tools for student support.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🧠 Open Counsellor Dashboard", key="counsellor", use_container_width=True, type="primary"):
            st.success("🧠 Opening Counsellor Dashboard...")
            st.markdown("""<meta http-equiv="refresh" content="0; url=http://localhost:8504" />""", unsafe_allow_html=True)
            st.markdown("""<script>window.location.href = 'http://localhost:8504';</script>""", unsafe_allow_html=True)

def features_section():
    """Display key features"""
    st.markdown("## ✨ Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-item">
            <h4>🤖 AI-Powered Risk Assessment</h4>
            <p>Advanced machine learning algorithms analyze multiple factors to predict student dropout risk with high accuracy.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-item">
            <h4>📊 Real-time Analytics</h4>
            <p>Interactive dashboards provide instant insights into student performance and risk indicators.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-item">
            <h4>🎯 Personalized Interventions</h4>
            <p>Tailored recommendations and support strategies based on individual student risk profiles.</p>
        </div>
        """, unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown("""
        <div class="feature-item">
            <h4>🔒 Secure & Private</h4>
            <p>Role-based access control ensures student data privacy and security compliance.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div class="feature-item">
            <h4>📈 Progress Tracking</h4>
            <p>Monitor intervention effectiveness and student progress over time with detailed analytics.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown("""
        <div class="feature-item">
            <h4>🤝 Collaborative Care</h4>
            <p>Seamless coordination between teachers, counsellors, and support staff for holistic student care.</p>
        </div>
        """, unsafe_allow_html=True)

def statistics_section():
    """Display platform statistics"""
    st.markdown("""
    <div class="stats-container">
        <h3 style="text-align: center; margin-bottom: 2rem;">📊 Platform Impact</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stats-container">
            <div class="stat-item">
                <div class="stat-number">95%</div>
                <div class="stat-label">Prediction Accuracy</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stats-container">
            <div class="stat-item">
                <div class="stat-number">85%</div>
                <div class="stat-label">Early Intervention Success</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stats-container">
            <div class="stat-item">
                <div class="stat-number">1000+</div>
                <div class="stat-label">Students Supported</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stats-container">
            <div class="stat-item">
                <div class="stat-number">50+</div>
                <div class="stat-label">Schools Using Platform</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def quick_access_section():
    """Quick access and login section"""
    st.markdown("## 🔐 Quick Access")
    st.markdown("Need to authenticate first? Use our unified login portal:")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔐 Go to Login Portal", use_container_width=True, type="secondary"):
            st.success("🔐 Opening Login Portal...")
            st.markdown("""<meta http-equiv="refresh" content="0; url=http://localhost:8500" />""", unsafe_allow_html=True)
            st.markdown("""<script>window.location.href = 'http://localhost:8500';</script>""", unsafe_allow_html=True)

def footer_section():
    """Footer with additional information"""
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🏫 For Educational Institutions**
        - Comprehensive student monitoring
        - Data-driven decision making
        - Improved retention rates
        """)
    
    with col2:
        st.markdown("""
        **👨‍💼 For Administrators**
        - Institution-wide analytics
        - Performance benchmarking
        - Resource optimization
        """)
    
    with col3:
        st.markdown("""
        **🔧 Technical Support**
        - 24/7 system monitoring
        - Regular updates & maintenance
        - Dedicated support team
        """)
    
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; padding: 2rem;'>"
        "<h4>🛡️ DropSafe - Advanced Student Risk Assessment Platform</h4>"
        "<p>Empowering educators with AI-driven insights for student success</p>"
        "<p>© 2024 DropSafe Platform. All rights reserved.</p>"
        "</div>",
        unsafe_allow_html=True
    )

def main():
    """Main application function"""
    # Hero Section
    hero_section()
    
    # Dashboard Selection Cards
    dashboard_cards()
    
    # Features Section
    features_section()
    
    # Statistics Section
    statistics_section()
    
    # Quick Access Section
    quick_access_section()
    
    # Footer Section
    footer_section()

if __name__ == "__main__":
    main()