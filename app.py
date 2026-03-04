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

# --- CSS: 基盤情報の完全固定と余白の装飾 ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Roboto+Mono:wght@400;700&display=swap');
    
    /* 1. 背景の暗黒化とグリッドの復活 */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main {{
        background-color: #000201 !important;
    }}
    .stApp {{
        background-image: 
            linear-gradient(rgba(0, 255, 65, 0.15) 1.5px, transparent 1.5px), 
            linear-gradient(90deg, rgba(0, 255, 65, 0.15) 1.5px, transparent 1.5px);
        background-size: 50px 50px;
        background-attachment: fixed;
    }}

    /* 2. 重厚なスキャンライン（減速） */
    [data-testid="stAppViewContainer"]::after {{
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(to bottom, transparent 0%, rgba(0, 255, 65, 0.15) 50%, transparent 100%);
        background-size: 100% 400%; z-index: 1000; pointer-events: none;
        animation: scan-slow 8s linear infinite;
    }}

    /* 3. 両端の余白を埋める「システム・オーバーレイ」 */
    @media (min-width: 1200px) {{
        body::before {{
            content: "SYS_COORDINATES: 35.6895° N, 139.6917° E // NODE_ACTIVE // 100111001";
            position: fixed; left: 30px; top: 50%; writing-mode: vertical-rl;
            font-family: 'Roboto Mono'; font-size: 0.8rem; color: {CONFIG["primary"]}; opacity: 0.4; z-index: 5;
        }}
        body::after {{
            content: ">> DATABASE_INTEL_STREAM\\A >> ENCRYPTED_CONNECTION\\A >> STATUS: SECURE";
            white-space: pre; position: fixed; right: 30px; top: 50%;
            font-family: 'Roboto Mono'; font-size: 0.8rem; color: {CONFIG["neon_blue"]}; opacity: 0.4; z-index: 5;
            border-right: 2px solid {CONFIG["neon_blue"]}; padding-right: 10px;
        }}
    }}

    /* 4. コンテンツ配置の最適化 */
    .main .block-container {{
        max-width: 900px !important; padding: 2rem 0 !important;
    }}

    /* タイトル & 衛星 */
    .header-box {{ text-align: center; margin-bottom: 40px; }}
    .title-main {{
        color: #FFFFFF; font-family: 'Orbitron'; font-size: 2rem; letter-spacing: 10px;
        text-shadow: 0 0 15px {CONFIG["primary"]}; margin-top: 20px;
    }}
    .sat-icon {{ font-size: 6rem; filter: drop-shadow(0 0 25px {CONFIG["primary"]}); animation: float 4s ease-in-out infinite; }}

    /* ニュースカード */
    .news-card {{
        background: rgba(0, 12, 6, 0.95); border: 1px solid {CONFIG["primary"]};
        border-left: 10px solid {CONFIG["primary"]}; padding: 30px; margin-bottom: 25px;
        transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    .news-card:hover {{ border-color: {CONFIG["neon_pink"]}; border-left-color: {CONFIG["neon_pink"]}; transform: scale(1.03); }}
    .news-card a {{ color: white !important; font-size: 1.3rem; font-weight: 900; text-decoration: none !important; text-shadow: 0 0 5px {CONFIG["neon_blue"]}; }}

    /* ボタンコンソール */
    .stButton > button {{
        height: 60px !important; width: 100% !important; border-radius: 0px !important;
        font-family: 'Orbitron' !important; font-size: 1.1rem !important;
        background: rgba(0, 255, 65, 0.05) !important; border: 2px solid {CONFIG["primary"]} !important;
        color: {CONFIG["primary"]} !important; transition: 0.3s !important;
    }}
    .stButton > button:hover {{ background: {CONFIG["neon_pink"]} !important; color: white !important; box-shadow: 0 0 40px {CONFIG["neon_pink"]}; }}

    @keyframes scan-slow {{ 0% {{ background-position: 0 -100%; }} 100% {{ background-position: 0 300%; }} }}
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
        <div style="color:{CONFIG['neon_pink']}; font-family:'Roboto Mono'; font-size:0.9rem; margin-bottom:10px;">
            // SYNC_TS: {dt}
        </div>
        <a href="{entry.link}" target="_blank">{entry.title}</a>
    </div>
    """, unsafe_allow_html=True)

# 下部コンソール
st.markdown('<div style="height:40px;"></div>', unsafe_allow_html=True)
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
