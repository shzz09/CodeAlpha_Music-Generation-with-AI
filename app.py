
import streamlit as st
import subprocess
import os
import sys
from pathlib import Path

# ---------------- PATHS ----------------

BASE_DIR = Path(__file__).resolve().parent

MIDI_FILE = BASE_DIR / "generated_music.mid"
WAV_FILE = BASE_DIR / "generated_music.wav"

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="MelodyAI Studio",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- SESSION STATE ----------------

if "music_ready" not in st.session_state:
    st.session_state.music_ready = False

if "track_length" not in st.session_state:
    st.session_state.track_length = "Medium"

if "track_creativity" not in st.session_state:
    st.session_state.track_creativity = 1.0

if "generation_count" not in st.session_state:
    st.session_state.generation_count = 0

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

.stApp {
    background: #0d0d12;
    color: #f5f3ff;
    font-family: 'DM Sans', sans-serif;
}

header, footer {
    visibility: hidden;
}

.block-container {
    max-width: 1150px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

.brand {
    font-family: 'Space Grotesk';
    font-size: 26px;
    font-weight: 700;
    color: #ffffff;
}

.brand span {
    color: #a78bfa;
}

.nav {
    text-align: right;
    color: #aaa6ba;
    font-size: 13px;
    letter-spacing: 1px;
    padding-top: 10px;
}

.hero {
    padding: 75px 0 35px;
}

.eyebrow {
    color: #a78bfa;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 3px;
}

.hero h1 {
    font-family: 'Space Grotesk';
    font-size: 54px;
    line-height: 1.12;
    font-weight: 700;
    color: #ffffff;
    margin: 15px 0;
}

.hero h1 span {
    color: #a78bfa;
}

.hero p {
    color: #9995a8;
    font-size: 16px;
}

.panel {
    background: #171720;
    border: 1px solid #292738;
    border-radius: 18px;
    padding: 26px;
}

.panel-title {
    font-family: 'Space Grotesk';
    font-size: 21px;
    font-weight: 600;
    color: #ffffff;
}

.muted {
    color: #9995a8;
    font-size: 13px;
}

.stButton > button {
    background: linear-gradient(100deg, #8b5cf6, #a78bfa);
    color: white;
    border: none;
    border-radius: 10px;
    height: 50px;
    font-weight: 700;
    font-size: 15px;
    width: 100%;
}

.stButton > button:hover {
    background: #7c3aed;
    color: white;
    border: none;
}

.stDownloadButton > button {
    background: #242333;
    color: #e9e4ff;
    border: 1px solid #39354c;
    border-radius: 9px;
    width: 100%;
}

.stDownloadButton > button:hover {
    background: #302b45;
    color: white;
    border-color: #8b5cf6;
}

.track {
    background: #171720;
    border: 1px solid #292738;
    padding: 20px;
    border-radius: 14px;
    margin-top: 15px;
}

.track-name {
    color: white;
    font-weight: 600;
    font-size: 16px;
}

.track-sub {
    color: #9995a8;
    font-size: 12px;
    margin-top: 5px;
}

.divider {
    border-top: 1px solid #292738;
    margin: 35px 0;
}

.stAudio {
    width: 100%;
}

.stSlider, .stSelectbox {
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

header1, header2 = st.columns([1, 1])

with header1:
    st.markdown(
        '<div class="brand">♪ Melody<span>AI</span></div>',
        unsafe_allow_html=True
    )

with header2:
    st.markdown(
        '<div class="nav">MUSIC STUDIO &nbsp; • &nbsp; CREATE</div>',
        unsafe_allow_html=True
    )

# ---------------- HERO ----------------

st.markdown("""
<div class="hero">
    <div class="eyebrow">YOUR PERSONAL MUSIC STUDIO</div>
    <h1>Turn your ideas<br>into <span>music.</span></h1>
    <p>Create original melodies with the power of AI.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- WORKSPACE ----------------

left, right = st.columns([0.85, 1.15], gap="large")

with left:

    st.markdown("""
    <div class="panel">
        <div class="panel-title">Create a new track</div>
        <div class="muted">Customize your music generation.</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    length_label = st.selectbox(
        "TRACK LENGTH",
        ["Short", "Medium", "Long", "Extended"]
    )

    length_map = {
        "Short": 150,
        "Medium": 300,
        "Long": 450,
        "Extended": 600
    }

    creativity = st.slider(
        "CREATIVITY",
        min_value=0.5,
        max_value=1.5,
        value=1.0,
        step=0.1
    )

    st.caption(
        "Higher creativity allows more variation in generated notes."
    )

    generate = st.button(
        "✦  Generate Music",
        use_container_width=True
    )

with right:

    st.markdown("""
    <div class="panel">
        <div class="panel-title">Music workspace</div>
        <div class="muted">Your generated music will appear here.</div>
        <br>
        <div style="height:130px;display:flex;align-items:center;
        justify-content:center;gap:7px;">
    """ + "".join(
        f'<div style="width:5px;height:{height}px;'
        'background:#8b5cf6;border-radius:8px;opacity:0.85;"></div>'
        for height in [
            25, 48, 75, 40, 95, 60, 115, 50, 80, 35, 105,
            65, 90, 45, 120, 55, 85, 30, 70, 100, 45, 80, 35
        ]
    ) + """
        </div>
        <div style="text-align:center;color:#9995a8;font-size:12px;">
            A new melody is waiting to be created
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- GENERATION ----------------

if generate:

    st.session_state.music_ready = False

    with st.spinner("Creating your music... Please wait."):

        env = os.environ.copy()

        env["MELODYAI_GENERATE_NOTES"] = str(
            length_map[length_label]
        )

        env["MELODYAI_TEMPERATURE"] = str(creativity)

        result = subprocess.run(
            [sys.executable, str(BASE_DIR / "generate.py")],
            cwd=BASE_DIR,
            env=env,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:

            st.error("Music generation failed.")

            st.code(result.stderr[-3000:])

        else:

            conversion = subprocess.run(
                [sys.executable, str(BASE_DIR / "convert_audio.py")],
                cwd=BASE_DIR,
                capture_output=True,
                text=True
            )

            if conversion.returncode != 0:

                st.error("Audio conversion failed.")

                st.code(conversion.stderr[-3000:])

            elif MIDI_FILE.exists() and WAV_FILE.exists():

                st.session_state.music_ready = True
                st.session_state.track_length = length_label
                st.session_state.track_creativity = creativity
                st.session_state.generation_count += 1

                st.success("Your music has been created!")

            else:

                st.error("Output files were not created. Check your scripts.")

# ---------------- GENERATED MUSIC ----------------

if st.session_state.music_ready:

    st.markdown(
        '<div class="divider"></div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="eyebrow">YOUR LATEST CREATION</div>
    <h2 style="font-family:'Space Grotesk';color:white;">
        Your music is ready.
    </h2>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="track">
        <div class="track-name">
            ♫ &nbsp; MelodyAI — Generated Track
        </div>
        <div class="track-sub">
            AI-generated piano melody
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.audio(
        str(WAV_FILE),
        format="audio/wav"
    )

    st.caption(
        f"Length: {st.session_state.track_length} "
        f"· Creativity: {st.session_state.track_creativity}"
    )

    download1, download2 = st.columns(2)

    with download1:

        with open(WAV_FILE, "rb") as file:

            st.download_button(
                "↓  Download WAV",
                data=file,
                file_name="MelodyAI_Track.wav",
                mime="audio/wav",
                use_container_width=True
            )

    with download2:

        with open(MIDI_FILE, "rb") as file:

            st.download_button(
                "↓  Download MIDI",
                data=file,
                file_name="MelodyAI_Track.mid",
                mime="audio/midi",
                use_container_width=True
            )

# ---------------- FOOTER ----------------

st.markdown(
    '<div class="divider"></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div style="text-align:center;color:#777386;font-size:12px;">'
    'MelodyAI Studio · Create something beautiful.'
    '</div>',
    unsafe_allow_html=True
)
