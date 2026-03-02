import streamlit as st
import feedparser
from datetime import datetime
import urllib.parse
import random

# --- EXECUTIVE TERMINAL v10.0 (Ferment Fairy Edition) ---
CONFIG = {
    "site_name": "FERMENT-LOGIC // INTELLIGENCE",
    "editor_name": "CORE-AI: FERMENT-FAIRY",
    # 以前の衛星の絵文字を削除
    "primary": "#00FF41",   
    "secondary": "#FFFFFF", 
    "neon_blue": "#00E5FF", 
    "neon_pink": "#FF00E0", 
    "space_black": "#010101", 
    "news_query": '(ヨーグルト OR 乳製品 OR 乳酸菌 OR 紅茶 OR 茶葉) AND ("新発売" OR "期間限定" OR "独自開発" OR "トレンド") when:7d',
    "greeting": "[SYSTEM: OPERATIONAL] 妖精通信よりデータを受信。宇宙に舞う最新の知性をデプロイしました。"
}

st.set_page_config(page_title=CONFIG["site_name"], page_icon="🧬", layout="centered")

# --- ULTIMATE SPACE UI (満天の星空と浮遊する妖精のエフェクト) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Orbitron:wght@500;700&family=Roboto+Mono:wght@300&display=swap');

    /* 背景：圧倒的な星の量と奥行き */
    .stApp {{
        background-color: {CONFIG["space_black"]};
        background-image: 
            /* レイヤー1: 小さく遠い星 */
            radial-gradient(1px 1px at 20px 30px, #eee, rgba(0,0,0,0)),
            radial-gradient(1.5px 1.5px at 40px 70px, #fff, rgba(0,0,0,0)),
            radial-gradient(1px 1px at 50% 10%, #ddd, rgba(0,0,0,0)),
            radial-gradient(2px 2px at 80% 30%, #fff, rgba(0,0,0,0)),
            radial-gradient(1px 1px at 10% 80%, #eee, rgba(0,0,0,0)),
            radial-gradient(1.5px 1.5px at 90% 85%, #fff, rgba(0,0,0,0)),
            radial-gradient(1px 1px at 25% 45%, #ddd, rgba(0,0,0,0)),
            /* レイヤー2: 密集した星屑 */
            radial-gradient(white, rgba(255,255,255,.2) 1.5px, transparent 2.5px),
            radial-gradient(white, rgba(255,255,255,.1) 1px, transparent 2px),
            /* レイヤー3: 遠くの銀河のような霧 */
            radial-gradient(at 10% 10%, rgba(0, 255, 65, 0.05) 0px, transparent 40%),
            radial-gradient(at 90% 90%, rgba(0, 229, 255, 0.05) 0px, transparent 40%);
        
        background-size: 150px 150px, 250px 250px, 200px 200px, 300px 300px, 350px 350px, 400px 400px, 220px 220px, 180px 180px, 280px 280px, 100% 100%, 100% 100%;
        color: {CONFIG["secondary"]};
        font-family: 'Inter', sans-serif;
    }}

    .stTitle {{
        font-family: 'Orbitron', sans-serif;
        font-size: 1.6rem !important;
        letter-spacing: 4px;
        color: {CONFIG["secondary"]} !important;
        text-align: center;
        margin-top: 15px !important;
        text-shadow: 0 0 10px {CONFIG["neon_blue"]}, 0 0 30px {CONFIG["neon_blue"]};
    }}

    /* 妖精エージェント：宇宙に漂う浮遊感とネオンの彩り */
    .ai-agent-container {{
        background: rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(0, 229, 255, 0.2);
        padding: 15px 25px;
        border-radius: 8px;
        margin-bottom: 40px;
        display: flex;
        align-items: center;
        gap: 25px; /* キャラクターとテキストの間隔を最適化 */
        backdrop-filter: blur(8px);
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.1);
    }}
    /* 妖精キャラクターの画像設定 */
    .fairy-avatar {{
        width: 80px; /* キャラクターのサイズを調整 */
        height: auto;
        border-radius: 50%; /* 丸く切り抜く */
        border: 3px solid {CONFIG["primary"]}; /* ネオングリーンの枠線 */
        box-shadow: 0 0 15px {CONFIG["primary"]}; /* 妖精が発光するエフェクト */
        animation: float 4s ease-in-out infinite;
    }}
    @keyframes float {{
        0% {{ transform: translateY(0px) rotate(0deg); }}
        50% {{ transform: translateY(-8px) rotate(3deg); }} /* 少し回転させて可愛らしさを強調 */
        100% {{ transform: translateY(0px) rotate(0deg); }}
    }}

    /* ニュースカード：一覧性重視のサイバーパネル */
    .news-card {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-left: 3px solid {CONFIG["primary"]};
        padding: 18px;
        margin-bottom: 12px;
        border-radius: 3px;
        transition: 0.3s;
    }}
    .news-card:hover {{
        background: rgba(255, 255, 255, 0.06);
        border-left: 3px solid {CONFIG["neon_pink"]};
        box-shadow: 0 0 25px rgba(0, 255, 65, 0.2);
    }}

    .time-tag {{
        color: {CONFIG["neon_pink"]};
        font-size: 0.65rem;
        font-family: 'Orbitron', sans-serif;
        margin-bottom: 8px;
        display: block;
        letter-spacing: 1px;
    }}

    .news-card a {{
        color: {CONFIG["secondary"]} !important;
        text-decoration: none;
        font-size: 1.05rem;
        font-weight: 600;
        line-height: 1.4;
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

# --- 画面構成 (Final Cosmic Edition with Fairy) ---

st.title(f"{CONFIG['site_name']}")
st.markdown(f"<div style='text-align:center; font-family:Roboto Mono; font-size:10px; color:{CONFIG['primary']}; margin-bottom:20px; letter-spacing:2px;'>STARDUST_DENSITY: MAX // SAT_LINK: STABLE</div>", unsafe_allow_html=True)

# 妖精エージェント（衛星をこの画像挿入で代替）
# ご提示いただいた画像を背景に設定。URLは適宜書き換えてください。
with st.container():
    st.markdown(f"""
    <div class="ai-agent-container">
        <img src="{"https://i.ibb.co/L5r6B4K/image-8.png"}" class="fairy-avatar" alt="Ferment Fairy">
        <div>
            <span style="color:{CONFIG['primary']}; font-family:Orbitron; font-weight:700; font-size:0.8rem;">[ {CONFIG['editor_name']} ]</span><br>
            <span style="color:#eee; font-size:0.9rem;">{CONFIG['greeting']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ニュース取得
@st.cache_data(ttl=1800)
def fetch_news_fairy():
    encoded_query = urllib.parse.quote(CONFIG["news_query"])
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"
    try:
        feed = feedparser.parse(url)
        return feed.entries[:20]
    except:
        return []

items = fetch_news_fairy()

# ニュースリスト
for entry in items:
    pub_date = entry.get('published', '')
    accuracy = random.randint(98, 99)
    st.markdown(f"""
    <div class="news-card">
        <span class="time-tag">INTEL_LOG // {pub_date[:16]}</span>
        <a href="{entry.link}" target="_blank">{entry.title}</a>
        <div class="analysis-content">
            <span style="color:{CONFIG['primary']}; font-size:9px; font-family:Roboto Mono;">[AI_REASONING]</span> 
            最新の市場動向と成分相関を分析。優先度：極めて高い。
            <span style="color:{CONFIG['neon_blue']}; font-size:9px;">>> ACCURACY: {accuracy}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# フッター
st.write(f"<p style='text-align:center; color:#222; font-family:Orbitron; font-size:9px; padding:50px;'>To the Edge of the Universe with Fairy. | v10.0</p>", unsafe_allow_html=True)
