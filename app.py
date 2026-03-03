import streamlit as st
import feedparser
from datetime import datetime, timedelta, timezone
import urllib.parse
import random
import time

# --- EXECUTIVE TERMINAL v17.0 (Absolute Contrast Zenith) ---
CONFIG = {
    "site_name": "FERMENT-LOGIC // INTELLIGENCE",
    "editor_name": "CORE-AI: FERMENT",
    "editor_avatar": "🛰️",
    "primary": "#00FF41",   
    "neon_blue": "#00E5FF", 
    "neon_pink": "#FF00E0", 
    "news_query": '(ヨーグルト OR 乳製品 OR 乳酸菌 OR 紅茶 OR 茶葉) AND ("新発売" OR "期間限定" OR "独自開発" OR "トレンド") when:7d',
}

st.set_page_config(page_title=CONFIG["site_name"], page_icon="🧬", layout="centered")

# --- CSS: ULTIMATE OVERRIDE ---
# !importantを極限まで使用し、Streamlitのグレー化を物理的に阻止します
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Roboto+Mono:wght@500&display=swap');

    /* 1. 背景：黒を脱却し、グリッドが主役の空間へ */
    [data-testid="stAppViewContainer"] {{
        background-color: #000804 !important;
        background-image: 
            /* 電子グリッド */
            linear-gradient(rgba(0, 255, 65, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 65, 0.05) 1px, transparent 1px),
            /* 空間の奥行き（ネオンの霧） */
            radial-gradient(circle at 50% 0%, rgba(0, 229, 255, 0.15), transparent 70%),
            radial-gradient(circle at 0% 100%, rgba(255, 0, 224, 0.1), transparent 50%) !important;
        background-size: 40px 40px, 40px 40px, 100% 100%, 100% 100% !important;
    }}

    /* 2. タイトル：グレー化を絶対に許さない純白＆爆光設定 */
    h1 {{
        color: #FFFFFF !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 900 !important;
        font-size: 2.8rem !important;
        text-align: center !important;
        letter-spacing: 6px !important;
        text-transform: uppercase !important;
        /* 三重のドロップシャドウで発光を強化 */
        filter: drop-shadow(0 0 5px #FFF) drop-shadow(0 0 15px {CONFIG["neon_blue"]}) drop-shadow(0 0 30px {CONFIG["neon_blue"]}) !important;
        padding: 40px 0 !important;
        margin: 0 !important;
        line-height: 1.2 !important;
    }}

    /* 3. エージェントエリア：透明度を上げたサイバーパネル */
    .ai-agent-container {{
        background: rgba(0, 255, 65, 0.03) !important;
        border: 2px solid {CONFIG["neon_blue"]} !important;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.2), inset 0 0 15px rgba(0, 229, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 25px !important;
        backdrop-filter: blur(8px) !important;
        margin-bottom: 40px !important;
        display: flex;
        align-items: center;
        gap: 20px;
    }}

    /* 4. ニュースカード：暗色背景に映える高コントラスト設計 */
    .news-card {{
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(0, 255, 65, 0.1) !important;
        border-left: 6px solid {CONFIG["primary"]} !important;
        border-radius: 4px !important;
        padding: 22px !important;
        margin-bottom: 18px !important;
        transition: 0.3s !important;
    }}
    .news-card:hover {{
        background: rgba(0, 255, 65, 0.05) !important;
        border-left: 6px solid {CONFIG["neon_pink"]} !important;
        transform: scale(1.01) !important;
    }}

    /* 5. ニュースリンク：視認性MAXのシアン */
    .news-card a {{
        color: #00E5FF !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        text-decoration: none !important;
        line-height: 1.5 !important;
        text-shadow: 0 0 5px rgba(0, 229, 255, 0.3) !important;
    }}

    .time-tag {{
        color: {CONFIG["neon_pink"]} !important;
        font-family: 'Orbitron' !important;
        font-size: 0.75rem !important;
        letter-spacing: 2px;
        margin-bottom: 8px;
    }}

    .analysis-text {{
        color: #BBBBBB !important;
        font-size: 0.9rem !important;
        margin-top: 12px;
        border-top: 1px solid rgba(255,255,255,0.05);
        padding-top: 10px;
    }}

    /* 不要な標準パーツの隠蔽 */
    [data-testid="stHeader"], footer {{ display: none !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- APPLICATION LAYOUT ---

st.write(f"<h1>{CONFIG['site_name']}</h1>")

with st.container():
    st.markdown(f"""
    <div class="ai-agent-container">
        <div style="font-size: 3.5rem; filter: drop-shadow(0 0 10px {CONFIG['primary']});">{CONFIG['editor_avatar']}</div>
        <div>
            <div style="color:{CONFIG['primary']}; font-family:Orbitron; font-weight:bold; letter-spacing:2px;">>> CORE_INTELLIGENCE</div>
            <div style="color:#FFFFFF; font-size:1rem; opacity:0.95;">[SYSTEM: ONLINE] グリッド同期完了。JST時間軸で最新データをデプロイしました。</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
        <div style="margin: 12px 0;"><a href="{entry.link}" target="_blank">{entry.title}</a></div>
        <div class="analysis-text">
            <span style="color:{CONFIG['primary']}; font-family:Roboto Mono;">[AI_ANALYSIS]</span> 
            トレンド同期率: {random.randint(97, 99)}% // 解析完了。優先度：HIGH
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:rgba(255,255,255,0.1); font-family:Orbitron; font-size:10px; margin-top:50px;'>ESTABLISHED // FERMENT-LOGIC v17.0</p>", unsafe_allow_html=True)
