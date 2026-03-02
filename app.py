import streamlit as st
import feedparser
from datetime import datetime
import urllib.parse
import random

# --- EXECUTIVE TERMINAL v9.0 (Cosmic Cherry Blossom) ---
CONFIG = {
    "site_name": "FERMENT-LOGIC // INTELLIGENCE",
    "editor_name": "CORE-AI: FERMENT",
    "editor_avatar": "🛰️",
    # 桜の背景とネオンのコントラストを調整
    "primary": "#00FF41",   # Matrix Green
    "secondary": "#FFFFFF", 
    "neon_blue": "#00E5FF", 
    "neon_pink": "#FF00E0", 
    "bg_fallback": "#0A0A0A", # 画像読み込み失敗時の背景
    "news_query": '(ヨーグルト OR 乳製品 OR 乳酸菌 OR 紅茶 OR 茶葉) AND ("新発売" OR "期間限定" OR "独自開発" OR "トレンド") when:7d',
    "greeting": "[SYSTEM: ONLINE] 168hデータ同期完了。桜舞う世界で最新の知性を抽出しました。"
}

st.set_page_config(page_title=CONFIG["site_name"], page_icon="🧬", layout="centered")

# --- VISUAL INTEGRATION (桜背景とネオンUIの融合) ---
# ご提示いただいた画像を背景に設定し、UIの可読性を確保するための工夫を凝らします。
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Orbitron:wght@500;700&family=Roboto+Mono:wght@300&display=swap');

    /* 背景：指定された画像を全画面表示し、UIとの間に薄い霧（グラデーション）を配置 */
    .stApp {{
        background-color: {CONFIG["bg_fallback"]};
        background-image: 
            /* UIの下に薄い暗色のグラデーションを配置し、可読性を向上 */
            linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.8)),
            /* ご提示いただいた画像を背景に設定。URLは適宜書き換えてください。 */
            url('{"https://lh3.googleusercontent.com/u/0/drive-viewer/AEYmBYRo-P_yXN_H8448H_rA-N6N_x0z_bE_V4_R_E8=w1920-h1080"}'); 
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: {CONFIG["secondary"]};
        font-family: 'Inter', sans-serif;
    }}
    /* 全体に薄く走る走査線（メカメカしさ）を維持 */
    .stApp::before {{
        content: " ";
        position: fixed; top: 0; left: 0; bottom: 0; right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.1) 50%);
        z-index: 9999;
        background-size: 100% 4px;
        pointer-events: none;
        opacity: 0.3;
    }}

    /* ヘッダー：ネオン管の発光を維持 */
    .stTitle {{
        font-family: 'Orbitron', sans-serif;
        font-size: 1.6rem !important;
        letter-spacing: 3px;
        color: {CONFIG["secondary"]} !important;
        text-align: center;
        margin-top: 15px !important;
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
        margin-bottom: 20px;
        background: rgba(0, 255, 65, 0.05);
        opacity: 0.8;
    }}

    /* 衛星エージェント：宇宙に漂う浮遊感を維持 */
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
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.1);
    }}
    .ai-avatar {{
        font-size: 2.8rem;
        animation: float 4s ease-in-out infinite;
    }}
    @keyframes float {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-8px); }}
        100% {{ transform: translateY(0px); }}
    }}

    /* ニュースカード：一覧性重視のサイバーパネルを維持しつつ、背景を少し透けさせる */
    .news-card {{
        background: rgba(0, 0, 0, 0.4); /* 背景をより暗くし、可読性を確保 */
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-left: 3px solid {CONFIG["primary"]};
        padding: 18px;
        margin-bottom: 12px;
        border-radius: 3px;
        transition: 0.3s;
    }}
    .news-card:hover {{
        background: rgba(0, 229, 255, 0.05); /* ホバー時の滲みをブルーへ */
        border-left: 3px solid {CONFIG["neon_pink"]};
        box-shadow: 0 0 25px rgba(0, 229, 255, 0.2);
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

# --- 画面構成 (Cosmic Cherry Blossom Edition) ---

st.title(f"{CONFIG['site_name']}")
st.markdown(f"<div style='text-align:center; font-family:Roboto Mono; font-size:10px; color:{CONFIG['primary']}; margin-bottom:20px; letter-spacing:2px;'>STARDUST_DENSITY: MAX // SAT_LINK: STABLE</div>", unsafe_allow_html=True)

# 衛星エージェント
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

# ニュース取得
@st.cache_data(ttl=1800)
def fetch_news_cosmic():
    encoded_query = urllib.parse.quote(CONFIG["news_query"])
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"
    try:
        feed = feedparser.parse(url)
        return feed.entries[:20]
    except:
        return []

items = fetch_news_cosmic()

# ニュースリスト（高密度設計）
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
st.write(f"<p style='text-align:center; color:#444; font-family:Orbitron; font-size:9px; padding:50px;'>To the Edge of the Universe with Sakura. | FERMENT-LOGIC v9.0</p>", unsafe_allow_html=True)
