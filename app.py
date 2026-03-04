import streamlit as st
import feedparser
from datetime import datetime, timedelta, timezone
import urllib.parse
import time
import re

# --- CONFIG ---
CONFIG = {
    "site_name": "FERMENT-LOGIC // INTELLIGENCE",
    "editor_avatar": "🛰️",
    "primary": "#00FF41",   
    "neon_blue": "#00E5FF", 
    "neon_pink": "#FF00E0", 
    "query": '(ヨーグルト OR 乳製品 OR 乳酸菌 OR 紅茶 OR 茶葉) AND ("新発売" OR "期間限定" OR "独自開発" OR "トレンド") when:7d',
    "initial_display": 15,
    "step_display": 15
}

st.set_page_config(page_title=CONFIG["site_name"], layout="wide")

if "display_count" not in st.session_state:
    st.session_state.display_count = CONFIG["initial_display"]

# --- CSS: 心電図（パルス）背景 & 網目復活 ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Roboto+Mono:wght@400;700&display=swap');
    
    /* 基本基盤 */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main {{
        background-color: #000201 !important;
    }}

    /* 1. 網目（グリッド）の完全復活：背景固定 */
    .stApp {{
        background-image: 
            linear-gradient(rgba(0, 255, 65, 0.1) 1px, transparent 1px), 
            linear-gradient(90deg, rgba(0, 255, 65, 0.1) 1px, transparent 1px);
        background-size: 40px 40px;
        background-attachment: fixed;
    }}

    /* 2. 心電図（パルス・ウェーブ）の描画：あからさまなインパクト */
    .stApp::before {{
        content: ""; position: fixed; top: 0; left: 0; width: 200%; height: 100%;
        background: linear-gradient(90deg, 
            transparent 0%, 
            {CONFIG["primary"]} 45%, 
            {CONFIG["neon_blue"]} 50%, 
            {CONFIG["primary"]} 55%, 
            transparent 100%);
        /* 心電図のような鋭いラインを作るためのマスク */
        -webkit-mask-image: linear-gradient(0deg, transparent 48%, #fff 49%, #fff 51%, transparent 52%);
        mask-image: linear-gradient(0deg, transparent 48%, #fff 49%, #fff 51%, transparent 52%);
        opacity: 0.3;
        z-index: 0;
        animation: pulse-flow 6s linear infinite;
        pointer-events: none;
    }}

    /* 3. 2本目のパルス（時間差） */
    .stApp::after {{
        content: ""; position: fixed; top: 20%; left: -100%; width: 200%; height: 100%;
        background: linear-gradient(90deg, transparent 0%, {CONFIG["neon_pink"]} 50%, transparent 100%);
        -webkit-mask-image: linear-gradient(0deg, transparent 40%, #fff 41%, #fff 42%, transparent 43%);
        opacity: 0.15;
        z-index: 0;
        animation: pulse-flow 10s linear infinite reverse;
        pointer-events: none;
    }}

    @keyframes pulse-flow {{
        0% {{ transform: translateX(-50%); }}
        100% {{ transform: translateX(0%); }}
    }}

    /* コンテンツの浮き上がり（カードの可読性を守る） */
    .main .block-container {{
        max-width: 900px !important;
        position: relative;
        z-index: 10; /* 背景より上に配置 */
    }}

    /* ニュースカードのデザイン（image_d9d4ff.pngのグリーン枠をリスペクト） */
    .news-card {{
        background: rgba(0, 15, 8, 0.96);
        border: 2px solid {CONFIG["primary"]};
        border-radius: 4px;
        padding: 30px; margin-bottom: 25px;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.1);
        transition: 0.3s;
    }}
    .news-card:hover {{
        border-color: {CONFIG["neon_pink"]};
        box-shadow: 0 0 35px rgba(255, 0, 224, 0.25);
        transform: translateY(-5px);
    }}
    .news-card a {{
        color: #FFFFFF !important; font-size: 1.35rem; font-weight: 900;
        text-decoration: none !important; text-shadow: 0 0 8px {CONFIG["neon_blue"]};
    }}

    /* タイトル & 衛星 */
    .header-box {{ text-align: center; margin-bottom: 50px; }}
    .title-main {{
        color: #FFFFFF; font-family: 'Orbitron'; font-size: 2.2rem; letter-spacing: 12px;
        text-shadow: 0 0 20px {CONFIG["primary"]}; margin-top: 25px;
    }}
    .sat-icon {{ font-size: 6rem; filter: drop-shadow(0 0 30px {CONFIG["primary"]}); animation: float 4s ease-in-out infinite; }}

    /* 操作ボタン（DEFRAGを横並び） */
    .stButton > button {{
        height: 60px !important; border: 2px solid {CONFIG["primary"]} !important;
        background: rgba(0, 255, 65, 0.05) !important; color: {CONFIG["primary"]} !important;
        font-family: 'Orbitron' !important; font-size: 1.1rem !important; transition: 0.3s !important;
    }}
    .stButton > button:hover {{
        background: {CONFIG["neon_pink"]} !important; color: white !important; border-color: {CONFIG["neon_pink"]} !important;
    }}

    @keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-20px); }} }}
    header, footer {{ visibility: hidden !important; }}
</style>
""", unsafe_allow_html=True)

# --- LOGIC ---
@st.cache_data(ttl=60)
def fetch_news():
    q = urllib.parse.quote(CONFIG["query"])
    f = feedparser.parse(f"https://news.google.com/rss/search?q={q}&hl=ja&gl=JP&ceid=JP:ja")
    entries = f.entries
    unique_entries = []
    seen = set()
    for entry in entries:
        fp = re.sub(r'\s+', '', entry.title)[:20]
        if fp not in seen:
            unique_entries.append(entry)
            seen.add(fp)
    return unique_entries

# --- RENDERING ---
st.markdown(f"""
<div class="header-box">
    <div class="sat-icon">{CONFIG["editor_avatar"]}</div>
    <div class="title-main">{CONFIG["site_name"]}</div>
</div>
""", unsafe_allow_html=True)

all_items = fetch_news()
JST = timezone(timedelta(hours=+9), 'JST')
display_items = all_items[:st.session_state.display_count]

for entry in display_items:
    dt = datetime.fromtimestamp(time.mktime(entry.published_parsed), timezone.utc).astimezone(JST).strftime('%Y/%m/%d %H:%M') if entry.get('published_parsed') else "2026/--/--"
    st.markdown(f"""
    <div class="news-card">
        <div style="color:{CONFIG['neon_pink']}; font-family:'Roboto Mono'; font-size:0.9rem; margin-bottom:12px;">
            <span style="animation: blink 1s infinite;">▶</span> SYNC_TIMESTAMP // {dt}
        </div>
        <a href="{entry.link}" target="_blank">{entry.title}</a>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div style="height:50px;"></div>', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("EXPAND DATABASE"):
        st.session_state.display_count += CONFIG["step_display"]
        st.rerun()
with col2:
    if st.session_state.display_count > CONFIG["initial_display"]:
        if st.button("DEFRAG SYSTEM"):
            st.session_state.display_count = CONFIG["initial_display"]
            st.rerun()

st.markdown("""<style>@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }</style>""", unsafe_allow_html=True)
