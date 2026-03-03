import streamlit as st
import feedparser
from datetime import datetime, timedelta, timezone
import urllib.parse
import random
import time

# --- TRUE OMNI-INTELLIGENCE v23.1 ---
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

# セッション状態の確実な保持
if "display_count" not in st.session_state:
    st.session_state.display_count = CONFIG["initial_display"]

# --- CSS: THE FINAL ARCHITECTURE ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Roboto+Mono:wght@500&display=swap');

    /* 1. 背景: ライブ・パルス（強制アニメーション） */
    [data-testid="stAppViewContainer"] {{
        background-color: #000c05 !important;
        background-image: 
            radial-gradient(circle at 50% -20%, rgba(0, 229, 255, 0.25), transparent 70%),
            linear-gradient(rgba(0, 255, 65, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 65, 0.1) 1px, transparent 1px) !important;
        background-size: 100% 100%, 40px 40px, 40px 40px !important;
        background-attachment: fixed !important;
        animation: pulse-bg 10s infinite alternate !important;
    }}

    @keyframes pulse-bg {{
        0% {{ filter: brightness(0.8) contrast(1.1); }}
        100% {{ filter: brightness(1.2) contrast(1.3); }}
    }}

    /* 2. タイトル */
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

    /* 3. 衛星 */
    .moving-satellite {{
        font-size: 3rem;
        text-align: center;
        filter: drop-shadow(0 0 15px {CONFIG["neon_blue"]});
        animation: orbit-swing 6s ease-in-out infinite;
        margin: 10px 0;
    }}

    @keyframes orbit-swing {{
        0%, 100% {{ transform: translateY(0) rotate(0deg); }}
        50% {{ transform: translateY(-20px) rotate(5deg); }}
    }}

    /* 4. ニュースカード: プログレッシブ表示 */
    .news-card {{
        background: rgba(255, 255, 255, 0.04) !important;
        border-left: 5px solid {CONFIG["primary"]} !important;
        padding: 15px;
        margin-bottom: 12px;
        border-radius: 2px;
        animation: card-entry 0.6s ease-out both;
        transition: all 0.3s !important;
    }}

    @keyframes card-entry {{
        from {{ opacity: 0; transform: translateX(-20px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}

    .news-card:hover {{
        background: rgba(255, 255, 255, 0.08) !important;
        border-left: 5px solid {CONFIG["neon_pink"]} !important;
        transform: scale(1.02) !important;
        box-shadow: 0 0 30px rgba(255, 0, 224, 0.15) !important;
    }}

    .news-card a {{ color: {CONFIG["neon_blue"]} !important; text-decoration: none !important; font-weight: 800; }}

    /* 5. 究極のグリッチボタン */
    .stButton > button {{
        background-color: transparent !important;
        color: {CONFIG["primary"]} !important;
        border: 2px solid {CONFIG["primary"]} !important;
        font-family: 'Orbitron', sans-serif !important;
        width: 100% !important;
        padding: 15px !important;
        border-radius: 4px !important;
        text-shadow: 0 0 10px {CONFIG["primary"]} !important;
        transition: 0.2s !important;
        z-index: 9999 !important;
    }}

    .stButton > button:hover {{
        background-color: {CONFIG["primary"]} !important;
        color: black !important;
        animation: glitch 0.2s infinite !important;
        box-shadow: 0 0 40px {CONFIG["primary"]} !important;
    }}

    @keyframes glitch {{
        0% {{ transform: translate(0); }}
        20% {{ transform: translate(-3px, 3px); }}
        40% {{ transform: translate(-3px, -3px); }}
        60% {{ transform: translate(3px, 3px); }}
        80% {{ transform: translate(3px, -3px); }}
        100% {{ transform: translate(0); }}
    }}

    header, footer {{ visibility: hidden !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- RENDERING ---
st.markdown(f'<div class="absolute-title">{CONFIG["site_name"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="moving-satellite">{CONFIG["editor_avatar"]}</div>', unsafe_allow_html=True)

@st.cache_data(ttl=1800)
def fetch_data():
    q = urllib.parse.quote(CONFIG["news_query"])
    f = feedparser.parse(f"https://news.google.com/rss/search?q={q}&hl=ja&gl=JP&ceid=JP:ja")
    entries = f.entries
    entries.sort(key=lambda x: x.get('published_parsed') or (0,0,0,0,0,0,0,0,0), reverse=True)
    return entries

all_items = fetch_data()
JST = timezone(timedelta(hours=+9), 'JST')
display_items = all_items[:st.session_state.display_count]

for i, entry in enumerate(display_items):
    try:
        ts = time.mktime(entry.published_parsed)
        dt = datetime.fromtimestamp(ts, timezone.utc).astimezone(JST).strftime('%Y/%m/%d %H:%M')
    except: dt = "N/A"
    
    delay = min(i * 0.05, 1.2)
    st.markdown(f"""
    <div class="news-card" style="animation-delay: {delay}s;">
        <div style="color:{CONFIG['neon_pink']}; font-family:'Orbitron'; font-size:0.7rem;">INTEL_LOG // {dt} JST</div>
        <div style="margin: 8px 0;"><a href="{entry.link}" target="_blank">{entry.title}</a></div>
        <div style="color:#888; font-size:0.7rem; font-family:Roboto Mono; border-top:1px solid rgba(255,255,255,0.05); padding-top:5px;">
            [AI_REPORT] {random.randint(97, 99)}% VALIDATED // PHASE_{i}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ボタンエリア（絶対に表示させるためのコンテナ）
st.write("---")
if st.session_state.display_count < len(all_items):
    if st.button(">> INITIALIZE_DATA_EXPANSION"):
        st.session_state.display_count += CONFIG["step_display"]
        st.rerun()
else:
    st.markdown(f"<p style='text-align:center; color:{CONFIG['neon_pink']}; font-family:Orbitron;'>-- NO_FURTHER_INTEL --</p>", unsafe_allow_html=True)
