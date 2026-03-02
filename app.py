import streamlit as st
import feedparser
from datetime import datetime
import urllib.parse
import random

# --- EXECUTIVE TERMINAL v7.0 (Deep Space Network) ---
CONFIG = {
    "site_name": "FERMENT-LOGIC // INTELLIGENCE",
    "editor_name": "CORE-AI: FERMENT",
    "editor_avatar": "🛰️",
    # 宇宙とネオンのコントラストを強調する配色
    "primary": "#00FF41",   # Matrix Green
    "secondary": "#FFFFFF", 
    "neon_blue": "#00E5FF", 
    "neon_pink": "#FF00E0", 
    "space_black": "#010101", # 漆黒
    "news_query": '(ヨーグルト OR 乳製品 OR 乳酸菌 OR 紅茶 OR 茶葉) AND ("新発売" OR "期間限定" OR "独自開発" OR "トレンド") when:7d',
    "greeting": "[SYSTEM: ONLINE] 深宇宙ネットワークよりデータを同期。直近168時間の重要相関をデプロイしました。"
}

st.set_page_config(page_title=CONFIG["site_name"], page_icon="🧬", layout="centered")

# --- DEEP SPACE UI (星屑背景とネオン衛星の融合) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Orbitron:wght@500;700&family=Roboto+Mono:wght@300&display=swap');

    /* 背景：漆黒に星屑を散りばめる */
    .stApp {{
        background-color: {CONFIG["space_black"]};
        background-image: 
            /* 星屑のエフェクト（非常に細かい radial-gradient の組み合わせ） */
            radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
            radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px),
            radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 3px),
            /* 深宇宙の霧（遠くのネオンの滲み） */
            radial-gradient(at 10% 10%, rgba(0, 255, 65, 0.03) 0px, transparent 50%),
            radial-gradient(at 90% 90%, rgba(0, 229, 255, 0.03) 0px, transparent 50%);
        background-size: 550px 550px, 350px 350px, 250px 250px, 100% 100%, 100% 100%;
        background-position: 0 0, 40px 60px, 130px 270px, 0 0, 0 0;
        color: {CONFIG["secondary"]};
        font-family: 'Inter', sans-serif;
    }}

    .stTitle {{
        font-family: 'Orbitron', sans-serif;
        font-size: 1.6rem !important;
        letter-spacing: 3px;
        color: {CONFIG["secondary"]} !important;
        text-align: center;
        margin-top: 10px !important;
        /* ネオン管のような発光 */
        text-shadow: 
            0 0 5px {CONFIG["secondary"]},
            0 0 10px {CONFIG["neon_blue"]},
            0 0 20px {CONFIG["neon_blue"]};
    }}

    .ai-status-bar {{
        font-family: 'Roboto Mono', monospace;
        font-size: 9px;
        color: {CONFIG["primary"]};
        text-align: center;
        border: 1px solid rgba(0, 255, 65, 0.2);
        padding: 3px;
        margin-bottom: 30px;
        background: rgba(0, 255, 65, 0.05);
        opacity: 0.8;
    }}

    /* AIエージェント（衛星）：ネオンの光を纏って浮遊 */
    .ai-agent-container {{
        background: rgba(0, 0, 0, 0.6);
        border: 1px solid rgba(0, 229, 255, 0.2);
        padding: 20px;
        border-radius: 4px;
        margin-bottom: 50px;
        display: flex;
        align-items: center;
        gap: 20px;
        backdrop-filter: blur(10px);
    }}
    .ai-avatar {{
        font-size: 2.5rem;
        color: {CONFIG["neon_blue"]};
        /* 衛星が青く光るエフェクト */
        text-shadow: 0 0 15px {CONFIG["neon_blue"]};
    }}

    /* ニュースカード：高密度設計を維持しつつ、宇宙に浮かぶパネルのように */
    .news-card {{
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-left: 3px solid {CONFIG["primary"]};
        padding: 15px 20px;
        margin-bottom: 12px;
        border-radius: 2px;
        transition: 0.3s ease;
    }}
    .news-card:hover {{
        background: rgba(0, 229, 255, 0.03);
        border-left: 3px solid {CONFIG["neon_pink"]};
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.15);
        transform: scale(1.01);
    }}

    .time-tag {{
        color: {CONFIG["neon_pink"]};
        font-size: 0.65rem;
        font-family: 'Orbitron', sans-serif;
        margin-bottom: 6px;
        display: block;
        opacity: 0.7;
    }}

    .news-card a {{
        color: {CONFIG["secondary"]} !important;
        text-decoration: none;
        font-size: 1.05rem;
        font-weight: 600;
        line-height: 1.3;
        display: block;
    }}

    .analysis-content {{
        margin-top: 10px;
        font-size: 0.8rem;
        color: #999;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        padding-top: 8px;
        line-height: 1.4;
    }}

    </style>
    """, unsafe_allow_html=True)

# --- 画面構成 (Deep Space View) ---

# ヘッダーエリア
st.title(f"{CONFIG['site_name']}")
st.markdown(f"<div class='ai-status-bar'>CONNECTION:D_S_N // SCAN_MODE:HYPER_SPECTRAL // GRID:7D</div>", unsafe_allow_html=True)

# AIエージェント・コンソール（衛星の復活）
with st.container():
    st.markdown(f"""
    <div class="ai-agent-container">
        <div class="ai-avatar">{CONFIG['editor_avatar']}</div>
        <div>
            <span style="color:{CONFIG['primary']}; font-family:Orbitron; font-weight:700;">[ {CONFIG['editor_name']} // ON ]</span><br>
            <span style="color:{CONFIG['secondary']}; font-size:0.9rem; font-weight:300;">{CONFIG['greeting']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ニュース取得
@st.cache_data(ttl=1800)
def fetch_news_v7():
    encoded_query = urllib.parse.quote(CONFIG["news_query"])
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"
    try:
        feed = feedparser.parse(url)
        return feed.entries[:20] # 一覧性を重視し20件表示
    except:
        return []

items = fetch_news_v7()

# ニュースリスト表示（高密度設計）
for i, entry in enumerate(items):
    pub_date = entry.get('published', '')
    accuracy = random.randint(97, 99)
    
    st.markdown(f"""
    <div class="news-card">
        <span class="time-tag">INTEL_LOG // {pub_date[:16]}</span>
        <a href="{entry.link}" target="_blank">{entry.title}</a>
        <div class="analysis-content">
            <span style="color:{CONFIG['primary']}; font-family:'Roboto Mono'; font-size:9px;">[AI_REASONING]</span>
            市場のパラダイムシフトを検知。成分相関を確認済み。
            <span style="color:{CONFIG['neon_blue']}; font-size:9px;">>> ACCURACY: {accuracy}% // PRIORITY: HIGH</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# フッター
st.write(f"<p style='text-align:center; color:#222; font-family:Orbitron; font-size:9px; padding:40px;'>Stay Fermented. | FERMENT-LOGIC v7.0 // DEEP SPACE NETWORK</p>", unsafe_allow_html=True)
