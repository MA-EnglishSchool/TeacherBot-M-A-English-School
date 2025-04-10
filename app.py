
import streamlit as st
import openai
from gtts import gTTS
import uuid
import os

openai.api_key = st.secrets["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"]

st.set_page_config(page_title="TeacherBot - M&A English School", page_icon="🗽", layout="centered")

st.markdown("""
    <div style="text-align: center;">
        <img src="assets/logo.jpg" width="300"/>
        <h1 style="color: white; font-family: Arial;">👩‍🏫 Welcome to TeacherBot</h1>
        <h3 style="color: #f0f0f0;">Your virtual English teacher from <span style="color:#FFC107;">M&A English School</span></h3>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown(
    """
    <style>
    body {
        background-color: #8B0000;
    }
    .stApp {
        background: linear-gradient(to right, #1f355e, #8B0000);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "step" not in st.session_state:
    st.session_state.step = 0
if "name" not in st.session_state:
    st.session_state.name = ""
if "age" not in st.session_state:
    st.session_state.age = ""
if "level" not in st.session_state:
    st.session_state.level = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

def falar(texto):
    tts = gTTS(text=texto, lang='en')
    filename = f"{uuid.uuid4()}.mp3"
    tts.save(filename)
    st.audio(filename, format="audio/mp3", autoplay=True)
    return filename

if st.session_state.step == 0:
    st.session_state.name = st.text_input("👋 What’s your name?")
    if st.session_state.name:
        st.session_state.step = 1

if st.session_state.step == 1:
    st.session_state.age = st.text_input(f"Nice to meet you, {st.session_state.name}! How old are you?")
    if st.session_state.age:
        st.session_state.step = 2

if st.session_state.step == 2:
    st.session_state.level = st.selectbox("What’s your English level?", ["Choose...", "A1", "A2", "B1", "B2"])
    if st.session_state.level != "Choose...":
        st.session_state.step = 3
        st.session_state.messages.append({
            "role": "system",
            "content": f"You are a friendly English teacher. The student is {st.session_state.name}, {st.session_state.age} years old, level {st.session_state.level}. Help them in a kind, simple and encouraging way."
        })
        falar(f"Welcome, {st.session_state.name}! Let's learn English together!")

if st.session_state.step == 3:
    st.subheader("❓ Ask your English question below!")
    user_input = st.text_input("✍️ Type here:")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        resposta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=st.session_state.messages
        )
        bot_reply = resposta["choices"][0]["message"]["content"]
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

        st.markdown(f"**👩‍🏫 TeacherBot:** {bot_reply}")
        falar(bot_reply)
