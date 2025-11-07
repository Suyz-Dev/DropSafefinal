"""
Setup script for Google Gemini API key configuration
"""

import os
import streamlit as st

def setup_gemini_api_key():
    """Setup Google Gemini API key"""
    st.title("🤖 Google Gemini API Key Setup")
    
    st.markdown("""
    ## Google Gemini Integration Setup
    
    To enable the advanced AI counseling features powered by Google Gemini, 
    you need to provide your Google API key.
    
    ### Steps to get your API key:
    1. Go to [Google AI Studio](https://aistudio.google.com/)
    2. Sign in with your Google account
    3. Create a new API key
    4. Copy the API key
    5. Paste it in the field below
    """)
    
    # Check if API key is already set
    current_key = os.getenv("GOOGLE_API_KEY", "")
    if current_key:
        st.info("✅ Google API key is already configured")
        if st.button("🔄 Reset API Key"):
            os.environ["GOOGLE_API_KEY"] = ""
            st.success("API key reset. Please enter a new one below.")
            st.rerun()
    else:
        st.warning("⚠️ Google API key is not configured")
    
    # Input for API key
    api_key = st.text_input("Enter your Google API Key:", type="password", 
                           help="Your API key will be stored securely in environment variables")
    
    if st.button("💾 Save API Key"):
        if api_key:
            os.environ["GOOGLE_API_KEY"] = api_key
            st.success("✅ API key saved successfully!")
            st.info("Restart the application to enable Gemini features")
        else:
            st.error("❌ Please enter a valid API key")

if __name__ == "__main__":
    setup_gemini_api_key()