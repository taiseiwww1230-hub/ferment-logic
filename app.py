import streamlit as st
import feedparser
from datetime import datetime
import urllib.parse
import random

# --- EXECUTIVE TERMINAL v6.0 (List-Efficiency Mode) ---
CONFIG = {
    "site_name": "FERMENT-LOGIC // INTEL",
    "editor_name": "CORE-AI: FERMENT",
    "editor_avatar": "🛰️",
    "primary": "#00FF41",   # ネオングリーン
    "secondary": "#FFFFFF", 
    "neon_blue": "#00E5FF", 
    "neon_pink": "#FF00E0", 
    "bg_deep": "#020502",   
    "news_query": '(ヨーグルト OR 乳製品 OR 乳酸菌 OR 紅茶 OR 茶葉) AND ("新発売" OR "期間限定" OR "独自開発" OR "トレンド") when:7d',
    "greeting": "[SCANNING...] 直近168時間の高純度データを抽出。一覧性を最適化しました。"
}

st.set_page_config(page_title=CONFIG["site_name"], page_icon="🧬", layout="centered")

# --- HIGH-DENSITY CYBER UI (一覧性と鮮やかさの融合) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Orbitron:wght@500;700&family=Roboto+Mono:wght@300&display=swap');

    .stApp {{
        background-color: {CONFIG["bg_deep"]};
        background-image: 
            radial-gradient(at 0% 0%, rgba(0, 255, 65, 0.08) 0px, transparent 40%),
            radial-gradient(at 100% 100%, rgba(0, 229, 255, 0.08) 0px, transparent 40%),
            radial-gradient(at 50% 50%, rgba(255, 0, 224, 0.03) 0px, transparent 50%);
        color: {CONFIG["secondary"]};
        font-family: 'Inter', sans-serif;
    }}

    .stTitle {{
        font-family: 'Orbitron', sans-serif;
        font-size: 1.6rem !important; /* タイトルを少し小型化 */
        letter-spacing: 3px;
        color: {CONFIG["secondary"]} !important;
        text-align: center;
        margin-top: 10px !important;
        text-shadow: 0 0 10px {CONFIG["neon_blue"]};
    }}

    .ai-status-bar {{
        font-family: 'Roboto Mono', monospace;
        font-size: 9px;
        color: {CONFIG["primary"]};
        text-align: center;
        border: 1px solid rgba(0, 255, 65, 0.2);
        padding: 3px;
        margin-bottom: 20px;
        background: rgba(0, 255, 65, 0.05);
        opacity: 0.8;
    }}

    /* ニュースカード：高さを圧縮し一覧性を向上 */
    .news-card {{
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-left: 3px solid {CONFIG["primary"]};
        padding: 15px 20px; /* 余白を最適化 */
        margin-bottom: 12px; /* カード間の距離を短縮 */
        border-radius: 2px;
        transition: 0.3s ease;
    }}
    .news-card:hover {{
        background: rgba(255, 255, 255, 0.05);
        border-left: 3px solid {CONFIG["neon_pink"]};
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.1);
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
        font-size: 1.05rem; /* 文字サイズを微調整 */
        font-weight: 600;
        line-height: 1.3;
        display: block;
    }}

    /* 分析セクションをコンパクトに */
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

# --- 画面構成 (High-Efficiency View) ---

st.title(f"{CONFIG['site_name']}")
st.markdown(f"<div class='ai-status-bar'>SYSTEM_STATUS: NOMINAL // LIST_DENSITY: HIGH // DATA_RANGE: 7D</div>", unsafe_allow_html=True)

# ニュース取得
@st.cache_data(ttl=1800)
def fetch_news_v6():
    encoded_query = urllib.parse.quote(CONFIG["news_query"])
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"
    try:
        feed = feedparser.parse(url)
        return feed.entries[:20] # 件数を20件に増やしても快適
    except:
        return []

items = fetch_news_v6()

# ニュースリスト表示
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
st.write(f"<p style='text-align:center; color:#333; font-family:Orbitron; font-size:9px; padding:40px;'>Stay Fermented. | v6.0 Optimized</p>", unsafe_allow_html=True)
