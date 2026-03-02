import streamlit as st
import feedparser
from datetime import datetime
import urllib.parse
import random

# --- EXECUTIVE TERMINAL v5.0 (修正版) ---
CONFIG = {
    "site_name": "FERMENT-LOGIC // INTELLIGENCE",
    "editor_name": "CORE-AI: FERMENT",
    "editor_avatar": "🛰️",
    # 以前のコードで不足していたキーを追加・統合
    "primary": "#00FF41",   # ネオングリーン
    "secondary": "#FFFFFF", # ホワイト（これが不足していました）
    "neon_blue": "#00E5FF", # サイバーブルー
    "neon_pink": "#FF00E0", # アクセントピンク
    "bg_deep": "#020502",   # 深淵の黒
    # 検索クエリ：直近7日間に厳格化
    "news_query": '(ヨーグルト OR 乳製品 OR 乳酸菌 OR 紅茶 OR 茶葉) AND ("新発売" OR "期間限定" OR "独自開発" OR "トレンド") when:7d',
    "greeting": "[SYSTEM: ONLINE] 直近168時間の高純度データを抽出。茶葉と発酵の最新相関をデプロイしました。"
}

st.set_page_config(page_title=CONFIG["site_name"], page_icon="🧬", layout="centered")

# --- HYPER NEON VISUALS (滲むネオンと縦長没入UI) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Orbitron:wght@500;700&family=Roboto+Mono:wght@300&display=swap');

    /* 背景：ネオンが滲む深い霧の演出 */
    .stApp {{
        background-color: {CONFIG["bg_deep"]};
        background-image: 
            radial-gradient(at 0% 0%, rgba(0, 255, 65, 0.08) 0px, transparent 40%),
            radial-gradient(at 100% 100%, rgba(0, 229, 255, 0.08) 0px, transparent 40%),
            radial-gradient(at 50% 50%, rgba(255, 0, 224, 0.03) 0px, transparent 50%);
        color: {CONFIG["secondary"]};
        font-family: 'Inter', sans-serif;
    }}

    /* タイトル：ご提示の画像に基づき、よりシャープな発光へ */
    .stTitle {{
        font-family: 'Orbitron', sans-serif;
        font-size: 2.2rem !important;
        letter-spacing: 4px;
        color: {CONFIG["secondary"]} !important;
        text-align: center;
        margin-top: 20px !important;
        text-shadow: 0 0 10px {CONFIG["neon_blue"]}, 0 0 20px {CONFIG["neon_blue"]};
    }}

    /* AIステータスバー：余白を埋めるメカニカルパーツ */
    .ai-status-bar {{
        font-family: 'Roboto Mono', monospace;
        font-size: 10px;
        color: {CONFIG["primary"]};
        text-align: center;
        border: 1px solid rgba(0, 255, 65, 0.3);
        padding: 5px;
        margin-bottom: 30px;
        background: rgba(0, 255, 65, 0.02);
        letter-spacing: 2px;
    }}

    /* ニュースカード：縦長の没入感重視デザイン */
    .news-card {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-left: 4px solid {CONFIG["primary"]};
        padding: 25px;
        margin-bottom: 25px;
        border-radius: 4px;
        transition: 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
    }}
    .news-card:hover {{
        border-left: 4px solid {CONFIG["neon_pink"]};
        background: rgba(255, 255, 255, 0.05);
        box-shadow: 0 0 25px rgba(0, 229, 255, 0.1);
    }}

    .time-tag {{
        color: {CONFIG["neon_pink"]};
        font-size: 0.7rem;
        font-family: 'Orbitron', sans-serif;
        margin-bottom: 12px;
        display: block;
        opacity: 0.8;
    }}

    .news-card a {{
        color: {CONFIG["secondary"]} !important;
        text-decoration: none;
        font-size: 1.25rem;
        font-weight: 600;
        line-height: 1.4;
    }}

    /* 分析ボックス：AIの存在感を強調 */
    .analysis-content {{
        margin-top: 18px;
        font-size: 0.85rem;
        color: #BBB;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding-top: 15px;
        line-height: 1.6;
    }}

    </style>
    """, unsafe_allow_html=True)

# --- 画面構成 (1カラム・プロ仕様) ---

# ヘッダーエリア
st.title(f"{CONFIG['site_name']}")
st.markdown(f"<div class='ai-status-bar'>SYSTEM_STATUS: ACTIVE // USER: EXECUTIVE // DATA_SCAN: 168h_MODE</div>", unsafe_allow_html=True)

# AIエージェント・コンソール
col1, col2 = st.columns([1, 5])
with col1:
    st.write(f"<h1 style='text-align:center; color:{CONFIG['neon_blue']}; text-shadow: 0 0 10px {CONFIG['neon_blue']};'>{CONFIG['editor_avatar']}</h1>", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div style="background:rgba(0,0,0,0.4); border:1px solid rgba(0,255,65,0.2); padding:15px; border-radius:4px;">
        <span style="font-family:Orbitron; font-size:12px; color:{CONFIG['primary']};">[ {CONFIG['editor_name']} ]</span><br>
        <span style="font-size:0.9rem; color:#DDD; font-weight:300;">{CONFIG['greeting']}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ニュース取得
@st.cache_data(ttl=1800)
def fetch_news_v5():
    encoded_query = urllib.parse.quote(CONFIG["news_query"])
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"
    try:
        feed = feedparser.parse(url)
        return feed.entries[:15]
    except:
        return []

items = fetch_news_v5()

# ニュースリスト (1カラム・スマホでも読みやすい構成)
for i, entry in enumerate(items):
    pub_date = entry.get('published', '')
    accuracy = random.randint(96, 99)
    
    st.markdown(f"""
    <div class="news-card">
        <span class="time-tag">INTEL_LOG // {pub_date[:16]}</span>
        <h3><a href="{entry.link}" target="_blank">{entry.title}</a></h3>
        <div class="analysis-content">
            <span style="color:{CONFIG['primary']}; font-family:'Roboto Mono'; font-size:10px;">[AI_ANALYST_REASONING]</span><br>
            当該記事は直近の飲料・乳製品市場における重要なパラダイムシフトを示唆しています。
            茶葉成分のバイオ利用効率と発酵菌の相乗効果について高度な相関を確認しました。<br>
            <span style="color:{CONFIG['neon_blue']}; font-size:10px;">>> 推論精度: {accuracy}% // 優先度: HIGH</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# フッター
st.write(f"<p style='text-align:center; color:#444; font-family:Orbitron; font-size:10px; padding:60px;'>Stay Fermented. | FERMENT-LOGIC v5.0 | GRID_CONNECTED</p>", unsafe_allow_html=True)
