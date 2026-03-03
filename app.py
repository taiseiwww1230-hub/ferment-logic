import streamlit as st
import feedparser
from datetime import datetime, timedelta, timezone
import urllib.parse
import time

# --- v25.1 NEURAL_PULSE (ライブ・エナジー・オーバーレイモデル) ---
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

# --- CSS: ライブパルス・エンジンの実装 ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Roboto+Mono&display=swap');
    
    /* 1. 基本背景の漆黒化 */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main {{
        background-color: #000502 !important;
        color: white !important;
        overflow-x: hidden;
    }}

    /* 2. 背景グリッドの鼓動 (Breathing Grid) */
    [data-testid="stAppViewContainer"]::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background-image: 
            linear-gradient(rgba(0, 255, 65, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 65, 0.1) 1px, transparent 1px);
        background-size: 40px 40px;
        z-index: 0;
        animation: grid-pulse 4s ease-in-out infinite alternate;
    }}

    /* 3. ライブ・スキャンライン (Scanning Line) */
    [data-testid="stAppViewContainer"]::after {{
        content: "";
        position: fixed;
        top: -100%; left: 0; width: 100%; height: 100%;
        background: linear-gradient(
            to bottom,
            transparent 0%,
            rgba(0, 255, 65, 0) 45%,
            rgba(0, 255, 65, 0.1) 50%,
            rgba(0, 255, 65, 0) 55%,
            transparent 100%
        );
        z-index: 9999;
        pointer-events: none;
        animation: scan-line 8s linear infinite;
    }}

    /* アニメーション定義 */
    @keyframes grid-pulse {{
        0% {{ opacity: 0.2; transform: scale(1.0); }}
        100% {{ opacity: 0.5; transform: scale(1.02); }}
    }}

    @keyframes scan-line {{
        0% {{ top: -100%; }}
        100% {{ top: 100%; }}
    }}

    /* タイトル：ネオン発光の深化 */
    .title {{
        color: #FFFFFF !important;
        font-family: 'Orbitron';
        font-size: 2.2rem;
        text-align: center;
        text-shadow: 0 0 10px {CONFIG["primary"]}, 0 0 20px {CONFIG["neon_blue"]}, 0 0 40px {CONFIG["neon_blue"]};
        padding: 40px 0 10px 0;
        letter-spacing: 6px;
        position: relative;
        z-index: 100;
    }}

    .satellite {{
        text-align: center;
        font-size: 4.5rem;
        filter: drop-shadow(0 0 30px {CONFIG["neon_blue"]});
        animation: satellite-float 5s ease-in-out infinite;
        margin-bottom: 20px;
        position: relative;
        z-index: 100;
    }}
    @keyframes satellite-float {{
        0%, 100% {{ transform: translateY(0) rotate(-5deg); filter: brightness(1); }}
        50% {{ transform: translateY(-20px) rotate(5deg); filter: brightness(1.5); }}
    }}

    /* ニュースカード：フローティング・エフェクト */
    .news-card {{
        background: rgba(0, 15, 5, 0.85) !important;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(0, 255, 65, 0.2) !important;
        border-left: 4px solid {CONFIG["primary"]} !important;
        padding: 25px;
        margin-bottom: 20px;
        border-radius: 4px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        z-index: 100;
    }}
    .news-card:hover {{
        transform: translateX(10px) scale(1.02);
        border-left: 4px solid {CONFIG["neon_pink"]} !important;
        box-shadow: -10px 0 30px rgba(0, 255, 65, 0.2);
        background: rgba(0, 30, 10, 0.95) !important;
    }}
    
    .news-card a {{
        color: {CONFIG["neon_blue"]} !important;
        font-size: 1.15rem;
        font-weight: 800;
        text-decoration: none !important;
        line-height: 1.4;
    }}

    /* ボタン：サイバーパンク・スタイル */
    .stButton > button {{
        background: rgba(0, 255, 65, 0.05) !important;
        color: {CONFIG["primary"]} !important;
        border: 1px solid {CONFIG["primary"]} !important;
        height: 60px !important;
        width: 100% !important;
        font-family: 'Orbitron' !important;
        letter-spacing: 2px;
        transition: 0.3s;
    }}
    .stButton > button:hover {{
        background: {CONFIG["primary"]} !important;
        color: black !important;
        box-shadow: 0 0 40px {CONFIG["primary"]};
    }}

    /* 不要なUIの排除 */
    header, footer {{ visibility: hidden !important; }}
    [data-testid="stSidebar"] {{ display: none; }}
</style>
""", unsafe_allow_html=True)

# --- データの描画 ---
st.markdown(f'<div class="title">{CONFIG["site_name"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="satellite">{CONFIG["editor_avatar"]}</div>', unsafe_allow_html=True)

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

for entry in display_items:
    try:
        ts = time.mktime(entry.published_parsed)
        dt = datetime.fromtimestamp(ts, timezone.utc).astimezone(JST).strftime('%Y/%m/%d %H:%M')
    except: dt = "2026/--/-- --:--"
    
    st.markdown(f"""
    <div class="news-card">
        <div style="color:{CONFIG['neon_pink']}; font-family:'Orbitron'; font-size:0.85rem; margin-bottom:8px;">
            <span style="opacity:0.7;">●</span> SYNC_TS // {dt} JST
        </div>
        <div><a href="{entry.link}" target="_blank">{entry.title}</a></div>
        <div style="margin-top:12px; color:rgba(0, 255, 65, 0.5); font-size:0.7rem; font-family:'Roboto Mono';">
            >> STATUS: DATA_RETRIEVED [OK] <br>
            >> ORIGIN: GOOGLE_NEWS_NODE_B4
        </div>
    </div>
    """, unsafe_allow_html=True)

if st.session_state.display_count < len(all_items):
    if st.button(">> DEPLOY_FURTHER_INTEL"):
        st.session_state.display_count += CONFIG["step_display"]
        st.rerun()
