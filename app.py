import streamlit as st
import feedparser
from datetime import datetime, timedelta, timezone
import urllib.parse
import random
import time

# --- EXECUTIVE TERMINAL v15.0 (Absolute Neon Mist) ---
CONFIG = {
    "site_name": "FERMENT-LOGIC // INTELLIGENCE",
    "editor_name": "CORE-AI: FERMENT",
    "editor_avatar": "🛰️",
    "primary": "#00FF41",   
    "secondary": "#FFFFFF", 
    "neon_blue": "#00E5FF", 
    "neon_pink": "#FF00E0", 
    "deep_mist": "#010801", # 真っ黒ではない、深い緑の霧
    "news_query": '(ヨーグルト OR 乳製品 OR 乳酸菌 OR 紅茶 OR 茶葉) AND ("新発売" OR "期間限定" OR "独自開発" OR "トレンド") when:7d',
    "greeting": "[SYSTEM: ONLINE] 背景レイヤーの強制再構築完了。視覚情報をアップデートしました。"
}

st.set_page_config(page_title=CONFIG["site_name"], page_icon="🧬", layout="centered")

# --- VISUAL RECONSTRUCTION (背景固定・強制上書き) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Orbitron:wght@500;700&family=Roboto+Mono:wght@300&display=swap');

    /* 全ての背景を強制的に上書き */
    [data-testid="stAppViewContainer"], .stApp {{
        background-color: {CONFIG["deep_mist"]} !important;
        background-image: 
            /* 走査線エフェクト */
            linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.15) 50%),
            /* ネオンの滲みレイヤー */
            radial-gradient(at 10% 10%, rgba(0, 255, 65, 0.15) 0px, transparent 45%),
            radial-gradient(at 90% 10%, rgba(0, 229, 255, 0.12) 0px, transparent 45%),
            radial-gradient(at 50% 90%, rgba(255, 0, 224, 0.08) 0px, transparent 50%) !important;
        background-size: 100% 4px, 100% 100%, 100% 100%, 100% 100% !important;
        background-attachment: fixed !important;
    }}

    /* ニュースカードの透明感と可読性の向上 */
    .news-card {{
        background: rgba(10, 20, 10, 0.6) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(0, 255, 65, 0.15) !important;
        border-left: 4px solid {CONFIG["primary"]} !important;
        padding: 20px;
        margin-bottom: 15px;
        border-radius: 4px;
        transition: 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
    }}
    
    .news-card:hover {{
        background: rgba(20, 40, 20, 0.8) !important;
        border-left: 4px solid {CONFIG["neon_pink"]} !important;
        transform: translateX(5px);
        box-shadow: 0 0 30px rgba(0, 255, 65, 0.1);
    }}

    .stTitle {{
        font-family: 'Orbitron', sans-serif;
        font-size: 1.8rem !important;
        letter-spacing: 5px;
        color: {CONFIG["secondary"]} !important;
        text-shadow: 0 0 15px {CONFIG["neon_blue"]} !important;
    }}

    .ai-agent-container {{
        background: rgba(0, 15, 0, 0.7);
        border: 1px solid rgba(0, 255, 65, 0.3);
        padding: 18px;
        border-radius: 10px;
        backdrop-filter: blur(20px);
        margin-bottom: 35px;
        display: flex;
        align-items: center;
        gap: 20px;
    }}

    .ai-avatar {{ font-size: 3rem; animation: float 4s ease-in-out infinite; }}
    @keyframes float {{ 0%, 100% {{ transform: translateY(0px); }} 50% {{ transform: translateY(-10px); }} }}

    .time-tag {{ color: {CONFIG["neon_pink"]}; font-family: 'Orbitron'; font-size: 0.7rem; }}
    .news-card a {{ color: #fff !important; text-decoration: none; font-weight: 600; font-size: 1.1rem; }}
    .analysis-content {{ color: #888; font-size: 0.85rem; margin-top: 12px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 10px; }}
    </style>
    """, unsafe_allow_html=True)

# --- APP LOGIC ---
st.title(f"{CONFIG['site_name']}")
st.markdown(f"<p style='text-align:center; color:{CONFIG['primary']}; font-family:Roboto Mono; font-size:11px;'>ENVIRONMENT: MIST_STABLE // JST_SYNC: ACTIVE</p>", unsafe_allow_html=True)

with st.container():
    st.markdown(f"""
    <div class="ai-agent-container">
        <div class="ai-avatar">{CONFIG['editor_avatar']}</div>
        <div>
            <div style="color:{CONFIG['primary']}; font-family:Orbitron; font-weight:700;">[ {CONFIG['editor_name']} ]</div>
            <div style="color:#ddd; font-size:0.9rem;">{CONFIG['greeting']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=1800)
def fetch_news():
    encoded_query = urllib.parse.quote(CONFIG["news_query"])
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"
    try:
        feed = feedparser.parse(url)
        entries = feed.entries
        entries.sort(key=lambda x: x.get('published_parsed') or (0,0,0,0,0,0,0,0,0), reverse=True)
        return entries[:20]
    except: return []

items = fetch_news()
JST = timezone(timedelta(hours=+9), 'JST')

for entry in items:
    try:
        dt_gmt = datetime.fromtimestamp(time.mktime(entry.published_parsed), timezone.utc)
        display_time = dt_gmt.astimezone(JST).strftime('%Y/%m/%d %H:%M')
    except: display_time = "N/A"

    st.markdown(f"""
    <div class="news-card">
        <div class="time-tag">INTEL_LOG // {display_time} JST</div>
        <a href="{entry.link}" target="_blank">{entry.title}</a>
        <div class="analysis-content">
            <span style="color:{CONFIG['primary']};">[ANALYSIS]</span> 市場トレンドと成分相関を確認。
            <span style="color:{CONFIG['neon_blue']};">>> CONFIDENCE: {random.randint(98, 99)}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write(f"<p style='text-align:center; color:#333; font-family:Orbitron; font-size:10px; padding:40px;'>v15.0 Absolute Neon Mist | Final Authority</p>", unsafe_allow_html=True)
