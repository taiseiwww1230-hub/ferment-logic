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

if "display_count" not in st.session_state:
    st.session_state.display_count = CONFIG["initial_display"]

# --- CSS: フェードアウト & 折りたたみロジック ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Roboto+Mono:wght@400;700&display=swap');
    
    [data-testid="stAppViewContainer"] {{ background-color: #000201 !important; }}
    .main .block-container {{ max-width: 100% !important; padding: 2rem 5% !important; display: flex; flex-direction: column; align-items: center; }}
    .news-wrapper {{ max-width: 850px; width: 100%; z-index: 100; }}

    /* 右上メトリクスの固定 & フェードアウト設定 */
    .side-metrics {{
        position: sticky; top: 40px; margin-left: auto; margin-right: 40px;
        width: 220px; font-family: 'Roboto Mono'; font-size: 0.85rem; color: {CONFIG["neon_blue"]};
        opacity: 0.8; z-index: 500; border-right: 4px solid {CONFIG["neon_blue"]};
        padding-right: 15px; text-align: right; line-height: 1.8;
    }}

    /* スクロールに合わせて衛星とメトリクスを消す（Streamlitのスクロールに同期） */
    [data-testid="stVerticalBlock"] > div:first-child {{
        position: sticky; top: 0; z-index: 1000;
    }}

    /* 背景（維持） */
    [data-testid="stAppViewContainer"]::before {{
        content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background-image: linear-gradient(rgba(0, 255, 65, 0.15) 2px, transparent 2px), linear-gradient(90deg, rgba(0, 255, 65, 0.15) 2px, transparent 2px);
        background-size: 50px 50px; z-index: 0; animation: grid-pulse 3s ease-in-out infinite alternate;
    }}

    /* タイトル & 衛星 */
    .title {{ color: #FFFFFF; font-family: 'Orbitron'; font-size: 1.8rem; text-align: center; text-shadow: 0 0 20px {CONFIG["primary"]}; letter-spacing: 10px; padding: 40px 0; }}
    .satellite {{ font-size: 6rem; text-align: center; filter: drop-shadow(0 0 30px {CONFIG["primary"]}); animation: float 4s ease-in-out infinite; margin-bottom: 30px; }}

    /* ニュースカード & 折りたたみ演出 */
    .news-card {{
        background: rgba(0, 10, 5, 0.95); border: 1px solid {CONFIG["primary"]}; border-left: 10px solid {CONFIG["primary"]};
        padding: 30px; margin-bottom: 25px; transition: 0.3s; position: relative;
    }}
    .news-card:hover {{ border-color: {CONFIG["neon_pink"]}; border-left-color: {CONFIG["neon_pink"]}; transform: scale(1.02); }}
    .news-card a {{ color: white !important; font-size: 1.3rem; font-weight: 900; text-decoration: none !important; text-shadow: 0 0 5px {CONFIG["neon_blue"]}; display: block; }}

    /* 折りたたみボタン（右端） */
    .collapse-btn {{
        position: absolute; right: 10px; top: 10px; font-family: 'Roboto Mono';
        font-size: 0.7rem; color: {CONFIG["primary"]}; cursor: pointer; border: 1px solid {CONFIG["primary"]};
        padding: 2px 5px; opacity: 0.5;
    }}
    .collapse-btn:hover {{ opacity: 1; color: {CONFIG["neon_pink"]}; border-color: {CONFIG["neon_pink"]}; }}

    /* 下部：EXPANDボタン */
    .stButton > button {{
        background: transparent !important; color: {CONFIG["primary"]} !important; border: 4px solid {CONFIG["primary"]} !important;
        width: 100% !important; max-width: 850px !important; height: 80px !important; font-family: 'Orbitron' !important;
        font-size: 1.8rem !important; transition: 0.3s !important; margin-top: 30px;
    }}
    .stButton > button:hover {{ background: {CONFIG["neon_pink"]} !important; color: white !important; box-shadow: 0 0 60px {CONFIG["neon_pink"]} !important; }}

    @keyframes grid-pulse {{ 0% {{ opacity: 0.1; }} 100% {{ opacity: 0.6; }} }}
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

# ヘッダーエリア（スクロールで消える）
header_container = st.container()
with header_container:
    st.markdown(f'<div class="title">{CONFIG["site_name"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="satellite">{CONFIG["editor_avatar"]}</div>', unsafe_allow_html=True)
    # メトリクスをここに配置
    st.markdown(f"""
    <div class="side-metrics">
        >> LATENCY: 24ms<br>
        >> UPLINK: SECURE<br>
        >> STATUS: MONITORING<br>
        >> SOURCE: G_INTEL
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="news-wrapper">', unsafe_allow_html=True)

all_items = fetch_news()
JST = timezone(timedelta(hours=+9), 'JST')
display_items = all_items[:st.session_state.display_count]

for i, entry in enumerate(display_items):
    dt = "2026/--/--"
    if entry.get('published_parsed'):
        dt = datetime.fromtimestamp(time.mktime(entry.published_parsed), timezone.utc).astimezone(JST).strftime('%Y/%m/%d %H:%M')
    
    # 折りたたみ管理用のキーを生成
    col_key = f"collapsed_{i}"
    if col_key not in st.session_state:
        st.session_state[col_key] = False

    # ニュースカード表示
    if not st.session_state[col_key]:
        # 通常表示
        st.markdown(f"""
        <div class="news-card">
            <div style="color:{CONFIG['neon_pink']}; font-family:'Orbitron'; font-size:0.9rem; margin-bottom:10px;">
                ▶ SYNC_TS // {dt} JST
            </div>
            <a href="{entry.link}" target="_blank">{entry.title}</a>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"[-] SHRINK_DATA_{i}", key=f"btn_{i}"):
            st.session_state[col_key] = True
            st.rerun()
    else:
        # 折りたたみ表示
        st.markdown(f"""
        <div style="background:rgba(0,255,65,0.05); border:1px dashed {CONFIG['primary']}; padding:10px; margin-bottom:10px; font-family:'Roboto Mono'; font-size:0.8rem; color:{CONFIG['primary']};">
            [DATA_MINIMIZED] // {entry.title[:30]}...
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"[+] RESTORE_{i}", key=f"btn_{i}"):
            st.session_state[col_key] = False
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# 下部ボタン
if st.session_state.display_count < len(all_items):
    if st.button("[ EXPAND DATABASE ]"):
        st.session_state.display_count += CONFIG["step_display"]
        st.rerun()
