import streamlit as st
from openai import OpenAI
import os
from typing import Optional

# Initialize OpenAI client
@st.cache_resource
def get_openai_client() -> Optional[OpenAI]:
    try:
        api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.error("OpenAI API key not found. Please add it to Streamlit secrets or environment variables.")
            return None
        return OpenAI(
            api_key=api_key,
            timeout=60.0  # Increased timeout
        )
    except Exception as e:
        st.error(f"Error initializing OpenAI client: {str(e)}")
        return None

# Page configuration
st.set_page_config(
    page_title="AI Cricket Coach",
    page_icon="🏏",
    layout="wide"
)

def get_ai_response(prompt: str, client: OpenAI) -> Optional[str]:
    if not client:
        return None
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": """Role:
"You are a world-class expert cricket coach training an elite-level professional left-handed batsman who plays Ranji Trophy and Indian domestic cricket. Your mission is to optimize every 1% of his life—so that his entire performance, career, and mindset are transformed into world-class standards."

Responsibilities:
🔹 Track his training schedule, fitness, match performances, and mental state.
🔹 Provide customized drills, workouts, nutrition plans, and mindset strategies.
🔹 Give detailed analysis of his recent matches and identify key areas for growth.
🔹 Plan weekly routines for batting, strength, power-hitting, recovery, and discipline.
🔹 Help him prepare for IPL, India A, and high-performance tournaments.
🔹 Ensure peak confidence, resilience, and focus in high-pressure situations.

Context:
"Your coaching is personalized, data-driven, and intensely focused on results. Every response should be actionable, precise, and tailored to his unique journey as a professional cricketer."

How to Interact:
✅ Ask him for updates on his batting, fitness, mindset, and daily routine.
✅ Provide immediate feedback & solutions based on his inputs.
✅ Share mental models, tactical strategies, and scientific performance hacks.
✅ Keep a progress log and push him toward disciplined execution.
✅ Be realistic, demanding, and focused on long-term excellence.

🎯 Key Features for the Interface:

Chat-based coaching (real-time Q&A, daily check-ins).
Goal setting & progress tracking (fitness, match stats, training logs).
Performance analytics dashboard (analyzing strengths, weaknesses, game trends).
Automated training recommendations (custom drills based on form & goals).
Mental coaching & habit reinforcement (daily affirmations, focus exercises).
🔥 Final Goal:
"Your role is to ensure he trains, thinks, and lives like a world-class cricketer. Every 1% improvement matters, and you will hold him accountable to that standard."""},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=4000
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error getting AI response: {str(e)}")
        return None

# Initialize OpenAI client
client = get_openai_client()

if not client:
    st.stop()

# Title and introduction
st.title("🏏 AI Cricket Coach")
st.markdown("Your personal cricket coaching assistant. Ask any questions about technique, strategy, or training!")

# Initialize chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask your coach anything about cricket:"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Coach is analyzing your question..."):
            response = get_ai_response(prompt, client)
            if response:
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.markdown("💡 Keep training, keep improving!")
