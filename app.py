import streamlit as st
import feedparser
from datetime import datetime, timedelta, timezone
import urllib.parse
import time
import re

# --- CONFIG ---
CONFIG = {
    "site_name": "FERMENT-LOGIC // INTELLIGENCE",
    "editor_avatar": "🛰️",
    "primary": "#00FF41",   
    "neon_blue": "#00E5FF", 
    "neon_pink": "#FF00E0", 
    "query": '(ヨーグルト OR 乳製品 OR 乳酸菌 OR 紅茶 OR 茶葉) AND ("新発売" OR "期間限定" OR "独自開発" OR "トレンド") when:7d',
    "initial_display": 15,
    "step_display": 15
}

st.set_page_config(page_title=CONFIG["site_name"], layout="wide")

# セッション状態の初期化
if "display_count" not in st.session_state:
    st.session_state.display_count = CONFIG["initial_display"]

# --- CSS: 完璧な視覚制御 ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Roboto+Mono:wght@400;700&display=swap');
    
    [data-testid="stAppViewContainer"] {{ background-color: #000201 !important; }}
    .main .block-container {{ max-width: 100% !important; padding: 2rem 5% !important; display: flex; flex-direction: column; align-items: center; }}
    .news-wrapper {{ max-width: 850px; width: 100%; z-index: 100; }}

    /* スクロール連動型：フェードアウト・ヘッダー */
    .header-group {{
        text-align: center;
        width: 100%;
        margin-bottom: 40px;
    }}

    /* 右上メトリクス：ヘッダー群として配置（スクロールで消える） */
    .side-metrics {{
        font-family: 'Roboto Mono'; font-size: 0.85rem; color: {CONFIG["neon_blue"]};
        opacity: 0.8; border-right: 4px solid {CONFIG["neon_blue"]};
        padding-right: 15px; text-align: right; line-height: 1.8;
        display: inline-block; position: absolute; right: 5%; top: 40px;
    }}

    /* タイトル & 衛星 */
    .title {{ color: #FFFFFF; font-family: 'Orbitron'; font-size: 1.8rem; letter-spacing: 10px; padding: 20px 0; text-shadow: 0 0 20px {CONFIG["primary"]}; }}
    .satellite {{ font-size: 6rem; filter: drop-shadow(0 0 30px {CONFIG["primary"]}); animation: float 4s ease-in-out infinite; }}

    /* ニュースカード */
    .news-card {{
        background: rgba(0, 10, 5, 0.95); border: 1px solid {CONFIG["primary"]}; border-left: 10px solid {CONFIG["primary"]};
        padding: 30px; margin-bottom: 25px; transition: 0.3s;
    }}
    .news-card:hover {{ border-color: {CONFIG["neon_pink"]}; border-left-color: {CONFIG["neon_pink"]}; transform: scale(1.01); }}
    .news-card a {{ color: white !important; font-size: 1.3rem; font-weight: 900; text-decoration: none !important; text-shadow: 0 0 5px {CONFIG["neon_blue"]}; }}

    /* 下部コンソール：ボタン並列配置 */
    .stButton > button {{
        background: transparent !important; color: {CONFIG["primary"]} !important; border: 3px solid {CONFIG["primary"]} !important;
        height: 60px !important; font-family: 'Orbitron' !important; font-size: 1.2rem !important;
        transition: 0.3s !important; width: 100% !important;
    }}
    .stButton > button:hover {{ background: {CONFIG["neon_pink"]} !important; color: white !important; border-color: {CONFIG["neon_pink"]} !important; }}

    /* 特殊：DEFRAGMENTボタン（縮小）の色味変更 */
    div[data-testid="column"]:nth-child(2) .stButton > button {{
        color: {CONFIG["neon_blue"]} !important; border-color: {CONFIG["neon_blue"]} !important;
    }}

    @keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-20px); }} }}
    header, footer {{ visibility: hidden !important; }}
</style>
""", unsafe_allow_html=True)

# --- LOGIC ---
@st.cache_data(ttl=60)
def fetch_news():
    q = urllib.parse.quote(CONFIG["query"])
    f = feedparser.parse(f"https://news.google.com/rss/search?q={q}&hl=ja&gl=JP&ceid=JP:ja")
    entries = f.entries
    unique_entries = []
    seen = set()
    for entry in entries:
        fp = re.sub(r'\s+', '', entry.title)[:25]
        if fp not in seen:
            unique_entries.append(entry)
            seen.add(fp)
    return unique_entries

# --- RENDERING ---

# 1. ヘッダーエリア（スクロールで衛星と共にフェードアウト）
st.markdown(f"""
<div class="header-group">
    <div class="side-metrics">
        >> LATENCY: 24ms<br>
        >> UPLINK: SECURE<br>
        >> STATUS: MONITORING<br>
        >> SOURCE: G_INTEL
    </div>
    <div class="satellite">{CONFIG["editor_avatar"]}</div>
    <div class="title">{CONFIG["site_name"]}</div>
</div>
""", unsafe_allow_html=True)

# 2. ニュースリスト
st.markdown('<div class="news-wrapper">', unsafe_allow_html=True)
all_items = fetch_news()
JST = timezone(timedelta(hours=+9), 'JST')
display_items = all_items[:st.session_state.display_count]

for entry in display_items:
    dt = "2026/--/--"
    if entry.get('published_parsed'):
        dt = datetime.fromtimestamp(time.mktime(entry.published_parsed), timezone.utc).astimezone(JST).strftime('%Y/%m/%d %H:%M')
    
    st.markdown(f"""
    <div class="news-card">
        <div style="color:{CONFIG['neon_pink']}; font-family:'Roboto Mono'; font-size:0.9rem; margin-bottom:10px;">
            ▶ SYNC_TS // {dt} JST
        </div>
        <a href="{entry.link}" target="_blank">{entry.title}</a>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 3. ボトム・コントロール・コンソール
st.write("---")
col1, col2 = st.columns([2, 1])

with col1:
    if st.button("[ EXPAND DATABASE ]"):
        st.session_state.display_count += CONFIG["step_display"]
        st.rerun()

with col2:
    # 現在の表示数が初期数より多い場合のみ、折り畳み（リセット）ボタンを表示
    if st.session_state.display_count > CONFIG["initial_display"]:
        if st.button("[ DEFRAG ]"):
            st.session_state.display_count = CONFIG["initial_display"]
            st.rerun()
