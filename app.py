# career_planner_app.py

import streamlit as st
from streamlit_option_menu import option_menu
import pycountry
import os
from dotenv import load_dotenv
import google.generativeai as genai
import pdfkit
from tempfile import NamedTemporaryFile



# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in your .env file.")

# Configure Gemini
genai.configure(api_key=gemini_api_key)

# Initialize page list and session state
page_list = [
    "Welcome",
    "RIASEC Quiz",
    "Academics & Aptitude",
    "Personality & Preferences",
    "Location"
]

if "page_index" not in st.session_state:
    st.session_state.page_index = 0
if "user_inputs" not in st.session_state:
    st.session_state.user_inputs = {}

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title="Career Planner Menu",
        options=page_list,
        icons=["house", "grid", "book", "person", "globe"],
        menu_icon="cast",
        default_index=st.session_state.page_index
    )
    st.session_state.page_index = page_list.index(selected)

# Navigation Buttons
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.session_state.page_index > 0:
        if st.button("⬅️ Previous"):
            st.session_state.page_index -= 1
with col2:
    if st.button("🏠 Home"):
        st.session_state.page_index = 0
with col3:
    if st.session_state.page_index < len(page_list) - 1:
        if st.button("Next ➡️"):
            st.session_state.page_index += 1

selected = page_list[st.session_state.page_index]

# --- Page: Welcome ---
if selected == "Welcome":
    st.title("🎯 AI Career Planner")
    st.markdown("""
    Welcome to the **AI Career Planner**!

    🎓 Designed for students in **Grade 9 and above**, this tool uses AI to guide your career exploration
    based on interests, strengths, preferences, and goals.

    👉 Click **Next** to begin!
    """)

    st.session_state.name = st.text_input("What's your name?", value=st.session_state.get("name", ""))
    st.session_state.grade = st.selectbox("Your current grade/level:",
        ["9th", "10th", "11th", "12th", "Graduate", "Other"], index=0)
    st.session_state.goal_clarity = st.radio("How clear are your career goals?",
        ["Very clear", "Somewhat clear", "Not clear at all"])

    st.session_state.user_inputs.update({
        "name": st.session_state.name,
        "grade": st.session_state.grade,
        "goal_clarity": st.session_state.goal_clarity
    })

# --- Page: RIASEC Quiz ---
elif selected == "RIASEC Quiz":
    st.title("🧠 RIASEC Quick Quiz")

    st.session_state.fav_subjects = st.multiselect("Which subjects do you enjoy most?", [
        "Math", "Science", "Art", "Music", "Drama", "Business", "Economics", 
        "Biology", "Psychology", "Engineering", "Robotics", "Accounting", "CS Theory"
    ], default=st.session_state.get("fav_subjects", []))

    st.session_state.work_style = st.radio("Which work style do you prefer most?", [
        "Working alone on analysis", "Building or fixing things", "Helping or teaching people",
        "Leading projects or selling", "Designing or expressing ideas", "Organizing data or routines"
    ], index=0)

    st.session_state.interest_clusters = st.multiselect("Which areas interest you?", [
        "🧪 Science & Research", "🛠️ Engineering / Mechanics", "🎭 Arts / Design / Creativity",
        "🧑‍🏫 Education / Healthcare", "💼 Business / Marketing", "🗂️ Data / Finance / Admin"
    ], default=st.session_state.get("interest_clusters", []))

    st.session_state.user_inputs.update({
        "fav_subjects": st.session_state.fav_subjects,
        "work_style": st.session_state.work_style,
        "interest_clusters": st.session_state.interest_clusters
    })

# --- Page: Academics & Aptitude ---
elif selected == "Academics & Aptitude":
    st.title("📘 Academics & Aptitude")

    st.session_state.strong_subjects = st.multiselect("Subjects you're good at:", 
        ["Math", "Biology", "Physics", "Chemistry", "English", "CS"], 
        default=st.session_state.get("strong_subjects", []))
    
    st.session_state.math_score = st.slider("Math Score", 0, 100, 75)
    st.session_state.science_score = st.slider("Science Score", 0, 100, 75)
    st.session_state.language_score = st.slider("Language Score", 0, 100, 75)

    st.session_state.logic = st.slider("Logical Reasoning", 1, 5, 3)
    st.session_state.spatial = st.slider("Spatial Skills", 1, 5, 3)
    st.session_state.verbal = st.slider("Verbal Skills", 1, 5, 3)
    st.session_state.creativity = st.slider("Creativity", 1, 5, 3)
    st.session_state.memory = st.slider("Memory", 1, 5, 3)

    st.session_state.user_inputs.update({
        "strong_subjects": st.session_state.strong_subjects,
        "scores": {
            "Math": st.session_state.math_score,
            "Science": st.session_state.science_score,
            "Language": st.session_state.language_score
        },
        "aptitudes": {
            "Logic": st.session_state.logic,
            "Spatial": st.session_state.spatial,
            "Verbal": st.session_state.verbal,
            "Creativity": st.session_state.creativity,
            "Memory": st.session_state.memory
        }
    })

# --- Page: Personality & Preferences ---
elif selected == "Personality & Preferences":
    st.title("🧍 Personality & Preferences")

    st.session_state.work_env = st.radio("Do you enjoy working:", ["With people", "Alone", "With ideas", "With tools"])
    st.session_state.thinking = st.radio("Are you more of a:", ["Creative thinker", "Practical executor"])
    st.session_state.structure = st.radio("Do you prefer:", ["Structured routines", "Freedom to explore"])
    st.session_state.priorities = st.multiselect("Important lifestyle factors:", 
        ["High income", "Flexibility", "Travel opportunities", "Job security"], 
        default=st.session_state.get("priorities", []))
    st.session_state.long_study = st.radio("Are you okay with long study durations (like medicine)?", ["Yes", "No"])

    st.session_state.user_inputs.update({
        "work_env": st.session_state.work_env,
        "thinking": st.session_state.thinking,
        "structure": st.session_state.structure,
        "priorities": st.session_state.priorities,
        "long_study": st.session_state.long_study
    })

# --- Page: Location ---
elif selected == "Location":
    st.title("🌍 Location & Language Preferences")

    countries = sorted([country.name for country in pycountry.countries])
    countries.append("Remote")

    st.session_state.study_location = st.selectbox("Preferred study/work location:", countries, index=countries.index("Remote"))

    languages = sorted({lang.name for lang in pycountry.languages if hasattr(lang, 'name')})
    if "Other" not in languages:
        languages.append("Other")

    st.session_state.lang_comfort = st.multiselect("Language comfort:", languages, default=st.session_state.get("lang_comfort", []))

    st.session_state.user_inputs.update({
        "study_location": st.session_state.study_location,
        "lang_comfort": st.session_state.lang_comfort
    })

    st.success("🎓 You've completed all sections! Click below to generate AI-based career suggestions.")

    if st.button("🔍 Generate AI Career Suggestions"):
        with st.spinner("Analyzing your profile..."):
            try:
                prompt = (
                     
                "You are an expert career counselor AI. Based on the following user's data, suggest 3-5 ideal careers. "
                "For each career:\n"
                "- Provide a short explanation why it's a good fit.\n"
                "- Suggest a few specific steps (courses, extracurriculars, degrees, certifications) the user can take "
                "to reach that career goal.\n\n"
                f"User Data:\n{st.session_state.user_inputs}"
            )
                

                model = genai.GenerativeModel('gemini-2.0-flash-001')
                response = model.generate_content(prompt)

                st.markdown("### 🎓 AI-Powered Career Suggestions:")
                st.markdown(response.text)
               
            except Exception as e:
                st.error(f"Something went wrong: {e}")
