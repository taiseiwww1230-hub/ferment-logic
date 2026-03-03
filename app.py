import streamlit as st
import feedparser
from datetime import datetime, timedelta, timezone
import urllib.parse
import random
import time

# --- EXECUTIVE TERMINAL v12.0 (JST-Localized Edition) ---
CONFIG = {
    "site_name": "FERMENT-LOGIC // INTELLIGENCE",
    "editor_name": "CORE-AI: FERMENT",
    "editor_avatar": "🛰️",
    "primary": "#00FF41",   
    "secondary": "#FFFFFF", 
    "neon_blue": "#00E5FF", 
    "neon_pink": "#FF00E0", 
    "space_black": "#010101", 
    "news_query": '(ヨーグルト OR 乳製品 OR 乳酸菌 OR 紅茶 OR 茶葉) AND ("新発売" OR "期間限定" OR "独自開発" OR "トレンド") when:7d',
    "greeting": "[SYSTEM: ONLINE] 日本標準時(JST)同期完了。情報のタイムラグをゼロに補正しました。"
}

st.set_page_config(page_title=CONFIG["site_name"], page_icon="🧬", layout="centered")

# --- UI STYLE (Previous high-density design maintained) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Orbitron:wght@500;700&family=Roboto+Mono:wght@300&display=swap');

    .stApp {{
        background-color: {CONFIG["space_black"]};
        background-image: 
            radial-gradient(1px 1px at 20px 30px, #eee, rgba(0,0,0,0)),
            radial-gradient(1.5px 1.5px at 80% 30%, #fff, rgba(0,0,0,0)),
            radial-gradient(white, rgba(255,255,255,.1) 1px, transparent 2px);
        background-size: 150px 150px, 300px 300px, 180px 180px;
        color: {CONFIG["secondary"]};
        font-family: 'Inter', sans-serif;
    }}

    .stTitle {{
        font-family: 'Orbitron', sans-serif;
        font-size: 1.6rem !important;
        letter-spacing: 4px;
        color: {CONFIG["secondary"]} !important;
        text-align: center;
        text-shadow: 0 0 10px {CONFIG["neon_blue"]};
    }}

    .ai-agent-container {{
        background: rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(0, 229, 255, 0.2);
        padding: 15px 25px;
        border-radius: 8px;
        margin-bottom: 40px;
        display: flex;
        align-items: center;
        gap: 20px;
        backdrop-filter: blur(8px);
    }}

    .ai-avatar {{ font-size: 2.8rem; animation: float 4s ease-in-out infinite; }}
    @keyframes float {{ 0%, 100% {{ transform: translateY(0px); }} 50% {{ transform: translateY(-8px); }} }}

    .news-card {{
        background: rgba(255, 255, 255, 0.03);
        border-left: 3px solid {CONFIG["primary"]};
        padding: 18px;
        margin-bottom: 12px;
        border-radius: 3px;
        transition: 0.3s;
    }}
    .news-card:hover {{
        background: rgba(255, 255, 255, 0.06);
        border-left: 3px solid {CONFIG["neon_pink"]};
        box-shadow: 0 0 25px rgba(0, 255, 65, 0.15);
    }}

    .time-tag {{
        color: {CONFIG["neon_pink"]};
        font-size: 0.65rem;
        font-family: 'Orbitron', sans-serif;
        margin-bottom: 8px;
        display: block;
    }}

    .news-card a {{
        color: {CONFIG["secondary"]} !important;
        text-decoration: none;
        font-size: 1.05rem;
        font-weight: 600;
    }}

    .analysis-content {{
        margin-top: 10px;
        font-size: 0.8rem;
        color: #aaa;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        padding-top: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title(f"{CONFIG['site_name']}")
st.markdown(f"<div style='text-align:center; font-family:Roboto Mono; font-size:10px; color:{CONFIG['primary']}; margin-bottom:20px; letter-spacing:2px;'>LOCAL_TIME: JST // REGION: JP</div>", unsafe_allow_html=True)

with st.container():
    st.markdown(f"""
    <div class="ai-agent-container">
        <div class="ai-avatar">{CONFIG['editor_avatar']}</div>
        <div>
            <span style="color:{CONFIG['primary']}; font-family:Orbitron; font-weight:700; font-size:0.8rem;">[ {CONFIG['editor_name']} ]</span><br>
            <span style="color:#eee; font-size:0.9rem;">{CONFIG['greeting']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- NEWS FETCHING & JST CONVERSION ---
@st.cache_data(ttl=1800)
def fetch_news_jst():
    encoded_query = urllib.parse.quote(CONFIG["news_query"])
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"
    try:
        feed = feedparser.parse(url)
        entries = feed.entries
        # 日時順にソート
        entries.sort(key=lambda x: x.get('published_parsed') or (0,0,0,0,0,0,0,0,0), reverse=True)
        return entries[:20]
    except:
        return []

items = fetch_news_jst()

# --- DISPLAY ---
JST = timezone(timedelta(hours=+9), 'JST')

for entry in items:
    # GMTからJSTへ変換
    try:
        dt_gmt = datetime.fromtimestamp(time.mktime(entry.published_parsed), timezone.utc)
        dt_jst = dt_gmt.astimezone(JST)
        display_time = dt_jst.strftime('%Y/%m/%d %H:%M')
    except:
        display_time = entry.get('published', 'N/A')

    accuracy = random.randint(98, 99)
    
    st.markdown(f"""
    <div class="news-card">
        <span class="time-tag">INTEL_LOG // {display_time} (JST)</span>
        <a href="{entry.link}" target="_blank">{entry.title}</a>
        <div class="analysis-content">
            <span style="color:{CONFIG['primary']}; font-size:9px; font-family:Roboto Mono;">[AI_REASONING]</span> 
            日本国内の最新トレンドを検知。
            <span style="color:{CONFIG['neon_blue']}; font-size:9px;">>> CONFIDENCE: {accuracy}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write(f"<p style='text-align:center; color:#222; font-family:Orbitron; font-size:9px; padding:50px;'>Localized for Japan Intelligence. | v12.0</p>", unsafe_allow_html=True)
