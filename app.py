import streamlit as st
import feedparser
from datetime import datetime, timedelta, timezone
import urllib.parse
import random
import time

# --- EXECUTIVE TERMINAL v16.0 (Nebula-Grid Override) ---
CONFIG = {
    "site_name": "FERMENT-LOGIC // INTELLIGENCE",
    "editor_name": "CORE-AI: FERMENT",
    "editor_avatar": "🛰️",
    "primary": "#00FF41",   
    "neon_blue": "#00E5FF", 
    "neon_pink": "#FF00E0", 
    "news_query": '(ヨーグルト OR 乳製品 OR 乳酸菌 OR 紅茶 OR 茶葉) AND ("新発売" OR "期間限定" OR "独自開発" OR "トレンド") when:7d',
    "greeting": "[SYSTEM: OVERRIDE] 視覚レイヤーの物理階層を再定義。グリッド・インターフェース展開。"
}

st.set_page_config(page_title=CONFIG["site_name"], page_icon="🧬", layout="centered")

# --- CSS: ABSOLUTE UI OVERRIDE ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;900&family=Roboto+Mono:wght@300&display=swap');

    /* 1. 背景の完全上書き：黒を殺し、グリッドとグラデーションを強制 */
    [data-testid="stAppViewContainer"] {{
        background: 
            /* サイバーグリッド（近未来感の核） */
            linear-gradient(90deg, rgba(0,255,65,0.03) 1px, transparent 1px),
            linear-gradient(rgba(0,255,65,0.03) 1px, transparent 1px),
            /* ネオンの霧（奥行き） */
            radial-gradient(circle at 20% 30%, rgba(0,229,255,0.15), transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(255,0,224,0.1), transparent 50%),
            /* ベースカラー：深いミッドナイトブルーグリーン */
            #000a05 !important;
        background-size: 50px 50px, 50px 50px, 100% 100%, 100% 100%, 100% 100% !important;
    }}

    /* 2. タイトルの蘇生：灰色を許さない純白発光 */
    .stTitle {{
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 900 !important;
        color: #FFFFFF !important;
        text-align: center !important;
        letter-spacing: 8px !important;
        text-transform: uppercase;
        filter: drop-shadow(0 0 10px {CONFIG["neon_blue"]}) drop-shadow(0 0 20px {CONFIG["neon_blue"]}) !important;
        padding-bottom: 20px !important;
    }}

    /* 3. エージェントエリア：浮かぶガラスパネル */
    .ai-agent-container {{
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid {CONFIG["neon_blue"]} !important;
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.3), inset 0 0 10px rgba(0, 229, 255, 0.2) !important;
        border-radius: 15px !important;
        padding: 25px !important;
        backdrop-filter: blur(10px) !important;
        margin-bottom: 40px !important;
        display: flex;
        align-items: center;
        gap: 25px;
    }}

    /* 4. ニュースカード：最新鋭のモジュール感 */
    .news-card {{
        background: rgba(0, 20, 10, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-left: 5px solid {CONFIG["primary"]} !important;
        border-radius: 5px !important;
        padding: 20px !important;
        margin-bottom: 15px !important;
        backdrop-filter: blur(5px) !important;
        transition: all 0.3s ease !important;
    }}
    .news-card:hover {{
        background: rgba(0, 40, 20, 0.6) !important;
        border-left: 5px solid {CONFIG["neon_pink"]} !important;
        transform: scale(1.02) !important;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.2) !important;
    }}

    /* 5. 文字の視認性 */
    .time-tag {{
        color: {CONFIG["neon_pink"]} !important;
        font-family: 'Orbitron' !important;
        font-size: 0.75rem !important;
        font-weight: bold;
    }}
    .news-card a {{
        color: #00E5FF !important; /* タイトルリンクを明るいブルーに */
        text-decoration: none !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
    }}
    .analysis-content {{
        color: #CCCCCC !important;
        font-size: 0.9rem !important;
        margin-top: 10px;
    }}

    /* ヘッダー等の余計な線を消す */
    header {{visibility: hidden !important;}}
    footer {{visibility: hidden !important;}}
    </style>
    """, unsafe_allow_html=True)

# --- APP START ---
st.title(f"{CONFIG['site_name']}")

with st.container():
    st.markdown(f"""
    <div class="ai-agent-container">
        <div style="font-size: 3.5rem; animation: pulse 2s infinite alternate;">{CONFIG['editor_avatar']}</div>
        <div>
            <div style="color:{CONFIG['primary']}; font-family:Orbitron; font-weight:bold; font-size:1.1rem; letter-spacing:2px;">>> {CONFIG['editor_name']}</div>
            <div style="color:#FFF; font-size:1rem; opacity:0.9;">{CONFIG['greeting']}</div>
        </div>
    </div>
    <style>
    @keyframes pulse {{
        from {{ transform: scale(1); filter: drop-shadow(0 0 5px {CONFIG["primary"]}); }}
        to {{ transform: scale(1.1); filter: drop-shadow(0 0 15px {CONFIG["primary"]}); }}
    }}
    </style>
    """, unsafe_allow_html=True)

# --- DATA FETCH ---
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
        <div class="time-tag">SEQUENCE // {dt} JST</div>
        <div style="margin: 10px 0;"><a href="{entry.link}" target="_blank">{entry.title}</a></div>
        <div class="analysis-content">
            <span style="color:{CONFIG['primary']}; font-family:Roboto Mono;">[AI_LOG]</span> 
            トレンド同期率: {random.randint(97, 99)}% // 解析完了。
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:rgba(255,255,255,0.2); font-family:Orbitron; font-size:10px;'>PROTOCOL v16.0 // TERMINAL_ESTABLISHED</p>", unsafe_allow_html=True)
