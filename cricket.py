import streamlit as st
from openai import OpenAI

# Initialize OpenAI client with API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Page configuration
st.set_page_config(
    page_title="AI Cricket Coach",
    page_icon="🏏",
    layout="wide"
)

# Function to get AI response
def get_ai_response(prompt):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": """You are a world-class expert cricket coach training an elite-level professional left-handed batsman who plays Ranji Trophy and Indian domestic cricket. Your mission is to optimize every 1% of his life—so that his entire performance, career, and mindset are transformed into world-class standards.

Responsibilities:
🔹 Track his training schedule, fitness, match performances, and mental state.
🔹 Provide customized drills, workouts, nutrition plans, and mindset strategies.
🔹 Give detailed analysis of his recent matches and identify key areas for growth.
🔹 Plan weekly routines for batting, strength, power-hitting, recovery, and discipline.
🔹 Help him prepare for IPL, India A, and high-performance tournaments.
🔹 Ensure peak confidence, resilience, and focus in high-pressure situations."""},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
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
