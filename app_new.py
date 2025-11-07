# Enhanced Multi-Role DROPSAFE Dashboard
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
import joblib
import numpy as np
from datetime import datetime
import json
import os
import hashlib

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="DROPSAFE - Multi-Role Analytics",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'selected_role' not in st.session_state:
    st.session_state.selected_role = None
if 'student_data' not in st.session_state:
    st.session_state.student_data = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_credentials' not in st.session_state:
    st.session_state.user_credentials = {}
if 'is_first_time_user' not in st.session_state:
    st.session_state.is_first_time_user = True
if 'student_alerts' not in st.session_state:
    st.session_state.student_alerts = {}
if 'alert_notifications' not in st.session_state:
    st.session_state.alert_notifications = []

# --- ENHANCED CSS ---
st.markdown("""
<style>
    /* Hero/Welcome Section */
    .hero-welcome-section {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0D9488 100%);
        border-radius: 24px;
        padding: 4rem 2rem;
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
        color: white;
        text-align: center;
    }
    .hero-content {
        position: relative;
        z-index: 2;
        max-width: 800px;
        margin: 0 auto;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .hero-headline {
        font-size: 3.2rem;
        font-weight: 800;
        margin-bottom: 1rem;
        line-height: 1.1;
        background: linear-gradient(135deg, #ffffff 0%, #0D9488 50%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero-subheading {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        color: #E2E8F0;
        opacity: 0.9;
    }
    .hero-description {
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 3rem;
        color: #CBD5E1;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
        text-align: center;
    }
    .hero-actions {
        display: flex;
        gap: 1rem;
        justify-content: center;
        flex-wrap: wrap;
    }
    .cta-primary {
        background: linear-gradient(135deg, #F0FDFA 0%, #CCFBF1 50%, #0D9488 100%);
        color: #0F172A;
        border: 1px solid #0D9488;
        padding: 1rem 2rem;
        border-radius: 12px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(13, 148, 136, 0.2);
    }
    .cta-primary:hover {
        background: linear-gradient(135deg, #CCFBF1 0%, #99F6E4 50%, #0F766E 100%);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(13, 148, 136, 0.3);
    }
    .cta-secondary {
        background: linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 50%, rgba(255, 255, 255, 0.9) 100%);
        color: #0F172A;
        border: 2px solid #94A3B8;
        padding: 1rem 2rem;
        border-radius: 12px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 16px rgba(148, 163, 184, 0.2);
    }
    .cta-secondary:hover {
        background: linear-gradient(135deg, #E2E8F0 0%, #CBD5E1 50%, #94A3B8 100%);
        color: white;
        border-color: #64748B;
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(148, 163, 184, 0.3);
    }
    .hero-background {
        position: absolute;
        top: 0;
        right: 0;
        width: 100%;
        height: 100%;
        z-index: 1;
        overflow: hidden;
    }
    .education-icons {
        position: absolute;
        top: 20%;
        right: 10%;
        display: flex;
        flex-direction: column;
        gap: 2rem;
        opacity: 0.2;
    }
    .edu-icon {
        font-size: 3rem;
        animation: float 4s ease-in-out infinite;
        filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
    }
    .edu-icon:nth-child(2) { animation-delay: 0.5s; }
    .edu-icon:nth-child(3) { animation-delay: 1s; }
    .edu-icon:nth-child(4) { animation-delay: 1.5s; }
    .edu-icon:nth-child(5) { animation-delay: 2s; }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-headline {
            font-size: 2.5rem;
        }
        .hero-subheading {
            font-size: 1.2rem;
        }
        .hero-actions {
            flex-direction: column;
            align-items: center;
        }
        .cta-primary, .cta-secondary {
            width: 100%;
            max-width: 280px;
        }
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-headline {
            font-size: 2.5rem;
        }
        .hero-subheading {
            font-size: 1.2rem;
        }
        .hero-actions {
            flex-direction: column;
            align-items: center;
        }
        .cta-primary, .cta-secondary {
            width: 100%;
            max-width: 280px;
        }
    }
    .hero-section {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0D9488 100%);
        padding: 3rem 2rem;
        border-radius: 24px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 
            0 8px 32px rgba(15, 23, 42, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1),
            inset 0 -1px 0 rgba(255, 255, 255, 0.05);
    }
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><defs><filter id="glow"><feGaussianBlur stdDeviation="3" result="coloredBlur"/><feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><g filter="url(%23glow)" opacity="0.3"><circle cx="80" cy="60" r="3" fill="%230D9488"/><circle cx="150" cy="90" r="2" fill="%2306B6D4"/><circle cx="220" cy="70" r="3" fill="%230D9488"/><circle cx="320" cy="120" r="2" fill="%2306B6D4"/><circle cx="120" cy="150" r="2" fill="%230D9488"/><circle cx="280" cy="180" r="3" fill="%2306B6D4"/><line x1="80" y1="60" x2="150" y2="90" stroke="%230D9488" stroke-width="1" opacity="0.5"/><line x1="150" y1="90" x2="220" y2="70" stroke="%2306B6D4" stroke-width="1" opacity="0.4"/><line x1="220" y1="70" x2="320" y2="120" stroke="%230D9488" stroke-width="1" opacity="0.3"/><line x1="150" y1="90" x2="120" y2="150" stroke="%2306B6D4" stroke-width="1" opacity="0.4"/><line x1="320" y1="120" x2="280" y2="180" stroke="%230D9488" stroke-width="1" opacity="0.5"/></g></svg>') no-repeat right center;
        background-size: 400px 300px;
        opacity: 0.6;
        z-index: 1;
    }
    .hero-nav {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 2rem;
        flex-wrap: wrap;
    }
    .nav-button {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        padding: 1rem 2rem;
        border: 1px solid rgba(13, 148, 136, 0.3);
        border-radius: 16px;
        text-decoration: none;
        font-weight: 600;
        font-size: 1.1em;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        backdrop-filter: blur(16px);
        position: relative;
        overflow: hidden;
        box-shadow: 
            0 4px 16px rgba(15, 23, 42, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1),
            inset 0 -1px 0 rgba(0, 0, 0, 0.1);
    }
    .nav-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(13, 148, 136, 0.3), transparent);
        transition: left 0.6s;
    }
    .nav-button:hover {
        background: rgba(13, 148, 136, 0.2);
        border-color: rgba(13, 148, 136, 0.6);
        transform: translateY(-2px);
        box-shadow: 
            0 8px 32px rgba(13, 148, 136, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2),
            inset 0 -1px 0 rgba(0, 0, 0, 0.1);
    }
    .nav-button:hover::before {
        left: 100%;
    }
    .nav-button.active {
        background: rgba(255, 255, 255, 0.9);
        color: #667eea;
        border-color: white;
    }
    .hero-title {
        font-size: 3.8em;
        font-weight: 800;
        margin-bottom: 1rem;
        position: relative;
        z-index: 2;
        background: linear-gradient(135deg, #ffffff 0%, #0D9488 50%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: none;
        filter: drop-shadow(0 4px 8px rgba(13, 148, 136, 0.3));
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.2em;
    }
    .hero-title::before {
        content: '🛡️';
        font-size: 0.8em;
        filter: drop-shadow(0 0 10px rgba(13, 148, 136, 0.8));
        animation: pulse 2s ease-in-out infinite alternate;
    }
    .hero-subtitle {
        font-size: 1.3em;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }
    .hero-description {
        font-size: 1.1em;
        opacity: 0.8;
        max-width: 600px;
        margin: 0 auto;
    }
    .main-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0D9488 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 
            0 12px 40px rgba(15, 23, 42, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.1),
            inset 0 -1px 0 rgba(255, 255, 255, 0.05);
    }
    .role-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        margin: 1rem;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    .role-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border: 2px solid #667eea;
    }
    .dashboard-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.8rem;
        border-radius: 16px;
        backdrop-filter: blur(16px);
        border: 1px solid rgba(13, 148, 136, 0.2);
        border-left: 4px solid #0D9488;
        margin: 1rem 0;
        box-shadow: 
            0 8px 32px rgba(15, 23, 42, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.8);
        transition: all 0.3s ease;
    }
    .dashboard-card:hover {
        transform: translateY(-2px);
        box-shadow: 
            0 12px 40px rgba(15, 23, 42, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.9);
        border-color: rgba(13, 148, 136, 0.4);
    }
    .risk-very-high { background: linear-gradient(135deg, #ff6b6b, #ee5a52); color: white; padding: 0.8rem 1.5rem; border-radius: 25px; font-weight: bold; display: inline-block; margin: 0.3rem; }
    .risk-high { background: linear-gradient(135deg, #ff9f43, #ff8c00); color: white; padding: 0.8rem 1.5rem; border-radius: 25px; font-weight: bold; display: inline-block; margin: 0.3rem; }
    .risk-medium { background: linear-gradient(135deg, #ffa726, #ff9800); color: white; padding: 0.8rem 1.5rem; border-radius: 25px; font-weight: bold; display: inline-block; margin: 0.3rem; }
    .risk-low { background: linear-gradient(135deg, #66bb6a, #4caf50); color: white; padding: 0.8rem 1.5rem; border-radius: 25px; font-weight: bold; display: inline-block; margin: 0.3rem; }
    .student-profile {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    .alert-success { background: linear-gradient(135deg, #d4edda, #c3e6cb); color: #155724; padding: 1.2rem; border-radius: 10px; border-left: 5px solid #28a745; margin: 1rem 0; }
    .alert-warning { background: linear-gradient(135deg, #fff3cd, #ffeaa7); color: #856404; padding: 1.2rem; border-radius: 10px; border-left: 5px solid #ffc107; margin: 1rem 0; }
    .alert-danger { background: linear-gradient(135deg, #f8d7da, #f5c6cb); color: #721c24; padding: 1.2rem; border-radius: 10px; border-left: 5px solid #dc3545; margin: 1rem 0; }
    .feature-card {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 60%, #0D9488 100%);
        color: white;
        padding: 2.2rem;
        border-radius: 18px;
        margin: 1rem 0;
        text-align: center;
        position: relative;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 
            0 12px 32px rgba(15, 23, 42, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.4s ease;
    }
    .feature-card:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 
            0 16px 48px rgba(13, 148, 136, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    .glassmorphism {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    }
    .neumorphism {
        background: #f0f0f3;
        border-radius: 20px;
        box-shadow: 
            20px 20px 60px #bebebe,
            -20px -20px 60px #ffffff,
            inset 5px 5px 10px #bebebe,
            inset -5px -5px 10px #ffffff;
    }
    .network-bg {
        position: relative;
        overflow: hidden;
    }
    .network-bg::after {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, rgba(13, 148, 136, 0.1) 2px, transparent 2px);
        background-size: 20px 20px;
        opacity: 0.4;
        animation: float 3s ease-in-out infinite;
    }
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    .stat-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        backdrop-filter: blur(16px);
        border: 1px solid rgba(13, 148, 136, 0.2);
        box-shadow: 
            0 8px 32px rgba(15, 23, 42, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.8);
        transition: all 0.3s ease;
    }
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 
            0 12px 40px rgba(13, 148, 136, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.9);
    }
    .footer-section {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
        text-align: center;
    }
    
    /* Clean Navigation Button Styling */
    .stButton button {
        background: rgba(13, 148, 136, 0.1);
        color: #0F172A;
        border: 1px solid rgba(13, 148, 136, 0.3);
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.9rem;
        padding: 0.6rem 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 8px rgba(13, 148, 136, 0.15);
        height: 40px;
        width: 100%;
        cursor: pointer;
    }
    .stButton button:hover {
        background: rgba(13, 148, 136, 0.2);
        color: #0D9488;
        border-color: rgba(13, 148, 136, 0.5);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(13, 148, 136, 0.25);
    }
    .stButton button:active {
        background: rgba(13, 148, 136, 0.25);
        transform: translateY(0);
        box-shadow: 0 2px 6px rgba(13, 148, 136, 0.2);
    }
    .stButton button:focus {
        outline: none;
        box-shadow: 0 0 0 2px rgba(13, 148, 136, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# --- HERO SECTION & NAVIGATION ---
def show_hero_section():
    """Display header with logo and navigation buttons in single line"""
    # Create header with flexbox layout similar to React component
    st.markdown("""
    <div style="
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: white;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        padding: 0.75rem 1.5rem;
        border-radius: 0.75rem;
        margin-bottom: 2rem;
    ">
        <!-- Left Section: Logo + Text -->
        <div style="
            display: flex;
            align-items: center;
            gap: 0.75rem;
        ">
            <span style="font-size: 1.875rem;">🛡️</span>
            <div>
                <h1 style="
                    font-weight: bold;
                    font-size: 1.25rem;
                    color: #1f2937;
                    margin: 0;
                    line-height: 1.2;
                ">DROPSAFE</h1>
            </div>
        </div>

    </div>
    """, unsafe_allow_html=True)
    
    # Hero/Welcome Section
    st.markdown("""
    <div class="hero-welcome-section">
        <div class="hero-content">
            <h1 class="hero-headline">Welcome to DROPSAFE</h1>
            <h2 class="hero-subheading">Manage Attendance, Scores, and Fees easily</h2>
            <p class="hero-description">
                Streamline your educational administration with our comprehensive platform. 
                Track student performance, monitor attendance, and manage financial records 
                all in one intelligent system powered by AI insights.
            </p>
            <div class="hero-actions">
                <div style="margin-top: 2rem; text-align: center;">
                    <!-- Get Started button will be positioned here -->
                </div>
            </div>
        </div>
        <div class="hero-background">
            <div class="education-icons">
                <span class="edu-icon">🎓</span>
                <span class="edu-icon">📚</span>
                <span class="edu-icon">🏫</span>
                <span class="edu-icon">✏️</span>
                <span class="edu-icon">📊</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Get Started Login Button - simplified for reliable navigation
    st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        login_clicked = st.button(
            "🚀 Get Started - Login Here", 
            key="hero_login_btn", 
            help="Click to access login page", 
            type="primary",
            use_container_width=True
        )
        
        if login_clicked:
            # Always go to login page first
            st.session_state.current_page = 'login'
            st.rerun()
    
    # About Section
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # About Section Header
    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.95);
        border-radius: 24px;
        padding: 3rem 2rem;
        margin: 2rem 0;
        backdrop-filter: blur(16px);
        border: 1px solid rgba(13, 148, 136, 0.1);
        box-shadow: 0 8px 32px rgba(15, 23, 42, 0.1);
        text-align: center;
    ">
        <h2 style="
            font-size: 2.5rem;
            font-weight: 800;
            color: #0F172A;
            margin-bottom: 1.5rem;
            background: linear-gradient(135deg, #0F172A 0%, #0D9488 50%, #06B6D4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        ">📊 About DROPSAFE</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Description using Streamlit markdown
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <p style="font-size: 1.2rem; color: #475569; max-width: 800px; margin: 0 auto; line-height: 1.8;">
            DROPSAFE is an AI-powered early intervention system designed to help educational institutions identify students at risk of dropping out. Our comprehensive platform combines advanced machine learning algorithms with intuitive dashboards to provide actionable insights for students, teachers, and counselors.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Section using Streamlit columns
    st.markdown("### 🎯 Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="
            background: white;
            padding: 2rem 1.5rem;
            border-radius: 16px;
            text-align: center;
            border: 1px solid rgba(13, 148, 136, 0.1);
            box-shadow: 0 4px 16px rgba(15, 23, 42, 0.05);
            margin-bottom: 1rem;
        ">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
            <h3 style="font-size: 1.3rem; font-weight: 700; color: #0F172A; margin: 1rem 0 0.5rem 0;">Smart Risk Assessment</h3>
            <p style="font-size: 1rem; line-height: 1.6; color: #64748B; margin: 0;">AI-powered analysis of attendance, grades, and fee status to identify at-risk students early.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="
            background: white;
            padding: 2rem 1.5rem;
            border-radius: 16px;
            text-align: center;
            border: 1px solid rgba(13, 148, 136, 0.1);
            box-shadow: 0 4px 16px rgba(15, 23, 42, 0.05);
            margin-bottom: 1rem;
        ">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📈</div>
            <h3 style="font-size: 1.3rem; font-weight: 700; color: #0F172A; margin: 1rem 0 0.5rem 0;">Real-time Analytics</h3>
            <p style="font-size: 1rem; line-height: 1.6; color: #64748B; margin: 0;">Live monitoring and visualization of student performance metrics and trends.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background: white;
            padding: 2rem 1.5rem;
            border-radius: 16px;
            text-align: center;
            border: 1px solid rgba(13, 148, 136, 0.1);
            box-shadow: 0 4px 16px rgba(15, 23, 42, 0.05);
            margin-bottom: 1rem;
        ">
            <div style="font-size: 3rem; margin-bottom: 1rem;">👥</div>
            <h3 style="font-size: 1.3rem; font-weight: 700; color: #0F172A; margin: 1rem 0 0.5rem 0;">Multi-Role Dashboards</h3>
            <p style="font-size: 1rem; line-height: 1.6; color: #64748B; margin: 0;">Customized interfaces for students, teachers, and counselors with role-specific analytics.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="
            background: white;
            padding: 2rem 1.5rem;
            border-radius: 16px;
            text-align: center;
            border: 1px solid rgba(13, 148, 136, 0.1);
            box-shadow: 0 4px 16px rgba(15, 23, 42, 0.05);
            margin-bottom: 1rem;
        ">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🔔</div>
            <h3 style="font-size: 1.3rem; font-weight: 700; color: #0F172A; margin: 1rem 0 0.5rem 0;">Early Intervention</h3>
            <p style="font-size: 1rem; line-height: 1.6; color: #64748B; margin: 0;">Automated alerts and personalized recommendations for timely support.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Impact Statistics Section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0D9488 100%);
        border-radius: 20px;
        color: white;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
    ">
        <h3 style="font-size: 2rem; font-weight: 700; color: white; margin-bottom: 2rem;">Our Impact</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Statistics using Streamlit metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Early Identification", value="85%", delta="Improvement")
    
    with col2:
        st.metric(label="Dropout Reduction", value="70%", delta="Success Rate")
    
    with col3:
        st.metric(label="User Satisfaction", value="95%", delta="Positive Feedback")
    
    with col4:
        st.metric(label="Institutions", value="50+", delta="Currently Served")

def show_about_page():
    """Display the About Us page"""
    show_hero_section()
    
    st.markdown("""
    <div class="main-header">
        <h1>ℹ️ About DROPSAFE</h1>
        <p>Transforming Education Through Intelligent Analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🎯 Our Mission
        DROPSAFE is an innovative AI-powered platform designed to help educational institutions 
        identify students at risk of dropping out and implement timely interventions to ensure 
        their academic success.
        
        ### 🌟 Key Features
        - **Multi-Role Dashboard**: Tailored experiences for Students, Teachers, and Counselors
        - **AI-Powered Risk Assessment**: Advanced machine learning algorithms for accurate predictions
        - **Real-time Analytics**: Live monitoring of student performance metrics
        - **Intervention Recommendations**: Personalized action plans for at-risk students
        - **Comprehensive Reporting**: Detailed insights for institutional improvement
        
        ### 🏆 Our Impact
        - **85%** improvement in early identification of at-risk students
        - **70%** reduction in dropout rates in pilot institutions
        - **95%** user satisfaction across all stakeholder groups
        - **50+** educational institutions currently using our platform
        """)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🎓 For Students</h3>
            <p>Personal analytics and improvement recommendations</p>
        </div>
        
        <div class="feature-card">
            <h3>👩‍🏫 For Teachers</h3>
            <p>Classroom insights and intervention tools</p>
        </div>
        
        <div class="feature-card">
            <h3>🧠 For Counselors</h3>
            <p>Advanced analytics and case management</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    ### 🤝 Our Team
    DROPSAFE is developed by a passionate team of educators, data scientists, and software engineers 
    committed to leveraging technology for educational excellence.
    
    ### 📞 Contact Us
    For more information about DROPSAFE or to schedule a demo, please contact us at:
    - 📧 Email: info@dropsafe.edu
    - 📱 Phone: +1 (555) 123-4567
    - 🌐 Website: www.dropsafe.edu
    """)

def show_registration_page():
    """Display the Registration page for first-time users"""
    # Add back button to return to home page
    if st.button("← Back to Home", key="reg_back_to_home_btn", help="Return to home page"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    st.markdown("""
    <div class="main-header">
        <h1>📝 Register - First Time User</h1>
        <p>Create Your DROPSAFE Account</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="dashboard-card">
            <h3 style="text-align: center; color: #667eea;">👤 New User Registration</h3>
            <p style="text-align: center; color: #6b7280;">Please provide your details to create your account</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("registration_form"):
            full_name = st.text_input("📋 Full Name *", placeholder="Enter your full name")
            email = st.text_input("📧 Email Address *", placeholder="Enter your email address")
            student_id = st.text_input("🆔 Student ID *", placeholder="Enter your student ID")
            role = st.selectbox("👥 Select Your Role *", ["Student", "Teacher", "Counselor"])
            
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                register_button = st.form_submit_button("🚀 Create Account", use_container_width=True)
            
            if register_button:
                if full_name and email and student_id:
                    # Generate credentials
                    username, password = generate_credentials(full_name, student_id)
                    
                    # Use backend registration
                    success, message = register_user(username, password, full_name, email, student_id, role)
                    
                    if success:
                        # Mark as not first time user
                        st.session_state.is_first_time_user = False
                        st.session_state.registration_success = True  # Set success flag
                        
                        # Show success and credentials
                        st.success("🎉 Account Created Successfully!")
                        
                        st.markdown("""
                        <div style="background: linear-gradient(135deg, #d4edda, #c3e6cb); 
                                   color: #155724; padding: 2rem; border-radius: 15px; 
                                   margin: 1rem 0; border-left: 5px solid #28a745;">
                            <h3 style="margin-top: 0; color: #155724;">🔑 Your Login Credentials</h3>
                            <p style="font-size: 1.1em; margin: 0.5rem 0;"><strong>Username:</strong> <code style="background: rgba(0,0,0,0.1); padding: 0.2rem 0.5rem; border-radius: 4px;">{}</code></p>
                            <p style="font-size: 1.1em; margin: 0.5rem 0;"><strong>Password:</strong> <code style="background: rgba(0,0,0,0.1); padding: 0.2rem 0.5rem; border-radius: 4px;">{}</code></p>
                            <p style="margin: 1rem 0 0 0; font-weight: 600;">⚠️ Please save these credentials securely. You will need them to log in.</p>
                        </div>
                        """.format(username, password), unsafe_allow_html=True)
                        
                        # Save success info for display outside form
                        st.session_state.temp_credentials = {'username': username, 'password': password}
                        
                        # Auto redirect to login after 5 seconds
                        st.markdown("<br>", unsafe_allow_html=True)
                    else:
                        st.error(f"⚠️ {message}")
                        
                else:
                    st.warning("⚠️ Please fill in all required fields.")
        
        # Continue to login button outside the form
        if st.session_state.get('registration_success', False):
            col_continue1, col_continue2, col_continue3 = st.columns([1, 2, 1])
            with col_continue2:
                if st.button("✅ Continue to Login", key="continue_login_btn", type="primary", use_container_width=True):
                    st.session_state.current_page = 'login'
                    st.session_state.registration_success = False  # Reset flag
                    st.rerun()
        
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem; padding: 1rem; background: #f8f9fa; border-radius: 10px;">
            <h4>ℹ️ Registration Information</h4>
            <p><strong>First Time Users:</strong> Complete registration to get your login credentials</p>
            <p><strong>Returning Users:</strong> Use the login page with your existing credentials</p>
        </div>
        """, unsafe_allow_html=True)

def show_login_page():
    """Display the Login page"""
    # Add back button to return to home page
    if st.button("← Back to Home", key="back_to_home_btn", help="Return to home page"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    # Don't show hero section on login page to avoid confusion
    st.markdown("""
    <div class="main-header">
        <h1>🔐 Login to DROPSAFE</h1>
        <p>Access Your Personalized Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.logged_in:
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div class="dashboard-card">
                <h3 style="text-align: center; color: #667eea;">🔑 User Authentication</h3>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("login_form"):
                username = st.text_input("👤 Username", placeholder="Enter your username")
                password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
                
                col_a, col_b, col_c = st.columns([1, 1, 1])
                with col_a:
                    login_button = st.form_submit_button("🚀 Login", use_container_width=True)
                with col_c:
                    register_button = st.form_submit_button("📝 Register", use_container_width=True)
                
                if login_button:
                    if username and password:
                        # Use backend authentication
                        success, user_data, message = authenticate_user(username, password)
                        if success and user_data is not None:
                            st.session_state.logged_in = True
                            st.session_state.selected_role = user_data['role']
                            st.session_state.current_page = 'dashboard'
                            st.success(f"Welcome {user_data['full_name']}! Redirecting to {user_data['role'].title()} Dashboard...")
                            st.rerun()
                        else:
                            st.error(f"🚫 {message}")
                    else:
                        st.warning("⚠️ Please fill in all fields.")
                
                if register_button:
                    # Redirect to registration page
                    st.session_state.current_page = 'register'
                    st.rerun()
            
            # Password Reset Section
            st.markdown("<hr style='margin: 2rem 0; border-color: rgba(0,0,0,0.1);'>", unsafe_allow_html=True)
            
            st.markdown("""
            <div style="text-align: center; margin: 1rem 0; padding: 1.5rem; 
                       background: linear-gradient(135deg, #fff3cd, #ffeaa7); 
                       border-radius: 15px; border-left: 5px solid #ffc107;">
                <h4 style="color: #856404; margin-top: 0;">🔄 Forgot Your Password?</h4>
                <p style="color: #856404; margin-bottom: 0;">Reset your password using your username and student ID</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("password_reset_form"):
                st.markdown("**Password Reset**")
                reset_username = st.text_input("👤 Username", placeholder="Enter your username", key="reset_username")
                reset_student_id = st.text_input("🆔 Student ID", placeholder="Enter your student ID", key="reset_student_id")
                
                col_reset = st.columns([1, 2, 1])
                with col_reset[1]:
                    reset_button = st.form_submit_button("🔄 Reset Password", use_container_width=True)
                
                if reset_button:
                    if reset_username and reset_student_id:
                        success, result = reset_password(reset_username, reset_student_id)
                        if success:
                            st.success("✅ Password reset successful!")
                            st.markdown("""
                            <div style="background: linear-gradient(135deg, #d4edda, #c3e6cb); 
                                       color: #155724; padding: 2rem; border-radius: 15px; 
                                       margin: 1rem 0; border-left: 5px solid #28a745;">
                                <h4 style="margin-top: 0; color: #155724;">🔑 Your New Password</h4>
                                <p style="font-size: 1.1em; margin: 0.5rem 0;"><strong>Username:</strong> <code style="background: rgba(0,0,0,0.1); padding: 0.2rem 0.5rem; border-radius: 4px;">{}</code></p>
                                <p style="font-size: 1.1em; margin: 0.5rem 0;"><strong>New Password:</strong> <code style="background: rgba(0,0,0,0.1); padding: 0.2rem 0.5rem; border-radius: 4px;">{}</code></p>
                                <p style="margin: 1rem 0 0 0; font-weight: 600;">⚠️ Please save this new password securely. Use it to log in above.</p>
                            </div>
                            """.format(reset_username, result), unsafe_allow_html=True)
                        else:
                            st.error(f"❌ {result}")
                    else:
                        st.warning("⚠️ Please fill in all fields for password reset.")
        
        # Add footer
        show_footer()
    else:
        st.success("✅ You are already logged in!")
        st.markdown("""
        <div class="alert-success">
            <h3>🎉 Login Successful!</h3>
            <p>You can now access your personalized dashboard. Use the navigation above to explore different sections.</p>
        </div>
        """)

# --- UTILITY FUNCTIONS ---
def generate_credentials(full_name, student_id):
    """Generate unique username and password for new users"""
    import random
    import string
    
    # Generate username: first part of name + last 4 digits of student ID
    name_part = full_name.split()[0].lower()[:6]
    id_part = str(student_id)[-4:] if len(str(student_id)) >= 4 else str(student_id)
    username = f"{name_part}{id_part}"
    
    # Generate random 8-character password
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    
    return username, password

def store_user_credentials(username, password, full_name, email, student_id, role):
    """Store user credentials securely in session state"""
    st.session_state.user_credentials[username] = {
        'password': password,
        'full_name': full_name,
        'email': email,
        'student_id': student_id,
        'role': role
    }

def check_user_exists(student_id):
    """Check if user with given student ID already exists"""
    for creds in st.session_state.user_credentials.values():
        if creds.get('student_id') == student_id:
            return True
    return False

# --- BACKEND STORAGE FUNCTIONS ---
def hash_password(password):
    """Hash password for secure storage"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users_from_file():
    """Load users from JSON file"""
    users_file = 'users_data.json'
    if os.path.exists(users_file):
        try:
            with open(users_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    return {}

def save_users_to_file(users_data):
    """Save users to JSON file"""
    users_file = 'users_data.json'
    try:
        with open(users_file, 'w') as f:
            json.dump(users_data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving user data: {e}")
        return False

def register_user(username, password, full_name, email, student_id, role):
    """Register a new user and save to backend"""
    # Load existing users
    users_data = load_users_from_file()
    
    # Check if username already exists
    if username in users_data:
        return False, "Username already exists"
    
    # Check if student ID already exists
    for user_data in users_data.values():
        if user_data.get('student_id') == student_id:
            return False, "Student ID already registered"
    
    # Hash password for security
    hashed_password = hash_password(password)
    
    # Create new user record
    user_record = {
        'password': hashed_password,
        'full_name': full_name,
        'email': email,
        'student_id': student_id,
        'role': role.lower(),
        'created_at': datetime.now().isoformat(),
        'last_login': None
    }
    
    # Add to users data
    users_data[username] = user_record
    
    # Save to file
    if save_users_to_file(users_data):
        # Also update session state
        if 'user_credentials' not in st.session_state:
            st.session_state.user_credentials = {}
        st.session_state.user_credentials[username] = user_record
        return True, "User registered successfully"
    else:
        return False, "Error saving user data"

def authenticate_user(username, password):
    """Authenticate user against stored data"""
    # Load users from file
    users_data = load_users_from_file()
    
    # Check if username exists
    if username not in users_data:
        return False, None, "Username not found"
    
    # Check password
    stored_password = users_data[username]['password']
    if hash_password(password) == stored_password:
        # Update last login
        users_data[username]['last_login'] = datetime.now().isoformat()
        save_users_to_file(users_data)
        
        # Update session state
        if 'user_credentials' not in st.session_state:
            st.session_state.user_credentials = {}
        st.session_state.user_credentials[username] = users_data[username]
        
        return True, users_data[username], "Login successful"
    else:
        return False, None, "Invalid password"

def reset_password(username, student_id):
    """Reset password for a user after verification"""
    import random
    import string
    
    # Load users from file
    users_data = load_users_from_file()
    
    # Check if username exists
    if username not in users_data:
        return False, "Username not found"
    
    # Verify student ID matches
    if users_data[username]['student_id'] != student_id:
        return False, "Student ID does not match our records"
    
    # Generate new password
    new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    
    # Update password in data
    users_data[username]['password'] = hash_password(new_password)
    users_data[username]['last_login'] = None  # Reset last login
    
    # Save to file
    if save_users_to_file(users_data):
        # Update session state
        if 'user_credentials' not in st.session_state:
            st.session_state.user_credentials = {}
        st.session_state.user_credentials[username] = users_data[username]
        
        return True, new_password
    else:
        return False, "Error updating password"

def initialize_backend_data():
    """Initialize backend data on app start"""
    # Load existing users into session state
    users_data = load_users_from_file()
    if 'user_credentials' not in st.session_state:
        st.session_state.user_credentials = users_data
    else:
        # Merge with session state
        st.session_state.user_credentials.update(users_data)
    
    # Initialize alerts system
    load_alerts_from_file()

# --- ALERT MANAGEMENT FUNCTIONS ---
def save_alerts_to_file():
    """Save alerts to JSON file"""
    alerts_file = 'student_alerts.json'
    try:
        alerts_data = {
            'student_alerts': st.session_state.get('student_alerts', {}),
            'alert_notifications': st.session_state.get('alert_notifications', [])
        }
        with open(alerts_file, 'w') as f:
            json.dump(alerts_data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving alerts: {e}")
        return False

def load_alerts_from_file():
    """Load alerts from JSON file"""
    alerts_file = 'student_alerts.json'
    if os.path.exists(alerts_file):
        try:
            with open(alerts_file, 'r') as f:
                alerts_data = json.load(f)
                st.session_state.student_alerts = alerts_data.get('student_alerts', {})
                st.session_state.alert_notifications = alerts_data.get('alert_notifications', [])
        except (json.JSONDecodeError, FileNotFoundError):
            st.session_state.student_alerts = {}
            st.session_state.alert_notifications = []
    else:
        st.session_state.student_alerts = {}
        st.session_state.alert_notifications = []

def send_alert_to_student(student_id, message, alert_type, sender, priority="Normal"):
    """Send an alert to a specific student"""
    alert_id = f"alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{student_id}"
    
    alert = {
        'id': alert_id,
        'student_id': student_id,
        'message': message,
        'type': alert_type,  # 'performance', 'attendance', 'fee', 'general'
        'priority': priority,  # 'High', 'Normal', 'Low'
        'sender': sender,
        'timestamp': datetime.now().isoformat(),
        'read': False,
        'responded': False
    }
    
    # Add to student-specific alerts
    if student_id not in st.session_state.student_alerts:
        st.session_state.student_alerts[student_id] = []
    
    st.session_state.student_alerts[student_id].append(alert)
    
    # Add to general notifications
    st.session_state.alert_notifications.append(alert)
    
    # Save to file
    save_alerts_to_file()
    
    return alert_id

def get_student_alerts(student_id):
    """Get all alerts for a specific student"""
    return st.session_state.student_alerts.get(student_id, [])

def mark_alert_as_read(student_id, alert_id):
    """Mark an alert as read"""
    if student_id in st.session_state.student_alerts:
        for alert in st.session_state.student_alerts[student_id]:
            if alert['id'] == alert_id:
                alert['read'] = True
                break
    
    # Update in notifications list
    for alert in st.session_state.alert_notifications:
        if alert['id'] == alert_id:
            alert['read'] = True
            break
    
    save_alerts_to_file()

def get_unread_alerts_count(student_id):
    """Get count of unread alerts for a student"""
    alerts = get_student_alerts(student_id)
    return len([alert for alert in alerts if not alert['read']])

@st.cache_data
def load_and_merge_data(att_file, sc_file, fee_file):
    try:
        df_att = pd.read_excel(att_file)
        df_sc = pd.read_excel(sc_file)
        df_fee = pd.read_excel(fee_file)
        return df_att.merge(df_sc, on='Student_ID').merge(df_fee, on='Student_ID')
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def calculate_risk_score(row):
    score = 0
    if row['Attendance'] < 70: score += 4
    elif row['Attendance'] < 80: score += 2
    if row['Test_Score'] < 40: score += 3
    elif row['Test_Score'] < 60: score += 1.5
    fee_status = str(row['Fee_Status']).lower()
    if 'overdue' in fee_status: score += 3
    elif 'pending' in fee_status: score += 1.5
    return round(score, 1)

def predict_with_ml(df):
    try:
        model = joblib.load('dropout_model.joblib')
        status_map = {'paid': 0, 'pending': 1, 'overdue': 2}
        df['Fee_Status_Code'] = df['Fee_Status'].astype(str).str.lower().map(status_map).fillna(0)
        features = df[['Attendance', 'Test_Score', 'Fee_Status_Code']].fillna(0)
        predictions = model.predict(features)
        return ['High Risk' if p == 1 else 'Low Risk' for p in predictions]
    except:
        return ['Rule-Based'] * len(df)

def process_data(df):
    if df is None: return None
    df['Rule_Score'] = df.apply(calculate_risk_score, axis=1)
    df['ML_Prediction'] = predict_with_ml(df)
    conditions = [
        (df['Rule_Score'] >= 7) & (df['ML_Prediction'] == 'High Risk'),
        (df['Rule_Score'] >= 6),
        (df['Rule_Score'] >= 3) | (df['ML_Prediction'] == 'High Risk')
    ]
    choices = ['Very High Risk', 'High Risk', 'Medium Risk']
    df['Final_Risk'] = np.select(conditions, choices, default='Low Risk')
    return df

# --- DATA UPLOAD ---
def show_upload():
    st.sidebar.markdown("""
    <div style="background: linear-gradient(180deg, #667eea 0%, #764ba2 100%); 
               padding: 1.5rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 1rem;">
        <h3 style="margin: 0;">📊 Data Upload</h3>
    </div>
    """, unsafe_allow_html=True)

    att_file = st.sidebar.file_uploader("📈 Attendance File", type=["xlsx", "xls"], key="att")
    score_file = st.sidebar.file_uploader("📝 Test Scores File", type=["xlsx", "xls"], key="score")  
    fee_file = st.sidebar.file_uploader("💰 Fee Status File", type=["xlsx", "xls"], key="fee")

    files_count = sum([bool(att_file), bool(score_file), bool(fee_file)])
    st.sidebar.markdown(f"**Progress: {files_count}/3 files**")
    
    if files_count == 3:
        st.sidebar.success("🎉 All files uploaded!")
        with st.spinner('Processing...'):
            data = load_and_merge_data(att_file, score_file, fee_file)
            st.session_state.student_data = process_data(data)
    elif files_count > 0:
        st.sidebar.warning(f"⚠️ {3-files_count} more needed")
    else:
        st.sidebar.info("📁 Upload files to begin")
    
    return st.session_state.student_data

# --- ROLE SELECTION / HOME PAGE ---
def show_role_selection():
    show_hero_section()  # Add hero section at the top
    
    # Add footer
    show_footer()

def show_footer():
    """Display a simplified footer section using Streamlit components"""
    st.markdown("---")
    
    # Create a container with background styling
    with st.container():
        st.markdown("""
        <div style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); 
                    color: white; padding: 3rem 2rem; border-radius: 20px; margin-top: 2rem; 
                    margin-bottom: 3rem; text-align: center; width: 100%; min-height: 200px;
                    backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.1);
                    box-shadow: 0 12px 40px rgba(15, 23, 42, 0.4);">
            <h2 style="color: white; margin-bottom: 0.5rem; font-size: 2.5rem; font-weight: 800;">🛡️ DROPSAFE</h2>
            <p style="color: #E2E8F0; margin-bottom: 2rem; font-size: 1.3rem; font-weight: 500;">Transforming Education Through Intelligent Analytics</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Use columns for the three sections
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; text-align: center;">
                <h4 style="color: #0D9488; margin-bottom: 1rem;">About DROPSAFE</h4>
                <p style="color: #CBD5E1; font-size: 0.9rem;">AI-powered platform for identifying students at risk and providing educational insights.</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; text-align: center;">
                <h4 style="color: #0D9488; margin-bottom: 1rem;">Contact</h4>
                <p style="color: #CBD5E1; font-size: 0.9rem;">Email: support@dropsafe.edu<br>Phone: +1 (555) 123-4567</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; text-align: center;">
                <h4 style="color: #0D9488; margin-bottom: 1rem;">Features</h4>
                <p style="color: #CBD5E1; font-size: 0.9rem;">Multi-role dashboards, AI predictions, real-time analytics</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Copyright section
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem; padding: 1rem; border-top: 1px solid rgba(13, 148, 136, 0.3);">
            <p style="color: #94A3B8; margin: 0; font-size: 0.9rem;">
                © 2024 DROPSAFE Educational Analytics. All rights reserved.
            </p>
        </div>
        """, unsafe_allow_html=True)


# --- STUDENT DASHBOARD ---
def show_student_dashboard():
    st.markdown("""
    <div class="main-header">
        <h1>🎓 Student Dashboard</h1>
        <p>Your Personal Academic Analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("← Back to Role Selection"):
        st.session_state.selected_role = None
        st.rerun()
    
    # Get current student ID for alerts
    current_student_id = None
    current_user_data = None
    current_username = None
    if st.session_state.get('logged_in') and 'user_credentials' in st.session_state:
        for username, user_data in st.session_state.user_credentials.items():
            if user_data.get('role') == 'student':
                current_user_data = user_data
                current_username = username
                current_student_id = user_data.get('student_id')
                break
    
    # Notices & Alerts Section - Priority placement at top
    if current_student_id:
        student_alerts = get_student_alerts(current_student_id)
        unread_count = get_unread_alerts_count(current_student_id)
        
        if student_alerts:
            # Show alert banner if there are unread alerts
            if unread_count > 0:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
                    color: white;
                    padding: 1rem 2rem;
                    border-radius: 12px;
                    margin: 1rem 0;
                    text-align: center;
                    box-shadow: 0 4px 16px rgba(255, 107, 107, 0.3);
                    animation: pulse 2s infinite;
                ">
                    <h3 style="margin: 0; color: white;">🚨 You have {unread_count} new alert{'s' if unread_count != 1 else ''}!</h3>
                    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Please check the Notices & Alerts section below</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Notices & Alerts Section
            st.markdown("### 📢 Notices & Alerts")
            
            # Create tabs for different alert types
            alert_tab1, alert_tab2, alert_tab3 = st.tabs(["🚨 All Alerts", "📊 Performance Alerts", "📅 Other Notices"])
            
            with alert_tab1:
                st.markdown("#### 📋 All Notifications")
                
                # Sort alerts by timestamp (newest first)
                sorted_alerts = sorted(student_alerts, key=lambda x: x['timestamp'], reverse=True)
                
                for alert in sorted_alerts:
                    # Determine alert styling based on priority and read status
                    if not alert['read']:
                        border_color = "#ff6b6b" if alert['priority'] == 'High' else "#ffa726" if alert['priority'] == 'Normal' else "#66bb6a"
                        bg_gradient = "linear-gradient(135deg, #fff5f5 0%, #ffeaa7 100%)" if alert['priority'] == 'High' else "linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)"
                    else:
                        border_color = "#e9ecef"
                        bg_gradient = "linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%)"
                    
                    # Format timestamp
                    try:
                        from datetime import datetime as dt
                        alert_time = dt.fromisoformat(alert['timestamp']).strftime('%B %d, %Y at %I:%M %p')
                    except:
                        alert_time = alert['timestamp']
                    
                    # Alert type emoji
                    type_emoji = {
                        'performance': '📊',
                        'attendance': '📅', 
                        'fee': '💰',
                        'general': '📢'
                    }.get(alert['type'], '📢')
                    
                    # Priority emoji
                    priority_emoji = {
                        'High': '🚨',
                        'Normal': '⚠️',
                        'Low': 'ℹ️'
                    }.get(alert['priority'], 'ℹ️')
                    
                    st.markdown(f"""
                    <div style="
                        background: {bg_gradient};
                        border-left: 4px solid {border_color};
                        padding: 1.5rem;
                        border-radius: 12px;
                        margin: 1rem 0;
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                        {'opacity: 0.7;' if alert['read'] else ''}
                    ">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                            <h4 style="margin: 0; color: #0F172A;">
                                {type_emoji} {priority_emoji} {alert['type'].title()} Alert
                                {'<span style="background: #28a745; color: white; padding: 0.2rem 0.5rem; border-radius: 8px; font-size: 0.8rem; margin-left: 0.5rem;">READ</span>' if alert['read'] else '<span style="background: #dc3545; color: white; padding: 0.2rem 0.5rem; border-radius: 8px; font-size: 0.8rem; margin-left: 0.5rem;">NEW</span>'}
                            </h4>
                            <span style="font-size: 0.9rem; color: #6c757d;">{alert_time}</span>
                        </div>
                        <p style="margin: 0.5rem 0; color: #495057; line-height: 1.5;">{alert['message']}</p>
                        <p style="margin: 0; font-size: 0.9rem; color: #6c757d;">From: {alert['sender']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Mark as read button for unread alerts
                    if not alert['read']:
                        col1, col2, col3 = st.columns([1, 1, 4])
                        with col1:
                            if st.button(f"✅ Mark as Read", key=f"read_{alert['id']}"):
                                mark_alert_as_read(current_student_id, alert['id'])
                                st.success("Alert marked as read!")
                                st.rerun()
            
            with alert_tab2:
                st.markdown("#### 📊 Performance & Academic Alerts")
                performance_alerts = [alert for alert in sorted_alerts if alert['type'] in ['performance', 'attendance']]
                
                if performance_alerts:
                    for alert in performance_alerts:
                        # Same styling as above but filtered for performance alerts
                        if not alert['read']:
                            border_color = "#ff6b6b" if alert['priority'] == 'High' else "#ffa726"
                            bg_gradient = "linear-gradient(135deg, #fff5f5 0%, #ffeaa7 100%)" if alert['priority'] == 'High' else "linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)"
                        else:
                            border_color = "#e9ecef"
                            bg_gradient = "linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%)"
                        
                        try:
                            from datetime import datetime as dt
                            alert_time = dt.fromisoformat(alert['timestamp']).strftime('%B %d, %Y at %I:%M %p')
                        except:
                            alert_time = alert['timestamp']
                        
                        type_emoji = '📊' if alert['type'] == 'performance' else '📅'
                        priority_emoji = '🚨' if alert['priority'] == 'High' else '⚠️' if alert['priority'] == 'Normal' else 'ℹ️'
                        
                        st.markdown(f"""
                        <div style="
                            background: {bg_gradient};
                            border-left: 4px solid {border_color};
                            padding: 1.5rem;
                            border-radius: 12px;
                            margin: 1rem 0;
                            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                            {'opacity: 0.7;' if alert['read'] else ''}
                        ">
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                                <h4 style="margin: 0; color: #0F172A;">
                                    {type_emoji} {priority_emoji} {alert['type'].title()} Alert
                                    {'<span style="background: #28a745; color: white; padding: 0.2rem 0.5rem; border-radius: 8px; font-size: 0.8rem; margin-left: 0.5rem;">READ</span>' if alert['read'] else '<span style="background: #dc3545; color: white; padding: 0.2rem 0.5rem; border-radius: 8px; font-size: 0.8rem; margin-left: 0.5rem;">NEW</span>'}
                                </h4>
                                <span style="font-size: 0.9rem; color: #6c757d;">{alert_time}</span>
                            </div>
                            <p style="margin: 0.5rem 0; color: #495057; line-height: 1.5;">{alert['message']}</p>
                            <p style="margin: 0; font-size: 0.9rem; color: #6c757d;">From: {alert['sender']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if not alert['read']:
                            col1, col2, col3 = st.columns([1, 1, 4])
                            with col1:
                                if st.button(f"✅ Mark as Read", key=f"perf_read_{alert['id']}"):
                                    mark_alert_as_read(current_student_id, alert['id'])
                                    st.success("Alert marked as read!")
                                    st.rerun()
                else:
                    st.info("📊 No performance alerts at this time. Keep up the good work!")
            
            with alert_tab3:
                st.markdown("#### 📢 General Notices")
                other_alerts = [alert for alert in sorted_alerts if alert['type'] in ['fee', 'general']]
                
                if other_alerts:
                    for alert in other_alerts:
                        # Same styling pattern
                        if not alert['read']:
                            border_color = "#ff6b6b" if alert['priority'] == 'High' else "#ffa726"
                            bg_gradient = "linear-gradient(135deg, #fff5f5 0%, #ffeaa7 100%)" if alert['priority'] == 'High' else "linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)"
                        else:
                            border_color = "#e9ecef"
                            bg_gradient = "linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%)"
                        
                        try:
                            from datetime import datetime as dt
                            alert_time = dt.fromisoformat(alert['timestamp']).strftime('%B %d, %Y at %I:%M %p')
                        except:
                            alert_time = alert['timestamp']
                        
                        type_emoji = '💰' if alert['type'] == 'fee' else '📢'
                        priority_emoji = '🚨' if alert['priority'] == 'High' else '⚠️' if alert['priority'] == 'Normal' else 'ℹ️'
                        
                        st.markdown(f"""
                        <div style="
                            background: {bg_gradient};
                            border-left: 4px solid {border_color};
                            padding: 1.5rem;
                            border-radius: 12px;
                            margin: 1rem 0;
                            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                            {'opacity: 0.7;' if alert['read'] else ''}
                        ">
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                                <h4 style="margin: 0; color: #0F172A;">
                                    {type_emoji} {priority_emoji} {alert['type'].title()} Notice
                                    {'<span style="background: #28a745; color: white; padding: 0.2rem 0.5rem; border-radius: 8px; font-size: 0.8rem; margin-left: 0.5rem;">READ</span>' if alert['read'] else '<span style="background: #dc3545; color: white; padding: 0.2rem 0.5rem; border-radius: 8px; font-size: 0.8rem; margin-left: 0.5rem;">NEW</span>'}
                                </h4>
                                <span style="font-size: 0.9rem; color: #6c757d;">{alert_time}</span>
                            </div>
                            <p style="margin: 0.5rem 0; color: #495057; line-height: 1.5;">{alert['message']}</p>
                            <p style="margin: 0; font-size: 0.9rem; color: #6c757d;">From: {alert['sender']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if not alert['read']:
                            col1, col2, col3 = st.columns([1, 1, 4])
                            with col1:
                                if st.button(f"✅ Mark as Read", key=f"other_read_{alert['id']}"):
                                    mark_alert_as_read(current_student_id, alert['id'])
                                    st.success("Alert marked as read!")
                                    st.rerun()
                else:
                    st.info("📢 No general notices at this time.")
        else:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #e8f5e8 0%, #c3e6cb 100%);
                color: #155724;
                padding: 2rem;
                border-radius: 15px;
                margin: 1rem 0;
                text-align: center;
                border-left: 5px solid #28a745;
            ">
                <h3 style="margin: 0 0 0.5rem 0; color: #155724;">📢 No New Alerts</h3>
                <p style="margin: 0; opacity: 0.8;">You're all caught up! No new notifications from your teachers.</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Student Profile Section
    st.markdown("### 🎓 College Student Profile")
    
    # Get current logged-in user data
    current_user_data = None
    current_username = None
    if st.session_state.get('logged_in') and 'user_credentials' in st.session_state:
        # Find the current user's data based on the selected role
        for username, user_data in st.session_state.user_credentials.items():
            if user_data.get('role') == 'student':
                current_user_data = user_data
                current_username = username
                break
    
    # Profile information in columns
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        ">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🎓</div>
            <h3 style="margin: 0 0 0.5rem 0; color: white;">College Student</h3>
            <p style="margin: 0; opacity: 0.9;">Academic Profile</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if current_user_data and current_username:
            # Display actual user registration data
            full_name = current_user_data.get('full_name', 'Not Available')
            email = current_user_data.get('email', 'Not Available')
            student_id = current_user_data.get('student_id', 'Not Available')
            created_at = current_user_data.get('created_at', 'Not Available')
            last_login = current_user_data.get('last_login', 'Never')
            
            # Format dates if available
            if created_at != 'Not Available':
                try:
                    from datetime import datetime as dt
                    created_date = dt.fromisoformat(created_at).strftime('%B %d, %Y')
                except:
                    created_date = created_at
            else:
                created_date = 'Not Available'
                
            if last_login and last_login != 'Never' and last_login != 'Not Available':
                try:
                    from datetime import datetime as dt
                    last_login_date = dt.fromisoformat(last_login).strftime('%B %d, %Y at %I:%M %p')
                except:
                    last_login_date = last_login
            else:
                last_login_date = 'Never'
        else:
            # Default values if no user data found
            full_name = 'College Student'
            email = 'student@college.edu'
            student_id = 'COL-2024-001'
            current_username = 'student_user'
            created_date = 'Not Available'
            last_login_date = 'Never'
        
        st.markdown(f"""
        <div style="
            background: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 15px;
            border: 1px solid rgba(13, 148, 136, 0.2);
            box-shadow: 0 4px 16px rgba(15, 23, 42, 0.1);
        ">
            <h4 style="color: #0F172A; margin-top: 0;">Personal Information</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                <div>
                    <strong style="color: #0D9488;">Full Name:</strong><br>
                    <span style="color: #475569;">{full_name}</span>
                </div>
                <div>
                    <strong style="color: #0D9488;">Student ID:</strong><br>
                    <span style="color: #475569;">{student_id}</span>
                </div>
                <div>
                    <strong style="color: #0D9488;">Username:</strong><br>
                    <span style="color: #475569;">{current_username if current_username else 'Not Available'}</span>
                </div>
                <div>
                    <strong style="color: #0D9488;">Academic Year:</strong><br>
                    <span style="color: #475569;">2024-2025</span>
                </div>
                <div>
                    <strong style="color: #0D9488;">Email:</strong><br>
                    <span style="color: #475569;">{email}</span>
                </div>
                <div>
                    <strong style="color: #0D9488;">Program:</strong><br>
                    <span style="color: #475569;">Bachelor of Science</span>
                </div>
                <div>
                    <strong style="color: #0D9488;">Registration Date:</strong><br>
                    <span style="color: #475569;">{created_date}</span>
                </div>
                <div>
                    <strong style="color: #0D9488;">Last Login:</strong><br>
                    <span style="color: #475569;">{last_login_date}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Academic Overview for College Student
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📚 Academic Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="📊 Current CGPA", value="3.75", delta="+0.15 this semester")
    
    with col2:
        st.metric(label="📅 Attendance Rate", value="88%", delta="+3% this month")
    
    with col3:
        st.metric(label="📝 Assignments", value="12/15", delta="3 pending")
    
    with col4:
        st.metric(label="🎯 Course Credits", value="18/20", delta="2 remaining")
    
    # Note: Data upload is not available for students
    st.info("📊 Student dashboards use pre-loaded institutional data. Data upload is available for teachers and counselors.")
    
    # Enhanced Data Display Section
    st.markdown("### 📋 My Academic Data")
    
    # Check if there's any student data available (uploaded by teachers/counselors)
    data = st.session_state.get('student_data', None)
    
    if data is not None and len(data) > 0:
        st.success(f"✅ Academic data is available ({len(data)} student records loaded by faculty)")
        
        # Create tabs for different data views
        tab1, tab2, tab3 = st.tabs(["📊 My Performance", "📈 Class Analytics", "📋 Raw Data View"])
        
        with tab1:
            # Personal student data selection
            st.markdown("#### 🎯 Select Your Student ID")
            student_id = st.selectbox("Choose your Student ID to view personal analytics:", 
                                    [''] + list(data['Student_ID'].unique()), 
                                    key="student_id_selector")
            
            if student_id:
                student_row = data[data['Student_ID'] == student_id]
                if len(student_row) > 0:
                    student = student_row.iloc[0]
                    
                    # Personal Performance Card
                    st.markdown(f"""
                    <div class="student-profile">
                        <h2>📊 Performance Analytics - ID: {student_id}</h2>
                        <h3 style="color: white;">Risk Level: {student['Final_Risk']}</h3>
                        <p>Risk Score: {student['Rule_Score']}/10</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Detailed metrics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("📈 Attendance", f"{student['Attendance']}%")
                    with col2:
                        st.metric("📝 Test Score", f"{student['Test_Score']}")
                    with col3:
                        st.metric("💰 Fee Status", student['Fee_Status'])
                    with col4:
                        st.metric("📊 Risk Score", f"{student['Rule_Score']}/10")
                    
                    # Personalized recommendations
                    st.markdown("#### 💡 Personalized Recommendations")
                    recommendations = []
                    
                    if student['Attendance'] < 80:
                        recommendations.append({
                            'title': '📈 Improve Attendance',
                            'message': f"Your attendance is {student['Attendance']}%. Aim for 85%+",
                            'type': 'warning' if student['Attendance'] < 70 else 'info'
                        })
                    
                    if student['Test_Score'] < 70:
                        recommendations.append({
                            'title': '📚 Academic Support',
                            'message': f"Test score: {student['Test_Score']}. Consider tutoring",
                            'type': 'warning'
                        })
                    
                    if student['Fee_Status'].lower() in ['pending', 'overdue']:
                        recommendations.append({
                            'title': '💰 Fee Payment',
                            'message': "Please resolve your fee status",
                            'type': 'danger' if student['Fee_Status'].lower() == 'overdue' else 'warning'
                        })
                    
                    if not recommendations:
                        recommendations.append({
                            'title': '🎉 Great Job!',
                            'message': "You're doing well! Keep it up!",
                            'type': 'success'
                        })
                    
                    for rec in recommendations:
                        st.markdown(f"""
                        <div class="alert-{rec['type']}">
                            <h4 style="margin-top: 0;">{rec['title']}</h4>
                            <p style="margin-bottom: 0;">{rec['message']}</p>
                        </div>
                        """, unsafe_allow_html=True)
        
        with tab2:
            # Class-wide analytics for context
            st.markdown("#### 📈 Class Performance Overview")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                avg_attendance = data['Attendance'].mean()
                st.metric("📅 Class Avg Attendance", f"{avg_attendance:.1f}%")
            with col2:
                avg_score = data['Test_Score'].mean()
                st.metric("📝 Class Avg Score", f"{avg_score:.1f}")
            with col3:
                high_risk_count = len(data[data['Final_Risk'].isin(['High Risk', 'Very High Risk'])])
                st.metric("⚠️ High Risk Students", f"{high_risk_count}/{len(data)}")
            
            # Risk distribution chart
            import plotly.express as px
            fig = px.pie(data['Final_Risk'].value_counts().reset_index(), 
                        values='count', names='Final_Risk',
                        title="Class Risk Distribution",
                        color_discrete_map={
                            'Very High Risk': '#ff6b6b',
                            'High Risk': '#ff9f43', 
                            'Medium Risk': '#ffa726',
                            'Low Risk': '#66bb6a'
                        })
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Raw data display
            st.markdown("#### 📋 Complete Dataset (Faculty Uploaded)")
            st.info("This shows the complete academic dataset uploaded by your teachers/counselors.")
            
            # Data summary
            st.markdown(f"**Dataset Information:**")
            col_info1, col_info2, col_info3 = st.columns(3)
            with col_info1:
                st.metric("📊 Total Records", len(data))
            with col_info2:
                st.metric("📋 Data Columns", len(data.columns))
            with col_info3:
                st.metric("📅 Last Updated", datetime.now().strftime("%Y-%m-%d"))
            
            # Advanced filtering options
            st.markdown("**📝 Data Filtering & Display Options**")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                # Column selection with better defaults
                default_columns = ['Student_ID', 'Attendance', 'Test_Score', 'Fee_Status', 'Final_Risk', 'Rule_Score']
                available_defaults = [col for col in default_columns if col in data.columns]
                
                show_columns = st.multiselect(
                    "📑 Select columns to display:",
                    options=data.columns.tolist(),
                    default=available_defaults if available_defaults else data.columns.tolist()[:6]
                )
                
                # Risk level filter
                risk_filter = st.multiselect(
                    "⚠️ Filter by Risk Level:",
                    options=['All'] + data['Final_Risk'].unique().tolist(),
                    default=['All']
                )
            
            with col2:
                max_rows = st.number_input("📊 Max rows to show:", min_value=10, max_value=len(data), value=min(50, len(data)))
                
                # Search functionality
                search_student = st.text_input("🔍 Search Student ID:", placeholder="Enter Student ID")
            
            if show_columns:
                # Apply filters
                filtered_data = data.copy()
                
                # Apply risk filter
                if risk_filter and 'All' not in risk_filter:
                    filtered_data = filtered_data[filtered_data['Final_Risk'].isin(risk_filter)]
                
                # Apply student ID search
                if search_student:
                    filtered_data = filtered_data[filtered_data['Student_ID'].astype(str).str.contains(search_student, case=False, na=False)]
                
                # Select columns and limit rows
                display_data = filtered_data[show_columns].head(max_rows)
                
                # Show filtering results
                if len(filtered_data) < len(data):
                    st.info(f"📊 Showing {len(display_data)} of {len(filtered_data)} filtered records (from {len(data)} total)")
                else:
                    st.info(f"📊 Showing {len(display_data)} of {len(data)} total records")
                
                # Enhanced data display with styling
                st.markdown("**📋 Data Table:**")
                
                # Color-code risk levels in the dataframe if Final_Risk column is selected
                if 'Final_Risk' in show_columns:
                    def highlight_risk(val):
                        if val == 'Very High Risk':
                            return 'background-color: #ffebee; color: #c62828;'
                        elif val == 'High Risk':
                            return 'background-color: #fff3e0; color: #ef6c00;'
                        elif val == 'Medium Risk':
                            return 'background-color: #fff8e1; color: #f57f17;'
                        elif val == 'Low Risk':
                            return 'background-color: #e8f5e8; color: #2e7d32;'
                        return ''
                    
                    if 'Final_Risk' in display_data.columns:
                        styled_data = display_data.style.applymap(highlight_risk, subset=['Final_Risk'])
                        st.dataframe(styled_data, use_container_width=True)
                    else:
                        st.dataframe(display_data, use_container_width=True)
                else:
                    st.dataframe(display_data, use_container_width=True)
                
                # Enhanced download options
                st.markdown("**📥 Download Options:**")
                col_dl1, col_dl2, col_dl3 = st.columns(3)
                
                with col_dl1:
                    # Download filtered data as CSV
                    csv = display_data.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Filtered Data (CSV)",
                        data=csv,
                        file_name=f'student_data_filtered_{datetime.now().strftime("%Y%m%d_%H%M")}.csv',
                        mime='text/csv'
                    )
                
                with col_dl2:
                    # Download complete dataset
                    if st.button("📊 Download Complete Dataset"):
                        complete_csv = data.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Complete Data (CSV)",
                            data=complete_csv,
                            file_name=f'complete_student_data_{datetime.now().strftime("%Y%m%d_%H%M")}.csv',
                            mime='text/csv',
                            key="complete_download"
                        )
                
                with col_dl3:
                    # Download summary report
                    if st.button("📈 Generate Summary Report"):
                        summary_stats = data.describe()
                        summary_csv = summary_stats.to_csv()
                        st.download_button(
                            label="📊 Download Summary Stats",
                            data=summary_csv,
                            file_name=f'data_summary_{datetime.now().strftime("%Y%m%d_%H%M")}.csv',
                            mime='text/csv',
                            key="summary_download"
                        )
            else:
                st.warning("⚠️ Please select at least one column to display the data.")
    else:
        st.markdown("""
        <div class="alert-warning">
            <h3>📁 No Data Available</h3>
            <p>No academic data has been uploaded yet. Please ask your teachers or counselors to upload the institutional data files to view your dashboard analytics.</p>
            <ul>
                <li>Teachers can upload class performance data</li>
                <li>Counselors can upload institution-wide analytics</li>
                <li>Once uploaded, your personal analytics will appear here</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# --- TEACHER DASHBOARD ---
def show_teacher_dashboard():
    st.markdown("""
    <div class="main-header">
        <h1>👩‍🏫 Teacher Dashboard</h1>
        <p>Classroom Analytics & Student Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("← Back to Role Selection"):
        st.session_state.selected_role = None
        st.rerun()
    
    data = show_upload()
    
    if data is not None and len(data) > 0:
        total = len(data)
        high_risk = len(data[data['Final_Risk'].isin(['Very High Risk', 'High Risk'])])
        avg_attendance = data['Attendance'].mean()
        avg_score = data['Test_Score'].mean()
        
        st.markdown("### 📊 Class Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 Total Students", total)
        with col2:
            st.metric("⚠️ At-Risk Students", high_risk, f"{(high_risk/total*100):.1f}%")
        with col3:
            st.metric("📈 Avg Attendance", f"{avg_attendance:.1f}%")
        with col4:
            st.metric("📝 Avg Test Score", f"{avg_score:.1f}")
        
        # At-risk students list
        st.markdown("### ⚠️ Students Requiring Attention")
        at_risk = data[data['Final_Risk'].isin(['Very High Risk', 'High Risk'])].sort_values('Rule_Score', ascending=False)
        
        if len(at_risk) > 0:
            # Alert Management Section
            st.markdown("#### 📤 Send Alerts to Students")
            
            # Quick alert for at-risk students
            for _, student in at_risk.iterrows():
                risk_class = student['Final_Risk'].lower().replace(' ', '-')
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="dashboard-card">
                        <h4>Student ID: {student['Student_ID']} <span class="risk-{risk_class}">{student['Final_Risk']}</span></h4>
                        <p>Attendance: {student['Attendance']}% | Test Score: {student['Test_Score']} | Fee: {student['Fee_Status']} | Risk Score: {student['Rule_Score']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if st.button(f"📨 Send Alert", key=f"alert_{student['Student_ID']}"):
                        st.session_state[f"show_alert_form_{student['Student_ID']}"] = True
                
                # Show alert form if button clicked
                if st.session_state.get(f"show_alert_form_{student['Student_ID']}", False):
                    with st.expander(f"📝 Send Alert to Student {student['Student_ID']}", expanded=True):
                        with st.form(f"alert_form_{student['Student_ID']}"):
                            alert_type = st.selectbox(
                                "Alert Type:",
                                ['performance', 'attendance', 'fee', 'general'],
                                key=f"type_{student['Student_ID']}"
                            )
                            
                            priority = st.selectbox(
                                "Priority:",
                                ['High', 'Normal', 'Low'],
                                key=f"priority_{student['Student_ID']}"
                            )
                            
                            # Pre-filled message based on student issues
                            suggested_message = ""
                            if student['Attendance'] < 70:
                                suggested_message += f"Your attendance is {student['Attendance']}%, which is below the required minimum. Please improve your class attendance. "
                            if student['Test_Score'] < 50:
                                suggested_message += f"Your recent test score of {student['Test_Score']} indicates academic difficulties. Please consider additional study support. "
                            if student['Fee_Status'].lower() in ['pending', 'overdue']:
                                suggested_message += f"Your fee status is {student['Fee_Status']}. Please resolve this at the earliest. "
                            
                            if not suggested_message:
                                suggested_message = "We've noticed some areas where you could improve. Please see me for a discussion."
                            
                            alert_message = st.text_area(
                                "Message:",
                                value=suggested_message,
                                height=100,
                                key=f"message_{student['Student_ID']}"
                            )
                            
                            col_send1, col_send2 = st.columns([1, 1])
                            with col_send1:
                                send_alert = st.form_submit_button("📤 Send Alert")
                            with col_send2:
                                cancel_alert = st.form_submit_button("❌ Cancel")
                            
                            if send_alert and alert_message:
                                # Get current teacher info
                                current_teacher = "Teacher"
                                if st.session_state.get('logged_in') and 'user_credentials' in st.session_state:
                                    for username, user_data in st.session_state.user_credentials.items():
                                        if user_data.get('role') == 'teacher':
                                            current_teacher = user_data.get('full_name', 'Teacher')
                                            break
                                
                                alert_id = send_alert_to_student(
                                    student['Student_ID'],
                                    alert_message,
                                    alert_type,
                                    current_teacher,
                                    priority
                                )
                                
                                st.success(f"✅ Alert sent successfully to Student {student['Student_ID']}!")
                                st.session_state[f"show_alert_form_{student['Student_ID']}"] = False
                                st.rerun()
                            
                            if cancel_alert:
                                st.session_state[f"show_alert_form_{student['Student_ID']}"] = False
                                st.rerun()
            
            # Bulk alert section
            st.markdown("#### 📢 Send Bulk Alert to All At-Risk Students")
            with st.expander("📝 Compose Bulk Alert"):
                with st.form("bulk_alert_form"):
                    bulk_alert_type = st.selectbox("Alert Type:", ['performance', 'attendance', 'fee', 'general'])
                    bulk_priority = st.selectbox("Priority:", ['High', 'Normal', 'Low'])
                    bulk_message = st.text_area(
                        "Message for all at-risk students:",
                        "Your recent academic performance indicates you may need additional support. Please schedule a meeting with me to discuss improvement strategies.",
                        height=100
                    )
                    
                    send_bulk = st.form_submit_button("📤 Send to All At-Risk Students")
                    
                    if send_bulk and bulk_message:
                        # Get current teacher info
                        current_teacher = "Teacher"
                        if st.session_state.get('logged_in') and 'user_credentials' in st.session_state:
                            for username, user_data in st.session_state.user_credentials.items():
                                if user_data.get('role') == 'teacher':
                                    current_teacher = user_data.get('full_name', 'Teacher')
                                    break
                        
                        sent_count = 0
                        for _, student in at_risk.iterrows():
                            send_alert_to_student(
                                student['Student_ID'],
                                bulk_message,
                                bulk_alert_type,
                                current_teacher,
                                bulk_priority
                            )
                            sent_count += 1
                        
                        st.success(f"✅ Bulk alert sent to {sent_count} at-risk students!")
                        st.rerun()
        else:
            st.success("🎉 No high-risk students identified!")
        
        # Class performance charts
        st.markdown("### 📈 Class Performance Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            fig_risk = px.pie(data['Final_Risk'].value_counts().reset_index(), 
                             values='count', names='Final_Risk',
                             title="Risk Distribution",
                             color_discrete_map={
                                 'Very High Risk': '#ff6b6b',
                                 'High Risk': '#ff9f43', 
                                 'Medium Risk': '#ffa726',
                                 'Low Risk': '#66bb6a'
                             })
            st.plotly_chart(fig_risk, use_container_width=True)
        
        with col2:
            fig_scatter = px.scatter(data, x='Attendance', y='Test_Score', 
                                   color='Final_Risk', size='Rule_Score',
                                   title="Attendance vs Test Score",
                                   color_discrete_map={
                                       'Very High Risk': '#ff6b6b',
                                       'High Risk': '#ff9f43',
                                       'Medium Risk': '#ffa726', 
                                       'Low Risk': '#66bb6a'
                                   })
            st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.markdown("""
        <div class="alert-warning">
            <h3>📁 Upload Required</h3>
            <p>Upload student data to access teacher analytics.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Add footer
    show_footer()

# --- COUNSELOR DASHBOARD ---
def show_counselor_dashboard():
    st.markdown("""
    <div class="main-header">
        <h1>🧠 Counselor Dashboard</h1>
        <p>Advanced Analytics & Intervention Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("← Back to Role Selection"):
        st.session_state.selected_role = None
        st.rerun()
    
    data = show_upload()
    
    if data is not None and len(data) > 0:
        st.markdown("### 📊 Institution-Wide Analytics")
        
        # Advanced metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("👥 Total Students", len(data))
        with col2:
            very_high = len(data[data['Final_Risk'] == 'Very High Risk'])
            st.metric("🚨 Critical Cases", very_high)
        with col3:
            high = len(data[data['Final_Risk'] == 'High Risk'])
            st.metric("⚠️ High Risk", high)
        with col4:
            overdue_fees = len(data[data['Fee_Status'].str.lower() == 'overdue'])
            st.metric("💰 Fee Issues", overdue_fees)
        with col5:
            low_attendance = len(data[data['Attendance'] < 70])
            st.metric("📉 Poor Attendance", low_attendance)
        
        # Detailed analytics
        st.markdown("### 📈 Comprehensive Analysis")
        
        tab1, tab2, tab3 = st.tabs(["Risk Analysis", "Performance Trends", "Intervention Planning"])
        
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                # Risk by fee status
                risk_fee = pd.crosstab(data['Fee_Status'], data['Final_Risk'])
                fig_bar = px.bar(risk_fee.reset_index().melt(id_vars='Fee_Status'),
                               x='Fee_Status', y='value', color='Final_Risk',
                               title="Risk Distribution by Fee Status")
                st.plotly_chart(fig_bar, use_container_width=True)
            
            with col2:
                # Attendance vs Risk
                fig_box = px.box(data, x='Final_Risk', y='Attendance',
                               title="Attendance Distribution by Risk Level")
                st.plotly_chart(fig_box, use_container_width=True)
        
        with tab2:
            # Performance metrics
            fig_hist1 = px.histogram(data, x='Attendance', color='Final_Risk',
                                   title="Attendance Distribution", nbins=20)
            st.plotly_chart(fig_hist1, use_container_width=True)
            
            fig_hist2 = px.histogram(data, x='Test_Score', color='Final_Risk',
                                   title="Test Score Distribution", nbins=20)
            st.plotly_chart(fig_hist2, use_container_width=True)
        
        with tab3:
            st.markdown("#### 🎯 Intervention Recommendations")
            
            # Priority students
            priority = data[data['Final_Risk'] == 'Very High Risk'].sort_values('Rule_Score', ascending=False)
            
            if len(priority) > 0:
                st.markdown("**Immediate Intervention Required:**")
                for _, student in priority.head(10).iterrows():
                    st.markdown(f"""
                    <div class="dashboard-card">
                        <h4>🚨 Student ID: {student['Student_ID']}</h4>
                        <p><strong>Issues:</strong> 
                        {'Low Attendance (' + str(student['Attendance']) + '%) ' if student['Attendance'] < 70 else ''}
                        {'Poor Performance (' + str(student['Test_Score']) + ') ' if student['Test_Score'] < 50 else ''}
                        {'Fee Issues (' + student['Fee_Status'] + ')' if student['Fee_Status'].lower() != 'paid' else ''}
                        </p>
                        <p><strong>Recommended Actions:</strong> Personal counseling, academic support, financial aid review</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("🎉 No critical intervention cases at this time!")
        
        # Download complete report
        st.markdown("### 📋 Data Export")
        if st.button("📥 Download Complete Analysis Report"):
            csv = data.to_csv(index=False)
            st.download_button(
                label="💾 Download CSV Report",
                data=csv,
                file_name=f'dropsafe_analysis_{datetime.now().strftime("%Y%m%d_%H%M")}.csv',
                mime='text/csv'
            )
    else:
        st.markdown("""
        <div class="alert-warning">
            <h3>📁 Upload Required</h3>
            <p>Upload student data to access counselor analytics.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Add footer
    show_footer()

# --- MAIN APPLICATION LOGIC ---
def main():
    # Handle different pages based on current_page state
    if st.session_state.current_page == 'about':
        show_about_page()
    elif st.session_state.current_page == 'register':
        show_registration_page()
    elif st.session_state.current_page == 'login':
        show_login_page()
    elif st.session_state.current_page == 'home':
        show_role_selection()
    elif st.session_state.current_page == 'dashboard' and st.session_state.logged_in:
        # Show role-specific dashboard if logged in
        if st.session_state.selected_role == "student":
            show_student_dashboard()
        elif st.session_state.selected_role == "teacher":
            show_teacher_dashboard()
        elif st.session_state.selected_role == "counselor":
            show_counselor_dashboard()
    else:
        # Default to login page for any unhandled state
        st.session_state.current_page = 'login'
        show_login_page()

if __name__ == "__main__":
    # Initialize backend data first
    initialize_backend_data()
    main()