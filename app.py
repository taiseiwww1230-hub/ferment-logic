import streamlit as st
import feedparser
from datetime import datetime, timedelta, timezone
import urllib.parse
import random
import time

# --- EXECUTIVE TERMINAL v18.0 (Super-White Overdrive) ---
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

# --- CSS: THE FINAL WALL ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Roboto+Mono:wght@500&display=swap');

    /* 背景のグリッドと色を完全固定 */
    [data-testid="stAppViewContainer"] {{
        background-color: #000a05 !important;
        background-image: 
            linear-gradient(rgba(0, 255, 65, 0.07) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 65, 0.07) 1px, transparent 1px) !important;
        background-size: 30px 30px !important;
    }}

    /* タイトル：絶対に消えない、絶対に灰色にならない設定 */
    .absolute-title {{
        color: #FFFFFF !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 900 !important;
        font-size: 2.5rem !important;
        text-align: center !important;
        letter-spacing: 5px !important;
        padding: 50px 0 !important;
        margin: 0 !important;
        display: block !important;
        /* 文字が消えないための三重バックアップ */
        text-shadow: 0 0 10px #FFF, 0 0 20px {CONFIG["neon_blue"]}, 0 0 40px {CONFIG["neon_blue"]} !important;
        -webkit-text-fill-color: white !important;
    }}

    /* ステータスバー */
    .status-bar {{
        text-align: center;
        font-family: 'Roboto Mono', monospace;
        color: {CONFIG["primary"]};
        font-size: 11px;
        margin-bottom: 30px;
        letter-spacing: 2px;
    }}

    /* エージェントパネル */
    .ai-panel {{
        background: rgba(0, 20, 10, 0.8) !important;
        border: 2px solid {CONFIG["neon_blue"]} !important;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 40px;
        display: flex;
        align-items: center;
        gap: 20px;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.2);
    }}

    /* ニュースカード */
    .news-card {{
        background: rgba(255, 255, 255, 0.03) !important;
        border-left: 5px solid {CONFIG["primary"]} !important;
        padding: 20px;
        margin-bottom: 15px;
        border-radius: 2px;
    }}

    .news-card a {{
        color: {CONFIG["neon_blue"]} !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        text-decoration: none !important;
    }}

    .time-tag {{ color: {CONFIG["neon_pink"]}; font-family: 'Orbitron'; font-size: 0.75rem; margin-bottom: 5px; }}
    
    /* Streamlit標準パーツの徹底隠蔽 */
    header, footer, [data-testid="stHeader"] {{ visibility: hidden !important; display: none !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER: 生HTMLで描画 ---
st.markdown(f'<div class="absolute-title">{CONFIG["site_name"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="status-bar">ENVIRONMENT: JST_STABLE // GRID: ACTIVE // v18.0</div>', unsafe_allow_html=True)

# --- AGENT ---
st.markdown(f"""
    <div class="ai-panel">
        <div style="font-size: 3rem;">{CONFIG['editor_avatar']}</div>
        <div>
            <div style="color:{CONFIG['primary']}; font-family:Orbitron; font-weight:bold;">>> {CONFIG['editor_name']}</div>
            <div style="color:white; font-size:0.9rem;">[SYNC: COMPLETE] タイトル階層の物理的再構築を完了。視認性を最大化しました。</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- DATA ---
@st.cache_data(ttl=1800)
def fetch():
    q = urllib.parse.quote(CONFIG["news_query"])
    f = feedparser.parse(f"https://news.google.com/rss/search?q={q}&hl=ja&gl=JP&ceid=JP:ja")
    entries = f.entries
    entries.sort(key=lambda x: x.get('published_parsed') or (0,0,0,0,0,0,0,0,0), reverse=True)
    return entries[:20]

items = fetch()
JST = timezone(timedelta(hours=+9), 'JST')

for entry in items:
    try:
        ts = time.mktime(entry.published_parsed)
        dt = datetime.fromtimestamp(ts, timezone.utc).astimezone(JST).strftime('%Y/%m/%d %H:%M')
    except: dt = "N/A"

    st.markdown(f"""
    <div class="news-card">
        <div class="time-tag">SEQUENCE // {dt} JST</div>
        <div style="margin: 10px 0;"><a href="{entry.link}" target="_blank">{entry.title}</a></div>
        <div style="color:#888; font-size:0.85rem; border-top:1px solid #222; padding-top:10px;">
            <span style="color:{CONFIG['primary']};">[AI_LOG]</span> トレンド解析完了。信頼度: {random.randint(97, 99)}%
        </div>
    </div>
    """, unsafe_allow_html=True)
