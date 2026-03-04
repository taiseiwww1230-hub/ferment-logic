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

# --- CSS: 限界突破の視覚支配ロジック ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Roboto+Mono:wght@400;700&display=swap');
    
    /* 1. 暗黒空間の強制確保（すべての層を透明化） */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main, .block-container {{
        background-color: transparent !important;
        background: transparent !important;
    }}

    /* 2. htmlの最底辺に「あからさまな」背景を固定 */
    html {{
        background-color: #000402 !important;
        /* 網目（グリッド）を拡大縮小させて「鼓動」を表現 */
        background-image: 
            linear-gradient(rgba(0, 255, 65, 0.2) 2px, transparent 2px), 
            linear-gradient(90deg, rgba(0, 255, 65, 0.2) 2px, transparent 2px);
        background-size: 50px 50px;
        background-position: center center;
        animation: grid-heartbeat 1.5s ease-in-out infinite; /* 1.5秒周期の鼓動 */
    }}

    /* 3. あからさまな「心電図パルス」 */
    html::before {{
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent 0%, {CONFIG["primary"]} 50%, transparent 100%);
        -webkit-mask-image: linear-gradient(0deg, transparent 49%, #fff 50%, transparent 51%);
        opacity: 0.6; z-index: -1;
        animation: pulse-horizontal 4s linear infinite;
    }}

    /* 4. あからさまな「スキャン光線」の復活 */
    html::after {{
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(to bottom, transparent 0%, rgba(0, 255, 65, 0.4) 50%, transparent 50.5%, transparent 100%);
        background-size: 100% 200%;
        z-index: 9999; pointer-events: none;
        animation: scan-ray 5s linear infinite; /* 5秒で一巡する光線 */
    }}

    /* アニメーション定義 */
    @keyframes grid-heartbeat {{
        0%, 100% {{ background-size: 50px 50px; opacity: 0.5; }}
        10% {{ background-size: 55px 55px; opacity: 1; }} /* 収縮 */
        20% {{ background-size: 50px 50px; opacity: 0.8; }}
        30% {{ background-size: 52px 52px; opacity: 1; }} /* 二度打ち */
    }}
    @keyframes pulse-horizontal {{
        0% {{ transform: translateX(-100%); opacity: 0; }}
        50% {{ opacity: 0.8; }}
        100% {{ transform: translateX(100%); opacity: 0; }}
    }}
    @keyframes scan-ray {{
        0% {{ background-position: 0 -100%; }}
        100% {{ background-position: 0 100%; }}
    }}

    /* コンテンツエリア */
    .block-container {{ max-width: 900px !important; padding-top: 4rem !important; }}
    .header-box {{ text-align: center; margin-bottom: 50px; }}
    .title-main {{
        color: #FFFFFF; font-family: 'Orbitron'; font-size: 2.2rem; letter-spacing: 12px;
        text-shadow: 0 0 25px {CONFIG["primary"]}; margin-top: 25px;
    }}
    .sat-icon {{ font-size: 6rem; filter: drop-shadow(0 0 40px {CONFIG["primary"]}); animation: float 3s ease-in-out infinite; }}

    /* ニュースカード */
    .news-card {{
        background: rgba(0, 10, 5, 0.9) !important;
        border: 2px solid {CONFIG["primary"]} !important;
        border-left: 15px solid {CONFIG["primary"]} !important;
        padding: 30px; margin-bottom: 25px; transition: 0.2s;
    }}
    .news-card:hover {{
        border-color: {CONFIG["neon_pink"]} !important;
        border-left-color: {CONFIG["neon_pink"]} !important;
        transform: scale(1.02); box-shadow: 0 0 50px rgba(255, 0, 224, 0.4);
    }}
    .news-card a {{ color: white !important; font-size: 1.4rem; font-weight: 900; text-decoration: none !important; }}

    /* 操作ボタン */
    .stButton > button {{
        height: 70px !important; border: 4px solid {CONFIG["primary"]} !important;
        background: rgba(0, 255, 65, 0.1) !important; color: {CONFIG["primary"]} !important;
        font-family: 'Orbitron' !important; font-size: 1.3rem !important;
    }}
    .stButton > button:hover {{ background: {CONFIG["neon_pink"]} !important; color: white !important; }}

    @keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-30px); }} }}
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
        <div style="color:{CONFIG['neon_pink']}; font-family:'Roboto Mono'; font-size:1rem; margin-bottom:12px;">
            <span style="animation: blink 0.5s infinite;">●</span> LIVE_FEED // {dt}
        </div>
        <a href="{entry.link}" target="_blank">{entry.title}</a>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div style="height:50px;"></div>', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("EXPAND"):
        st.session_state.display_count += CONFIG["step_display"]
        st.rerun()
with col2:
    if st.session_state.display_count > CONFIG["initial_display"]:
        if st.button("DEFRAG"):
            st.session_state.display_count = CONFIG["initial_display"]
            st.rerun()

st.markdown("""<style>@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }</style>""", unsafe_allow_html=True)
