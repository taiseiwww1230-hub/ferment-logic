import streamlit as st
import feedparser
from datetime import datetime, timedelta, timezone
import urllib.parse
import time
import re

# --- CONFIGURATION ---
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

# layout="wide" で全画面を解放
st.set_page_config(page_title=CONFIG["site_name"], layout="wide")

if "display_count" not in st.session_state:
    st.session_state.display_count = CONFIG["initial_display"]

# --- CSS: 究極の統合エンジニアリング ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Roboto+Mono:wght@400;700&display=swap');
    
    /* 基本背景とスクロールの制御 */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main {{
        background-color: #000201 !important;
        color: white !important;
    }}

    /* 1. 背景グリッド：ドクン、ドクンという鼓動 */
    [data-testid="stAppViewContainer"]::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background-image: 
            linear-gradient(rgba(0, 255, 65, 0.15) 2px, transparent 2px),
            linear-gradient(90deg, rgba(0, 255, 65, 0.15) 2px, transparent 2px);
        background-size: 50px 50px;
        z-index: 0;
        animation: grid-pulse-extreme 3s ease-in-out infinite alternate;
    }}

    /* 2. 強烈なスキャンライン & デジタルノイズ */
    [data-testid="stAppViewContainer"]::after {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: repeating-linear-gradient(0deg, rgba(0, 0, 0, 0.15), rgba(0, 0, 0, 0.15) 1px, transparent 1px, transparent 2px), 
                    linear-gradient(to bottom, transparent 0%, rgba(0, 255, 65, 0) 40%, rgba(0, 255, 65, 0.3) 50%, rgba(0, 255, 65, 0) 60%, transparent 100%);
        background-size: 100% 100%, 100% 400%;
        z-index: 9999;
        pointer-events: none;
        animation: scan-line-extreme 4s linear infinite;
    }}

    /* 3. 左右の余白活用（強制表示・高優先度） */
    @media (min-width: 1024px) {{
        .main::before {{
            content: "101101...DECRYPTING...LOG_STREAM...NODE_77...ANALYZING...010101...VITAL_PULSE_OK...NODE_B4_ACTIVE...11001010...SYSTEM_STABLE...01101";
            position: fixed !important;
            left: 30px !important; top: 100px !important; width: 100px !important; height: 80vh !important;
            font-family: 'Roboto Mono' !important; font-size: 0.75rem !important; color: {CONFIG["primary"]} !important;
            opacity: 0.35 !important; overflow: hidden !important; word-break: break-all !important;
            writing-mode: vertical-rl !important; text-orientation: upright !important;
            z-index: 100 !important; animation: log-scroll 25s linear infinite !important;
            display: block !important;
        }}
        .main::after {{
            content: ">> LATENCY: 22ms\\A >> UPLINK: STABLE\\A >> SECURITY: LEVEL_4\\A >> SOURCE: RSS_GNEWS\\A >> MODE: AUTO_DISCOVERY";
            white-space: pre !important; position: fixed !important;
            right: 40px !important; top: 150px !important; width: 220px !important;
            font-family: 'Roboto Mono' !important; font-size: 0.8rem !important; color: {CONFIG["neon_blue"]} !important;
            opacity: 0.5 !important; z-index: 100 !important; border-right: 3px solid {CONFIG["neon_blue"]} !important; padding-right: 15px !important;
            text-align: right !important; line-height: 2 !important;
            display: block !important;
        }}
    }}

    /* アニメーション定義 */
    @keyframes log-scroll {{ 0% {{ transform: translateY(0); }} 100% {{ transform: translateY(-50%); }} }}
    @keyframes grid-pulse-extreme {{ 0% {{ opacity: 0.1; transform: scale(1.0); }} 100% {{ opacity: 0.7; transform: scale(1.05); }} }}
    @keyframes scan-line-extreme {{ 0% {{ background-position: 0% 0%, 0% -100%; }} 100% {{ background-position: 0% 0%, 0% 100%; }} }}

    /* メインコンテンツ幅の制限（中央配置の徹底） */
    .block-container {{
        max-width: 850px !important;
        padding-top: 2rem !important;
        z-index: 1000;
        margin: auto !important;
    }}

    /* タイトル：1.8remへ縮小・発光維持 */
    .title {{
        color: #FFFFFF !important;
        font-family: 'Orbitron' !important;
        font-size: 1.8rem !important;
        text-align: center !important;
        text-shadow: 0 0 15px {CONFIG["primary"]}, 0 0 30px {CONFIG["neon_blue"]}, 0 0 60px {CONFIG["neon_blue"]} !important;
        padding: 40px 0 10px 0 !important;
        letter-spacing: 8px !important;
        position: relative !important;
        z-index: 1000 !important;
    }}

    .satellite {{
        text-align: center !important;
        font-size: 5rem !important;
        filter: drop-shadow(0 0 40px {CONFIG["primary"]}) !important;
        animation: satellite-float 4s ease-in-out infinite !important;
        position: relative !important;
        z-index: 1000 !important;
        margin-bottom: 20px !important;
    }}
    @keyframes satellite-float {{ 0%, 100% {{ transform: translateY(0) scale(1.0); }} 50% {{ transform: translateY(-25px) scale(1.1); }} }}

    /* ニュースカード：UI厳守 */
    .news-card {{
        background: rgba(0, 10, 5, 0.9) !important;
        border: 2px solid rgba(0, 255, 65, 0.4) !important;
        border-left: 8px solid {CONFIG["primary"]} !important;
        padding: 25px !important;
        margin-bottom: 25px !important;
        transition: 0.2s ease-out !important;
        position: relative !important;
        z-index: 1000 !important;
    }}
    .news-card:hover {{
        border: 2px solid {CONFIG["neon_pink"]} !important;
        border-left: 8px solid {CONFIG["neon_pink"]} !important;
        transform: scale(1.03) !important;
        box-shadow: 0 0 40px rgba(255, 0, 224, 0.3) !important;
    }}
    .news-card a {{
        color: #FFFFFF !important;
        text-shadow: 0 0 5px {CONFIG["neon_blue"]} !important;
        font-size: 1.2rem !important;
        font-weight: 900 !important;
        text-decoration: none !important;
    }}

    /* ボタン：ADD MORE INTEL */
    .stButton > button {{
        background: rgba(0, 255, 65, 0.1) !important;
        color: {CONFIG["primary"]} !important;
        border: 3px solid {CONFIG["primary"]} !important;
        height: 70px !important;
        width: 100% !important;
        font-family: 'Orbitron' !important;
        font-size: 1.4rem !important;
        font-weight: bold !important;
        letter-spacing: 3px !important;
        text-shadow: 0 0 10px {CONFIG["primary"]} !important;
        transition: 0.2s !important;
        position: relative !important;
        z-index: 2000 !important;
        margin-top: 20px !important;
    }}
    .stButton > button:hover {{
        background: {CONFIG["neon_pink"]} !important;
        color: white !important;
        border: 3px solid {CONFIG["neon_pink"]} !important;
        box-shadow: 0 0 50px {CONFIG["neon_pink"]} !important;
        transform: translateY(-5px) !important;
    }}

    header, footer {{ visibility: hidden !important; }}
</style>
""", unsafe_allow_html=True)

# --- LOGIC: 重複排除・データ取得 ---
@st.cache_data(ttl=1) # デバッグのため一時的にキャッシュを無効化
def fetch_news():
    q = urllib.parse.quote(CONFIG["query"])
    f = feedparser.parse(f"https://news.google.com/rss/search?q={q}&hl=ja&gl=JP&ceid=JP:ja")
    entries = f.entries
    
    unique_entries = []
    seen_titles = set()

    for entry in entries:
        # 重複排除: タイトルの空白や記号を無視して比較
        norm_title = re.sub(r'[\s\-｜｜「」『』]', '', entry.title)
        # 指紋生成（冒頭30文字）
        title_fingerprint = norm_title[:30]

        if title_fingerprint not in seen_titles:
            unique_entries.append(entry)
            seen_titles.add(title_fingerprint)
    
    unique_entries.sort(key=lambda x: x.get('published_parsed') or (0,0,0,0,0,0,0,0,0), reverse=True)
    return unique_entries

# --- RENDERING ---
st.markdown(f'<div class="title">{CONFIG["site_name"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="satellite">{CONFIG["editor_avatar"]}</div>', unsafe_allow_html=True)

all_items = fetch_news()
JST = timezone(timedelta(hours=+9), 'JST')
display_items = all_items[:st.session_state.display_count]

for entry in display_items:
    try:
        ts = time.mktime(entry.published_parsed)
        dt = datetime.fromtimestamp(ts, timezone.utc).astimezone(JST).strftime('%Y/%m/%d %H:%M')
    except:
        dt = "2026/--/-- --:--"
    
    st.markdown(f"""
    <div class="news-card">
        <div style="color:{CONFIG['neon_pink']}; font-family:'Orbitron'; font-size:0.9rem; margin-bottom:10px;">
            <span style="animation: blink 1s infinite;">▶</span> SYNC_TS // {dt} JST
        </div>
        <div><a href="{entry.link}" target="_blank">{entry.title}</a></div>
        <div style="margin-top:15px; color:rgba(0, 255, 65, 0.7); font-size:0.75rem; font-family:'Roboto Mono'; border-top: 1px solid rgba(0,255,65,0.2); padding-top:10px;">
            >> INTEL_STATUS: VERIFIED <br>
            >> ACCESS_LEVEL: UNRESTRICTED
        </div>
    </div>
    """, unsafe_allow_html=True)

# 下部ボタン
if st.session_state.display_count < len(all_items):
    if st.button("[ ADD MORE INTEL ]"):
        st.session_state.display_count += CONFIG["step_display"]
        st.rerun()

# 重滅ブリンクアニメーション（カード用）
st.markdown("""<style>@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }</style>""", unsafe_allow_html=True)
