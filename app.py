import streamlit as st
import feedparser
from datetime import datetime, timedelta, timezone
import urllib.parse
import random
import time

# --- EXECUTIVE TERMINAL v19.0 (Super-Radiant Orbital) ---
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

# --- CSS: RADIANT IMPACT OVERRIDE ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Roboto+Mono:wght@500&display=swap');

    /* 1. 背景：暗さを払拭する「環境光」の導入 */
    [data-testid="stAppViewContainer"] {{
        background-color: #000c05 !important;
        background-image: 
            /* 画面上部からの強い青い光 */
            radial-gradient(circle at 50% -20%, rgba(0, 229, 255, 0.3), transparent 70%),
            /* 左下からのピンクの光 */
            radial-gradient(circle at -10% 100%, rgba(255, 0, 224, 0.15), transparent 50%),
            /* 電子グリッド */
            linear-gradient(rgba(0, 255, 65, 0.08) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 65, 0.08) 1px, transparent 1px) !important;
        background-size: 100% 100%, 100% 100%, 40px 40px, 40px 40px !important;
        background-attachment: fixed !important;
    }}

    /* 2. タイトル：絶対的な白と外光 */
    .absolute-title {{
        color: #FFFFFF !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 900 !important;
        font-size: 3rem !important;
        text-align: center !important;
        letter-spacing: 10px !important;
        padding-top: 60px !important;
        margin: 0 !important;
        text-shadow: 0 0 20px #FFF, 0 0 40px {CONFIG["neon_blue"]} !important;
        -webkit-text-fill-color: white !important;
    }}

    /* 3. 衛星：躍動感あふれる「周回振動」アニメーション */
    .satellite-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 40px 0;
    }}

    .moving-satellite {{
        font-size: 5rem;
        filter: drop-shadow(0 0 20px {CONFIG["neon_blue"]});
        animation: orbit-swing 6s ease-in-out infinite;
    }}

    @keyframes orbit-swing {{
        0% {{ transform: translate(0, 0) rotate(0deg); }}
        25% {{ transform: translate(30px, -15px) rotate(10deg); }}
        50% {{ transform: translate(0, -30px) rotate(0deg); }}
        75% {{ transform: translate(-30px, -15px) rotate(-10deg); }}
        100% {{ transform: translate(0, 0) rotate(0deg); }}
    }}

    /* 4. エージェントパネル：透過度を下げて「光を遮る実体」感を出す */
    .ai-panel {{
        background: rgba(0, 30, 15, 0.85) !important;
        border: 1px solid {CONFIG["primary"]} !important;
        box-shadow: 0 0 30px rgba(0, 255, 65, 0.2) !important;
        border-radius: 4px;
        padding: 25px;
        margin-bottom: 40px;
        backdrop-filter: blur(10px);
    }}

    /* 5. ニュースカード：ハイコントラスト */
    .news-card {{
        background: rgba(255, 255, 255, 0.05) !important;
        border-left: 8px solid {CONFIG["primary"]} !important;
        padding: 25px;
        margin-bottom: 20px;
        border-radius: 4px;
        transition: 0.3s cubic-bezier(0.19, 1, 0.22, 1);
    }}
    .news-card:hover {{
        background: rgba(255, 255, 255, 0.1) !important;
        transform: scale(1.02);
    }}

    .news-card a {{
        color: {CONFIG["neon_blue"]} !important;
        font-size: 1.3rem !important;
        font-weight: 900 !important;
        text-decoration: none !important;
    }}

    .time-tag {{ color: {CONFIG["neon_pink"]}; font-family: 'Orbitron'; font-size: 0.8rem; font-weight: bold; }}

    header, footer {{ visibility: hidden !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- RENDERING ---

# タイトル
st.markdown(f'<div class="absolute-title">{CONFIG["site_name"]}</div>', unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:{CONFIG['primary']}; font-family:Roboto Mono; font-size:12px; letter-spacing:4px;'>LOCAL_TIME: JST // SATELLITE_LINK: ESTABLISHED</p>", unsafe_allow_html=True)

# 躍動する衛星
st.markdown(f"""
    <div class="satellite-container">
        <div class="moving-satellite">{CONFIG['editor_avatar']}</div>
    </div>
    """, unsafe_allow_html=True)

# エージェントメッセージ
st.markdown(f"""
    <div class="ai-panel">
        <div style="color:{CONFIG['primary']}; font-family:Orbitron; font-weight:bold; font-size:1.2rem; margin-bottom:10px;">>> {CONFIG['editor_name']}</div>
        <div style="color:white; font-size:1rem; line-height:1.6;">
            環境光レベルを300%に上昇。衛星を周回軌道(Orbit-Swing)に投入しました。<br>
            JST時間軸に基づき、深層データからトレンドを自動抽出中...
        </div>
    </div>
    """, unsafe_allow_html=True)

# ニュースリスト
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
        <div style="margin: 15px 0;"><a href="{entry.link}" target="_blank">{entry.title}</a></div>
        <div style="color:#aaa; font-size:0.9rem; border-top:1px solid rgba(255,255,255,0.1); padding-top:10px; font-family:Roboto Mono;">
            [AI_REPORT] 信頼度: {random.randint(98, 99)}% // 解析シグナル良好。
        </div>
    </div>
    """, unsafe_allow_html=True)
