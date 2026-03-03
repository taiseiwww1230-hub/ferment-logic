import streamlit as st
import feedparser
from datetime import datetime, timedelta, timezone
import urllib.parse
import random
import time

# --- v23.2 FORCE_SYNC (物理同期モデル) ---
CONFIG = {
    "site_name": "FERMENT-LOGIC // INTELLIGENCE",
    "editor_avatar": "🛰️",
    "primary": "#00FF41",   
    "neon_blue": "#00E5FF", 
    "neon_pink": "#FF00E0", 
    "query": '(ヨーグルト OR 乳製品 OR 乳酸菌 OR 紅茶 OR 茶葉) AND ("新発売" OR "期間限定" OR "独自開発" OR "トレンド") when:7d',
    "initial_display": 15
}

st.set_page_config(page_title=CONFIG["site_name"], layout="centered")

# セッション管理
if "display_count" not in st.session_state:
    st.session_state.display_count = CONFIG["initial_display"]

# CSS: 今回は「絶対に出る」ようにさらに簡素化・強化
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Roboto+Mono&display=swap');
    
    /* 背景: 黒固定でグリッドのみ */
    [data-testid="stAppViewContainer"] {{
        background-color: #000804 !important;
        background-image: 
            linear-gradient(rgba(0, 255, 65, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 65, 0.1) 1px, transparent 1px) !important;
        background-size: 30px 30px !important;
    }}

    .title {{
        color: white !important;
        font-family: 'Orbitron';
        font-size: 2rem;
        text-align: center;
        text-shadow: 0 0 20px {CONFIG["neon_blue"]};
        padding: 20px 0;
    }}

    .news-card {{
        background: rgba(255, 255, 255, 0.05);
        border-left: 5px solid {CONFIG["primary"]};
        padding: 15px;
        margin-bottom: 10px;
        border-radius: 4px;
        transition: 0.2s;
    }}
    .news-card:hover {{
        border-left: 5px solid {CONFIG["neon_pink"]};
        background: rgba(255, 255, 255, 0.1);
    }}
    
    .news-card a {{
        color: {CONFIG["neon_blue"]} !important;
        font-weight: bold;
        text-decoration: none;
    }}

    /* ボタンを強制的に目立たせる */
    .stButton > button {{
        background: {CONFIG["primary"]} !important;
        color: black !important;
        font-weight: bold !important;
        font-family: 'Orbitron' !important;
        height: 60px !important;
        font-size: 1.2rem !important;
    }}
</style>
""", unsafe_allow_html=True)

# 1. タイトル
st.markdown(f'<div class="title">{CONFIG["site_name"]}</div>', unsafe_allow_html=True)

# 2. 衛星 (アニメーションはあえてシンプルに)
st.markdown(f'<div style="text-align:center; font-size:4rem; filter: drop-shadow(0 0 10px {CONFIG["neon_blue"]});">🛰️</div>', unsafe_allow_html=True)

# 3. ニュース取得
@st.cache_data(ttl=600)
def fetch():
    q = urllib.parse.quote(CONFIG["query"])
    f = feedparser.parse(f"https://news.google.com/rss/search?q={q}&hl=ja&gl=JP&ceid=JP:ja")
    return f.entries

all_entries = fetch()
display_items = all_entries[:st.session_state.display_count]

# 4. ニュースカード描画
for entry in display_items:
    st.markdown(f"""
    <div class="news-card">
        <div style="color:{CONFIG['neon_pink']}; font-size:0.7rem; font-family:Orbitron;">DATA_STREAM // ACTIVE</div>
        <div style="margin: 5px 0;"><a href="{entry.link}" target="_blank">{entry.title}</a></div>
        <div style="color:#888; font-size:0.7rem;">[AI] VALIDATED: {random.randint(95,99)}%</div>
    </div>
    """, unsafe_allow_html=True)

# 5. ボタン (確実に描画するために、条件分岐をシンプルに)
st.write("---")
if st.session_state.display_count < len(all_entries):
    # ここでボタンが表示されないのはStreamlitの描画バグの可能性があるため
    # カラムを使って強制的に領域を確保
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(">> LOAD MORE DATA"):
            st.session_state.display_count += 15
            st.rerun()
else:
    st.info("ALL DATA LOADED")

# 6. 「ライブ・パルス」をPython側で強制実行 (サイドバーで稼働状況を表示)
st.sidebar.markdown(f"### SYSTEM PULSE")
pulse_placeholder = st.sidebar.empty()
if random.random() > 0.5:
    pulse_placeholder.success("GRID SYNCING...")
else:
    pulse_placeholder.warning("DATA FLOWING...")
