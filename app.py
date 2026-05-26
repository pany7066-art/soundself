import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

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
</style>
""", unsafe_allow_html=True)

# ── My tracks ────────────────────────────────────────────────────────────────
SAMPLE_TRACKS = [
    {
        "title": "Xia Dan Shui He Xie Zhe Wo Deng Jie Zu Pu",
        "artist": "Kau-kung Ngak-tui",
        "genre": "Hakka Folk",
        "bpm": 72,
        "mood": "nostalgia",
        "year": 1999,
        "language": "Hakka",
        "comment": "The river writes our genealogy. Ancestors carried this land on their backs so we could stand on it.",
    },
    {
        "title": "Abracadabra",
        "artist": "Lady Gaga",
        "genre": "Dance-pop",
        "bpm": 126,
        "mood": "peak hour",
        "year": 2025,
        "language": "English",
        "comment": "Finding magic inside chaos — that is the whole point of pop music done right.",
    },
    {
        "title": "Kawaii Dake Ja Dame Desu Ka",
        "artist": "CUTIE STREET",
        "genre": "J-Pop",
        "bpm": 118,
        "mood": "morning ritual",
        "year": 2024,
        "language": "Japanese",
        "comment": "Cuteness is not weakness. This song knows that better than most.",
    },
    {
        "title": "Don't Say You Love Me",
        "artist": "Jin",
        "genre": "Pop Ballad",
        "bpm": 85,
        "mood": "rainy day",
        "year": 2025,
        "language": "Korean",
        "comment": "Holding back the words makes every syllable heavier. Restraint as emotion.",
    },
    {
        "title": "Kaiju",
        "artist": "Sakanaction",
        "genre": "Alt-rock",
        "bpm": 180,
        "mood": "deep focus",
        "year": 2025,
        "language": "Japanese",
        "comment": "Knowledge itself is the monster — it devours you before you can name it.",
    },
    {
        "title": "Anytime Anywhere",
        "artist": "milet",
        "genre": "Pop Ballad",
        "bpm": 109,
        "mood": "nostalgia",
        "year": 2023,
        "language": "Japanese",
        "comment": "The ending of Frieren feels like grief and warmth arriving at the same moment.",
    },
]

SAMPLE_USERS = [
    {"name": "Yuna K.", "match": 89, "genres": ["J-Pop", "Pop Ballad", "Hakka Folk"],
     "tracks": ["Anytime Anywhere – milet", "Yoru ni Kakeru – YOASOBI"]},
    {"name": "Minhyuk P.", "match": 81, "genres": ["Dance-pop", "Alt-rock", "Pop Ballad"],
     "tracks": ["Abracadabra – Lady Gaga", "New Jeans – New Jeans"]},
    {"name": "Sojin L.", "match": 74, "genres": ["Pop Ballad", "J-Pop", "R&B"],
     "tracks": ["Don't Say You Love Me – Jin", "Blinding Lights – The Weeknd"]},
    {"name": "Jaeyoung C.", "match": 58, "genres": ["Alt-rock", "Electronic", "Dance-pop"],
     "tracks": ["Kaiju – Sakanaction", "Closer – NIN"]},
]

MOOD_TAGS = ["late-night drive", "rainy day", "deep focus",
             "morning ritual", "peak hour", "nostalgia"]

# ── Session state init ────────────────────────────────────────────────────────
if "tracks" not in st.session_state:
    st.session_state.tracks = SAMPLE_TRACKS.copy()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎵 SoundSelf")
    st.markdown("*share your music. share your worldview.*")
    st.divider()

    page = st.radio(
        "Navigate",
        ["My Music Profile", "Taste Compatibility", "Mood Tags",
         "Taste Map", "Curator Feed", "Spotify Import"],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown('<div class="section-header">add a track</div>', unsafe_allow_html=True)
    with st.form("add_track", clear_on_submit=True):
        new_title  = st.text_input("Title")
        new_artist = st.text_input("Artist")
        new_genre  = st.selectbox("Genre",
            ["Pop Ballad", "J-Pop", "Dance-pop", "Alt-rock", "Hakka Folk",
             "Indie", "Folk", "Electronic", "Trip-hop", "R&B", "Classical", "Jazz", "Other"])
        new_bpm    = st.number_input("BPM", 40, 200, 90)
        new_mood   = st.selectbox("Mood tag", MOOD_TAGS)
        new_comment= st.text_area("Your one-line comment", height=70)
        submitted  = st.form_submit_button("+ Add track")
        if submitted and new_title and new_artist:
            st.session_state.tracks.append({
                "title": new_title, "artist": new_artist, "genre": new_genre,
                "bpm": new_bpm, "mood": new_mood,
                "year": datetime.now().year, "comment": new_comment,
            })
            st.success(f"Added: {new_title}")

df = pd.DataFrame(st.session_state.tracks)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — MY MUSIC PROFILE
# ══════════════════════════════════════════════════════════════════════════════
if page == "My Music Profile":
    st.markdown('<div class="main-title">My Music World</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">a profile that speaks louder than words</div>',
                unsafe_allow_html=True)

    # ── Stats row ──
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tracks", len(df))
    c2.metric("Genres", df["genre"].nunique())
    c3.metric("Avg BPM", int(df["bpm"].mean()))
    c4.metric("Mood tags", df["mood"].nunique())

    st.divider()

    # ── Filter ──
    col_filter, _ = st.columns([2, 3])
    with col_filter:
        genre_filter = st.multiselect(
            "Filter by genre", options=df["genre"].unique().tolist(), default=[])

    display_df = df if not genre_filter else df[df["genre"].isin(genre_filter)]

    # ── Genre bar chart ──
    st.markdown('<div class="section-header">genre breakdown</div>', unsafe_allow_html=True)
    genre_counts = df["genre"].value_counts().reset_index()
    genre_counts.columns = ["genre", "count"]
    fig_genre = px.bar(
        genre_counts, x="genre", y="count",
        color="genre", color_discrete_sequence=px.colors.qualitative.Pastel,
        height=220,
    )
    fig_genre.update_layout(showlegend=False, margin=dict(l=0,r=0,t=10,b=0),
                            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                            xaxis=dict(title=""), yaxis=dict(title=""))
    st.plotly_chart(fig_genre, use_container_width=True)

    # ── Track cards ──
    st.markdown('<div class="section-header">your tracks</div>', unsafe_allow_html=True)
    for _, row in display_df.iterrows():
        with st.expander(f"**{row['title']}** — {row['artist']}  ·  {row['genre']}  ·  {row['bpm']} bpm"):
            st.markdown(f'<div class="track-comment">"{row["comment"]}"</div>',
                        unsafe_allow_html=True)
            st.caption(f"🏷️ {row['mood']}  ·  {row.get('year', '—')}")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — TASTE COMPATIBILITY
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Taste Compatibility":
    st.markdown('<div class="main-title">Taste Compatibility</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">discover who truly gets your curation</div>',
                unsafe_allow_html=True)

    # ── Match bars ──
    st.markdown('<div class="section-header">curators ranked by match score</div>',
                unsafe_allow_html=True)

    user_df = pd.DataFrame(SAMPLE_USERS)
    fig_match = go.Figure()
    fig_match.add_trace(go.Bar(
        x=user_df["match"],
        y=user_df["name"],
        orientation="h",
        marker_color=["#5DCAA5", "#378ADD", "#AFA9EC", "#D85A30"],
        text=[f"{m}%" for m in user_df["match"]],
        textposition="outside",
    ))
    fig_match.update_layout(
        height=220, margin=dict(l=0,r=40,t=10,b=0),
        xaxis=dict(range=[0,100], title="compatibility %"),
        yaxis=dict(title=""),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_match, use_container_width=True)

    st.divider()
    st.markdown('<div class="section-header">shared genre overlap</div>',
                unsafe_allow_html=True)

    my_genres = set(df["genre"].unique())
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

    st.markdown('<div class="section-header">curator profiles</div>',
                unsafe_allow_html=True)
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

    # ── Mood donut ──
    mood_counts = df["mood"].value_counts().reset_index()
    mood_counts.columns = ["mood", "count"]
    fig_mood = px.pie(
        mood_counts, values="count", names="mood", hole=0.55,
        color_discrete_sequence=px.colors.qualitative.Pastel,
        height=260,
    )
    fig_mood.update_layout(margin=dict(l=0,r=0,t=10,b=0),
                            paper_bgcolor="rgba(0,0,0,0)",
                            legend=dict(orientation="v", x=1, y=0.5))
    st.plotly_chart(fig_mood, use_container_width=True)

    st.divider()
    selected_mood = st.selectbox("Browse tracks by mood", ["— all —"] + MOOD_TAGS)

    filtered = df if selected_mood == "— all —" else df[df["mood"] == selected_mood]

    st.markdown(f'<div class="section-header">'
                f'{len(filtered)} track{"s" if len(filtered)!=1 else ""} found</div>',
                unsafe_allow_html=True)

    for _, row in filtered.iterrows():
        col_a, col_b = st.columns([3, 1])
        with col_a:
            st.markdown(f"**{row['title']}** — {row['artist']}")
            st.markdown(f'<div class="track-comment">"{row["comment"]}"</div>',
                        unsafe_allow_html=True)
        with col_b:
            st.caption(row["genre"])
            st.caption(f"{row['bpm']} bpm")
        st.divider()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — TASTE MAP
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Taste Map":
    st.markdown('<div class="main-title">Taste Map</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">your musical identity, visualized</div>',
                unsafe_allow_html=True)

    # Map BPM → mood axis (intensity), genre → electronic axis
    GENRE_X = {
        "Dance-pop": 0.92, "Electronic": 0.88, "Alt-rock": 0.72,
        "J-Pop": 0.60, "Pop Ballad": 0.45, "Trip-hop": 0.50,
        "R&B": 0.42, "Indie": 0.38, "Folk": 0.18,
        "Hakka Folk": 0.10, "Classical": 0.08, "Jazz": 0.28, "Other": 0.50,
    }

    df_map = df.copy()
    df_map["x"] = df_map["genre"].map(lambda g: GENRE_X.get(g, 0.5))
    df_map["y"] = (df_map["bpm"] - df_map["bpm"].min()) / (df_map["bpm"].max() - df_map["bpm"].min() + 1)
    df_map["size"] = 18

    fig_map = px.scatter(
        df_map, x="x", y="y", text="title",
        color="genre", size="size",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        hover_data={"title": True, "artist": True, "bpm": True,
                    "mood": True, "x": False, "y": False, "size": False},
        height=400,
        labels={"x": "← folk / acoustic · · · electronic / digital →",
                 "y": "← calm · · · intense →"},
    )
    fig_map.update_traces(textposition="top center", marker_opacity=0.85)
    fig_map.update_layout(
        margin=dict(l=0,r=0,t=20,b=0),
        plot_bgcolor="rgba(0,0,0,0.02)", paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=True, gridcolor="rgba(128,128,128,0.1)", range=[-0.05, 1.05]),
        yaxis=dict(showgrid=True, gridcolor="rgba(128,128,128,0.1)", range=[-0.05, 1.05]),
        legend=dict(orientation="h", y=-0.15),
    )
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown('<div class="section-header">BPM distribution by genre</div>',
                unsafe_allow_html=True)
    fig_bpm = px.box(
        df, x="genre", y="bpm", color="genre",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        height=240,
    )
    fig_bpm.update_layout(showlegend=False, margin=dict(l=0,r=0,t=10,b=0),
                           plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                           xaxis_title="", yaxis_title="bpm")
    st.plotly_chart(fig_bpm, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — CURATOR FEED
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
# Credentials live in Streamlit Cloud secrets — never exposed to the browser.
# Flow: Authorization Code (with client_secret) + state CSRF validation.
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Spotify Import":
    from spotify_module import (
        get_auth_url, handle_callback, get_valid_token,
        fetch_liked_songs, fetch_audio_features, build_track_df,
    )

    st.markdown('<div class="main-title">🎧 Spotify Liked Songs</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="tagline">import your saved tracks and analyze your real taste</div>',
                unsafe_allow_html=True)

    # ── Handle OAuth callback on every page load ───────────────────────────────
    # handle_callback() detects ?code=&state=, validates CSRF state, exchanges
    # the code server-side (client_secret never leaves the server), stores the
    # token in session_state, and clears the URL.
    if handle_callback():
        st.rerun()

    # ── Not yet authenticated ──────────────────────────────────────────────────
    if "spotify_token" not in st.session_state:
        st.markdown("### Connect your Spotify account")
        st.info(
            "Credentials are stored securely in Streamlit Cloud secrets. "
            "Clicking the button below will redirect you to Spotify's official "
            "login page over HTTPS — no credentials are handled by this app."
        )
        if st.button("🎵 Login with Spotify", type="primary"):
            auth_url = get_auth_url()          # state CSRF token set inside
            st.markdown(
                f'<meta http-equiv="refresh" content="0; url={auth_url}">',
                unsafe_allow_html=True,
            )
            st.markdown(f"[Click here if not redirected automatically]({auth_url})")
        st.stop()

    # ── Authenticated ──────────────────────────────────────────────────────────
    access_token = get_valid_token()           # auto-refreshes if needed
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
        with st.spinner("Loading audio features (BPM, energy, valence…)"):
            feats = fetch_audio_features(access_token, ids)
        st.caption(f"Audio features fetched: {len(feats)}")
        sp_df = build_track_df(raw, feats)
        st.session_state["sp_liked_df"] = sp_df
        if len(sp_df) == 0:
            st.warning("0 tracks imported. If API returned 0 items, add your Spotify account email to User Management in the Spotify Dashboard.")
        else:
            st.success(f"Imported {len(sp_df)} tracks!")

    sp_df = st.session_state.get("sp_liked_df")
    if sp_df is None or sp_df.empty:
        st.stop()

    # ── Stats ──────────────────────────────────────────────────────────────────
    import plotly.express as px
    import plotly.graph_objects as go

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tracks", len(sp_df))
    c2.metric("Avg BPM", int(sp_df["bpm"].mean()))
    c3.metric("Avg Energy", f"{sp_df['energy'].mean():.0%}")
    c4.metric("Avg Valence", f"{sp_df['valence'].mean():.0%}")

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs(["🎵 Track List", "🗺️ Taste Map", "📊 Audio Features", "📤 Export"])

    # ── Tab 1: Track list ──────────────────────────────────────────────────────
    with tab1:
        mood_sel = st.selectbox("Filter by auto-mood",
            ["— all —", "peak hour", "morning ritual", "deep focus", "rainy day", "nostalgia"])
        disp = sp_df if mood_sel == "— all —" else sp_df[sp_df["auto_mood"] == mood_sel]
        for _, row in disp.head(50).iterrows():
            cola, colb, colc = st.columns([3, 1, 1])
            with cola:
                link = f"[**{row['title']}**]({row['spotify_url']})" if row['spotify_url'] else f"**{row['title']}**"
                st.markdown(f"{link}  —  {row['artist']}")
                st.caption(row["album"] + "  ·  " + str(row["year"]))
            with colb:
                st.caption(f"♩ {row['bpm']} bpm")
                st.caption(f"⚡ energy {row['energy']:.0%}")
            with colc:
                st.caption(f"☀️ valence {row['valence']:.0%}")
                st.caption(row["auto_mood"])
            st.divider()
        if len(disp) > 50:
            st.info(f"Showing first 50 of {len(disp)} tracks. Export CSV for full list.")

    # ── Tab 2: Taste map (valence × energy) ───────────────────────────────────
    with tab2:
        st.markdown('<div class="section-header">valence (happiness) × energy — your emotional fingerprint</div>',
                    unsafe_allow_html=True)
        fig_taste = px.scatter(
            sp_df, x="valence", y="energy",
            color="auto_mood", hover_data=["title", "artist", "bpm"],
            color_discrete_sequence=px.colors.qualitative.Pastel,
            labels={"valence": "← sad · · · happy →", "energy": "← calm · · · intense →"},
            height=420,
            opacity=0.75,
        )
        fig_taste.update_layout(
            margin=dict(l=0,r=0,t=10,b=0),
            plot_bgcolor="rgba(0,0,0,0.02)", paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(range=[0, 1], showgrid=True, gridcolor="rgba(128,128,128,0.1)"),
            yaxis=dict(range=[0, 1], showgrid=True, gridcolor="rgba(128,128,128,0.1)"),
            legend=dict(orientation="h", y=-0.15),
        )
        # Quadrant labels
        for (x, y, txt) in [(0.25,0.85,"deep focus\n(dark + intense)"),
                             (0.75,0.85,"peak hour\n(happy + intense)"),
                             (0.25,0.15,"rainy day\n(dark + calm)"),
                             (0.75,0.15,"morning ritual\n(happy + calm)")]:
            fig_taste.add_annotation(x=x, y=y, text=txt, showarrow=False,
                                      font=dict(size=9, color="#aaa"), align="center")
        st.plotly_chart(fig_taste, use_container_width=True)

        st.markdown('<div class="section-header">BPM distribution</div>', unsafe_allow_html=True)
        fig_bpm2 = px.histogram(sp_df, x="bpm", nbins=30, height=200,
                                 color_discrete_sequence=["#5DCAA5"])
        fig_bpm2.update_layout(margin=dict(l=0,r=0,t=10,b=0),
                                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                                bargap=0.05, showlegend=False)
        st.plotly_chart(fig_bpm2, use_container_width=True)

    # ── Tab 3: Audio feature radar ─────────────────────────────────────────────
    with tab3:
        st.markdown('<div class="section-header">average audio profile</div>',
                    unsafe_allow_html=True)
        features = ["energy", "valence", "danceability", "acousticness",
                    "instrumentalness", "speechiness"]
        avg_vals = [sp_df[f].mean() for f in features]
        fig_radar = go.Figure(go.Scatterpolar(
            r=avg_vals + [avg_vals[0]],
            theta=features + [features[0]],
            fill="toself",
            fillcolor="rgba(93,202,165,0.2)",
            line=dict(color="#5DCAA5", width=2),
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(range=[0,1], showticklabels=True,
                                       tickfont=dict(size=9))),
            height=350, margin=dict(l=30,r=30,t=20,b=20),
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        st.markdown('<div class="section-header">danceability vs popularity</div>',
                    unsafe_allow_html=True)
        fig_dp = px.scatter(sp_df, x="danceability", y="popularity",
                             hover_data=["title","artist"], height=260,
                             color="energy", color_continuous_scale="Teal",
                             labels={"danceability":"danceability","popularity":"popularity"})
        fig_dp.update_layout(margin=dict(l=0,r=0,t=10,b=0),
                              plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                              coloraxis_showscale=False)
        st.plotly_chart(fig_dp, use_container_width=True)

    # ── Tab 4: Export ──────────────────────────────────────────────────────────
    with tab4:
        st.markdown("Download your full liked-songs dataset as CSV — use it in your SoundSelf profile or for further analysis.")
        csv = sp_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name="soundself_liked_songs.csv",
            mime="text/csv",
        )
        st.markdown("**Import top tracks into My Music Profile:**")
        top_n = st.slider("How many top-energy tracks to import", 3, 20, 5)
        top_tracks = sp_df.nlargest(top_n, "energy")
        if st.button(f"➕ Add {top_n} tracks to My Profile"):
            added = 0
            existing_titles = {t["title"] for t in st.session_state.tracks}
            for _, row in top_tracks.iterrows():
                if row["title"] not in existing_titles:
                    st.session_state.tracks.append({
                        "title":   row["title"],
                        "artist":  row["artist"],
                        "genre":   "Other",
                        "bpm":     int(row["bpm"]),
                        "mood":    row["auto_mood"],
                        "year":    int(str(row["year"])[:4]) if str(row["year"]).isdigit() else datetime.now().year,
                        "comment": f"Energy {row['energy']:.0%} · Valence {row['valence']:.0%} — imported from Spotify",
                    })
                    added += 1
            st.success(f"Added {added} new tracks to My Music Profile!")
