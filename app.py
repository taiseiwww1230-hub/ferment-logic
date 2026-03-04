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

# --- CSS: 限界突破の背景支配ロジック ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Roboto+Mono:wght@400;700&display=swap');
    
    /* 1. 全てのStreamlit標準背景を「透明」へ強制上書き */
    [data-testid="stAppViewContainer"], 
    [data-testid="stHeader"], 
    .main, 
    .block-container {{
        background: transparent !important;
    }}

    /* 2. 最背面（html自体）に「あからさまな」サイバー背景を配置 */
    html {{
        background-color: #000502 !important;
        /* あえて太く、光らせたグリッド */
        background-image: 
            linear-gradient(rgba(0, 255, 65, 0.2) 2px, transparent 2px),
            linear-gradient(90deg, rgba(0, 255, 65, 0.2) 2px, transparent 2px);
        background-size: 60px 60px;
        background-attachment: fixed;
        animation: deep-pulse 5s ease-in-out infinite alternate;
    }}

    /* 3. 画面全体を走る「あからさまな」スキャンライン */
    html::after {{
        content: "";
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(
            to bottom,
            transparent 0%,
            rgba(0, 255, 65, 0) 45%,
            rgba(0, 255, 65, 0.4) 50%,
            rgba(0, 255, 65, 0) 55%,
            transparent 100%
        );
        background-size: 100% 400%;
        z-index: 9999;
        pointer-events: none;
        animation: hyper-scan 3s linear infinite;
    }}

    /* 4. メインコンテンツの浮き上がり */
    .block-container {{
        max-width: 900px !important;
        padding-top: 5rem !important;
    }}

    .header-box {{ text-align: center; margin-bottom: 60px; position: relative; }}
    .title-main {{
        color: #FFFFFF; font-family: 'Orbitron'; font-size: 2.2rem; letter-spacing: 12px;
        text-shadow: 0 0 20px {CONFIG["primary"]}, 0 0 40px {CONFIG["neon_blue"]};
        margin-top: 25px;
    }}
    .sat-icon {{
        font-size: 6rem; filter: drop-shadow(0 0 35px {CONFIG["primary"]});
        animation: hyper-float 4s ease-in-out infinite;
    }}

    /* ニュースカード：背景を少し濃くして視認性確保 */
    .news-card {{
        background: rgba(0, 8, 4, 0.92) !important;
        border: 2px solid {CONFIG["primary"]} !important;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.1);
        padding: 30px; margin-bottom: 25px; border-left: 12px solid {CONFIG["primary"]} !important;
        transition: 0.3s;
    }}
    .news-card:hover {{
        border-color: {CONFIG["neon_pink"]} !important;
        border-left: 12px solid {CONFIG["neon_pink"]} !important;
        transform: scale(1.02) translateY(-5px);
        box-shadow: 0 0 40px rgba(255, 0, 224, 0.3);
    }}
    .news-card a {{
        color: white !important; font-size: 1.4rem; font-weight: 900;
        text-decoration: none !important; text-shadow: 0 0 10px {CONFIG["neon_blue"]};
    }}

    /* ボタンコンソール（洗練版） */
    .stButton > button {{
        height: 65px !important; border-radius: 0px !important; font-family: 'Orbitron' !important;
        font-size: 1.2rem !important; font-weight: bold !important;
        background: rgba(0, 255, 65, 0.1) !important; border: 3px solid {CONFIG["primary"]} !important;
        color: {CONFIG["primary"]} !important; transition: 0.3s !important; width: 100% !important;
    }}
    .stButton > button:hover {{
        background: {CONFIG["neon_pink"]} !important; color: white !important;
        border-color: {CONFIG["neon_pink"]} !important; box-shadow: 0 0 40px {CONFIG["neon_pink"]};
    }}

    /* アニメーション定義 */
    @keyframes deep-pulse {{ 0% {{ opacity: 0.3; }} 100% {{ opacity: 0.8; }} }}
    @keyframes hyper-scan {{ 0% {{ background-position: 0 -100%; }} 100% {{ background-position: 0 300%; }} }}
    @keyframes hyper-float {{ 0%, 100% {{ transform: translateY(0) scale(1.0); }} 50% {{ transform: translateY(-25px) scale(1.1); }} }}

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
        <div style="color:{CONFIG['neon_pink']}; font-family:'Roboto Mono'; font-size:1rem; margin-bottom:12px; font-weight:bold;">
            [ ACCESS_POINT // {dt} ]
        </div>
        <a href="{entry.link}" target="_blank">{entry.title}</a>
    </div>
    """, unsafe_allow_html=True)

# 下部操作エリア
st.markdown('<div style="margin-top:50px;"></div>', unsafe_allow_html=True)
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
