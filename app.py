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

# --- CSS: 白い鼓動を削除、光線をさらに低速化 ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Roboto+Mono:wght@400;700&display=swap');
    
    /* 暗黒背景：絶対維持 */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main, .block-container {{
        background-color: #000201 !important;
        background: #000201 !important;
    }}

    /* 背景グリッド：白い鼓動（アニメーション）を削除し、静止 */
    .stApp {{
        background-image: 
            linear-gradient(rgba(0, 255, 65, 0.12) 1.5px, transparent 1.5px), 
            linear-gradient(90deg, rgba(0, 255, 65, 0.12) 1.5px, transparent 1.5px);
        background-size: 55px 55px;
        background-attachment: fixed;
        /* アニメーションを削除 */
    }}

    /* ★修正点：スキャンライン（光線）を24秒かけて極限までゆっくり動かす★ */
    .stApp::before {{
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(to bottom, transparent 0%, rgba(0, 255, 65, 0.2) 50%, transparent 51%, transparent 100%);
        background-size: 100% 400%; z-index: 10; pointer-events: none;
        animation: scan-ultra-slow 24s linear infinite; 
    }}

    /* UI幅、ヘッダー、カード、ボタンのスタイルを厳格に維持（いじらない） */
    .main .block-container {{ max-width: 1000px !important; padding-top: 3rem !important; }}
    .header-box {{ text-align: center; margin-bottom: 50px; position: relative; }}
    .title-main {{ color: #FFFFFF; font-family: 'Orbitron'; font-size: 2.2rem; letter-spacing: 12px; text-shadow: 0 0 20px {CONFIG["primary"]}; margin-top: 25px; }}
    .sat-icon {{ font-size: 6rem; filter: drop-shadow(0 0 35px {CONFIG["primary"]}); animation: float 4s ease-in-out infinite; }}

    .news-card {{
        background: rgba(0, 15, 5, 0.95) !important;
        border: 1px solid {CONFIG["primary"]} !important;
        border-left: 12px solid {CONFIG["primary"]} !important;
        padding: 30px; margin-bottom: 30px; transition: 0.3s;
    }}
    .news-card:hover {{ border-color: {CONFIG["neon_pink"]} !important; border-left-color: {CONFIG["neon_pink"]} !important; transform: translateX(10px) scale(1.02); box-shadow: 0 0 40px rgba(255, 0, 224, 0.3); }}
    .news-card a {{ color: white !important; font-size: 1.4rem; font-weight: 900; text-decoration: none !important; text-shadow: 0 0 8px {CONFIG["neon_blue"]}; }}

    .stButton > button {{
        height: 65px !important; border: 3px solid {CONFIG["primary"]} !important;
        background: rgba(0, 255, 65, 0.05) !important; color: {CONFIG["primary"]} !important;
        font-family: 'Orbitron' !important; font-size: 1.2rem !important; border-radius: 0px !important;
    }}
    .stButton > button:hover {{ background: {CONFIG["neon_pink"]} !important; color: white !important; border-color: {CONFIG["neon_pink"]} !important; }}

    /* アニメーション定義 */
    @keyframes scan-ultra-slow {{ 0% {{ background-position: 0 -100%; }} 100% {{ background-position: 0 300%; }} }}
    @keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-20px); }} }}
    header, footer {{ visibility: hidden !important; }}
</style>
""", unsafe_allow_html=True)

# --- LOGIC & RENDERING (変更なし) ---
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

st.markdown(f'<div class="header-box"><div class="sat-icon">{CONFIG["editor_avatar"]}</div><div class="title-main">{CONFIG["site_name"]}</div></div>', unsafe_allow_html=True)

all_items = fetch_news()
JST = timezone(timedelta(hours=+9), 'JST')
display_items = all_items[:st.session_state.display_count]

for entry in display_items:
    dt = datetime.fromtimestamp(time.mktime(entry.published_parsed), timezone.utc).astimezone(JST).strftime('%Y/%m/%d %H:%M') if entry.get('published_parsed') else "2026/--/--"
    st.markdown(f"""<div class="news-card"><div style="color:{CONFIG['neon_pink']}; font-family:'Roboto Mono'; font-size:0.95rem; margin-bottom:12px; font-weight:bold;">▶ SYNC_TS // {dt} JST</div><a href="{entry.link}" target="_blank">{entry.title}</a><div style="margin-top:15px; color:{CONFIG['primary']}; font-size:0.8rem; font-family:'Roboto Mono'; opacity:0.7;">>> INTEL_STATUS: VERIFIED <br>>> ACCESS_LEVEL: UNRESTRICTED</div></div>""", unsafe_allow_html=True)

st.markdown('<div style="height:40px;"></div>', unsafe_allow_html=True)
col1, col2 = st.columns([1.5, 1])
with col1:
    if st.button("[ EXPAND DATABASE ]"):
        st.session_state.display_count += CONFIG["step_display"]; st.rerun()
with col2:
    if st.session_state.display_count > CONFIG["initial_display"]:
        if st.button("[ DEFRAG / SHRINK ]"):
            st.session_state.display_count = CONFIG["initial_display"]; st.rerun()
