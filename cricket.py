import streamlit as st
import openai
import pandas as pd

# Configure OpenAI API Key using Streamlit secrets
if "OPENAI_API_KEY" in st.secrets:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
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
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
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

# Title and introduction
st.title("🏏 AI Cricket Coach")
st.markdown("Your personalized path to cricket excellence")

# Initialize session state for user data
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}

# Sidebar for navigation
page = st.sidebar.selectbox(
    "Choose a section",
    ["Profile", "Training Plan", "AI Coach Chat"]
)

# Profile Section
if page == "Profile":
    st.header("Player Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Name", st.session_state.user_profile.get("name", ""))
        age = st.number_input("Age", 12, 50, st.session_state.user_profile.get("age", 18))
        role = st.selectbox(
            "Primary Role",
            ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"],
            index=["Batsman", "Bowler", "All-rounder", "Wicket-keeper"].index(
                st.session_state.user_profile.get("role", "Batsman")
            )
        )
    
    with col2:
        experience = st.slider(
            "Years of Experience",
            0, 20,
            st.session_state.user_profile.get("experience", 5)
        )
        current_level = st.selectbox(
            "Current Playing Level",
            ["School", "Club", "District", "State U19", "State Senior", "IPL", "International"],
            index=["School", "Club", "District", "State U19", "State Senior", "IPL", "International"].index(
                st.session_state.user_profile.get("current_level", "Club")
            )
        )
    
    if st.button("Save Profile"):
        st.session_state.user_profile = {
            "name": name,
            "age": age,
            "role": role,
            "experience": experience,
            "current_level": current_level
        }
        st.success("Profile saved successfully!")

# Training Plan Section
elif page == "Training Plan":
    st.header("Training Plan Generator")
    
    if st.session_state.user_profile:
        st.write(f"Creating plan for: {st.session_state.user_profile.get('name', 'Player')}")
        
        focus_areas = st.multiselect(
            "Select focus areas:",
            ["Batting Technique", "Power Hitting", "Bowling Variations", "Fielding", "Fitness", "Mental Strength"],
            default=["Batting Technique", "Fitness"]
        )
        
        duration = st.selectbox("Plan duration:", ["1 week", "2 weeks", "1 month"])
        
        if st.button("Generate Plan"):
            with st.spinner("Creating your personalized training plan..."):
                prompt = f"""
                Create a detailed cricket training plan for:
                Player: {st.session_state.user_profile.get('name')}
                Role: {st.session_state.user_profile.get('role')}
                Experience: {st.session_state.user_profile.get('experience')} years
                Level: {st.session_state.user_profile.get('current_level')}
                Focus Areas: {', '.join(focus_areas)}
                Duration: {duration}
                
                Include specific drills, exercises, and progression metrics.
                """
                
                plan = get_ai_response(prompt)
                if plan:
                    st.markdown(plan)
    else:
        st.warning("Please complete your profile first!")

# AI Coach Chat Section
elif page == "AI Coach Chat":
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
                    - Role: {st.session_state.user_profile.get('role')}
                    - Experience: {st.session_state.user_profile.get('experience')} years
                    - Level: {st.session_state.user_profile.get('current_level')}
                    
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
