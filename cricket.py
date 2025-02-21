import streamlit as st
from openai import OpenAI
import pandas as pd

# Configure OpenAI API Key using Streamlit secrets
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("OpenAI API key not found. Please add it to Streamlit secrets.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="AI Cricket Coach",
    page_icon="🏏",
    layout="wide"
)

# Function to get AI response
def get_ai_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert cricket coach with deep knowledge of technique, strategy, and training."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=4000
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error getting AI response: {str(e)}")
        return None

# Title and introduction
st.title("🏏 AI Cricket Coach")
st.markdown("Your personalized path to cricket excellence")

# Initialize session state for user data
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}

# Chat Section
st.header("Chat with Your AI Coach")

user_query = st.text_area("Ask your coach anything about cricket:")

if st.button("Get Advice"):
    if user_query:
        with st.spinner("Coach is analyzing your question..."):
            # Include profile context if available
            context = ""
            if st.session_state.user_profile:
                context = f"""
                Player Context:
                - Role: {st.session_state.user_profile.get('role', 'Not specified')}
                - Experience: {st.session_state.user_profile.get('experience', 'Not specified')} years
                - Level: {st.session_state.user_profile.get('current_level', 'Not specified')}
                
                Question: {user_query}
                """
            else:
                context = user_query
            
            response = get_ai_response(context)
            if response:
                st.markdown(response)
    else:
        st.warning("Please enter your question!")

# Footer
st.markdown("---")
st.markdown("💡 Keep training, keep improving!")
