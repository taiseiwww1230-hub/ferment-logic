import streamlit as st
import feedparser
from datetime import datetime, timedelta, timezone
import urllib.parse
import random
import time

# --- v24.5 ABSOLUTE_PULSE (静止画レイヤー+物理明滅モデル) ---
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

# --- CSS: どんな「白背景」も貫通して闇とパルスを作る ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Roboto+Mono&display=swap');
    
    /* 1. 全ての標準要素を強制的に闇へ落とす */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main {{
        background-color: #000804 !important;
        background-image: none !important;
    }}

    /* 2. ライブパルス・レイヤー：擬似的に「奥行き」と「鼓動」を作る */
    .main::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        /* グリッド風の静止画的テクスチャをCSSで高速描画 */
        background-image: 
            radial-gradient(circle at 50% 50%, rgba(0, 255, 65, 0.1), transparent 85%),
            repeating-linear-gradient(0deg, transparent 0, transparent 39px, rgba(0, 255, 65, 0.05) 40px),
            repeating-linear-gradient(90deg, transparent 0, transparent 39px, rgba(0, 255, 65, 0.05) 40px);
        z-index: -1;
        /* このレイヤー自体を明滅（パルス）させる */
        animation: pulse-engine 4s ease-in-out infinite alternate;
    }}

    @keyframes pulse-engine {{
        0% {{ opacity: 0.5; filter: contrast(1.2); }}
        100% {{ opacity: 1; filter: contrast(1.5) brightness(1.2); }}
    }}

    /* 3. タイトル：ネオン・グローを最大化 */
    .title {{
        color: #FFFFFF !important;
        font-family: 'Orbitron';
        font-size: 2.2rem;
        text-align: center;
        text-shadow: 0 0 20px {CONFIG["neon_blue"]}, 0 0 40px rgba(0, 229, 255, 0.5);
        padding: 30px 0 10px 0;
        letter-spacing: 5px;
    }}

    /* 4. 衛星：躍動感をキープ */
    .satellite {{
        text-align: center;
        font-size: 4rem;
        filter: drop-shadow(0 0 20px {CONFIG["neon_blue"]});
        animation: orbit-swing 6s ease-in-out infinite;
        margin-bottom: 25px;
    }}
    @keyframes orbit-swing {{
        0%, 100% {{ transform: translateY(0) rotate(0deg) scale(1); }}
        50% {{ transform: translateY(-20px) rotate(8deg) scale(1.05); }}
    }}

    /* 5. ニュースカード：白背景環境でも浮き出るように設計 */
    .news-card {{
        background: rgba(10, 20, 15, 0.8) !important;
        border: 1px solid rgba(0, 255, 65, 0.2) !important;
        border-left: 6px solid {CONFIG["primary"]} !important;
        padding: 18px;
        margin-bottom: 15px;
        border-radius: 4px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .news-card:hover {{
        border-left: 6px solid {CONFIG["neon_pink"]} !important;
        transform: scale(1.02) translateX(5px);
        background: rgba(20, 30, 25, 0.9) !important;
        box-shadow: 0 0 25px rgba(255, 0, 224, 0.2);
    }}
    
    .news-card a {{
        color: {CONFIG["neon_blue"]} !important;
        font-size: 1.15rem;
        font-weight: 900 !important;
        text-decoration: none !important;
    }}

    /* 6. ボタン：物理的な存在感 */
    .stButton > button {{
        background: rgba(0, 255, 65, 0.1) !important;
        color: {CONFIG["primary"]} !important;
        border: 2px solid {CONFIG["primary"]} !important;
        width: 100% !important;
        height: 60px !important;
        font-family: 'Orbitron' !important;
        font-weight: bold !important;
        letter-spacing: 2px !important;
        transition: 0.3s !important;
    }}
    .stButton > button:hover {{
        background: {CONFIG["primary"]} !important;
        color: #000 !important;
        box-shadow: 0 0 40px {CONFIG["primary"]} !important;
    }}

    header, footer {{ visibility: hidden !important; }}
</style>
""", unsafe_allow_html=True)

# --- RENDERING ---
st.markdown(f'<div class="title">{CONFIG["site_name"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="satellite">{CONFIG["editor_avatar"]}</div>', unsafe_allow_html=True)

# ニュース取得
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
        <div style="color:{CONFIG['neon_pink']}; font-family:'Orbitron'; font-size:0.8rem; font-weight:bold;">SEQUENCE // {dt} JST</div>
        <div style="margin: 10px 0;"><a href="{entry.link}" target="_blank">{entry.title}</a></div>
        <div style="color:rgba(255,255,255,0.6); font-size:0.75rem; border-top:1px solid rgba(0,255,65,0.1); padding-top:8px; font-family:'Roboto Mono';">
            >> [SYSTEM_CHECK] 同期率:{random.randint(96,99)}% // 解析ステータス: 良好
        </div>
    </div>
    """, unsafe_allow_html=True)

# LOAD MORE ボタン
if st.session_state.display_count < len(all_items):
    if st.button(">> INITIALIZE_DATA_EXPANSION"):
        st.session_state.display_count += CONFIG["step_display"]
        st.rerun()
else:
    st.markdown(f"<p style='text-align:center; color:{CONFIG['neon_pink']}; font-family:Orbitron; font-size:1.2rem; padding:20px;'>-- TERMINAL_END_OF_STREAM --</p>", unsafe_allow_html=True)
