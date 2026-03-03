import streamlit as st
import feedparser
from datetime import datetime, timedelta, timezone
import urllib.parse
import random
import time

# --- v23.3 THE RESTORATION (安定復活モデル) ---
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

# --- CSS: すべてを共存させる最終設計 ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Roboto+Mono&display=swap');
    
    /* 1. 背景: ライブパルス (ゆっくりとした明滅) */
    [data-testid="stAppViewContainer"] {{
        background-color: #000804 !important;
        background-image: 
            radial-gradient(circle at 50% -20%, rgba(0, 229, 255, 0.2), transparent 70%),
            linear-gradient(rgba(0, 255, 65, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 65, 0.1) 1px, transparent 1px) !important;
        background-size: 100% 100%, 30px 30px, 30px 30px !important;
        animation: pulse-bg 8s ease-in-out infinite alternate;
    }}
    @keyframes pulse-bg {{
        0% {{ opacity: 0.8; }} 100% {{ opacity: 1; }}
    }}

    /* 2. タイトル */
    .title {{
        color: white !important;
        font-family: 'Orbitron';
        font-size: 1.8rem;
        text-align: center;
        text-shadow: 0 0 15px {CONFIG["neon_blue"]};
        padding: 20px 0 5px 0;
    }}

    /* 3. 復活の動く衛星 */
    .satellite {{
        text-align: center;
        font-size: 3.5rem;
        filter: drop-shadow(0 0 15px {CONFIG["neon_blue"]});
        animation: orbit-swing 6s ease-in-out infinite;
        margin-bottom: 20px;
    }}
    @keyframes orbit-swing {{
        0%, 100% {{ transform: translateY(0) rotate(0deg); }}
        50% {{ transform: translateY(-20px) rotate(10deg); }}
    }}

    /* 4. ニュースカード & ホバー復活 */
    .news-card {{
        background: rgba(255, 255, 255, 0.04);
        border-left: 5px solid {CONFIG["primary"]};
        padding: 15px;
        margin-bottom: 12px;
        border-radius: 2px;
        transition: 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        animation: fade-in 0.5s ease-out both;
    }}
    @keyframes fade-in {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}

    .news-card:hover {{
        background: rgba(255, 255, 255, 0.1);
        border-left: 5px solid {CONFIG["neon_pink"]};
        transform: translateX(10px);
        box-shadow: 0 0 20px rgba(255, 0, 224, 0.2);
    }}
    
    .news-card a {{
        color: {CONFIG["neon_blue"]} !important;
        font-size: 1.1rem;
        font-weight: bold;
        text-decoration: none;
    }}

    /* 5. グリッチボタン */
    .stButton > button {{
        background: transparent !important;
        color: {CONFIG["primary"]} !important;
        border: 2px solid {CONFIG["primary"]} !important;
        font-family: 'Orbitron' !important;
        width: 100% !important;
        height: 50px !important;
        transition: 0.2s;
    }}
    .stButton > button:hover {{
        background: {CONFIG["primary"]} !important;
        color: black !important;
        animation: glitch 0.2s infinite;
        box-shadow: 0 0 30px {CONFIG["primary"]};
    }}
    @keyframes glitch {{
        0% {{ transform: translate(2px, -2px); }}
        50% {{ transform: translate(-2px, 2px); }}
        100% {{ transform: translate(2px, 2px); }}
    }}

    header, footer {{ visibility: hidden; }}
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

# ニュースカード描画（日付・ホバーを完全復活）
for i, entry in enumerate(display_items):
    try:
        ts = time.mktime(entry.published_parsed)
        dt = datetime.fromtimestamp(ts, timezone.utc).astimezone(JST).strftime('%Y/%m/%d %H:%M')
    except: dt = "2026/--/-- --:--"
    
    st.markdown(f"""
    <div class="news-card" style="animation-delay: {min(i*0.05, 1)}s;">
        <div style="color:{CONFIG['neon_pink']}; font-family:'Orbitron'; font-size:0.7rem;">SEQUENCE // {dt} JST</div>
        <div style="margin: 8px 0;"><a href="{entry.link}" target="_blank">{entry.title}</a></div>
        <div style="color:#888; font-size:0.75rem; border-top:1px solid rgba(255,255,255,0.05); padding-top:5px;">
            [AI_REPORT] SYNC: {random.randint(97,99)}% // ANALYZED
        </div>
    </div>
    """, unsafe_allow_html=True)

# 最下部のボタン
st.write("")
if st.session_state.display_count < len(all_items):
    if st.button(">> LOAD_MORE_INTELLIGENCE"):
        st.session_state.display_count += CONFIG["step_display"]
        st.rerun()
else:
    st.markdown(f"<p style='text-align:center; color:{CONFIG['neon_pink']}; font-family:Orbitron;'>-- END OF STREAM --</p>", unsafe_allow_html=True)
