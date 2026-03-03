import streamlit as st
import feedparser
from datetime import datetime, timedelta, timezone
import urllib.parse
import random
import time

# --- v24.6 VOID_PULSE (桎梏打破・物理オーバーレイモデル) ---
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

st.set_page_config(page_title=CONFIG["site_name"], layout="centered")

if "display_count" not in st.session_state:
    st.session_state.display_count = CONFIG["initial_display"]

# --- CSS: 画面の「一番手前」にパルスを固定する ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Roboto+Mono&display=swap');
    
    /* 1. 全ての標準要素を強制的に黒く塗りつぶす（桎梏からの解放） */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main {{
        background-color: #000804 !important;
        color: white !important;
    }}

    /* 2. 【核心】物理オーバーレイ・パルス */
    /* 背景ではなく「前面」に透明な膜を張り、そこを光らせる */
    [data-testid="stAppViewContainer"]::after {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        /* グリッドと中央の発光を強制描画 */
        background-image: 
            radial-gradient(circle at 50% 50%, rgba(0, 255, 65, 0.12), transparent 75%),
            linear-gradient(rgba(0, 255, 65, 0.08) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 65, 0.08) 1px, transparent 1px);
        background-size: 100% 100%, 40px 40px, 40px 40px;
        pointer-events: none; /* 下のボタンやリンクを触れるようにする */
        z-index: 999999; /* 全ての要素の「一番上」に配置 */
        animation: pulse-void 5s ease-in-out infinite alternate;
    }}

    @keyframes pulse-void {{
        0% {{ opacity: 0.3; filter: brightness(0.8); }}
        100% {{ opacity: 0.8; filter: brightness(1.4); }}
    }}

    /* タイトル：発光強化 */
    .title {{
        color: #FFFFFF !important;
        font-family: 'Orbitron';
        font-size: 2.2rem;
        text-align: center;
        text-shadow: 0 0 20px {CONFIG["neon_blue"]}, 0 0 30px {CONFIG["neon_blue"]};
        padding: 30px 0 10px 0;
        letter-spacing: 4px;
    }}

    /* 衛星：桎梏を超えて動く */
    .satellite {{
        text-align: center;
        font-size: 4rem;
        filter: drop-shadow(0 0 20px {CONFIG["neon_blue"]});
        animation: orbit-swing 6s ease-in-out infinite;
        position: relative;
        z-index: 10;
    }}
    @keyframes orbit-swing {{
        0%, 100% {{ transform: translateY(0) rotate(0deg); }}
        50% {{ transform: translateY(-15px) rotate(10deg); }}
    }}

    /* ニュースカード：ダーク・インテリジェンス */
    .news-card {{
        background: rgba(10, 25, 20, 0.9) !important;
        border: 1px solid rgba(0, 255, 65, 0.3) !important;
        border-left: 6px solid {CONFIG["primary"]} !important;
        padding: 20px;
        margin-bottom: 15px;
        border-radius: 2px;
        transition: 0.3s;
    }}
    .news-card:hover {{
        border-left: 6px solid {CONFIG["neon_pink"]} !important;
        background: rgba(20, 40, 30, 0.95) !important;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.2);
    }}
    
    .news-card a {{
        color: {CONFIG["neon_blue"]} !important;
        font-size: 1.1rem;
        font-weight: bold;
        text-decoration: none !important;
    }}

    /* ボタン：グリッチ */
    .stButton > button {{
        background: transparent !important;
        color: {CONFIG["primary"]} !important;
        border: 2px solid {CONFIG["primary"]} !important;
        height: 55px !important;
        width: 100% !important;
        font-family: 'Orbitron' !important;
    }}
    .stButton > button:hover {{
        background: {CONFIG["primary"]} !important;
        color: black !important;
        box-shadow: 0 0 30px {CONFIG["primary"]};
    }}

    header, footer {{ visibility: hidden !important; }}
</style>
""", unsafe_allow_html=True)

# --- RENDERING ---
st.markdown(f'<div class="title">{CONFIG["site_name"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="satellite">{CONFIG["editor_avatar"]}</div>', unsafe_allow_html=True)

# ニュース取得 (Google News RSS)
@st.cache_data(ttl=1800)
def fetch_news():
    q = urllib.parse.quote(CONFIG["query"])
    f = feedparser.parse(f"https://news.google.com/rss/search?q={q}&hl=ja&gl=JP&ceid=JP:ja")
    entries = f.entries
    entries.sort(key=lambda x: x.get('published_parsed') or (0,0,0,0,0,0,0,0,0), reverse=True)
    return entries

all_items = fetch_news()
JST = timezone(timedelta(hours=+9), 'JST')
display_items = all_items[:st.session_state.display_count]

for i, entry in enumerate(display_items):
    try:
        ts = time.mktime(entry.published_parsed)
        dt = datetime.fromtimestamp(ts, timezone.utc).astimezone(JST).strftime('%Y/%m/%d %H:%M')
    except: dt = "2026/--/-- --:--"
    
    st.markdown(f"""
    <div class="news-card">
        <div style="color:{CONFIG['neon_pink']}; font-family:'Orbitron'; font-size:0.8rem;">SYNC_TS // {dt} JST</div>
        <div style="margin: 10px 0;"><a href="{entry.link}" target="_blank">{entry.title}</a></div>
        <div style="color:rgba(255,255,255,0.6); font-size:0.75rem; border-top:1px solid rgba(0,255,65,0.1); padding-top:8px;">
            >> ANALYZING TREND... [OK]
        </div>
    </div>
    """, unsafe_allow_html=True)

# LOAD MORE
if st.session_state.display_count < len(all_items):
    if st.button(">> DEPLOY_FURTHER_INTEL"):
        st.session_state.display_count += CONFIG["step_display"]
        st.rerun()
