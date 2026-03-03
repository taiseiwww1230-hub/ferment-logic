import streamlit as st
import feedparser
from datetime import datetime, timedelta, timezone
import urllib.parse
import random
import time

# --- EXECUTIVE TERMINAL v22.0 (Neon Response) ---
CONFIG = {
    "site_name": "FERMENT-LOGIC // INTELLIGENCE",
    "editor_name": "CORE_INTELLIGENCE",
    "editor_avatar": "🛰️",
    "primary": "#00FF41",   
    "neon_blue": "#00E5FF", 
    "neon_pink": "#FF00E0", 
    "news_query": '(ヨーグルト OR 乳製品 OR 乳酸菌 OR 紅茶 OR 茶葉) AND ("新発売" OR "期間限定" OR "独自開発" OR "トレンド") when:7d',
    "initial_display": 15,
    "step_display": 15
}

st.set_page_config(page_title=CONFIG["site_name"], page_icon="🧬", layout="centered")

if "display_count" not in st.session_state:
    st.session_state.display_count = CONFIG["initial_display"]

# --- CSS: NEON INTERACTION & COMPACT UI ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Roboto+Mono:wght@500&display=swap');

    [data-testid="stAppViewContainer"] {{
        background-color: #000c05 !important;
        background-image: 
            radial-gradient(circle at 50% -20%, rgba(0, 229, 255, 0.2), transparent 70%),
            linear-gradient(rgba(0, 255, 65, 0.08) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 65, 0.08) 1px, transparent 1px) !important;
        background-size: 100% 100%, 40px 40px, 40px 40px !important;
        background-attachment: fixed !important;
    }}

    .absolute-title {{
        color: #FFFFFF !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 900 !important;
        font-size: 1.8rem !important;
        text-align: center !important;
        letter-spacing: 4px !important;
        padding-top: 25px !important;
        text-shadow: 0 0 10px #FFF, 0 0 20px {CONFIG["neon_blue"]} !important;
    }}

    .moving-satellite {{
        font-size: 3rem;
        text-align: center;
        filter: drop-shadow(0 0 15px {CONFIG["neon_blue"]});
        animation: orbit-swing 6s ease-in-out infinite;
        margin: 15px 0;
    }}

    @keyframes orbit-swing {{
        0%, 100% {{ transform: translate(0, 0) rotate(0deg); }}
        50% {{ transform: translate(0, -20px) rotate(0deg); }}
    }}

    /* ニュースカードの基本スタイル */
    .news-card {{
        background: rgba(255, 255, 255, 0.04) !important;
        border-left: 5px solid {CONFIG["primary"]} !important;
        padding: 15px;
        margin-bottom: 12px;
        border-radius: 2px;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important; /* なめらかな変化 */
        cursor: pointer;
    }}

    /* ★ ニュースカード：ホバー時の反応を追加 ★ */
    .news-card:hover {{
        background: rgba(255, 255, 255, 0.08) !important;
        border-left: 5px solid {CONFIG["neon_pink"]} !important; /* ピンクに変化 */
        transform: translateX(8px) !important; /* 右に少しズレる躍動感 */
        box-shadow: 0 0 20px rgba(255, 0, 224, 0.2) !important; /* ピンクの発光 */
    }}

    .news-card a {{
        color: {CONFIG["neon_blue"]} !important;
        font-size: 1.1rem !important;
        font-weight: 800 !important;
        text-decoration: none !important;
        transition: color 0.3s !important;
    }}
    
    /* ホバー時にリンクの色も微調整 */
    .news-card:hover a {{
        color: #FFFFFF !important;
    }}

    div.stButton > button {{
        background-color: transparent !important;
        color: {CONFIG["primary"]} !important;
        border: 2px solid {CONFIG["primary"]} !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 1rem !important;
        width: 100% !important;
        border-radius: 5px !important;
        padding: 10px 0 !important;
        transition: 0.3s !important;
        text-shadow: 0 0 10px {CONFIG["primary"]} !important;
    }}
    div.stButton > button:hover {{
        background-color: {CONFIG["primary"]} !important;
        color: black !important;
    }}

    header, footer {{ visibility: hidden !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown(f'<div class="absolute-title">{CONFIG["site_name"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="moving-satellite">{CONFIG["editor_avatar"]}</div>', unsafe_allow_html=True)

# --- DATA ---
@st.cache_data(ttl=1800)
def fetch_all_data():
    q = urllib.parse.quote(CONFIG["news_query"])
    f = feedparser.parse(f"https://news.google.com/rss/search?q={q}&hl=ja&gl=JP&ceid=JP:ja")
    entries = f.entries
    entries.sort(key=lambda x: x.get('published_parsed') or (0,0,0,0,0,0,0,0,0), reverse=True)
    return entries

all_items = fetch_all_data()
JST = timezone(timedelta(hours=+9), 'JST')

display_items = all_items[:st.session_state.display_count]

for entry in display_items:
    try:
        ts = time.mktime(entry.published_parsed)
        dt = datetime.fromtimestamp(ts, timezone.utc).astimezone(JST).strftime('%Y/%m/%d %H:%M')
    except: dt = "N/A"

    # HTML構造内に hover の反応が反映されるようにクラスを維持
    st.markdown(f"""
    <div class="news-card">
        <div style="color:{CONFIG['neon_pink']}; font-family:'Orbitron'; font-size:0.7rem;">INTEL_LOG // {dt} JST</div>
        <div style="margin: 8px 0;"><a href="{entry.link}" target="_blank">{entry.title}</a></div>
        <div style="color:#888; font-size:0.75rem; font-family:Roboto Mono;">[AI_REPORT] 分析完了 // {random.randint(97, 99)}% SYNC</div>
    </div>
    """, unsafe_allow_html=True)

# --- MORE INFO BUTTON ---
if st.session_state.display_count < len(all_items):
    if st.button(">> LOAD_MORE_INTELLIGENCE"):
        st.session_state.display_count += CONFIG["step_display"]
        st.rerun()
else:
    st.markdown(f"<p style='text-align:center; color:{CONFIG['neon_pink']}; font-family:Orbitron; font-size:0.8rem;'>-- ALL_DATA_RETRIEVED --</p>", unsafe_allow_html=True)
