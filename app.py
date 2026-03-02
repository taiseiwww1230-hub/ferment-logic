import streamlit as st
import feedparser
from datetime import datetime
import urllib.parse

# --- 設定エリア ---
CONFIG = {
    "site_name": "Ferment-Logic",
    "editor_name": "Ferment-AI",
    "editor_avatar": "🧬",
    "theme_color": "#00FF41", # マトリックス・グリーン
    "accent_color": "#00E5FF", # ネオンブルー
    "bg_color": "#0a0a0a",     # ダークモード
    "news_query": "ヨーグルト OR お茶 OR 飲料 新商品",
    "greeting": "System Online. 発酵ロジック展開中... 君の脳をアップデートするニュースを抽出したよ。"
}

st.set_page_config(page_title=CONFIG["site_name"], page_icon=CONFIG["editor_avatar"], layout="centered")

# --- AIチックな超華やかカスタムCSS ---
st.markdown(f"""
    <style>
    /* 全体の背景をサイバーな黒に */
    .stApp {{
        background-color: {CONFIG["bg_color"]};
        color: #e0e0e0;
    }}
    /* タイトルにネオン発光エフェクト */
    .stTitle {{
        color: {CONFIG["theme_color"]} !important;
        text-shadow: 0 0 10px {CONFIG["theme_color"]}, 0 0 20px {CONFIG["theme_color"]};
        font-family: 'Courier New', Courier, monospace;
        text-align: center;
        border-bottom: 2px solid {CONFIG["theme_color"]};
    }}
    /* ニュースカードをガラス細工風に（グラスモーフィズム） */
    .news-card {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid rgba(0, 255, 65, 0.3);
        margin-bottom: 20px;
        transition: 0.3s;
    }}
    .news-card:hover {{
        border: 1px solid {CONFIG["theme_color"]};
        box-shadow: 0 0 15px {CONFIG["theme_color"]};
        transform: translateY(-5px);
    }}
    /* タグを点滅させる */
    .status-tag {{
        background: transparent;
        color: {CONFIG["accent_color"]};
        border: 1px solid {CONFIG["accent_color"]};
        padding: 2px 12px;
        border-radius: 50px;
        font-size: 0.7em;
        font-family: 'Courier New', sans-serif;
        text-transform: uppercase;
        animation: blink 2s infinite;
    }}
    @keyframes blink {{
        0% {{ opacity: 1; }} 50% {{ opacity: 0.4; }} 100% {{ opacity: 1; }}
    }}
    </style>
    """, unsafe_allow_html=True)

# ヘッダー表示
st.title(f" {CONFIG['site_name']}")
st.write(f"<p style='text-align: center; color: {CONFIG['theme_color']}; font-family: monospace;'>>> ANALYZING RECENT FERMENTATION TRENDS...</p>", unsafe_allow_html=True)

# AI編集長エリア
with st.expander("✨ AI-EDITOR STATUS: ONLINE", expanded=True):
    col1, col2 = st.columns([1, 4])
    with col1:
        st.write(f"<h1 style='text-align:center;'>{CONFIG['editor_avatar']}</h1>", unsafe_allow_html=True)
    with col2:
        st.write(f"**{CONFIG['editor_name']}**: \n\n {CONFIG['greeting']}")

# ニュース取得
@st.cache_data(ttl=3600)
def fetch_news():
    encoded_query = urllib.parse.quote(CONFIG["news_query"])
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"
    try:
        feed = feedparser.parse(url)
        return feed.entries[:10]
    except:
        return []

news_items = fetch_news()

# カード表示
for entry in news_items:
    st.markdown(f"""
    <div class="news-card">
        <span class="status-tag">● AI_LOGIC_EXTRACTED</span>
        <h3 style="margin: 15px 0 10px 0;">
            <a href="{entry.link}" target="_blank" style="text-decoration:none; color:{CONFIG['theme_color']};">
                {entry.title}
            </a>
        </h3>
        <p style="font-size:0.8em; color:#aaa; font-family: monospace;">
            TIMESTAMP: {entry.get('published', 'N/A')}<br>
            [COMMENT]: 人工知能による解析の結果、本記事は君の健康マトリックスに正の影響を与えると推論される。
        </p>
    </div>
    """, unsafe_allow_html=True)

st.write("<p style='text-align: center; color: #333;'>- END OF ENCRYPTED DATA -</p>", unsafe_allow_html=True)
