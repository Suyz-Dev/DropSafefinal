"""
AI Chat Counselor System
Provides mental health support and guidance for students
"""

import streamlit as st
import random
from datetime import datetime
from shared_data import shared_data_manager

# Try to import Google Generative AI, with fallback to local responses
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None

class AIChatCounselor:
    def __init__(self):
        # Initialize Gemini if available
        self.gemini_model = None
        if GEMINI_AVAILABLE:
            try:
                # Get API key from environment variable
                import os
                api_key = os.getenv("GOOGLE_API_KEY")
                if api_key:
                    genai.configure(api_key=api_key)
                    # Initialize the model
                    self.gemini_model = genai.GenerativeModel('gemini-pro')
                else:
                    st.warning("Google API key not found. Set GOOGLE_API_KEY environment variable for Gemini integration.")
            except Exception as e:
                st.warning(f"Gemini initialization failed: {str(e)}")
                self.gemini_model = None
        
        self.counselor_responses = {
            "greeting": [
                "Hello! I'm here to listen and support you. How are you feeling today?",
                "Hi there! I'm your AI counselor. What's on your mind?",
                "Welcome! I'm here to help you work through any concerns. How can I assist you today?"
            ],
            "stress": [
                "I understand you're feeling stressed. Let's talk about what's causing this stress. Can you tell me more?",
                "Stress is very common, and you're not alone. What specific situations are making you feel this way?",
                "It's okay to feel stressed sometimes. Let's work together to find some coping strategies."
            ],
            "anxiety": [
                "Anxiety can feel overwhelming, but there are ways to manage it. Can you describe what triggers your anxiety?",
                "I hear that you're experiencing anxiety. Remember, this feeling is temporary and manageable.",
                "Let's explore some breathing techniques and grounding exercises that might help with your anxiety."
            ],
            "depression": [
                "Thank you for sharing this with me. Depression is serious, and I want you to know that help is available.",
                "You're brave for reaching out. While I can offer support, please consider speaking with a professional counselor.",
                "I'm here to listen. Remember that you matter, and there are people who care about you."
            ],
            "academic": [
                "Academic challenges are common. Let's talk about specific areas where you're struggling.",
                "It sounds like you're dealing with academic pressure. What subjects or tasks are most challenging?",
                "Academic stress is manageable with the right strategies. Let's work on a plan together."
            ],
            "positive": [
                "I'm glad to hear you're doing well! What's been going particularly good for you?",
                "That's wonderful! It's great that you're feeling positive. How can we maintain this momentum?",
                "I'm happy you're in a good place. What strategies have been helping you?"
            ],
            "crisis": [
                "I'm very concerned about what you've shared. Please reach out to a professional immediately.",
                "This sounds like a serious situation. Please contact emergency services or a crisis hotline.",
                "Your safety is the priority. Please speak with a trusted adult or counselor right away."
            ]
        }
        
        self.coping_strategies = [
            "🧘 Try deep breathing: Inhale for 4 counts, hold for 4, exhale for 4",
            "🚶 Take a short walk outside for fresh air and movement",
            "📝 Write down your thoughts and feelings in a journal",
            "🎵 Listen to calming music or sounds",
            "💭 Practice mindfulness: Focus on what you can see, hear, and feel right now",
            "🗣️ Talk to a trusted friend or family member",
            "📚 Take breaks during study sessions (try the 25-5 minute rule)",
            "😴 Ensure you're getting enough sleep (7-9 hours)",
            "🍎 Maintain a healthy diet and stay hydrated",
            "🎨 Engage in a creative activity you enjoy"
        ]
    
    def analyze_message(self, message: str) -> str:
        """Analyze student message and determine appropriate response category"""
        message_lower = message.lower()
        
        # Crisis indicators
        crisis_words = ['suicide', 'kill myself', 'end it all', 'want to die', 'hurt myself']
        if any(word in message_lower for word in crisis_words):
            return "crisis"
        
        # Depression indicators
        depression_words = ['depressed', 'hopeless', 'worthless', 'empty', 'sad all the time']
        if any(word in message_lower for word in depression_words):
            return "depression"
        
        # Anxiety indicators
        anxiety_words = ['anxious', 'panic', 'worry', 'nervous', 'scared', 'fear']
        if any(word in message_lower for word in anxiety_words):
            return "anxiety"
        
        # Stress indicators
        stress_words = ['stressed', 'overwhelmed', 'pressure', 'too much', 'can\'t cope']
        if any(word in message_lower for word in stress_words):
            return "stress"
        
        # Academic indicators
        academic_words = ['exam', 'study', 'grades', 'homework', 'assignment', 'academic']
        if any(word in message_lower for word in academic_words):
            return "academic"
        
        # Positive indicators
        positive_words = ['good', 'great', 'happy', 'fine', 'okay', 'better', 'well']
        if any(word in message_lower for word in positive_words):
            return "positive"
        
        # Default to greeting for general messages
        return "greeting"
    
    def generate_response(self, message: str, student_name: str = "Student") -> str:
        """Generate appropriate counselor response"""
        # Use Gemini if available and configured
        if self.gemini_model is not None:
            try:
                # Create a prompt for Gemini with context
                prompt = f"""
                You are a compassionate and professional student counselor AI. 
                A student named {student_name} has shared the following concern:
                
                "{message}"
                
                Please provide a supportive, empathetic, and helpful response. 
                Consider the student's emotional state and offer appropriate guidance.
                If the student is in crisis, recommend professional help.
                Keep your response concise but meaningful, around 2-3 sentences.
                """
                
                # Generate response using Gemini
                response = self.gemini_model.generate_content(prompt)
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                # Fallback to local responses if Gemini fails
                st.warning(f"Gemini response failed: {str(e)}")
        
        # Fallback to original local response generation
        category = self.analyze_message(message)
        base_response = random.choice(self.counselor_responses[category])
        
        # Add personalized touch
        if student_name != "Student":
            base_response = base_response.replace("Student", student_name)
        
        # Add coping strategy for stress/anxiety
        if category in ["stress", "anxiety"]:
            strategy = random.choice(self.coping_strategies)
            base_response += f"\n\n💡 **Helpful Strategy**: {strategy}"
        
        # Add professional help recommendation for serious issues
        if category in ["depression", "crisis"]:
            base_response += "\n\n🏥 **Important**: Please consider reaching out to a professional counselor or trusted adult for additional support."
        
        return base_response
    
    def render_chat_interface(self, student_id: str, student_name: str):
        """Render the chat interface in Streamlit with professional colors"""
        st.markdown("""
        <div style="background: linear-gradient(45deg, #8B5CF6, #7C3AED); color: white; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; text-align: center; box-shadow: 0 8px 25px rgba(139, 92, 246, 0.3);">
            <h3 style="margin: 0;">🤖 AI Chat Counselor</h3>
            <p style="margin: 0.5rem 0 0 0;">I'm here to listen and provide support 24/7</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize chat history in session state
        if f"chat_history_{student_id}" not in st.session_state:
            st.session_state[f"chat_history_{student_id}"] = []
            # Load previous chat history
            previous_chats = shared_data_manager.get_chat_history(student_id)
            for chat in previous_chats[-10:]:  # Show last 10 conversations
                st.session_state[f"chat_history_{student_id}"].append({
                    "student": chat["student_message"],
                    "counselor": chat["counselor_response"],
                    "timestamp": chat["timestamp"]
                })
        
        # Display chat history with professional styling
        chat_container = st.container()
        with chat_container:
            for chat in st.session_state[f"chat_history_{student_id}"]:
                # Student message with sky blue background
                st.markdown(f"""
                <div style="background: #EFF6FF; border-left: 4px solid #3B82F6; padding: 12px; border-radius: 8px; margin: 8px 0; text-align: right;">
                    <strong style="color: #1E40AF;">You:</strong> <span style="color: #374151;">{chat['student']}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Counselor response with purple accent
                st.markdown(f"""
                <div style="background: #F3E8FF; border-left: 4px solid #8B5CF6; padding: 12px; border-radius: 8px; margin: 8px 0;">
                    <strong style="color: #7C3AED;">🤖 Counselor:</strong> <span style="color: #374151;">{chat['counselor']}</span>
                </div>
                """, unsafe_allow_html=True)
        
        # Chat input
        with st.form(key=f"chat_form_{student_id}", clear_on_submit=True):
            user_message = st.text_area("💬 Share your thoughts, feelings, or concerns:", 
                                      placeholder="How are you feeling today? What's on your mind?",
                                      height=100)
            
            col1, col2 = st.columns([1, 4])
            with col1:
                send_button = st.form_submit_button("Send 📤", use_container_width=True)
            
            if send_button and user_message.strip():
                # Generate AI response
                counselor_response = self.generate_response(user_message, student_name)
                
                # Add to session state
                new_chat = {
                    "student": user_message,
                    "counselor": counselor_response,
                    "timestamp": datetime.now().isoformat()
                }
                st.session_state[f"chat_history_{student_id}"].append(new_chat)
                
                # Save to persistent storage
                shared_data_manager.save_chat_message(student_id, user_message, counselor_response)
                
                # Rerun to show new message
                st.rerun()
        
        # Satisfaction feedback buttons
        st.markdown("---")
        st.markdown("### 📝 Was this counseling session helpful?")
        
        # Check if feedback already exists
        existing_feedback = shared_data_manager.get_student_feedback(student_id)
        
        if existing_feedback:
            # Show existing feedback
            satisfaction = existing_feedback.get("satisfaction", "")
            if satisfaction == "satisfied":
                st.success("✅ You marked this session as helpful. Thank you for your feedback!")
            elif satisfaction == "unsatisfied":
                st.warning("⚠️ You marked this session as not helpful. We'll work to improve.")
        else:
            # Show feedback buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍 Yes, I'm satisfied", use_container_width=True, type="primary"):
                    shared_data_manager.save_counselor_feedback(student_id, student_name, "satisfied")
                    st.success("Thank you for your feedback! We're glad we could help.")
                    st.rerun()
            with col2:
                if st.button("👎 No, I'm unsatisfied", use_container_width=True):
                    shared_data_manager.save_counselor_feedback(student_id, student_name, "unsatisfied")
                    st.warning("Thank you for your feedback. We'll work to improve our support.")
                    st.rerun()
        
        # Help resources
        with st.expander("🆘 Emergency Resources & Help"):
            st.markdown("""
            **If you're in crisis or need immediate help:**
            - 🚨 Emergency: Call 102 (Ambulance) or 100 (Police)
            - 📞 National Suicide Prevention: 9152987821
            - 💬 Mental Health Helpline: 9820466726
            
            **Additional Resources:**
            - 🏥 Campus Counseling Center
            - 👥 Student Support Services
            - 📧 counseling@university.edu
            - 🌐 Online Mental Health Resources
            
            **Remember**: You're not alone, and seeking help is a sign of strength! 💪
            """)

# Global instance
ai_counselor = AIChatCounselor()