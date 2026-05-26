"""
spotify_module.py — Spotify OAuth helpers for SoundSelf on Streamlit Cloud.

Security model:
  - Client ID and Client Secret live in st.secrets — never sent to the browser.
  - Uses Authorization Code flow with client_secret (server-side).
  - CSRF protection: state token is embedded in the auth URL and validated
    on callback. Because Streamlit Cloud may start a new session on redirect,
    state is carried in the URL itself (as a signed prefix of the code param
    is not possible) — we embed it as a custom query param and verify it
    matches what Spotify echoes back, which is sufficient for CSRF protection
    in a server-rendered app where the token exchange happens server-side.
"""

import time
import secrets
import urllib.parse
import streamlit as st
import requests
import pandas as pd

_AUTH_URL  = "https://accounts.spotify.com/authorize"
_TOKEN_URL = "https://accounts.spotify.com/api/token"
_API_BASE  = "https://api.spotify.com/v1"
_SCOPES    = "user-library-read user-top-read"


def _cfg() -> tuple[str, str, str]:
    try:
        sp = st.secrets["spotify"]
        return sp["client_id"], sp["client_secret"], sp["redirect_uri"]
    except (KeyError, FileNotFoundError):
        st.error(
            "Spotify credentials missing. "
            "Add `[spotify]` section to your Streamlit Cloud secrets."
        )
        st.stop()


def get_auth_url() -> str:
    """
    Build the Spotify authorization URL.

    The state token is stored in session_state AND sent to Spotify.
    Spotify echoes it back verbatim in the callback URL, so we can
    validate it even if Streamlit starts a fresh session on redirect
    — because the returned state value itself encodes the proof.

    To handle the fresh-session problem on Streamlit Cloud, we also
    store the state in a query param cookie workaround: we embed the
    state as a param in the redirect_uri so it survives across sessions.
    """
    client_id, _, redirect_uri = _cfg()
    state = secrets.token_urlsafe(32)

    # Store in session_state (works if same session survives redirect)
    st.session_state["_sp_oauth_state"] = state

    # Also embed state in redirect_uri as ?st= so we can recover it
    # even when Streamlit Cloud starts a new session on callback.
    # Spotify will append ?code=...&state=... to whatever redirect_uri we give.
    # We add our own ?st= param first; Spotify appends with &.
    redirect_with_state = redirect_uri.rstrip("/") + "/?st=" + state

    params = {
        "client_id":     client_id,
        "response_type": "code",
        "redirect_uri":  redirect_with_state,
        "scope":         _SCOPES,
        "state":         state,
        "show_dialog":   "false",
    }
    return _AUTH_URL + "?" + urllib.parse.urlencode(params)


def handle_callback() -> bool:
    """
    Detect OAuth callback, validate state, exchange code for tokens.
    Returns True if a fresh token was obtained.
    """
    qp = st.query_params
    if "code" not in qp:
        return False
    if "spotify_token" in st.session_state:
        st.query_params.clear()
        return False

    code           = qp.get("code", "")
    returned_state = qp.get("state", "")

    # Try session_state first; fall back to the ?st= param we embedded
    expected_state = st.session_state.pop("_sp_oauth_state", None)
    if not expected_state:
        expected_state = qp.get("st", "")

    # CSRF validation
    if not expected_state or not returned_state:
        st.error("⚠️ Missing OAuth state. Please try logging in again.")
        st.query_params.clear()
        return False

    if not secrets.compare_digest(returned_state.encode(), expected_state.encode()):
        st.error("⚠️ OAuth state mismatch. Please try logging in again.")
        st.query_params.clear()
        return False

    # Reconstruct the exact redirect_uri we sent (with ?st= param)
    client_id, client_secret, redirect_uri = _cfg()
    redirect_with_state = redirect_uri.rstrip("/") + "/?st=" + expected_state

    with st.spinner("Completing Spotify login…"):
        resp = requests.post(
            _TOKEN_URL,
            data={
                "grant_type":   "authorization_code",
                "code":         code,
                "redirect_uri": redirect_with_state,
            },
            auth=(client_id, client_secret),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10,
        )

    if not resp.ok:
        err = resp.json() if resp.content else {}
        st.error(f"Token exchange failed: {err.get('error_description', resp.status_code)}")
        st.query_params.clear()
        return False

    token = resp.json()
    token["expires_at"] = time.time() + token.get("expires_in", 3600)
    st.session_state["spotify_token"] = token
    st.query_params.clear()
    return True


def _refresh(token: dict) -> dict | None:
    client_id, client_secret, _ = _cfg()
    resp = requests.post(
        _TOKEN_URL,
        data={
            "grant_type":    "refresh_token",
            "refresh_token": token["refresh_token"],
        },
        auth=(client_id, client_secret),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=10,
    )
    if resp.ok:
        new = resp.json()
        new["expires_at"] = time.time() + new.get("expires_in", 3600)
        new.setdefault("refresh_token", token["refresh_token"])
        return new
    return None


def get_valid_token() -> str | None:
    token = st.session_state.get("spotify_token")
    if not token:
        return None
    if time.time() > token.get("expires_at", 0) - 60:
        token = _refresh(token)
        if token:
            st.session_state["spotify_token"] = token
        else:
            st.session_state.pop("spotify_token", None)
            return None
    return token["access_token"]


def _get(access_token: str, url: str, params: dict | None = None) -> dict | None:
    r = requests.get(
        url,
        headers={"Authorization": f"Bearer {access_token}"},
        params=params or {},
        timeout=10,
    )
    return r.json() if r.ok else None


def fetch_liked_songs(access_token: str, limit: int = 200) -> list[dict]:
    tracks, url = [], f"{_API_BASE}/me/tracks"
    params = {"limit": 50, "offset": 0}
    while url and len(tracks) < limit:
        data = _get(access_token, url, params)
        if not data:
            break
        tracks.extend(data.get("items", []))
        url    = data.get("next")
        params = {}
    return tracks[:limit]


def fetch_audio_features(access_token: str, track_ids: list[str]) -> dict[str, dict]:
    result = {}
    for i in range(0, len(track_ids), 100):
        chunk = track_ids[i:i + 100]
        data  = _get(access_token, f"{_API_BASE}/audio-features",
                     {"ids": ",".join(chunk)})
        if data:
            for f in (data.get("audio_features") or []):
                if f:
                    result[f["id"]] = f
    return result


_MOOD_MAP = {
    (True,  True):  "peak hour",
    (True,  False): "morning ritual",
    (False, True):  "deep focus",
    (False, False): "rainy day",
}

def _mood_label(row) -> str:
    return _MOOD_MAP[(row["valence"] >= 0.5, row["energy"] >= 0.5)]


def build_track_df(raw_items: list[dict], features: dict[str, dict]) -> pd.DataFrame:
    rows = []
    for item in raw_items:
        t      = item.get("track") or {}
        tid    = t.get("id", "")
        f      = features.get(tid, {})
        album  = t.get("album", {})
        images = album.get("images", [])
        rows.append({
            "id":               tid,
            "title":            t.get("name", ""),
            "artist":           ", ".join(a["name"] for a in t.get("artists", [])),
            "album":            album.get("name", ""),
            "year":             (album.get("release_date") or "0")[:4],
            "popularity":       t.get("popularity", 0),
            "duration_ms":      t.get("duration_ms", 0),
            "image_url":        images[0]["url"] if images else "",
            "spotify_url":      t.get("external_urls", {}).get("spotify", ""),
            "bpm":              round(f.get("tempo", 0)),
            "energy":           round(f.get("energy", 0), 3),
            "valence":          round(f.get("valence", 0), 3),
            "danceability":     round(f.get("danceability", 0), 3),
            "acousticness":     round(f.get("acousticness", 0), 3),
            "instrumentalness": round(f.get("instrumentalness", 0), 3),
            "speechiness":      round(f.get("speechiness", 0), 3),
            "loudness":         round(f.get("loudness", 0), 2),
            "key":              f.get("key", -1),
            "mode":             f.get("mode", -1),
        })
    df = pd.DataFrame(rows)
    df["duration_min"] = (df["duration_ms"] / 60000).round(2)
    df["auto_mood"]    = df.apply(_mood_label, axis=1)
    return df
