import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import math

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SoundSelf",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,400;0,500;1,400&display=swap');
html, body, [class*="css"] { font-family: 'DM Mono', monospace; }
.main-title { font-size: 2rem; font-weight: 500; letter-spacing: -0.03em; margin-bottom: 0; }
.tagline { color: #888; font-size: 0.85rem; margin-bottom: 1.5rem; }
.track-comment { font-style: italic; font-size: 0.8rem; color: #888; }
.section-header { font-size: 0.7rem; text-transform: uppercase;
                  letter-spacing: 0.1em; color: #999; margin: 1rem 0 0.5rem; }
.insight-box { background: #1a1a2e; border-left: 3px solid #5DCAA5;
               padding: 0.8rem 1rem; border-radius: 4px; margin: 0.5rem 0;
               font-size: 0.85rem; line-height: 1.6; }
.insight-label { font-size: 0.65rem; text-transform: uppercase;
                 letter-spacing: 0.12em; color: #5DCAA5; margin-bottom: 0.3rem; }
.persona-card { background: #16213e; border: 1px solid #AFA9EC44;
                border-radius: 8px; padding: 1rem 1.2rem; margin: 0.4rem 0; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SAMPLE DATA — 30 tracks across diverse genres, languages, decades
# ══════════════════════════════════════════════════════════════════════════════
SAMPLE_TRACKS = [
    # ── J-Pop / Alt-rock (Japanese) ──────────────────────────────────────────
    {"title": "Kaiju", "artist": "Sakanaction", "genre": "Alt-rock", "bpm": 180,
     "mood": "deep focus", "year": 2025, "language": "Japanese",
     "comment": "Knowledge itself is the monster — it devours you before you can name it."},
    {"title": "Anytime Anywhere", "artist": "milet", "genre": "Pop Ballad", "bpm": 109,
     "mood": "nostalgia", "year": 2023, "language": "Japanese",
     "comment": "The ending of Frieren feels like grief and warmth arriving at the same moment."},
    {"title": "Kawaii Dake Ja Dame Desu Ka", "artist": "CUTIE STREET", "genre": "J-Pop", "bpm": 118,
     "mood": "morning ritual", "year": 2024, "language": "Japanese",
     "comment": "Cuteness is not weakness. This song knows that better than most."},
    {"title": "Idol", "artist": "YOASOBI", "genre": "J-Pop", "bpm": 180,
     "mood": "peak hour", "year": 2023, "language": "Japanese",
     "comment": "180 BPM of pure narrative momentum. The anime tie-in does not explain why it hits this hard."},
    {"title": "Yoru ni Kakeru", "artist": "YOASOBI", "genre": "J-Pop", "bpm": 132,
     "mood": "late-night drive", "year": 2019, "language": "Japanese",
     "comment": "A love story told at sprint pace. Tragedy wrapped in velocity."},
    {"title": "Gyakkō", "artist": "Ado", "genre": "J-Pop", "bpm": 145,
     "mood": "deep focus", "year": 2022, "language": "Japanese",
     "comment": "Her voice treats every song like it is the last one she will ever sing."},
    {"title": "Shikabane Odori", "artist": "Ado", "genre": "J-Pop", "bpm": 158,
     "mood": "peak hour", "year": 2022, "language": "Japanese",
     "comment": "Chaos as choreography. The whole album is a controlled explosion."},
    {"title": "TAIDADA", "artist": "ZUTOMAYO", "genre": "Alt-rock", "bpm": 172,
     "mood": "deep focus", "year": 2025, "language": "Japanese",
     "comment": "ZUTOMAYO keeps writing songs that feel like they are about something you cannot quite say."},
    {"title": "Yoru no Odoriko", "artist": "Sakanaction", "genre": "Alt-rock", "bpm": 128,
     "mood": "late-night drive", "year": 2013, "language": "Japanese",
     "comment": "Post-midnight Tokyo in sound form. Loneliness as aesthetics."},
    # ── K-Pop / Korean ───────────────────────────────────────────────────────
    {"title": "Don't Say You Love Me", "artist": "Jin", "genre": "Pop Ballad", "bpm": 85,
     "mood": "rainy day", "year": 2025, "language": "Korean",
     "comment": "Holding back the words makes every syllable heavier. Restraint as emotion."},
    {"title": "Lemon", "artist": "Kenshi Yonezu", "genre": "Pop Ballad", "bpm": 96,
     "mood": "rainy day", "year": 2018, "language": "Japanese",
     "comment": "Grief does not always announce itself. Sometimes it hides in a piano intro."},
    {"title": "Dynamite", "artist": "BTS", "genre": "Dance-pop", "bpm": 114,
     "mood": "morning ritual", "year": 2020, "language": "English",
     "comment": "Pure uncut dopamine. Sometimes that is exactly what you need and nothing more."},
    {"title": "Cupid", "artist": "FIFTY FIFTY", "genre": "K-Pop", "bpm": 107,
     "mood": "morning ritual", "year": 2023, "language": "Korean",
     "comment": "Deceptively simple. The hook rewires your brain in under 30 seconds."},
    {"title": "JANE DOE", "artist": "Kenshi Yonezu", "genre": "Pop Ballad", "bpm": 88,
     "mood": "rainy day", "year": 2026, "language": "Japanese",
     "comment": "The mystery is structural — Yonezu writes around the subject, never at it."},
    # ── Western Pop / Dance ──────────────────────────────────────────────────
    {"title": "Abracadabra", "artist": "Lady Gaga", "genre": "Dance-pop", "bpm": 126,
     "mood": "peak hour", "year": 2025, "language": "English",
     "comment": "Finding magic inside chaos — that is the whole point of pop music done right."},
    {"title": "Espresso", "artist": "Sabrina Carpenter", "genre": "Dance-pop", "bpm": 104,
     "mood": "morning ritual", "year": 2024, "language": "English",
     "comment": "Confidence as a complete aesthetic. Nothing wasted, nothing apologized for."},
    {"title": "Blinding Lights", "artist": "The Weeknd", "genre": "Synthpop", "bpm": 171,
     "mood": "late-night drive", "year": 2019, "language": "English",
     "comment": "Driving at 2am in a city that does not know your name. This is that song."},
    {"title": "As It Was", "artist": "Harry Styles", "genre": "Indie-pop", "bpm": 174,
     "mood": "morning ritual", "year": 2022, "language": "English",
     "comment": "Sadness dressed up as a good time. The dissonance is the whole point."},
    {"title": "Flowers", "artist": "Miley Cyrus", "genre": "Pop", "bpm": 118,
     "mood": "morning ritual", "year": 2023, "language": "English",
     "comment": "Self-sufficiency as a radical act. The production underlines every word."},
    {"title": "Levitating", "artist": "Dua Lipa", "genre": "Dance-pop", "bpm": 103,
     "mood": "peak hour", "year": 2020, "language": "English",
     "comment": "Disco revival done with actual conviction, not just nostalgia."},
    # ── Alternative / Indie ──────────────────────────────────────────────────
    {"title": "Anti-Hero", "artist": "Taylor Swift", "genre": "Indie-pop", "bpm": 97,
     "mood": "rainy day", "year": 2022, "language": "English",
     "comment": "Self-awareness this sharp usually sounds defensive. This sounds like freedom."},
    {"title": "Glimpse of Us", "artist": "Joji", "genre": "R&B", "bpm": 74,
     "mood": "rainy day", "year": 2022, "language": "English",
     "comment": "The quietest devastation. A whole relationship compressed into 3 minutes."},
    {"title": "Redbone", "artist": "Childish Gambino", "genre": "R&B", "bpm": 84,
     "mood": "late-night drive", "year": 2016, "language": "English",
     "comment": "Soul at a tempo that forces you to feel everything you have been avoiding."},
    {"title": "Motion Sickness", "artist": "Phoebe Bridgers", "genre": "Indie Folk", "bpm": 148,
     "mood": "rainy day", "year": 2017, "language": "English",
     "comment": "The specific ache of being changed by someone who did not earn it."},
    {"title": "Fake Plastic Trees", "artist": "Radiohead", "genre": "Alt-rock", "bpm": 72,
     "mood": "deep focus", "year": 1995, "language": "English",
     "comment": "Grief at slow tempo. Thom Yorke sounds genuinely exhausted in the best possible way."},
    # ── Heritage / Folk ──────────────────────────────────────────────────────
    {"title": "Xia Dan Shui He Xie Zhe Wo Deng Jie Zu Pu", "artist": "Kau-kung Ngak-tui",
     "genre": "Hakka Folk", "bpm": 72, "mood": "nostalgia", "year": 1999, "language": "Hakka",
     "comment": "The river writes our genealogy. Ancestors carried this land on their backs so we could stand on it."},
    {"title": "Scarborough Fair", "artist": "Simon & Garfunkel", "genre": "Folk", "bpm": 88,
     "mood": "nostalgia", "year": 1966, "language": "English",
     "comment": "A song about impossible conditions for love. Still feels contemporary."},
    {"title": "The Sound of Silence", "artist": "Simon & Garfunkel", "genre": "Folk", "bpm": 104,
     "mood": "deep focus", "year": 1964, "language": "English",
     "comment": "1964. Still the most accurate description of how social media feels."},
    # ── Electronic / Ambient ─────────────────────────────────────────────────
    {"title": "Teardrop", "artist": "Massive Attack", "genre": "Trip-hop", "bpm": 76,
     "mood": "deep focus", "year": 1998, "language": "English",
     "comment": "The heartbeat bassline was not a metaphor. It was a blueprint."},
    {"title": "Breathe", "artist": "Télépopmusik", "genre": "Electronic", "bpm": 95,
     "mood": "morning ritual", "year": 2001, "language": "English",
     "comment": "Calm as a manifesto. Everything you need, nothing you do not."},
]

SAMPLE_USERS = [
    {
        "name": "Yuna K.", "match": 89,
        "genres": ["J-Pop", "Pop Ballad", "Hakka Folk"],
        "tracks": ["Anytime Anywhere – milet", "Yoru ni Kakeru – YOASOBI",
                   "Don't Say You Love Me – Jin", "Lemon – Kenshi Yonezu",
                   "Scarborough Fair – Simon & Garfunkel"],
        "track_data": [
            {"title": "Anytime Anywhere",  "artist": "milet",              "genre": "Pop Ballad",  "bpm": 109, "mood": "nostalgia",         "year": 2023, "language": "Japanese"},
            {"title": "Yoru ni Kakeru",    "artist": "YOASOBI",            "genre": "J-Pop",       "bpm": 132, "mood": "late-night drive",   "year": 2019, "language": "Japanese"},
            {"title": "Don't Say You Love Me", "artist": "Jin",            "genre": "Pop Ballad",  "bpm": 85,  "mood": "rainy day",          "year": 2025, "language": "Korean"},
            {"title": "Lemon",             "artist": "Kenshi Yonezu",      "genre": "Pop Ballad",  "bpm": 96,  "mood": "rainy day",          "year": 2018, "language": "Japanese"},
            {"title": "Scarborough Fair",  "artist": "Simon & Garfunkel",  "genre": "Folk",        "bpm": 88,  "mood": "nostalgia",          "year": 1966, "language": "English"},
            {"title": "Kawaii Dake Ja Dame Desu Ka", "artist": "CUTIE STREET", "genre": "J-Pop",   "bpm": 118, "mood": "morning ritual",     "year": 2024, "language": "Japanese"},
            {"title": "Gyakkō",            "artist": "Ado",                "genre": "J-Pop",       "bpm": 145, "mood": "deep focus",         "year": 2022, "language": "Japanese"},
            {"title": "Xia Dan Shui He",   "artist": "Kau-kung Ngak-tui",  "genre": "Hakka Folk",  "bpm": 72,  "mood": "nostalgia",          "year": 1999, "language": "Hakka"},
        ],
        "bio": "J-Pop devotee and nostalgic folk listener. Music is memory for her.",
    },
    {
        "name": "Minhyuk P.", "match": 81,
        "genres": ["Dance-pop", "Alt-rock", "Pop Ballad"],
        "tracks": ["Abracadabra – Lady Gaga", "Kaiju – Sakanaction",
                   "Blinding Lights – The Weeknd", "Idol – YOASOBI"],
        "track_data": [
            {"title": "Abracadabra",       "artist": "Lady Gaga",          "genre": "Dance-pop",   "bpm": 126, "mood": "peak hour",          "year": 2025, "language": "English"},
            {"title": "Kaiju",             "artist": "Sakanaction",        "genre": "Alt-rock",    "bpm": 180, "mood": "deep focus",         "year": 2025, "language": "Japanese"},
            {"title": "Blinding Lights",   "artist": "The Weeknd",         "genre": "Synthpop",    "bpm": 171, "mood": "late-night drive",   "year": 2019, "language": "English"},
            {"title": "Idol",              "artist": "YOASOBI",            "genre": "J-Pop",       "bpm": 180, "mood": "peak hour",          "year": 2023, "language": "Japanese"},
            {"title": "Dynamite",          "artist": "BTS",                "genre": "Dance-pop",   "bpm": 114, "mood": "morning ritual",     "year": 2020, "language": "English"},
            {"title": "Levitating",        "artist": "Dua Lipa",           "genre": "Dance-pop",   "bpm": 103, "mood": "peak hour",          "year": 2020, "language": "English"},
            {"title": "As It Was",         "artist": "Harry Styles",       "genre": "Indie-pop",   "bpm": 174, "mood": "morning ritual",     "year": 2022, "language": "English"},
            {"title": "TAIDADA",           "artist": "ZUTOMAYO",           "genre": "Alt-rock",    "bpm": 172, "mood": "deep focus",         "year": 2025, "language": "Japanese"},
        ],
        "bio": "High-energy listener. Lives in the 160–180 BPM zone whenever possible.",
    },
    {
        "name": "Sojin L.", "match": 74,
        "genres": ["Pop Ballad", "J-Pop", "R&B"],
        "tracks": ["Don't Say You Love Me – Jin", "Blinding Lights – The Weeknd",
                   "Glimpse of Us – Joji", "Redbone – Childish Gambino"],
        "track_data": [
            {"title": "Don't Say You Love Me", "artist": "Jin",            "genre": "Pop Ballad",  "bpm": 85,  "mood": "rainy day",          "year": 2025, "language": "Korean"},
            {"title": "Glimpse of Us",     "artist": "Joji",               "genre": "R&B",         "bpm": 74,  "mood": "rainy day",          "year": 2022, "language": "English"},
            {"title": "Redbone",           "artist": "Childish Gambino",   "genre": "R&B",         "bpm": 84,  "mood": "late-night drive",   "year": 2016, "language": "English"},
            {"title": "Lemon",             "artist": "Kenshi Yonezu",      "genre": "Pop Ballad",  "bpm": 96,  "mood": "rainy day",          "year": 2018, "language": "Japanese"},
            {"title": "Anti-Hero",         "artist": "Taylor Swift",       "genre": "Indie-pop",   "bpm": 97,  "mood": "rainy day",          "year": 2022, "language": "English"},
            {"title": "Anytime Anywhere",  "artist": "milet",              "genre": "Pop Ballad",  "bpm": 109, "mood": "nostalgia",          "year": 2023, "language": "Japanese"},
            {"title": "Fake Plastic Trees","artist": "Radiohead",          "genre": "Alt-rock",    "bpm": 72,  "mood": "deep focus",         "year": 1995, "language": "English"},
        ],
        "bio": "R&B and ballad collector. Slow BPM, maximum emotional weight.",
    },
    {
        "name": "Jaeyoung C.", "match": 58,
        "genres": ["Alt-rock", "Electronic", "Dance-pop"],
        "tracks": ["Kaiju – Sakanaction", "Fake Plastic Trees – Radiohead",
                   "Teardrop – Massive Attack", "Breathe – Télépopmusik"],
        "track_data": [
            {"title": "Kaiju",             "artist": "Sakanaction",        "genre": "Alt-rock",    "bpm": 180, "mood": "deep focus",         "year": 2025, "language": "Japanese"},
            {"title": "Fake Plastic Trees","artist": "Radiohead",          "genre": "Alt-rock",    "bpm": 72,  "mood": "deep focus",         "year": 1995, "language": "English"},
            {"title": "Teardrop",          "artist": "Massive Attack",     "genre": "Trip-hop",    "bpm": 76,  "mood": "deep focus",         "year": 1998, "language": "English"},
            {"title": "Breathe",           "artist": "Télépopmusik",       "genre": "Electronic",  "bpm": 95,  "mood": "morning ritual",     "year": 2001, "language": "English"},
            {"title": "Yoru no Odoriko",   "artist": "Sakanaction",        "genre": "Alt-rock",    "bpm": 128, "mood": "late-night drive",   "year": 2013, "language": "Japanese"},
            {"title": "Motion Sickness",   "artist": "Phoebe Bridgers",    "genre": "Indie Folk",  "bpm": 148, "mood": "rainy day",          "year": 2017, "language": "English"},
            {"title": "The Sound of Silence", "artist": "Simon & Garfunkel","genre": "Folk",       "bpm": 104, "mood": "deep focus",         "year": 1964, "language": "English"},
            {"title": "TAIDADA",           "artist": "ZUTOMAYO",           "genre": "Alt-rock",    "bpm": 172, "mood": "deep focus",         "year": 2025, "language": "Japanese"},
        ],
        "bio": "Alt-rock purist. If there's no texture and tension, he's already skipped it.",
    },
    {
        "name": "Aiko T.", "match": 66,
        "genres": ["Indie-pop", "Folk", "Trip-hop"],
        "tracks": ["Motion Sickness – Phoebe Bridgers", "Teardrop – Massive Attack",
                   "As It Was – Harry Styles"],
        "track_data": [
            {"title": "Motion Sickness",   "artist": "Phoebe Bridgers",    "genre": "Indie Folk",  "bpm": 148, "mood": "rainy day",          "year": 2017, "language": "English"},
            {"title": "Teardrop",          "artist": "Massive Attack",     "genre": "Trip-hop",    "bpm": 76,  "mood": "deep focus",         "year": 1998, "language": "English"},
            {"title": "As It Was",         "artist": "Harry Styles",       "genre": "Indie-pop",   "bpm": 174, "mood": "morning ritual",     "year": 2022, "language": "English"},
            {"title": "Anti-Hero",         "artist": "Taylor Swift",       "genre": "Indie-pop",   "bpm": 97,  "mood": "rainy day",          "year": 2022, "language": "English"},
            {"title": "Flowers",           "artist": "Miley Cyrus",        "genre": "Pop",         "bpm": 118, "mood": "morning ritual",     "year": 2023, "language": "English"},
            {"title": "Scarborough Fair",  "artist": "Simon & Garfunkel",  "genre": "Folk",        "bpm": 88,  "mood": "nostalgia",          "year": 1966, "language": "English"},
            {"title": "Breathe",           "artist": "Télépopmusik",       "genre": "Electronic",  "bpm": 95,  "mood": "morning ritual",     "year": 2001, "language": "English"},
        ],
        "bio": "Indie explorer with a soft spot for atmospheric textures and acoustic warmth.",
    },
    {
        "name": "Riku M.", "match": 45,
        "genres": ["Dance-pop", "K-Pop", "Synthpop"],
        "tracks": ["Dynamite – BTS", "Cupid – FIFTY FIFTY",
                   "Espresso – Sabrina Carpenter", "Levitating – Dua Lipa"],
        "track_data": [
            {"title": "Dynamite",          "artist": "BTS",                "genre": "Dance-pop",   "bpm": 114, "mood": "morning ritual",     "year": 2020, "language": "English"},
            {"title": "Cupid",             "artist": "FIFTY FIFTY",        "genre": "K-Pop",       "bpm": 107, "mood": "morning ritual",     "year": 2023, "language": "Korean"},
            {"title": "Espresso",          "artist": "Sabrina Carpenter",  "genre": "Dance-pop",   "bpm": 104, "mood": "morning ritual",     "year": 2024, "language": "English"},
            {"title": "Levitating",        "artist": "Dua Lipa",           "genre": "Dance-pop",   "bpm": 103, "mood": "peak hour",          "year": 2020, "language": "English"},
            {"title": "Blinding Lights",   "artist": "The Weeknd",         "genre": "Synthpop",    "bpm": 171, "mood": "late-night drive",   "year": 2019, "language": "English"},
            {"title": "Flowers",           "artist": "Miley Cyrus",        "genre": "Pop",         "bpm": 118, "mood": "morning ritual",     "year": 2023, "language": "English"},
            {"title": "Abracadabra",       "artist": "Lady Gaga",          "genre": "Dance-pop",   "bpm": 126, "mood": "peak hour",          "year": 2025, "language": "English"},
        ],
        "bio": "Pure pop energy. Playlists are basically one long gym session.",
    },
    {
        "name": "Hana W.", "match": 70,
        "genres": ["R&B", "Indie Folk", "Pop Ballad"],
        "tracks": ["Redbone – Childish Gambino", "Glimpse of Us – Joji",
                   "The Sound of Silence – Simon & Garfunkel"],
        "track_data": [
            {"title": "Redbone",           "artist": "Childish Gambino",   "genre": "R&B",         "bpm": 84,  "mood": "late-night drive",   "year": 2016, "language": "English"},
            {"title": "Glimpse of Us",     "artist": "Joji",               "genre": "R&B",         "bpm": 74,  "mood": "rainy day",          "year": 2022, "language": "English"},
            {"title": "The Sound of Silence","artist": "Simon & Garfunkel","genre": "Folk",        "bpm": 104, "mood": "deep focus",         "year": 1964, "language": "English"},
            {"title": "Motion Sickness",   "artist": "Phoebe Bridgers",    "genre": "Indie Folk",  "bpm": 148, "mood": "rainy day",          "year": 2017, "language": "English"},
            {"title": "Fake Plastic Trees","artist": "Radiohead",          "genre": "Alt-rock",    "bpm": 72,  "mood": "deep focus",         "year": 1995, "language": "English"},
            {"title": "JANE DOE",          "artist": "Kenshi Yonezu",      "genre": "Pop Ballad",  "bpm": 88,  "mood": "rainy day",          "year": 2026, "language": "Japanese"},
            {"title": "Lemon",             "artist": "Kenshi Yonezu",      "genre": "Pop Ballad",  "bpm": 96,  "mood": "rainy day",          "year": 2018, "language": "Japanese"},
        ],
        "bio": "Slow-tempo curator. Emotional depth over everything — rainy playlists are her signature.",
    },
    {
        "name": "Seb D.", "match": 52,
        "genres": ["Folk", "Indie Folk", "Indie-pop"],
        "tracks": ["Scarborough Fair – Simon & Garfunkel", "The Sound of Silence – Simon & Garfunkel",
                   "Fake Plastic Trees – Radiohead"],
        "track_data": [
            {"title": "Scarborough Fair",  "artist": "Simon & Garfunkel",  "genre": "Folk",        "bpm": 88,  "mood": "nostalgia",          "year": 1966, "language": "English"},
            {"title": "The Sound of Silence","artist": "Simon & Garfunkel","genre": "Folk",        "bpm": 104, "mood": "deep focus",         "year": 1964, "language": "English"},
            {"title": "Fake Plastic Trees","artist": "Radiohead",          "genre": "Alt-rock",    "bpm": 72,  "mood": "deep focus",         "year": 1995, "language": "English"},
            {"title": "Motion Sickness",   "artist": "Phoebe Bridgers",    "genre": "Indie Folk",  "bpm": 148, "mood": "rainy day",          "year": 2017, "language": "English"},
            {"title": "Anti-Hero",         "artist": "Taylor Swift",       "genre": "Indie-pop",   "bpm": 97,  "mood": "rainy day",          "year": 2022, "language": "English"},
            {"title": "As It Was",         "artist": "Harry Styles",       "genre": "Indie-pop",   "bpm": 174, "mood": "morning ritual",     "year": 2022, "language": "English"},
            {"title": "Breathe",           "artist": "Télépopmusik",       "genre": "Electronic",  "bpm": 95,  "mood": "morning ritual",     "year": 2001, "language": "English"},
        ],
        "bio": "Heritage folk listener who also lets indie-pop sneak in. Vinyl > streaming.",
    },
]

MOOD_TAGS = ["late-night drive", "rainy day", "deep focus",
             "morning ritual", "peak hour", "nostalgia"]

# ── Session state ─────────────────────────────────────────────────────────────
if "tracks" not in st.session_state:
    st.session_state.tracks = SAMPLE_TRACKS.copy()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎵 SoundSelf")
    st.markdown("*share your music. share your worldview.*")
    st.divider()

    page = st.radio(
        "Navigate",
        ["My Music Profile", "Taste Analysis", "Mood Tags",
         "Taste Map", "User Comparison", "Curator Feed", "Spotify Import"],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown('<div class="section-header">add a track</div>', unsafe_allow_html=True)
    with st.form("add_track", clear_on_submit=True):
        new_title   = st.text_input("Title")
        new_artist  = st.text_input("Artist")
        new_genre   = st.selectbox("Genre",
            ["Pop Ballad", "J-Pop", "K-Pop", "Dance-pop", "Alt-rock", "Indie-pop",
             "Indie Folk", "Folk", "Hakka Folk", "Electronic", "Trip-hop", "R&B",
             "Synthpop", "Pop", "Classical", "Jazz", "Other"])
        new_bpm     = st.number_input("BPM", 40, 220, 110)
        new_mood    = st.selectbox("Mood tag", MOOD_TAGS)
        new_lang    = st.selectbox("Language",
            ["Japanese", "Korean", "English", "Chinese", "Hakka", "Spanish", "Other"])
        new_year    = st.number_input("Year", 1950, datetime.now().year, datetime.now().year)
        new_comment = st.text_area("Your one-line comment", height=70)
        submitted   = st.form_submit_button("+ Add track")
        if submitted and new_title and new_artist:
            st.session_state.tracks.append({
                "title": new_title, "artist": new_artist, "genre": new_genre,
                "bpm": new_bpm, "mood": new_mood, "year": int(new_year),
                "language": new_lang, "comment": new_comment,
            })
            st.success(f"Added: {new_title}")

df = pd.DataFrame(st.session_state.tracks)
df["decade"] = (df["year"] // 10 * 10).astype(str) + "s"

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — MY MUSIC PROFILE
# ══════════════════════════════════════════════════════════════════════════════
if page == "My Music Profile":
    st.markdown('<div class="main-title">My Music World</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">a profile that speaks louder than words</div>',
                unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Tracks", len(df))
    c2.metric("Genres", df["genre"].nunique())
    c3.metric("Languages", df["language"].nunique() if "language" in df.columns else "—")
    c4.metric("Avg BPM", int(df["bpm"].mean()))
    c5.metric("Decade span", f"{df['year'].min()//10*10}s–{df['year'].max()//10*10}s")

    st.divider()

    col_filter, _ = st.columns([2, 3])
    with col_filter:
        genre_filter = st.multiselect(
            "Filter by genre", options=sorted(df["genre"].unique().tolist()), default=[])

    display_df = df if not genre_filter else df[df["genre"].isin(genre_filter)]

    st.markdown('<div class="section-header">genre breakdown</div>', unsafe_allow_html=True)
    genre_counts = df["genre"].value_counts().reset_index()
    genre_counts.columns = ["genre", "count"]
    fig_genre = px.bar(
        genre_counts, x="genre", y="count",
        color="genre", color_discrete_sequence=px.colors.qualitative.Pastel,
        height=230,
    )
    fig_genre.update_layout(showlegend=False, margin=dict(l=0,r=0,t=10,b=0),
                            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                            xaxis=dict(title=""), yaxis=dict(title=""))
    st.plotly_chart(fig_genre, use_container_width=True)

    st.markdown('<div class="section-header">your tracks</div>', unsafe_allow_html=True)
    for _, row in display_df.iterrows():
        with st.expander(f"**{row['title']}** — {row['artist']}  ·  {row['genre']}  ·  {row['bpm']} bpm"):
            st.markdown(f'<div class="track-comment">"{row["comment"]}"</div>',
                        unsafe_allow_html=True)
            cols = st.columns(4)
            cols[0].caption(f"🎭 {row['mood']}")
            cols[1].caption(f"📅 {row['year']}")
            cols[2].caption(f"🌐 {row.get('language','—')}")
            cols[3].caption(f"♩ {row['bpm']} bpm")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — TASTE ANALYSIS (new, expanded from Taste Compatibility)
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Taste Analysis":
    st.markdown('<div class="main-title">Taste Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">what your library actually says about you</div>',
                unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🧠 Listener Persona",
        "📅 Timeline",
        "🌍 Language & Culture",
        "⚡ Energy Profile",
        "🤝 Compatibility",
    ])

    # ── TAB 1: Listener Persona ───────────────────────────────────────────────
    with tab1:
        st.markdown('<div class="section-header">your listener persona</div>',
                    unsafe_allow_html=True)

        # Compute persona dimensions from data
        avg_bpm      = df["bpm"].mean()
        top_mood     = df["mood"].value_counts().idxmax()
        top_genre    = df["genre"].value_counts().idxmax()
        lang_count   = df["language"].nunique() if "language" in df.columns else 1
        decade_range = df["year"].max() - df["year"].min()
        ballad_ratio = len(df[df["genre"].isin(["Pop Ballad", "Folk", "Indie Folk", "Hakka Folk"])]) / len(df)
        energy_ratio = len(df[df["genre"].isin(["Dance-pop", "Alt-rock", "J-Pop", "K-Pop", "Electronic"])]) / len(df)
        nostalgia_ratio = len(df[df["year"] < 2010]) / len(df)

        # Generate persona labels
        persona_traits = []
        if avg_bpm >= 130:
            persona_traits.append(("⚡ High-Energy Listener",
                "Your average BPM sits above 130 — you gravitate toward music that moves at a sprint. "
                "Playlists for commutes, workouts, and moments when stillness feels like a waste."))
        elif avg_bpm >= 100:
            persona_traits.append(("🌊 Mid-Tempo Dweller",
                "You live in the 100–130 BPM sweet spot — energetic enough to feel alive, "
                "grounded enough to think. The zone where most great pop songs live."))
        else:
            persona_traits.append(("🌙 Slow-Burn Listener",
                f"Your average BPM of {avg_bpm:.0f} says you prefer music that breathes. "
                "You are not in a rush. The space between notes matters as much as the notes."))

        if lang_count >= 4:
            persona_traits.append(("🌏 Cross-Cultural Explorer",
                f"You listen in {lang_count} languages. For you, not understanding every word "
                "is not a barrier — it is an invitation to feel without translating."))
        elif lang_count >= 2:
            persona_traits.append(("🗺️ Bilingual Ear",
                f"Your library spans {lang_count} languages. You follow artists across borders, "
                "which means your taste is defined by sound, not geography."))

        if nostalgia_ratio >= 0.25:
            persona_traits.append(("📼 Time Traveller",
                f"{nostalgia_ratio:.0%} of your tracks predate 2010. You do not just consume "
                "music from the present — you curate it across decades. History as taste."))

        if ballad_ratio >= 0.35:
            persona_traits.append(("🎭 Emotional Archivist",
                "More than a third of your library leans into ballads and folk. "
                "You use music to process — these songs are not just background, they are records."))

        if top_mood in ["deep focus", "rainy day"]:
            persona_traits.append(("🔬 Introspective Listener",
                f"'{top_mood}' is your dominant mood tag. You reach for music that matches or "
                "deepens a feeling, not one that distracts from it."))
        elif top_mood in ["peak hour", "morning ritual"]:
            persona_traits.append(("☀️ Energiser",
                f"'{top_mood}' dominates your tags. You use music as fuel — "
                "to start something, to sustain momentum, to feel capable."))

        for label, desc in persona_traits:
            st.markdown(f"""
            <div class="persona-card">
              <div style="font-size:0.95rem; font-weight:500; color:#AFA9EC; margin-bottom:0.4rem;">{label}</div>
              <div style="font-size:0.82rem; color:#ccc; line-height:1.6;">{desc}</div>
            </div>""", unsafe_allow_html=True)

        st.divider()

        # Radar: mood distribution
        st.markdown('<div class="section-header">mood fingerprint</div>',
                    unsafe_allow_html=True)
        mood_counts_all = df["mood"].value_counts()
        all_moods = MOOD_TAGS
        mood_vals  = [mood_counts_all.get(m, 0) for m in all_moods]

        fig_radar = go.Figure(go.Scatterpolar(
            r=mood_vals + [mood_vals[0]],
            theta=all_moods + [all_moods[0]],
            fill="toself",
            fillcolor="rgba(175,169,236,0.18)",
            line=dict(color="#AFA9EC", width=2),
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(range=[0, max(mood_vals)+1],
                                       showticklabels=False, gridcolor="#333")),
            height=320, margin=dict(l=30,r=30,t=20,b=20),
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        # Key conclusion
        dominant_moods = df["mood"].value_counts().head(2).index.tolist()
        st.markdown(f"""
        <div class="insight-box">
          <div class="insight-label">🔍 conclusion</div>
          Your two dominant moods are <strong>{dominant_moods[0]}</strong>
          {"and <strong>" + dominant_moods[1] + "</strong>" if len(dominant_moods) > 1 else ""}.
          This suggests a listener who alternates between introspection and activation —
          using music as both a mirror and an engine depending on the moment.
        </div>""", unsafe_allow_html=True)

    # ── TAB 2: Timeline ───────────────────────────────────────────────────────
    with tab2:
        st.markdown('<div class="section-header">tracks by release decade</div>',
                    unsafe_allow_html=True)

        decade_counts = df.groupby("decade").size().reset_index(name="count")
        decade_counts = decade_counts.sort_values("decade")
        fig_decade = px.bar(
            decade_counts, x="decade", y="count",
            color="count", color_continuous_scale="Teal",
            height=220, labels={"decade": "", "count": "tracks"},
        )
        fig_decade.update_layout(showlegend=False, coloraxis_showscale=False,
                                  margin=dict(l=0,r=0,t=10,b=0),
                                  plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_decade, use_container_width=True)

        # BPM over decades
        st.markdown('<div class="section-header">average BPM per decade — did your taste speed up?</div>',
                    unsafe_allow_html=True)
        bpm_decade = df.groupby("decade")["bpm"].mean().reset_index()
        bpm_decade.columns = ["decade", "avg_bpm"]
        bpm_decade = bpm_decade.sort_values("decade")
        fig_bpm_dec = px.line(
            bpm_decade, x="decade", y="avg_bpm",
            markers=True, height=200,
            color_discrete_sequence=["#5DCAA5"],
            labels={"decade": "", "avg_bpm": "avg BPM"},
        )
        fig_bpm_dec.update_layout(margin=dict(l=0,r=0,t=10,b=0),
                                   plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_bpm_dec, use_container_width=True)

        # Genre shift over decades
        st.markdown('<div class="section-header">genre mix by decade</div>',
                    unsafe_allow_html=True)
        genre_decade = df.groupby(["decade", "genre"]).size().reset_index(name="count")
        fig_gd = px.bar(
            genre_decade, x="decade", y="count", color="genre",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            height=260, labels={"decade": "", "count": "tracks"},
            barmode="stack",
        )
        fig_gd.update_layout(margin=dict(l=0,r=0,t=10,b=0), legend_title="genre",
                              plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_gd, use_container_width=True)

        # Newest vs oldest
        newest = df.nlargest(3, "year")[["title","artist","year"]]
        oldest = df.nsmallest(3, "year")[["title","artist","year"]]
        col_n, col_o = st.columns(2)
        with col_n:
            st.markdown('<div class="section-header">most recent additions</div>',
                        unsafe_allow_html=True)
            for _, r in newest.iterrows():
                st.caption(f"**{r['title']}** · {r['artist']} · {r['year']}")
        with col_o:
            st.markdown('<div class="section-header">oldest in your library</div>',
                        unsafe_allow_html=True)
            for _, r in oldest.iterrows():
                st.caption(f"**{r['title']}** · {r['artist']} · {r['year']}")

        decade_range = df["year"].max() - df["year"].min()
        peak_decade  = decade_counts.loc[decade_counts["count"].idxmax(), "decade"]
        st.markdown(f"""
        <div class="insight-box">
          <div class="insight-label">🔍 conclusion</div>
          Your library spans <strong>{decade_range} years</strong> of music history.
          Your heaviest concentration is in the <strong>{peak_decade}</strong>.
          {"That decade gap suggests your taste was formed across eras, not just the present moment."
           if decade_range > 20 else
           "A tight decade range means your taste is anchored in a specific cultural moment."}
        </div>""", unsafe_allow_html=True)

    # ── TAB 3: Language & Culture ─────────────────────────────────────────────
    with tab3:
        if "language" not in df.columns:
            st.info("Add a 'language' field to your tracks to enable this analysis.")
        else:
            st.markdown('<div class="section-header">language distribution</div>',
                        unsafe_allow_html=True)
            lang_counts = df["language"].value_counts().reset_index()
            lang_counts.columns = ["language", "count"]
            fig_lang = px.pie(
                lang_counts, values="count", names="language", hole=0.5,
                color_discrete_sequence=px.colors.qualitative.Pastel,
                height=260,
            )
            fig_lang.update_layout(margin=dict(l=0,r=0,t=10,b=0),
                                    paper_bgcolor="rgba(0,0,0,0)",
                                    legend=dict(orientation="v", x=1, y=0.5))
            st.plotly_chart(fig_lang, use_container_width=True)

            # Language × mood heatmap
            st.markdown('<div class="section-header">which language carries which mood?</div>',
                        unsafe_allow_html=True)
            lang_mood = df.groupby(["language", "mood"]).size().unstack(fill_value=0)
            fig_heat = px.imshow(
                lang_mood,
                color_continuous_scale="Teal",
                aspect="auto", height=280,
                labels=dict(x="mood", y="language", color="tracks"),
            )
            fig_heat.update_layout(margin=dict(l=0,r=0,t=10,b=0),
                                    paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_heat, use_container_width=True)

            # Language × avg BPM
            st.markdown('<div class="section-header">average BPM by language</div>',
                        unsafe_allow_html=True)
            lang_bpm = df.groupby("language")["bpm"].mean().reset_index().sort_values("bpm", ascending=False)
            fig_lb = px.bar(
                lang_bpm, x="language", y="bpm",
                color="bpm", color_continuous_scale="Purples",
                height=210, labels={"language": "", "bpm": "avg BPM"},
            )
            fig_lb.update_layout(coloraxis_showscale=False, showlegend=False,
                                  margin=dict(l=0,r=0,t=10,b=0),
                                  plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_lb, use_container_width=True)

            top_lang = lang_counts.iloc[0]["language"]
            pct      = lang_counts.iloc[0]["count"] / len(df)
            fastest_lang = lang_bpm.iloc[0]["language"]
            st.markdown(f"""
            <div class="insight-box">
              <div class="insight-label">🔍 conclusion</div>
              <strong>{top_lang}</strong> dominates at <strong>{pct:.0%}</strong> of your library.
              Your fastest language on average is <strong>{fastest_lang}</strong> —
              suggesting that when you listen in {fastest_lang}, you reach for energy and
              momentum over reflection.
              {"Listening across " + str(df['language'].nunique()) + " languages means your taste is defined by sound and feeling, not just lyrics you understand."
               if df['language'].nunique() >= 3 else ""}
            </div>""", unsafe_allow_html=True)

    # ── TAB 4: Energy Profile ─────────────────────────────────────────────────
    with tab4:
        st.markdown('<div class="section-header">BPM distribution — the shape of your energy</div>',
                    unsafe_allow_html=True)
        fig_hist = px.histogram(
            df, x="bpm", nbins=20, color="genre",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            height=240, labels={"bpm": "BPM", "count": "tracks"},
            marginal="rug",
        )
        fig_hist.update_layout(margin=dict(l=0,r=0,t=10,b=0), bargap=0.05,
                                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                                legend=dict(orientation="h", y=-0.3))
        st.plotly_chart(fig_hist, use_container_width=True)

        # BPM by genre box plot
        st.markdown('<div class="section-header">BPM range by genre</div>',
                    unsafe_allow_html=True)
        fig_box = px.box(
            df, x="genre", y="bpm", color="genre",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            height=260, points="all",
        )
        fig_box.update_layout(showlegend=False, margin=dict(l=0,r=0,t=10,b=0),
                               plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                               xaxis_title="", yaxis_title="bpm")
        st.plotly_chart(fig_box, use_container_width=True)

        # BPM vs mood scatter
        st.markdown('<div class="section-header">BPM vs mood — does speed predict feeling?</div>',
                    unsafe_allow_html=True)
        mood_order = {"rainy day": 1, "nostalgia": 2, "deep focus": 3,
                      "morning ritual": 4, "late-night drive": 5, "peak hour": 6}
        df_e = df.copy()
        df_e["mood_score"] = df_e["mood"].map(mood_order).fillna(3)

        fig_mv = px.scatter(
            df_e, x="bpm", y="mood", color="genre",
            size=[10]*len(df_e), hover_data=["title","artist","year"],
            color_discrete_sequence=px.colors.qualitative.Pastel,
            height=280,
            labels={"bpm": "BPM", "mood": "mood tag"},
            category_orders={"mood": list(mood_order.keys())},
        )
        fig_mv.update_layout(margin=dict(l=0,r=0,t=10,b=0),
                              plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                              legend=dict(orientation="h", y=-0.25))
        st.plotly_chart(fig_mv, use_container_width=True)

        # Stats
        high_bpm = df[df["bpm"] >= 140]
        low_bpm  = df[df["bpm"] < 90]
        c1, c2, c3 = st.columns(3)
        c1.metric("High-energy tracks (≥140 BPM)", len(high_bpm))
        c2.metric("Slow tracks (<90 BPM)", len(low_bpm))
        c3.metric("BPM range", f"{df['bpm'].min()} – {df['bpm'].max()}")

        # Correlation check
        corr = df_e[["bpm","mood_score"]].corr().iloc[0,1]
        corr_desc = (
            "a moderate positive correlation — faster tracks do tend to carry more energetic moods."
            if corr > 0.3 else
            "almost no correlation — you tag moods independently of tempo."
            if abs(corr) < 0.15 else
            "a slight negative correlation — your slowest tracks sometimes carry the heaviest emotional weight."
        )
        st.markdown(f"""
        <div class="insight-box">
          <div class="insight-label">🔍 conclusion</div>
          BPM vs mood correlation: <strong>{corr:.2f}</strong> — {corr_desc}
          Your fastest genre by average BPM is
          <strong>{df.groupby("genre")["bpm"].mean().idxmax()}</strong>
          ({df.groupby("genre")["bpm"].mean().max():.0f} BPM avg),
          your most contemplative is
          <strong>{df.groupby("genre")["bpm"].mean().idxmin()}</strong>
          ({df.groupby("genre")["bpm"].mean().min():.0f} BPM avg).
        </div>""", unsafe_allow_html=True)

    # ── TAB 5: Compatibility ──────────────────────────────────────────────────
    with tab5:
        st.markdown('<div class="section-header">curators ranked by match score</div>',
                    unsafe_allow_html=True)

        user_df = pd.DataFrame(SAMPLE_USERS)
        fig_match = go.Figure()
        fig_match.add_trace(go.Bar(
            x=user_df["match"], y=user_df["name"], orientation="h",
            marker_color=["#5DCAA5","#378ADD","#AFA9EC","#D85A30"],
            text=[f"{m}%" for m in user_df["match"]], textposition="outside",
        ))
        fig_match.update_layout(
            height=220, margin=dict(l=0,r=40,t=10,b=0),
            xaxis=dict(range=[0,100], title="compatibility %"),
            yaxis=dict(title=""),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_match, use_container_width=True)

        st.markdown('<div class="section-header">shared genre overlap</div>',
                    unsafe_allow_html=True)
        my_genres  = set(df["genre"].unique())
        overlap_data = []
        for u in SAMPLE_USERS:
            shared = my_genres.intersection(set(u["genres"]))
            overlap_data.append({"curator": u["name"], "match": u["match"],
                                  "shared_genres": ", ".join(shared) or "—",
                                  "shared_count": len(shared)})
        overlap_df = pd.DataFrame(overlap_data)

        fig_scatter = px.scatter(
            overlap_df, x="shared_count", y="match",
            text="curator", size="match",
            color="match", color_continuous_scale="Teal",
            labels={"shared_count": "shared genres", "match": "compatibility %"},
            height=260,
        )
        fig_scatter.update_traces(textposition="top center")
        fig_scatter.update_layout(margin=dict(l=0,r=0,t=10,b=0),
                                   plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                                   coloraxis_showscale=False)
        st.plotly_chart(fig_scatter, use_container_width=True)

        for u in SAMPLE_USERS:
            with st.expander(f"**{u['name']}** — {u['match']}% match"):
                st.caption("Genres: " + " · ".join(u["genres"]))
                st.caption("Recent tracks: " + " / ".join(u["tracks"]))


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — MOOD TAGS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Mood Tags":
    st.markdown('<div class="main-title">Mood Tag System</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">music filtered by emotional context</div>',
                unsafe_allow_html=True)

    col_chart, col_stats = st.columns([2, 1])
    with col_chart:
        mood_counts = df["mood"].value_counts().reset_index()
        mood_counts.columns = ["mood", "count"]
        fig_mood = px.pie(
            mood_counts, values="count", names="mood", hole=0.55,
            color_discrete_sequence=px.colors.qualitative.Pastel, height=280,
        )
        fig_mood.update_layout(margin=dict(l=0,r=0,t=10,b=0),
                                paper_bgcolor="rgba(0,0,0,0)",
                                legend=dict(orientation="v", x=1, y=0.5))
        st.plotly_chart(fig_mood, use_container_width=True)
    with col_stats:
        st.markdown('<div class="section-header">avg BPM per mood</div>',
                    unsafe_allow_html=True)
        mood_bpm = df.groupby("mood")["bpm"].mean().sort_values(ascending=False)
        for mood, bpm in mood_bpm.items():
            st.caption(f"**{mood}** — {bpm:.0f} bpm")

    st.divider()
    selected_mood = st.selectbox("Browse tracks by mood", ["— all —"] + MOOD_TAGS)
    filtered = df if selected_mood == "— all —" else df[df["mood"] == selected_mood]
    st.markdown(f'<div class="section-header">{len(filtered)} track{"s" if len(filtered)!=1 else ""} found</div>',
                unsafe_allow_html=True)

    for _, row in filtered.iterrows():
        col_a, col_b = st.columns([3, 1])
        with col_a:
            st.markdown(f"**{row['title']}** — {row['artist']}")
            st.markdown(f'<div class="track-comment">"{row["comment"]}"</div>',
                        unsafe_allow_html=True)
        with col_b:
            st.caption(row["genre"])
            st.caption(f"{row['bpm']} bpm · {row['year']}")
        st.divider()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — TASTE MAP
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Taste Map":
    st.markdown('<div class="main-title">Taste Map</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">your musical identity, visualized</div>',
                unsafe_allow_html=True)

    GENRE_X = {
        "Dance-pop": 0.92, "Electronic": 0.88, "Synthpop": 0.85,
        "K-Pop": 0.75, "Alt-rock": 0.72, "J-Pop": 0.60,
        "Indie-pop": 0.55, "Pop": 0.52, "Trip-hop": 0.50,
        "R&B": 0.42, "Pop Ballad": 0.40, "Indie Folk": 0.28,
        "Jazz": 0.28, "Folk": 0.18, "Hakka Folk": 0.10, "Classical": 0.08, "Other": 0.50,
    }

    df_map = df.copy()
    df_map["x"] = df_map["genre"].map(lambda g: GENRE_X.get(g, 0.5))
    bpm_min, bpm_max = df_map["bpm"].min(), df_map["bpm"].max()
    df_map["y"] = (df_map["bpm"] - bpm_min) / (bpm_max - bpm_min + 1)

    tab_map1, tab_map2 = st.tabs(["🗺️ 2D Taste Map", "📊 BPM Analysis"])

    with tab_map1:
        color_by = st.selectbox("Color by", ["genre", "mood", "decade"], index=0)
        fig_map = px.scatter(
            df_map, x="x", y="y", text="title",
            color=color_by, size=[18]*len(df_map),
            color_discrete_sequence=px.colors.qualitative.Pastel,
            hover_data={"title": True, "artist": True, "bpm": True,
                        "mood": True, "year": True, "x": False, "y": False},
            height=440,
            labels={"x": "← acoustic / folk · · · electronic / digital →",
                    "y": "← slow · · · intense →"},
        )
        fig_map.update_traces(textposition="top center", marker_opacity=0.85)
        fig_map.update_layout(
            margin=dict(l=0,r=0,t=20,b=0),
            plot_bgcolor="rgba(0,0,0,0.02)", paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=True, gridcolor="rgba(128,128,128,0.1)", range=[-0.05,1.05]),
            yaxis=dict(showgrid=True, gridcolor="rgba(128,128,128,0.1)", range=[-0.05,1.05]),
            legend=dict(orientation="h", y=-0.15),
        )
        st.plotly_chart(fig_map, use_container_width=True)

        # Quadrant analysis
        q_tl = df_map[(df_map["x"] < 0.5) & (df_map["y"] >= 0.5)]  # acoustic + intense
        q_tr = df_map[(df_map["x"] >= 0.5) & (df_map["y"] >= 0.5)] # electronic + intense
        q_bl = df_map[(df_map["x"] < 0.5) & (df_map["y"] < 0.5)]   # acoustic + slow
        q_br = df_map[(df_map["x"] >= 0.5) & (df_map["y"] < 0.5)]  # electronic + slow

        cc1, cc2, cc3, cc4 = st.columns(4)
        cc1.metric("🎸 Acoustic + Intense", len(q_tl))
        cc2.metric("⚡ Electronic + Intense", len(q_tr))
        cc3.metric("🌿 Acoustic + Slow", len(q_bl))
        cc4.metric("🌊 Electronic + Slow", len(q_br))

        dominant_quad = max(
            [("Acoustic + Intense", len(q_tl)), ("Electronic + Intense", len(q_tr)),
             ("Acoustic + Slow", len(q_bl)), ("Electronic + Slow", len(q_br))],
            key=lambda x: x[1]
        )
        st.markdown(f"""
        <div class="insight-box">
          <div class="insight-label">🔍 conclusion</div>
          Your library clusters most heavily in the <strong>{dominant_quad[0]}</strong> quadrant
          ({dominant_quad[1]} tracks). This is the zone that defines your musical center of gravity.
        </div>""", unsafe_allow_html=True)

    with tab_map2:
        fig_bpm = px.box(df, x="genre", y="bpm", color="genre",
                          color_discrete_sequence=px.colors.qualitative.Pastel,
                          height=260, points="all")
        fig_bpm.update_layout(showlegend=False, margin=dict(l=0,r=0,t=10,b=0),
                               plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                               xaxis_title="", yaxis_title="bpm")
        st.plotly_chart(fig_bpm, use_container_width=True)

        fig_bpm2 = px.histogram(df, x="bpm", nbins=25, height=200,
                                 color_discrete_sequence=["#5DCAA5"])
        fig_bpm2.update_layout(margin=dict(l=0,r=0,t=10,b=0), bargap=0.05,
                                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                                showlegend=False)
        st.plotly_chart(fig_bpm2, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — USER COMPARISON
# ══════════════════════════════════════════════════════════════════════════════
elif page == "User Comparison":
    st.markdown('<div class="main-title">User Comparison</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">explore how your taste overlaps — and diverges — with others</div>',
                unsafe_allow_html=True)

    # ── User selector ─────────────────────────────────────────────────────────
    user_names = [u["name"] for u in SAMPLE_USERS]
    selected_name = st.selectbox("Compare with", user_names,
                                  format_func=lambda n: f"{n}  ({next(u['match'] for u in SAMPLE_USERS if u['name']==n)}% match)")
    other = next(u for u in SAMPLE_USERS if u["name"] == selected_name)
    other_df = pd.DataFrame(other["track_data"])

    # ── Header row ────────────────────────────────────────────────────────────
    col_me, col_vs, col_them = st.columns([5, 1, 5])
    with col_me:
        st.markdown(f"""
        <div class="persona-card">
          <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:#5DCAA5;margin-bottom:0.4rem;">you</div>
          <div style="font-size:1.1rem;font-weight:500;">My Profile</div>
          <div style="font-size:0.8rem;color:#999;margin-top:0.3rem;">{len(df)} tracks · avg {df['bpm'].mean():.0f} BPM · {df['language'].nunique()} languages</div>
        </div>""", unsafe_allow_html=True)
    with col_vs:
        st.markdown(f"""
        <div style="text-align:center;padding-top:1.2rem;">
          <div style="font-size:1.6rem;font-weight:500;color:#AFA9EC;">{other['match']}%</div>
          <div style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.1em;color:#666;">match</div>
        </div>""", unsafe_allow_html=True)
    with col_them:
        st.markdown(f"""
        <div class="persona-card">
          <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:#AFA9EC;margin-bottom:0.4rem;">{other['name']}</div>
          <div style="font-size:1.1rem;font-weight:500;">{other['name']}</div>
          <div style="font-size:0.8rem;color:#999;margin-top:0.3rem;">{len(other_df)} tracks · avg {other_df['bpm'].mean():.0f} BPM · {other_df['language'].nunique()} languages</div>
          <div style="font-size:0.78rem;color:#888;margin-top:0.4rem;font-style:italic;">"{other['bio']}"</div>
        </div>""", unsafe_allow_html=True)

    st.divider()

    tab_c1, tab_c2, tab_c3, tab_c4, tab_c5 = st.tabs([
        "🎭 Mood Radar",
        "🎸 Genre Overlap",
        "⚡ BPM Distribution",
        "🌍 Language & Era",
        "🎵 Shared Tracks",
    ])

    # ── TAB 1: Mood Radar ─────────────────────────────────────────────────────
    with tab_c1:
        st.markdown('<div class="section-header">mood fingerprint — you vs them</div>',
                    unsafe_allow_html=True)

        my_mood_counts   = df["mood"].value_counts()
        them_mood_counts = other_df["mood"].value_counts()
        moods = MOOD_TAGS

        my_vals   = [my_mood_counts.get(m, 0)   for m in moods]
        them_vals = [them_mood_counts.get(m, 0) for m in moods]

        # Normalise to % so track-count difference doesn't skew shapes
        my_pct   = [v / max(sum(my_vals), 1)   * 100 for v in my_vals]
        them_pct = [v / max(sum(them_vals), 1) * 100 for v in them_vals]

        fig_radar2 = go.Figure()
        fig_radar2.add_trace(go.Scatterpolar(
            r=my_pct + [my_pct[0]], theta=moods + [moods[0]],
            fill="toself", name="You",
            fillcolor="rgba(93,202,165,0.18)", line=dict(color="#5DCAA5", width=2),
        ))
        fig_radar2.add_trace(go.Scatterpolar(
            r=them_pct + [them_pct[0]], theta=moods + [moods[0]],
            fill="toself", name=other["name"],
            fillcolor="rgba(175,169,236,0.18)", line=dict(color="#AFA9EC", width=2),
        ))
        fig_radar2.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, max(max(my_pct), max(them_pct)) * 1.15],
                                        showticklabels=False, gridcolor="#333")),
            height=360, margin=dict(l=30, r=30, t=30, b=30),
            paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", y=-0.05),
        )
        st.plotly_chart(fig_radar2, use_container_width=True)

        # Mood delta table
        st.markdown('<div class="section-header">mood gap — where you diverge most</div>',
                    unsafe_allow_html=True)
        mood_delta = []
        for m, my, th in zip(moods, my_pct, them_pct):
            mood_delta.append({"mood": m, "you (%)": round(my, 1),
                                f"{other['name']} (%)": round(th, 1),
                                "gap": round(abs(my - th), 1)})
        delta_df = pd.DataFrame(mood_delta).sort_values("gap", ascending=False)
        fig_delta = px.bar(
            delta_df, x="mood", y="gap",
            color="gap", color_continuous_scale="RdYlGn_r",
            labels={"gap": "divergence (%)", "mood": ""},
            height=220,
        )
        fig_delta.update_layout(coloraxis_showscale=False, margin=dict(l=0, r=0, t=10, b=0),
                                  plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_delta, use_container_width=True)

        top_gap_mood = delta_df.iloc[0]
        shared_top   = delta_df[delta_df["gap"] < 5].iloc[0]["mood"] if len(delta_df[delta_df["gap"] < 5]) else "—"
        st.markdown(f"""
        <div class="insight-box">
          <div class="insight-label">🔍 conclusion</div>
          Your biggest mood divergence is <strong>{top_gap_mood['mood']}</strong>
          (you {top_gap_mood['you (%)']:.0f}% vs {other['name']} {top_gap_mood[f"{other['name']} (%)"]:.0f}%).
          Your closest shared mood context is <strong>{shared_top}</strong> — that's where your listening worlds overlap most naturally.
        </div>""", unsafe_allow_html=True)

    # ── TAB 2: Genre Overlap ──────────────────────────────────────────────────
    with tab_c2:
        st.markdown('<div class="section-header">genre distribution — side by side</div>',
                    unsafe_allow_html=True)

        all_genres = sorted(set(df["genre"].unique()) | set(other_df["genre"].unique()))
        my_genre_pct   = {g: len(df[df["genre"] == g]) / len(df) * 100           for g in all_genres}
        them_genre_pct = {g: len(other_df[other_df["genre"] == g]) / len(other_df) * 100 for g in all_genres}

        genre_compare = pd.DataFrame({
            "genre":      all_genres,
            "You":        [my_genre_pct[g]   for g in all_genres],
            other["name"]:[them_genre_pct[g] for g in all_genres],
        })
        genre_compare = genre_compare[(genre_compare["You"] > 0) |
                                       (genre_compare[other["name"]] > 0)]
        genre_compare = genre_compare.sort_values("You", ascending=False)

        fig_genre_bar = go.Figure()
        fig_genre_bar.add_trace(go.Bar(name="You", x=genre_compare["genre"],
                                        y=genre_compare["You"],
                                        marker_color="#5DCAA5"))
        fig_genre_bar.add_trace(go.Bar(name=other["name"], x=genre_compare["genre"],
                                        y=genre_compare[other["name"]],
                                        marker_color="#AFA9EC"))
        fig_genre_bar.update_layout(
            barmode="group", height=280,
            margin=dict(l=0, r=0, t=10, b=0),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            yaxis_title="share (%)", xaxis_title="",
            legend=dict(orientation="h", y=-0.2),
        )
        st.plotly_chart(fig_genre_bar, use_container_width=True)

        # Shared vs exclusive genres
        my_genres_set   = set(df["genre"].unique())
        them_genres_set = set(other_df["genre"].unique())
        shared_genres   = my_genres_set & them_genres_set
        only_mine       = my_genres_set - them_genres_set
        only_theirs     = them_genres_set - my_genres_set

        c1, c2, c3 = st.columns(3)
        c1.metric("Shared genres", len(shared_genres))
        c2.metric("Only in your library", len(only_mine))
        c3.metric(f"Only in {other['name']}'s library", len(only_theirs))

        st.markdown(f"""
        <div class="insight-box">
          <div class="insight-label">🔍 shared genres</div>
          {", ".join(sorted(shared_genres)) or "None"}<br>
          <span style="color:#999;font-size:0.78rem;">
            Genres you have that {other['name']} doesn't: {", ".join(sorted(only_mine)) or "None"}<br>
            Genres {other['name']} has that you don't: {", ".join(sorted(only_theirs)) or "None"}
          </span>
        </div>""", unsafe_allow_html=True)

    # ── TAB 3: BPM Distribution ───────────────────────────────────────────────
    with tab_c3:
        st.markdown('<div class="section-header">BPM distribution — tempo profile</div>',
                    unsafe_allow_html=True)

        fig_bpm_compare = go.Figure()
        fig_bpm_compare.add_trace(go.Histogram(
            x=df["bpm"], name="You", nbinsx=20,
            marker_color="#5DCAA5", opacity=0.65,
        ))
        fig_bpm_compare.add_trace(go.Histogram(
            x=other_df["bpm"], name=other["name"], nbinsx=20,
            marker_color="#AFA9EC", opacity=0.65,
        ))
        fig_bpm_compare.update_layout(
            barmode="overlay", height=260,
            margin=dict(l=0, r=0, t=10, b=0),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            xaxis_title="BPM", yaxis_title="tracks",
            legend=dict(orientation="h", y=-0.2),
        )
        st.plotly_chart(fig_bpm_compare, use_container_width=True)

        # Summary stats
        stats = {
            "metric":   ["Avg BPM", "Median BPM", "Min BPM", "Max BPM", "BPM Std Dev"],
            "You":      [f"{df['bpm'].mean():.0f}",   f"{df['bpm'].median():.0f}",
                         f"{df['bpm'].min()}",         f"{df['bpm'].max()}",
                         f"{df['bpm'].std():.0f}"],
            other["name"]: [f"{other_df['bpm'].mean():.0f}",   f"{other_df['bpm'].median():.0f}",
                            f"{other_df['bpm'].min()}",         f"{other_df['bpm'].max()}",
                            f"{other_df['bpm'].std():.0f}"],
        }
        stats_df = pd.DataFrame(stats).set_index("metric")
        st.dataframe(stats_df, use_container_width=True)

        bpm_diff = abs(df["bpm"].mean() - other_df["bpm"].mean())
        faster   = "You" if df["bpm"].mean() > other_df["bpm"].mean() else other["name"]
        st.markdown(f"""
        <div class="insight-box">
          <div class="insight-label">🔍 conclusion</div>
          <strong>{faster}</strong> listens faster on average by
          <strong>{bpm_diff:.0f} BPM</strong>.
          {"That's a significant gap — your energy profiles are quite different."
           if bpm_diff > 20 else
           "A small gap — you share a similar sense of musical pace."
           if bpm_diff < 8 else
           "A moderate gap — you overlap at medium tempos but diverge at the extremes."}
        </div>""", unsafe_allow_html=True)

    # ── TAB 4: Language & Era ─────────────────────────────────────────────────
    with tab_c4:
        col_lang, col_era = st.columns(2)

        with col_lang:
            st.markdown('<div class="section-header">language mix</div>', unsafe_allow_html=True)
            all_langs = sorted(set(df["language"].unique()) | set(other_df["language"].unique()))
            my_lang_pct   = {l: len(df[df["language"] == l]) / len(df) * 100           for l in all_langs}
            them_lang_pct = {l: len(other_df[other_df["language"] == l]) / len(other_df) * 100 for l in all_langs}

            lang_compare = pd.DataFrame({
                "language": all_langs,
                "You":       [my_lang_pct.get(l, 0)   for l in all_langs],
                other["name"]:[them_lang_pct.get(l, 0) for l in all_langs],
            })
            lang_compare = lang_compare[(lang_compare["You"] > 0) |
                                         (lang_compare[other["name"]] > 0)]
            fig_lang_bar = go.Figure()
            fig_lang_bar.add_trace(go.Bar(name="You",
                                           x=lang_compare["language"], y=lang_compare["You"],
                                           marker_color="#5DCAA5"))
            fig_lang_bar.add_trace(go.Bar(name=other["name"],
                                           x=lang_compare["language"],
                                           y=lang_compare[other["name"]],
                                           marker_color="#AFA9EC"))
            fig_lang_bar.update_layout(
                barmode="group", height=260,
                margin=dict(l=0, r=0, t=10, b=0),
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                yaxis_title="%", xaxis_title="",
                showlegend=False,
            )
            st.plotly_chart(fig_lang_bar, use_container_width=True)

        with col_era:
            st.markdown('<div class="section-header">release era mix</div>', unsafe_allow_html=True)
            my_df_era   = df.copy()
            them_df_era = other_df.copy()
            my_df_era["decade"]   = (my_df_era["year"] // 10 * 10).astype(str) + "s"
            them_df_era["decade"] = (them_df_era["year"] // 10 * 10).astype(str) + "s"

            all_decades = sorted(
                set(my_df_era["decade"].unique()) | set(them_df_era["decade"].unique())
            )
            my_era_pct   = {d: len(my_df_era[my_df_era["decade"] == d]) / len(my_df_era) * 100
                            for d in all_decades}
            them_era_pct = {d: len(them_df_era[them_df_era["decade"] == d]) / len(them_df_era) * 100
                            for d in all_decades}

            era_compare = pd.DataFrame({
                "decade": all_decades,
                "You":       [my_era_pct.get(d, 0)   for d in all_decades],
                other["name"]:[them_era_pct.get(d, 0) for d in all_decades],
            })
            fig_era = go.Figure()
            fig_era.add_trace(go.Bar(name="You",
                                      x=era_compare["decade"], y=era_compare["You"],
                                      marker_color="#5DCAA5"))
            fig_era.add_trace(go.Bar(name=other["name"],
                                      x=era_compare["decade"], y=era_compare[other["name"]],
                                      marker_color="#AFA9EC"))
            fig_era.update_layout(
                barmode="group", height=260,
                margin=dict(l=0, r=0, t=10, b=0),
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                yaxis_title="%", xaxis_title="",
                showlegend=False,
            )
            st.plotly_chart(fig_era, use_container_width=True)

        # Legend (shared, since both charts hide it)
        st.markdown(f"""
        <div style="display:flex;gap:1.5rem;margin-top:-0.5rem;margin-bottom:0.5rem;">
          <span style="color:#5DCAA5;font-size:0.8rem;">■ You</span>
          <span style="color:#AFA9EC;font-size:0.8rem;">■ {other['name']}</span>
        </div>""", unsafe_allow_html=True)

        # Language overlap insight
        shared_langs = set(df["language"].unique()) & set(other_df["language"].unique())
        my_era_peak   = max(my_era_pct,   key=my_era_pct.get)
        them_era_peak = max(them_era_pct, key=them_era_pct.get)
        st.markdown(f"""
        <div class="insight-box">
          <div class="insight-label">🔍 conclusion</div>
          You share <strong>{len(shared_langs)} language(s)</strong> in common
          ({", ".join(sorted(shared_langs)) or "none"}).
          Your peak era is the <strong>{my_era_peak}</strong>;
          {other['name']}'s is the <strong>{them_era_peak}</strong>.
          {"You're anchored in the same decade — a strong cultural touchpoint." if my_era_peak == them_era_peak
           else "Different peak eras suggest your musical references come from different cultural moments."}
        </div>""", unsafe_allow_html=True)

    # ── TAB 5: Shared Tracks ──────────────────────────────────────────────────
    with tab_c5:
        my_titles    = set(df["title"].str.strip().str.lower())
        them_titles  = set(other_df["title"].str.strip().str.lower())
        shared_titles = my_titles & them_titles

        st.markdown(f'<div class="section-header">{len(shared_titles)} track(s) in both libraries</div>',
                    unsafe_allow_html=True)

        if shared_titles:
            shared_rows = df[df["title"].str.strip().str.lower().isin(shared_titles)]
            for _, row in shared_rows.iterrows():
                st.markdown(f"**{row['title']}** — {row['artist']}")
                st.caption(f"{row['genre']}  ·  {row['bpm']} BPM  ·  {row['year']}  ·  {row.get('language','—')}")
                st.divider()
        else:
            st.info("No exact title matches — but your shared genres and moods still suggest musical common ground.")

        # Recommended bridge tracks
        st.markdown('<div class="section-header">recommended bridge tracks</div>',
                    unsafe_allow_html=True)
        st.caption("Tracks from your library that match their top genres — a starting point for sharing.")
        top_their_genres = other_df["genre"].value_counts().head(2).index.tolist()
        bridge = df[df["genre"].isin(top_their_genres)].head(5)
        if not bridge.empty:
            for _, row in bridge.iterrows():
                st.markdown(f"**{row['title']}** — {row['artist']}")
                st.caption(f"{row['genre']}  ·  {row['bpm']} BPM  ·  reason: matches {other['name']}'s top genre")
                st.divider()
        else:
            st.info("No bridge tracks found in overlapping genres.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — CURATOR FEED
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Curator Feed":
    st.markdown('<div class="main-title">Curator Discovery</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">music found through people, not algorithms</div>',
                unsafe_allow_html=True)

    FEED = [
        {"curator": "Yuna K.", "match": 89, "track": "Anytime Anywhere", "artist": "milet",
         "genre": "Pop Ballad", "comment": "This one rewired how I think about endings. Nothing resolves, and that's the beauty."},
        {"curator": "Minhyuk P.", "match": 81, "track": "Idol", "artist": "YOASOBI",
         "genre": "J-Pop", "comment": "180 BPM of pure narrative momentum. The anime tie-in doesn't explain why it hits this hard."},
        {"curator": "Sojin L.", "match": 74, "track": "Running Wild", "artist": "Jin",
         "genre": "Pop Ballad", "comment": "The gap between what you say and what you feel — this song lives exactly there."},
        {"curator": "Jaeyoung C.", "match": 58, "track": "Exit Music (For a Film)", "artist": "Radiohead",
         "genre": "Alt-rock", "comment": "A song designed to play as the credits roll on something irreversible."},
    ]

    min_match = st.slider("Minimum match %", 50, 100, 70, step=5)
    filtered_feed = [f for f in FEED if f["match"] >= min_match]

    for item in filtered_feed:
        with st.container():
            cola, colb = st.columns([5, 1])
            with cola:
                st.markdown(f"**{item['track']}** — {item['artist']}  ·  {item['genre']}")
                st.markdown(f'<div class="track-comment">"{item["comment"]}"</div>',
                            unsafe_allow_html=True)
                st.caption(f"curated by {item['curator']} ({item['match']}% match)")
            with colb:
                st.markdown(f"### {item['match']}%")
            st.divider()

    if not filtered_feed:
        st.info("No curators above that match threshold. Try lowering the slider.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — SPOTIFY IMPORT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Spotify Import":
    try:
        from spotify_module import (
            get_auth_url, handle_callback, get_valid_token,
            fetch_liked_songs, fetch_audio_features, build_track_df,
        )
    except ImportError:
        st.error("spotify_module.py not found. Make sure it is in the same directory as app.py.")
        st.stop()

    st.markdown('<div class="main-title">🎧 Spotify Liked Songs</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="tagline">import your saved tracks and analyze your real taste</div>',
                unsafe_allow_html=True)

    if handle_callback():
        st.rerun()

    if "spotify_token" not in st.session_state:
        st.markdown("### Connect your Spotify account")
        st.info(
            "Credentials are stored securely in Streamlit Cloud secrets. "
            "Clicking the button below will redirect you to Spotify's official login page."
        )
        if st.button("🎵 Login with Spotify", type="primary"):
            auth_url = get_auth_url()
            st.markdown(f'<meta http-equiv="refresh" content="0; url={auth_url}">',
                        unsafe_allow_html=True)
            st.markdown(f"[Click here if not redirected automatically]({auth_url})")
        st.stop()

    access_token = get_valid_token()
    if not access_token:
        st.warning("Session expired — please log in again.")
        st.session_state.pop("spotify_token", None)
        st.rerun()

    col_logout, col_limit = st.columns([1, 2])
    with col_logout:
        if st.button("Logout"):
            for k in ["spotify_token", "_sp_oauth_state", "sp_liked_df"]:
                st.session_state.pop(k, None)
            st.rerun()
    with col_limit:
        fetch_limit = st.slider("How many tracks to import", 50, 500, 100, step=50)

    if st.button("⬇️ Fetch Liked Songs", type="primary") or "sp_liked_df" not in st.session_state:
        with st.spinner(f"Fetching up to {fetch_limit} liked songs…"):
            raw = fetch_liked_songs(access_token, fetch_limit)
        st.caption(f"API returned {len(raw)} raw items")
        ids = [item["track"]["id"] for item in raw if item.get("track") and item["track"].get("id")]
        st.caption(f"Valid track IDs: {len(ids)}")
        with st.spinner("Loading audio features…"):
            feats = fetch_audio_features(access_token, ids)
        st.caption(f"Audio features fetched: {len(feats)}")
        sp_df = build_track_df(raw, feats)
        st.session_state["sp_liked_df"] = sp_df
        if len(sp_df) == 0:
            st.warning("0 tracks imported. Add your Spotify email to User Management in the Spotify Dashboard.")
        else:
            st.success(f"Imported {len(sp_df)} tracks!")

    sp_df = st.session_state.get("sp_liked_df")
    if sp_df is None or sp_df.empty:
        st.stop()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tracks", len(sp_df))
    c2.metric("Artists", sp_df["artist"].nunique())
    c3.metric("Avg Popularity", f"{sp_df['popularity'].mean():.0f}/100")
    c4.metric("Avg Duration", f"{sp_df['duration_min'].mean():.1f} min")

    st.divider()
    s_tab1, s_tab2, s_tab3, s_tab4 = st.tabs(["🎵 Tracks", "📊 Popularity", "📅 Timeline", "📤 Export"])

    with s_tab1:
        for _, row in sp_df.head(50).iterrows():
            cola, colb = st.columns([4, 1])
            with cola:
                link = f"[**{row['title']}**]({row['spotify_url']})" if row.get('spotify_url') else f"**{row['title']}**"
                st.markdown(f"{link}  —  {row['artist']}")
                st.caption(f"{row['album']}  ·  {row['year']}")
            with colb:
                st.caption(f"⭐ {row['popularity']}")
                st.caption(f"⏱ {row['duration_min']} min")
            st.divider()

    with s_tab2:
        fig_pop = px.histogram(sp_df, x="popularity", nbins=20, height=220,
                                color_discrete_sequence=["#AFA9EC"],
                                labels={"popularity": "Spotify popularity (0–100)"})
        fig_pop.update_layout(margin=dict(l=0,r=0,t=10,b=0), bargap=0.05,
                               plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                               showlegend=False)
        st.plotly_chart(fig_pop, use_container_width=True)

        pop_tiers = sp_df["pop_tier"].value_counts().reset_index()
        pop_tiers.columns = ["tier", "count"]
        fig_tier = px.pie(pop_tiers, values="count", names="tier", hole=0.5,
                           color_discrete_sequence=px.colors.qualitative.Pastel, height=240)
        fig_tier.update_layout(margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_tier, use_container_width=True)

        niche_pct = len(sp_df[sp_df["pop_tier"] == "niche"]) / len(sp_df)
        viral_pct = len(sp_df[sp_df["pop_tier"] == "viral"]) / len(sp_df)
        st.markdown(f"""
        <div class="insight-box">
          <div class="insight-label">🔍 conclusion</div>
          <strong>{niche_pct:.0%}</strong> of your liked songs score below 30 popularity (niche).
          <strong>{viral_pct:.0%}</strong> score above 80 (viral).
          {"Your taste leans underground — you discover music before it reaches most people."
           if niche_pct > 0.35 else
           "You follow mainstream taste closely — your library mirrors what most people are listening to."
           if viral_pct > 0.4 else
           "Your taste sits in the middle ground — a mix of crowd favourites and quieter discoveries."}
        </div>""", unsafe_allow_html=True)

    with s_tab3:
        sp_df["year_int"] = pd.to_numeric(sp_df["year"], errors="coerce")
        year_counts = sp_df.dropna(subset=["year_int"]).groupby("year_int").size().reset_index(name="count")
        fig_yr = px.bar(year_counts, x="year_int", y="count", height=220,
                         color_discrete_sequence=["#5DCAA5"],
                         labels={"year_int": "release year", "count": "tracks"})
        fig_yr.update_layout(margin=dict(l=0,r=0,t=10,b=0),
                              plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                              showlegend=False)
        st.plotly_chart(fig_yr, use_container_width=True)

        top_artists = sp_df["artist"].value_counts().head(10).reset_index()
        top_artists.columns = ["artist", "count"]
        fig_art = px.bar(top_artists, x="count", y="artist", orientation="h",
                          color="count", color_continuous_scale="Purples", height=300,
                          labels={"count": "liked tracks", "artist": ""})
        fig_art.update_layout(coloraxis_showscale=False, margin=dict(l=0,r=0,t=10,b=0),
                               plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_art, use_container_width=True)

    with s_tab4:
        csv = sp_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV", data=csv,
                            file_name="soundself_liked_songs.csv", mime="text/csv")
        st.markdown("**Import top tracks into My Music Profile:**")
        top_n = st.slider("How many top-popularity tracks to import", 3, 20, 5)
        top_tracks = sp_df.nlargest(top_n, "popularity")
        if st.button(f"➕ Add {top_n} tracks to My Profile"):
            added = 0
            existing = {t["title"] for t in st.session_state.tracks}
            for _, row in top_tracks.iterrows():
                if row["title"] not in existing:
                    st.session_state.tracks.append({
                        "title": row["title"], "artist": row["artist"],
                        "genre": "Other", "bpm": int(row.get("bpm", 100)),
                        "mood": row.get("auto_mood", "morning ritual"),
                        "year": int(str(row["year"])[:4]) if str(row["year"]).isdigit() else datetime.now().year,
                        "language": "Other",
                        "comment": f"Popularity {row['popularity']}/100 — imported from Spotify",
                    })
                    added += 1
            st.success(f"Added {added} new tracks to My Music Profile!")