import streamlit as st
import json, os
import asyncio
import edge_tts
import uuid
import datetime as dt

todayDate = dt.date.today()
oneDayAgo = todayDate - dt.timedelta(days=1)
TwoDaysAgo = todayDate - dt.timedelta(days=2)
todayDate = todayDate.strftime("%Y-%m-%d")
oneDayAgo = oneDayAgo.strftime("%Y-%m-%d")
TwoDaysAgo = TwoDaysAgo.strftime("%Y-%m-%d")

if not os.path.exists(todayDate):
    os.makedirs(todayDate)
os.system(f"rm -rf *.mp3")
if os.path.exists(oneDayAgo):
    os.system(f"rm -rf {oneDayAgo}")
if os.path.exists(TwoDaysAgo):
    os.system(f"rm -rf {TwoDaysAgo}")

st.set_page_config(
    page_title="Text to Speech (by Bing)",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://tts.hiblazar.com/help',
        'Report a bug': "https://tts.hiblazar.com/bug",
        'About': "# This is a header. This is Text to Speech!"
    }
)
st.title('Text to Speech (by Bing) v1.1')
# st.write (todayDate, yesterdayDate)
async def amain(text, VOICE, fileName) -> None:
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(f"{fileName}")

MAX_CHARS = 5000
parameters = st._get_query_params()

if parameters:
    if parameters.get('id')[0] == "vicgupta":
        MAX_CHARS = 100000

form = st.form(key='my_form')
with form:
    text = form.text_area(f'Enter Text (max {MAX_CHARS})', max_chars=MAX_CHARS)
    voices = [
        "en-US-AndrewNeural",
        "en-US-AriaNeural",
        "en-US-AvaNeural",
        "en-US-BrianNeural",
        "en-US-ChristopherNeural",
        "en-US-EmmaNeural",
        "en-US-EricNeural"
    ]

    selected_voice = form.selectbox('Select Voice', voices)
    submit_button = form.form_submit_button(label='Submit')

if submit_button:
    fileName = f"{todayDate}/" + str(uuid.uuid4()) + ".mp3"
    asyncio.run(amain(text, selected_voice, fileName))
    audio_file = open(fileName, "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")
    st.download_button(
        label="Download MP3",
        data=audio_bytes,
        file_name="output.mp3",
        mime="audio/mp3",
    )
