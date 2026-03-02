import streamlit as st
import feedparser
from datetime import datetime
import urllib.parse

# --- PRO CORE CONFIG (プロ仕様設定) ---
CONFIG = {
    "site_name": "FERMENT-LOGIC / OS v2.0",
    "editor_name": "UNIT: FERMENT-AI",
    "editor_avatar": "⚙️",
    "primary": "#00FF41",   # Matrix Green
    "secondary": "#00E5FF", # Cyber Blue
    "warning": "#FF3D00",   # Deep Orange
    "bg_black": "#050505",
    "glass": "rgba(0, 40, 0, 0.2)",
    # 検索クエリの最適化（紅茶や乳製品を網羅）
    "news_query": '(ヨーグルト OR 乳製品 OR 乳酸菌) AND (紅茶 OR お茶 OR 飲料) "新発売" OR "トレンド"',
    "greeting": "[SYSTEM START]... 抽出シーケンス完了。TEA & DAIRY セクターの重要データを統合しました。閲覧を許可します。"
}

st.set_page_config(page_title=CONFIG["site_name"], page_icon="🧬", layout="wide")

# --- HYPER CYBER VISUALS (超近未来・メカメカしいデザイン) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

    /* 全体背景：スキャンライン効果 */
    .stApp {{
        background: linear-gradient({CONFIG["bg_black"]}, #0a1a0a);
        color: {CONFIG["primary"]};
        font-family: 'Share Tech Mono', monospace;
    }}
    .stApp::before {{
        content: " ";
        position: fixed; top: 0; left: 0; bottom: 0; right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
        z-index: 9999;
        background-size: 100% 4px, 3px 100%;
        pointer-events: none;
    }}

    /* タイトル：軍用HUD風 */
    .stTitle {{
        font-size: 3rem !important;
        text-transform: uppercase;
        letter-spacing: 5px;
        text-shadow: 2px 2px 0px {CONFIG["bg_black"]}, 0 0 20px {CONFIG["primary"]};
        border-left: 10px solid {CONFIG["primary"]};
        padding-left: 20px !important;
        margin-bottom: 30px !important;
    }}

    /* ニュースカード：メカニカル装飾 */
    .news-card {{
        background: {CONFIG["glass"]};
        border: 1px solid {CONFIG["primary"]};
        border-right: 5px solid {CONFIG["primary"]};
        padding: 20px;
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
        clip-path: polygon(0% 0%, 100% 0%, 100% 90%, 95% 100%, 0% 100%);
    }}
    .news-card::before {{
        content: "LOG_DATA_0x" ;
        position: absolute; top: 5px; right: 10px;
        font-size: 10px; opacity: 0.5;
    }}
    .news-card:hover {{
        background: rgba(0, 255, 65, 0.1);
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.4);
    }}

    /* リンクの装飾 */
    .news-card a {{
        color: {CONFIG["secondary"]} !important;
        text-decoration: none;
        font-weight: bold;
        font-size: 1.2rem;
    }}

    /* AIコメントエリア */
    .ai-box {{
        border: 2px dashed {CONFIG["secondary"]};
        padding: 15px;
        background: rgba(0, 229, 255, 0.05);
        margin-bottom: 40px;
    }}

    /* スクロールバー */
    ::-webkit-scrollbar {{ width: 5px; }}
    ::-webkit-scrollbar-thumb {{ background: {CONFIG["primary"]}; }}
    </style>
    """, unsafe_allow_html=True)

# --- 画面構成 ---

# 上部ステータスバー
col_l, col_r = st.columns([2, 1])
with col_l:
    st.title(f"{CONFIG['site_name']}")
with col_r:
    st.write(f"""
    <div style="text-align:right; font-size:12px; border:1px solid {CONFIG['primary']}; padding:5px;">
    STATUS: NOMINAL<br>
    AUTH: ROOT_USER<br>
    LOCAL_TIME: {datetime.now().strftime('%H:%M:%S')}
    </div>
    """, unsafe_allow_html=True)

# AIエージェント
st.markdown(f"""
<div class="ai-box">
    <span style="color:{CONFIG['secondary']}; font-weight:bold;">[ {CONFIG['editor_name']} ]</span><br>
    {CONFIG['greeting']}
</div>
""", unsafe_allow_html=True)

# ニュース取得 (件数を15件に増加)
@st.cache_data(ttl=1800) # 30分キャッシュで鮮度重視
def fetch_news_pro():
    encoded_query = urllib.parse.quote(CONFIG["news_query"])
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"
    try:
        feed = feedparser.parse(url)
        return feed.entries[:15] # 15件まで拡張
    except:
        return []

items = fetch_news_pro()

# ニュースグリッド表示（PCでは2列、スマホでは1列に自動調整）
col1, col2 = st.columns(2)

for i, entry in enumerate(items):
    target_col = col1 if i % 2 == 0 else col2
    with target_col:
        st.markdown(f"""
        <div class="news-card">
            <div style="font-size:10px; color:{CONFIG['primary']};">>> ANALYSIS_COMPLETE: SECTOR_{i+1:02}</div>
            <h3 style="margin:10px 0;"><a href="{entry.link}" target="_blank">{entry.title}</a></h3>
            <div style="font-size:12px; color:#888; border-top:1px solid #333; padding-top:10px;">
                <span style="color:{CONFIG['primary']};">[REPORT]</span> 
                紅茶・ヨーグルト含有成分によるバイオメトリクス向上を検知。即時の摂取を推奨。
            </div>
            <div style="text-align:right; font-size:10px; margin-top:10px; opacity:0.6;">
                REF: {entry.get('published', 'UNKNOWN_DATE')}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.write(f"<div style='text-align:center; padding:50px; color:{CONFIG['primary']}; opacity:0.3;'>-- ACCESSING GLOBAL FERMENTATION GRID --</div>", unsafe_allow_html=True)
