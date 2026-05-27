# 🎵 SoundSelf — Music Taste Sharing App

> *Share your music. Share your worldview. Connect with people who truly get your taste.*

SoundSelf is a Streamlit web dashboard where users curate their favorite tracks with personal commentary, visualize their musical identity, and discover other curators through taste compatibility — not algorithms.

**Live demo:** [soundself-sakanamango.streamlit.app](https://soundself-sakanamango.streamlit.app)

---

## ✨ Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | **My Music Profile** | Register tracks with a one-line personal comment. Browse by genre. View listening stats. |
| 2 | **Taste Compatibility** | See which other curators match your genre and mood profile (0–100% score). |
| 3 | **Mood Tag System** | Tag tracks with emotional contexts — rainy day, deep focus, peak hour — and filter by feeling. |
| 4 | **Taste Map** | 2D scatter plot of your music on genre × intensity axes. Your musical identity, visualized. |
| 5 | **Curator Discovery Feed** | Explore recently-added tracks from high-compatibility curators. |
| 6 | **Spotify Import** | Connect your Spotify account and import your Liked Songs for analysis. |

---

## 🚀 Getting Started

### Local Development

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/soundself.git
cd soundself

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your Spotify credentials
mkdir .streamlit
# Edit .streamlit/secrets.toml — see Spotify Setup section below

# 4. Launch the app
streamlit run app.py
```

App will open at `http://localhost:8501`

### Deploying to Streamlit Cloud

1. Push the repo to GitHub (make sure `.streamlit/secrets.toml` is in `.gitignore`)
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your GitHub repo
3. Set the main file path to `app.py`
4. Add your credentials under **Settings → Secrets** (see below)
5. Click **Deploy**

---

## 🎧 Spotify Setup

SoundSelf can import your Liked Songs directly from Spotify. To enable this:

### 1. Create a Spotify App

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Click **Create app** and give it any name
3. Under **Redirect URIs**, add:
   - For local dev: `http://localhost:8501`
   - For Streamlit Cloud: `https://your-app-name.streamlit.app/`
4. Save and copy your **Client ID** and **Client Secret**
5. Under **User Management**, add your own Spotify account email

### 2. Configure Secrets

Create `.streamlit/secrets.toml` locally (do **not** commit this file):

```toml
[spotify]
client_id     = "your_client_id"
client_secret = "your_client_secret"
redirect_uri  = "http://localhost:8501"   # or your Streamlit Cloud URL
```

For Streamlit Cloud, paste the same content into **Settings → Secrets**.

> **Note:** Spotify's audio features API (BPM, energy, valence) requires Extended Quota Mode approval. Without it, the app imports track metadata (title, artist, album, popularity, duration) and uses those for analysis instead.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Language | Python 3.10+ |
| Charts | Plotly |
| Data | Pandas |
| Auth | Spotify OAuth 2.0 (Authorization Code flow) |
| Hosting | Streamlit Cloud |
| Version Control | GitHub |

---

## 📁 Project Structure

```
soundself/
├── app.py                  # Main Streamlit application (all 6 features)
├── spotify_module.py       # Spotify OAuth + API helpers
├── requirements.txt        # Python dependencies
├── .gitignore              # Excludes secrets.toml from version control
└── README.md               # This file
```

---

## 🔐 Security Notes

- Spotify credentials are stored in Streamlit Secrets (server-side environment variables) and are never exposed to the browser
- Token exchange uses the Authorization Code flow with `client_secret` via HTTP Basic Auth — the secret never leaves the server
- Access tokens are stored only in server-side `session_state`, not in cookies or URL parameters

---

## 🗺️ Build Roadmap

- [x] **Step 1** — Basic layout, sample data, track card UI, genre filter, GitHub deploy
- [x] **Step 2** — Taste map scatter plot, mood tag filter, compatibility logic, add-a-track
- [x] **Step 3** — Spotify OAuth integration, Liked Songs import, popularity analysis
- [ ] **Step 4** — Album art display, audio features (pending Extended Quota approval), UI polish

---

## 👤 Author

**[Your Name]** — Arts & Big Data, Sungkyunkwan University  
Final Project | Prof. Jahwan Koo | Spring 2026

---

*Built with 🎧 and Python*
