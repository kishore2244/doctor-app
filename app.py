import streamlit as st
import datetime
import json
import os
import base64

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="VitalEase ✨",
    page_icon="✨",
    layout="centered"
)

# ----------------------------
# BACKGROUND IMAGE
# Put bg1.jpg inside same folder
# ----------------------------
def get_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_base64("bg1.jpg")

# ----------------------------
# PREMIUM CSS
# ----------------------------
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{img}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.45);
        z-index: -1;
    }}

    h1,h2,h3,p,label,div {{
        color: white !important;
    }}

    .block-container {{
        background: rgba(255,255,255,0.08);
        padding: 2rem;
        border-radius: 24px;
        backdrop-filter: blur(10px);
    }}

    .stTextInput input {{
    background: rgba(0,0,0,0.45) !important;
    color: white !important;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.25);
    padding: 12px;
    font-size: 18px;
}

.stTextInput input::placeholder {{
    color: rgba(255,255,255,0.75) !important;
}}

    .stButton > button {{
        width: 100%;
        background: linear-gradient(90deg,#2563eb,#9333ea);
        color: white;
        border: none;
        border-radius: 14px;
        padding: 12px;
        font-size: 18px;
        font-weight: bold;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# FILE STORAGE
# ----------------------------
FILE_NAME = "memory.json"

def load_memory():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return {"history": []}

def save_memory(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file)

memory = load_memory()

# ----------------------------
# HEADER
# ----------------------------
st.markdown("<h1 style='text-align:center;'>👩‍⚕️ Miss Busy Doctor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>A calm companion for hectic days 😊</p>", unsafe_allow_html=True)

# ----------------------------
# INPUTS
# ----------------------------
nickname = st.text_input("Nickname 👀", "Stare Specialist 👀")

# ----------------------------
# EMOJI MOOD SELECTOR
# ----------------------------
if "mood" not in st.session_state:
    st.session_state.mood = "Normal 😌"

st.write("### Select Today's Mood")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("😊"):
        st.session_state.mood = "Normal 😊"
    if st.button("😴"):
        st.session_state.mood = "Tired 😴"
    if st.button("😵"):
        st.session_state.mood = "Stressed 😵"

with col2:
    if st.button("😄"):
        st.session_state.mood = "Happy 😄"
    if st.button("🏃"):
        st.session_state.mood = "Busy 🏃"
    if st.button("🥱"):
        st.session_state.mood = "Sleepy 🥱"

with col3:
    if st.button("🌙"):
        st.session_state.mood = "Night Duty 🌙"
    if st.button("🔥"):
        st.session_state.mood = "Roast Mode 🔥"
    if st.button("🌿"):
        st.session_state.mood = "Calm 🌿"

mood = st.session_state.mood

st.write("Selected Mood:", mood)

# ----------------------------
# ENERGY
# ----------------------------
energy = st.slider("Energy Level", 1, 10, 5)

# ----------------------------
# ANALYZE BUTTON
# ----------------------------
if st.button("Analyze Me ✨"):

    st.subheader(f"Smart Report for {nickname}")

    hour = datetime.datetime.now().hour

    if hour < 12:
        st.info("🌅 Morning mode: probably working already.")
    elif hour < 17:
        st.info("☀️ Afternoon mode: lunch skip chance high 😏")
    elif hour < 22:
        st.info("🌆 Evening mode: reply chance increased 😎")
    else:
        st.info("🌙 Night mode: duty or sleep active.")

    if mood == "Tired 😴":
        st.warning("Need food + nap immediately 😴")

    elif mood == "Happy 😄":
        st.success("Hehe mode activated 😂")

    elif mood == "Busy 🏃":
        st.info("Doctor mode ON 👩‍⚕️")

    elif mood == "Stressed 😵":
        st.error("Take break + hydrate 😌")

    elif mood == "Sleepy 🥱":
        st.warning("Power nap needed 😴")

    elif mood == "Night Duty 🌙":
        st.info("Survival mode active 🌙")

    elif mood == "Roast Mode 🔥":
        st.warning("Sarcasm mode ON 😂")

    elif mood == "Calm 🌿":
        st.success("Peace mode detected ✨")

    else:
        st.write("Stable mood 😌")

    if energy <= 3:
        st.write("🔋 Battery low.")
    elif energy >= 8:
        st.write("⚡ Super energy mode.")
    else:
        st.write("🔆 Balanced energy.")

    st.write("Reminder: Keep hydrated + smile 😊")

    entry = {
        "date": str(datetime.datetime.now())[:16],
        "mood": mood,
        "energy": energy
    }

    memory["history"].append(entry)
    save_memory(memory)

    

# ----------------------------
# DASHBOARD
# ----------------------------
st.subheader("📊 Dashboard")
if st.button("🗑️ Clear History"):
    memory["history"] = []
    save_memory(memory)
    st.success("History Cleared 😎")
    st.rerun()

history = memory["history"]

if len(history) > 0:
    st.write("Total Visits:", len(history))

    avg_energy = sum(item["energy"] for item in history) / len(history)
    st.write("Average Energy:", round(avg_energy, 1))

    mood_count = {}

    for item in history:
        mood_count[item["mood"]] = mood_count.get(item["mood"], 0) + 1

    common_mood = max(mood_count, key=mood_count.get)

    st.write("Most Common Mood:", common_mood)

    energy_values = [item["energy"] for item in history]
    st.line_chart(energy_values)

else:
    st.info("No history yet. Click Analyze Me ✨")
