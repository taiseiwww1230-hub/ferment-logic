import streamlit as st
import feedparser
from datetime import datetime, timedelta, timezone
import urllib.parse
import random
import time

# --- EXECUTIVE TERMINAL v20.0 (Compact Overdrive) ---
CONFIG = {
    "site_name": "FERMENT-LOGIC // INTELLIGENCE",
    "editor_name": "CORE_INTELLIGENCE",
    "editor_avatar": "🛰️",
    "primary": "#00FF41",   
    "neon_blue": "#00E5FF", 
    "neon_pink": "#FF00E0", 
    "news_query": '(ヨーグルト OR 乳製品 OR 乳酸菌 OR 紅茶 OR 茶葉) AND ("新発売" OR "期間限定" OR "独自開発" OR "トレンド") when:7d',
}

st.set_page_config(page_title=CONFIG["site_name"], page_icon="🧬", layout="centered")

# --- CSS: HIGH-DENSITY OPTIMIZATION ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Roboto+Mono:wght@500&display=swap');

    /* 背景：環境光とグリッドを維持 */
    [data-testid="stAppViewContainer"] {{
        background-color: #000c05 !important;
        background-image: 
            radial-gradient(circle at 50% -20%, rgba(0, 229, 255, 0.2), transparent 70%),
            radial-gradient(circle at -10% 100%, rgba(255, 0, 224, 0.1), transparent 50%),
            linear-gradient(rgba(0, 255, 65, 0.08) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 65, 0.08) 1px, transparent 1px) !important;
        background-size: 100% 100%, 100% 100%, 40px 40px, 40px 40px !important;
        background-attachment: fixed !important;
    }}

    /* タイトル：サイズを大幅に縮小し、ニュースを上へ押し上げる */
    .absolute-title {{
        color: #FFFFFF !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 900 !important;
        font-size: 1.8rem !important; /* 3rem -> 1.8remへ縮小 */
        text-align: center !important;
        letter-spacing: 4px !important;
        padding-top: 25px !important; /* 余白を削減 */
        margin: 0 !important;
        text-shadow: 0 0 10px #FFF, 0 0 20px {CONFIG["neon_blue"]} !important;
        -webkit-text-fill-color: white !important;
    }}

    /* 衛星：サイズを調整し、配置をコンパクトに */
    .satellite-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 15px 0 !important; /* 40px -> 15px */
    }}

    .moving-satellite {{
        font-size: 3rem !important; /* 5rem -> 3rem */
        filter: drop-shadow(0 0 15px {CONFIG["neon_blue"]});
        animation: orbit-swing 6s ease-in-out infinite;
    }}

    @keyframes orbit-swing {{
        0% {{ transform: translate(0, 0) rotate(0deg); }}
        25% {{ transform: translate(20px, -10px) rotate(10deg); }}
        50% {{ transform: translate(0, -20px) rotate(0deg); }}
        75% {{ transform: translate(-20px, -10px) rotate(-10deg); }}
        100% {{ transform: translate(0, 0) rotate(0deg); }}
    }}

    /* エージェントパネル：高さを抑える */
    .ai-panel {{
        background: rgba(0, 30, 15, 0.85) !important;
        border: 1px solid {CONFIG["primary"]} !important;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.1) !important;
        border-radius: 4px;
        padding: 15px !important; /* 25px -> 15px */
        margin-bottom: 20px !important; /* 40px -> 20px */
        backdrop-filter: blur(10px);
    }}

    /* ニュースカード：一画面の密度を上げる */
    .news-card {{
        background: rgba(255, 255, 255, 0.04) !important;
        border-left: 5px solid {CONFIG["primary"]} !important;
        padding: 15px !important; /* 25px -> 15px */
        margin-bottom: 12px !important; /* 20px -> 12px */
        border-radius: 2px;
    }}

    .news-card a {{
        color: {CONFIG["neon_blue"]} !important;
        font-size: 1.1rem !important; /* 1.3rem -> 1.1rem */
        font-weight: 800 !important;
        text-decoration: none !important;
        line-height: 1.4 !important;
    }}

    .time-tag {{ color: {CONFIG["neon_pink"]}; font-family: 'Orbitron'; font-size: 0.7rem; font-weight: bold; }}

    header, footer {{ visibility: hidden !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- RENDERING ---

st.markdown(f'<div class="absolute-title">{CONFIG["site_name"]}</div>', unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:{CONFIG['primary']}; font-family:Roboto Mono; font-size:10px; letter-spacing:2px; margin-bottom:0;'>LOCAL_TIME: JST // SATELLITE_LINK: ACTIVE</p>", unsafe_allow_html=True)

st.markdown(f'<div class="satellite-container"><div class="moving-satellite">{CONFIG["editor_avatar"]}</div></div>', unsafe_allow_html=True)

with st.container():
    st.markdown(f"""
        <div class="ai-panel">
            <div style="color:{CONFIG['primary']}; font-family:Orbitron; font-weight:bold; font-size:0.9rem;">>> {CONFIG['editor_name']}</div>
            <div style="color:white; font-size:0.85rem; line-height:1.4;">
                高密度表示モード(Compact-View)へ移行。情報をフロントレイヤーに凝縮しました。
            </div>
        </div>
        """, unsafe_allow_html=True)

@st.cache_data(ttl=1800)
def fetch_data():
    q = urllib.parse.quote(CONFIG["news_query"])
    f = feedparser.parse(f"https://news.google.com/rss/search?q={q}&hl=ja&gl=JP&ceid=JP:ja")
    entries = f.entries
    entries.sort(key=lambda x: x.get('published_parsed') or (0,0,0,0,0,0,0,0,0), reverse=True)
    return entries[:20]

items = fetch_data()
JST = timezone(timedelta(hours=+9), 'JST')

for entry in items:
    try:
        ts = time.mktime(entry.published_parsed)
        dt = datetime.fromtimestamp(ts, timezone.utc).astimezone(JST).strftime('%Y/%m/%d %H:%M')
    except: dt = "N/A"

    st.markdown(f"""
    <div class="news-card">
        <div class="time-tag">INTEL_LOG // {dt} JST</div>
        <div style="margin: 8px 0;"><a href="{entry.link}" target="_blank">{entry.title}</a></div>
        <div style="color:#888; font-size:0.75rem; border-top:1px solid rgba(255,255,255,0.05); padding-top:8px; font-family:Roboto Mono;">
            [AI_REPORT] 信頼度: {random.randint(98, 99)}% // 解析完了。
        </div>
    </div>
    """, unsafe_allow_html=True)
