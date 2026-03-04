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

# --- CSS: 表面レイヤーを直接支配する ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Roboto+Mono:wght@400;700&display=swap');
    
    /* 1. 全てのレイヤーを強制的に「深い黒」に固定（白を抹殺） */
    [data-testid="stAppViewContainer"], 
    [data-testid="stHeader"], 
    .main, 
    .block-container {{
        background-color: #000201 !important;
    }}

    /* 2. 最前面に「網目」と「心電図パルス」を合成した背景を配置 */
    [data-testid="stAppViewContainer"]::before {{
        content: "";
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        /* 網目（グリッド） */
        background-image: 
            linear-gradient(rgba(0, 255, 65, 0.15) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 65, 0.15) 1px, transparent 1px);
        background-size: 45px 45px;
        z-index: 0;
        pointer-events: none;
    }}

    /* 3. あからさまな「心電図パルス（鼓動）」 */
    [data-testid="stAppViewContainer"]::after {{
        content: "";
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        /* 心電図のような鋭いライン */
        background: linear-gradient(90deg, 
            transparent 0%, 
            transparent 45%, 
            {CONFIG["primary"]} 50%, 
            transparent 55%, 
            transparent 100%);
        background-size: 200% 100%;
        /* 鼓動のようなマスク */
        -webkit-mask-image: radial-gradient(circle at center, white 0%, transparent 80%);
        mask-image: radial-gradient(circle at center, white 0%, transparent 80%);
        opacity: 0.4;
        z-index: 1;
        pointer-events: none;
        animation: heart-pulse 2s cubic-bezier(0.4, 0, 0.2, 1) infinite;
    }}

    /* 4. スキャン光線（再復活） */
    .main::before {{
        content: "";
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(to bottom, transparent 0%, rgba(0, 255, 65, 0.2) 50%, transparent 100%);
        background-size: 100% 400%;
        z-index: 2;
        pointer-events: none;
        animation: scan-ray 6s linear infinite;
    }}

    @keyframes heart-pulse {{
        0% {{ background-position: 200% 0; opacity: 0.2; transform: scale(1); }}
        10% {{ opacity: 0.8; transform: scale(1.02); }} /* 収縮の瞬間 */
        20% {{ opacity: 0.4; transform: scale(1); }}
        100% {{ background-position: -200% 0; opacity: 0.2; }}
    }}

    @keyframes scan-ray {{
        0% {{ background-position: 0 -100%; }}
        100% {{ background-position: 0 100%; }}
    }}

    /* コンテンツエリア（被り防止） */
    .block-container {{
        max-width: 900px !important;
        position: relative;
        z-index: 100; /* 背景より上に */
        padding-top: 5rem !important;
    }}

    /* カードデザイン（画像イメージを忠実に再現） */
    .news-card {{
        background: rgba(0, 8, 4, 0.95) !important;
        border: 2px solid {CONFIG["primary"]} !important;
        border-left: 12px solid {CONFIG["primary"]} !important;
        padding: 30px; margin-bottom: 25px;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.15);
    }}
    .news-card a {{
        color: white !important; font-size: 1.35rem; font-weight: 900;
        text-decoration: none !important;
        text-shadow: 0 0 10px {CONFIG["neon_blue"]};
    }}

    /* ボタン（位置とサイズの適正化） */
    .stButton > button {{
        height: 60px !important; border: 3px solid {CONFIG["primary"]} !important;
        background: rgba(0, 255, 65, 0.1) !important; color: {CONFIG["primary"]} !important;
        font-family: 'Orbitron' !important; font-size: 1.1rem !important;
        width: 100% !important;
    }}
    .stButton > button:hover {{
        background: {CONFIG["neon_pink"]} !important; color: white !important;
    }}

    header, footer {{ visibility: hidden !important; }}
</style>
""", unsafe_allow_html=True)

# --- ニュース取得 & 描画 ---
st.markdown(f"""
<div style="text-align:center; margin-bottom:40px;">
    <div style="font-size:6rem; filter:drop-shadow(0 0 30px {CONFIG['primary']});">{CONFIG['editor_avatar']}</div>
    <div style="color:white; font-family:'Orbitron'; font-size:2rem; letter-spacing:10px; text-shadow:0 0 20px {CONFIG['primary']};">
        {CONFIG['site_name']}
    </div>
</div>
""", unsafe_allow_html=True)

all_items = fetch_news() # fetch_news関数は前述のものを流用
JST = timezone(timedelta(hours=+9), 'JST')
display_items = all_items[:st.session_state.display_count]

for entry in display_items:
    dt = datetime.fromtimestamp(time.mktime(entry.published_parsed), timezone.utc).astimezone(JST).strftime('%Y/%m/%d %H:%M') if entry.get('published_parsed') else "2026/--/--"
    st.markdown(f"""
    <div class="news-card">
        <div style="color:{CONFIG['neon_pink']}; font-family:'Roboto Mono'; font-size:0.95rem; margin-bottom:12px; font-weight:bold;">
            ▶ SYNC_TS // {dt} JST
        </div>
        <a href="{entry.link}" target="_blank">{entry.title}</a>
        <div style="margin-top:15px; color:{CONFIG['primary']}; font-size:0.8rem; opacity:0.7; font-family:'Roboto Mono'; border-top:1px solid rgba(0,255,65,0.2); padding-top:10px;">
            >> INTEL_STATUS: VERIFIED <br>
            >> ACCESS_LEVEL: UNRESTRICTED
        </div>
    </div>
    """, unsafe_allow_html=True)

# 操作パネル
st.markdown('<div style="height:30px;"></div>', unsafe_allow_html=True)
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
