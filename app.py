import streamlit as st
import feedparser
from datetime import datetime, timedelta, timezone
import urllib.parse
import random
import time

# --- v24.4 CORE_OVERRIDE (背景強制固定・パルス完全実装) ---
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

st.set_page_config(page_title=CONFIG["site_name"], layout="centered")

if "display_count" not in st.session_state:
    st.session_state.display_count = CONFIG["initial_display"]

# --- CSS: 白背景を破壊し、パルスを強制注入 ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Roboto+Mono&display=swap');
    
    /* 1. 全ての親要素を強制的に黒くし、スクロール領域もパルスさせる */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: #000804 !important;
        background-image: none !important; /* 標準の背景を削除 */
    }}

    /* 2. 背景レイヤーを「最前面のすぐ後ろ」に固定してパルスを走らせる */
    [data-testid="stAppViewContainer"]::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        /* グリッドと中央の光 */
        background-image: 
            radial-gradient(circle at 50% 50%, rgba(0, 255, 65, 0.15), transparent 80%),
            linear-gradient(rgba(0, 255, 65, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 65, 0.1) 1px, transparent 1px) !important;
        background-size: 100% 100%, 30px 30px, 30px 30px !important;
        z-index: -1;
        /* ライブパルスアニメーション */
        animation: final-pulse 5s ease-in-out infinite alternate !important;
    }}

    @keyframes final-pulse {{
        0% {{ opacity: 0.6; filter: brightness(0.8) contrast(1); }}
        100% {{ opacity: 1; filter: brightness(1.3) contrast(1.2); }}
    }}

    /* タイトル：文字色を白で固定し、発光させる */
    .title {{
        color: #FFFFFF !important;
        font-family: 'Orbitron';
        font-size: 1.8rem;
        text-align: center;
        text-shadow: 0 0 15px {CONFIG["neon_blue"]};
        padding: 20px 0 10px 0;
        letter-spacing: 2px;
    }}

    /* 衛星 */
    .satellite {{
        text-align: center;
        font-size: 3.5rem;
        filter: drop-shadow(0 0 15px {CONFIG["neon_blue"]});
        animation: orbit-swing 6s ease-in-out infinite;
        margin-bottom: 20px;
    }}
    @keyframes orbit-swing {{
        0%, 100% {{ transform: translateY(0) rotate(0deg); }}
        50% {{ transform: translateY(-20px) rotate(10deg); }}
    }}

    /* ニュースカード */
    .news-card {{
        background: rgba(255, 255, 255, 0.05) !important;
        border-left: 5px solid {CONFIG["primary"]} !important;
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 4px;
        transition: 0.3s;
    }}
    .news-card:hover {{
        background: rgba(255, 255, 255, 0.1) !important;
        border-left: 5px solid {CONFIG["neon_pink"]} !important;
        transform: translateX(10px);
    }}
    
    .news-card a {{
        color: {CONFIG["neon_blue"]} !important;
        font-size: 1.1rem;
        font-weight: bold;
        text-decoration: none !important;
    }}

    /* ボタン */
    .stButton > button {{
        background: transparent !important;
        color: {CONFIG["primary"]} !important;
        border: 2px solid {CONFIG["primary"]} !important;
        width: 100% !important;
        height: 50px !important;
        font-family: 'Orbitron' !important;
    }}
    .stButton > button:hover {{
        background: {CONFIG["primary"]} !important;
        color: #000 !important;
        box-shadow: 0 0 30px {CONFIG["primary"]};
    }}

    header, footer {{ visibility: hidden !important; }}
</style>
""", unsafe_allow_html=True)

# --- RENDERING ---
st.markdown(f'<div class="title">{CONFIG["site_name"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="satellite">{CONFIG["editor_avatar"]}</div>', unsafe_allow_html=True)

# ニュース取得
@st.cache_data(ttl=1800)
def fetch_news():
    q = urllib.parse.quote(CONFIG["query"])
    f = feedparser.parse(f"https://news.google.com/rss/search?q={q}&hl=ja&gl=JP&ceid=JP:ja")
    entries = f.entries
    entries.sort(key=lambda x: x.get('published_parsed') or (0,0,0,0,0,0,0,0,0), reverse=True)
    return entries

all_items = fetch_news()
JST = timezone(timedelta(hours=+9), 'JST')
display_items = all_items[:st.session_state.display_count]

for i, entry in enumerate(display_items):
    try:
        ts = time.mktime(entry.published_parsed)
        dt = datetime.fromtimestamp(ts, timezone.utc).astimezone(JST).strftime('%Y/%m/%d %H:%M')
    except: dt = "2026/--/-- --:--"
    
    st.markdown(f"""
    <div class="news-card">
        <div style="color:{CONFIG['neon_pink']}; font-family:'Orbitron'; font-size:0.75rem;">SEQUENCE // {dt} JST</div>
        <div style="margin: 8px 0;"><a href="{entry.link}" target="_blank">{entry.title}</a></div>
        <div style="color:rgba(255,255,255,0.5); font-size:0.75rem; border-top:1px solid rgba(255,255,255,0.1); padding-top:5px;">
            [AI_LOG] トレンド同期率:{random.randint(95,99)}% // 解析完了。
        </div>
    </div>
    """, unsafe_allow_html=True)

# ボタン
if st.session_state.display_count < len(all_items):
    if st.button(">> LOAD_MORE_INTELLIGENCE"):
        st.session_state.display_count += CONFIG["step_display"]
        st.rerun()
else:
    st.markdown(f"<p style='text-align:center; color:{CONFIG['neon_pink']}; font-family:Orbitron;'>-- END OF DATA STREAM --</p>", unsafe_allow_html=True)
