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

# --- CSS: 背景復活 & UI最適化 ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Roboto+Mono:wght@400;700&display=swap');
    
    /* 基本レイヤー設定 */
    html, body, [data-testid="stAppViewContainer"] {{
        background-color: #000201 !important;
        overflow-x: hidden;
    }}

    /* 1. 背景グリッドと光線の完全復活 */
    .stApp::before {{
        content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background-image: linear-gradient(rgba(0, 255, 65, 0.12) 1.5px, transparent 1.5px), 
                          linear-gradient(90deg, rgba(0, 255, 65, 0.12) 1.5px, transparent 1.5px);
        background-size: 45px 45px; z-index: -2; animation: grid-pulse 4s ease-in-out infinite alternate;
    }}
    .stApp::after {{
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: repeating-linear-gradient(0deg, rgba(0,0,0,0.15) 0px, rgba(0,0,0,0.15) 1px, transparent 1px, transparent 2px),
                    linear-gradient(to bottom, transparent 0%, rgba(0, 255, 65, 0.2) 50%, transparent 100%);
        background-size: 100% 100%, 100% 400%; z-index: -1; pointer-events: none; animation: scan 3.5s linear infinite;
    }}

    /* メインコンテンツの幅と余白 */
    .main .block-container {{
        max-width: 900px !important;
        padding: 2rem 1rem !important;
        background: transparent !important;
    }}

    /* ヘッダーエリア */
    .header-box {{
        text-align: center; margin-bottom: 50px; position: relative;
    }}
    .side-metrics-box {{
        position: absolute; right: 0; top: 20px; text-align: right;
        font-family: 'Roboto Mono'; font-size: 0.8rem; color: {CONFIG["neon_blue"]};
        border-right: 3px solid {CONFIG["neon_blue"]}; padding-right: 12px; line-height: 1.6; opacity: 0.8;
    }}
    .title-main {{
        color: #FFFFFF; font-family: 'Orbitron'; font-size: 2rem; letter-spacing: 12px;
        text-shadow: 0 0 15px {CONFIG["primary"]}; margin-top: 20px;
    }}
    .sat-icon {{
        font-size: 5.5rem; filter: drop-shadow(0 0 25px {CONFIG["primary"]});
        animation: float-sat 4s ease-in-out infinite;
    }}

    /* ニュースカード */
    .news-card {{
        background: rgba(0, 15, 5, 0.85); border: 1px solid rgba(0, 255, 65, 0.3);
        border-left: 8px solid {CONFIG["primary"]}; padding: 25px; margin-bottom: 20px;
        transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .news-card:hover {{
        border-color: {CONFIG["neon_pink"]}; border-left-color: {CONFIG["neon_pink"]};
        transform: translateX(10px); box-shadow: -10px 0 20px rgba(255, 0, 224, 0.15);
    }}
    .news-card a {{
        color: #e0e0e0 !important; font-size: 1.25rem; font-weight: 700;
        text-decoration: none !important; line-height: 1.4;
    }}

    /* ボタンコンソール（最下部） */
    .console-area {{
        display: flex; gap: 20px; justify-content: center; margin-top: 40px; padding-bottom: 60px;
    }}
    .stButton > button {{
        height: 55px !important; border-radius: 0px !important; font-family: 'Orbitron' !important;
        font-size: 1rem !important; font-weight: bold !important; letter-spacing: 2px !important;
        background: rgba(0, 255, 65, 0.05) !important; border: 2px solid {CONFIG["primary"]} !important;
        color: {CONFIG["primary"]} !important; transition: 0.2s !important;
    }}
    .stButton > button:hover {{
        background: {CONFIG["neon_pink"]} !important; color: white !important;
        border-color: {CONFIG["neon_pink"]} !important; box-shadow: 0 0 30px {CONFIG["neon_pink"]};
    }}

    /* アニメーション */
    @keyframes grid-pulse {{ 0% {{ opacity: 0.1; }} 100% {{ opacity: 0.5; }} }}
    @keyframes scan {{ 0% {{ background-position: 0 0, 0 -100%; }} 100% {{ background-position: 0 0, 0 100%; }} }}
    @keyframes float-sat {{ 0%, 100% {{ transform: translateY(0) rotate(5deg); }} 50% {{ transform: translateY(-15px) rotate(-5deg); }} }}

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

# ヘッダーエリア
st.markdown(f"""
<div class="header-box">
    <div class="side-metrics-box">
        >> LATENCY: 24ms<br>
        >> UPLINK: SECURE<br>
        >> STATUS: MONITORING<br>
        >> SOURCE: G_INTEL
    </div>
    <div class="sat-icon">{CONFIG["editor_avatar"]}</div>
    <div class="title-main">{CONFIG["site_name"]}</div>
</div>
""", unsafe_allow_html=True)

all_items = fetch_news()
JST = timezone(timedelta(hours=+9), 'JST')
display_items = all_items[:st.session_state.display_count]

# ニュースリスト表示
for entry in display_items:
    dt = "2026/--/--"
    if entry.get('published_parsed'):
        dt = datetime.fromtimestamp(time.mktime(entry.published_parsed), timezone.utc).astimezone(JST).strftime('%Y/%m/%d %H:%M')
    
    st.markdown(f"""
    <div class="news-card">
        <div style="color:{CONFIG['neon_pink']}; font-family:'Roboto Mono'; font-size:0.85rem; margin-bottom:8px; letter-spacing:1px;">
            // SYNC_TS: {dt}
        </div>
        <a href="{entry.link}" target="_blank">{entry.title}</a>
    </div>
    """, unsafe_allow_html=True)

# 最下部コンソールボタン
st.markdown('<div style="height:20px; border-top:1px solid rgba(0,255,65,0.2); margin-top:30px;"></div>', unsafe_allow_html=True)
c1, c2 = st.columns([1, 1])

with c1:
    if st.button("EXPAND DATABASE"):
        st.session_state.display_count += CONFIG["step_display"]
        st.rerun()

with c2:
    if st.session_state.display_count > CONFIG["initial_display"]:
        if st.button("DEFRAG SYSTEM"):
            st.session_state.display_count = CONFIG["initial_display"]
            st.rerun()
