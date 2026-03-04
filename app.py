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

# --- CSS: 画面支配 & メトリクス固定配置 ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Roboto+Mono:wght@400;700&display=swap');
    
    /* フレーム破壊 & 中央寄せ */
    [data-testid="stAppViewContainer"] {{ background-color: #000201 !important; }}
    .main .block-container {{
        max-width: 100% !important;
        padding: 2rem 5% !important;
        display: flex; flex-direction: column; align-items: center;
    }}
    .news-wrapper {{ max-width: 850px; width: 100%; z-index: 100; }}

    /* 背景エフェクト（維持） */
    [data-testid="stAppViewContainer"]::before {{
        content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background-image: linear-gradient(rgba(0, 255, 65, 0.15) 2px, transparent 2px), linear-gradient(90deg, rgba(0, 255, 65, 0.15) 2px, transparent 2px);
        background-size: 50px 50px; z-index: 0; animation: grid-pulse 3s ease-in-out infinite alternate;
    }}
    [data-testid="stAppViewContainer"]::after {{
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: repeating-linear-gradient(0deg, rgba(0,0,0,0.2) 0px, rgba(0,0,0,0.2) 1px, transparent 1px, transparent 2px),
                    linear-gradient(to bottom, transparent 0%, rgba(0, 255, 65, 0.3) 50%, transparent 100%);
        background-size: 100% 100%, 100% 400%; z-index: 999; pointer-events: none; animation: scan 4s linear infinite;
    }}

    /* 左端：強制システムログ (PCのみ) */
    @media (min-width: 1100px) {{
        body::before {{
            content: "SYSTEM_LOG: [OK] NODE_77 ACTIVE >> DATA_STREAM_STABLE >> DECRYPTING_INTEL_772... 101011010110101011010101";
            position: fixed; left: 20px; top: 0; width: 50px; height: 100vh;
            writing-mode: vertical-rl; font-family: 'Roboto Mono'; font-size: 0.8rem; color: {CONFIG["primary"]};
            opacity: 0.4; z-index: 1; animation: log-float 15s linear infinite;
        }}
    }}

    /* 右上：固定システムメトリクス (文字被り対策) */
    .side-metrics {{
        position: fixed; top: 40px; right: 40px; width: 220px;
        font-family: 'Roboto Mono'; font-size: 0.85rem; color: {CONFIG["neon_blue"]};
        opacity: 0.8; z-index: 2000; border-right: 4px solid {CONFIG["neon_blue"]};
        padding-right: 15px; text-align: right; line-height: 1.8;
        pointer-events: none; /* クリックを邪魔しない */
    }}

    @keyframes grid-pulse {{ 0% {{ opacity: 0.1; }} 100% {{ opacity: 0.6; }} }}
    @keyframes scan {{ 0% {{ background-position: 0 0, 0 -100%; }} 100% {{ background-position: 0 0, 0 100%; }} }}
    @keyframes log-float {{ 0% {{ transform: translateY(0); }} 100% {{ transform: translateY(-50%); }} }}

    /* タイトル & カードデザイン（維持） */
    .title {{ color: #FFFFFF; font-family: 'Orbitron'; font-size: 1.8rem; text-align: center; text-shadow: 0 0 20px {CONFIG["primary"]}; letter-spacing: 10px; padding: 40px 0; position: relative; z-index: 100; }}
    .satellite {{ font-size: 6rem; text-align: center; filter: drop-shadow(0 0 30px {CONFIG["primary"]}); animation: float 4s ease-in-out infinite; margin-bottom: 30px; position: relative; z-index: 100; }}
    @keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-20px); }} }}
    .news-card {{ background: rgba(0, 10, 5, 0.95); border: 1px solid {CONFIG["primary"]}; border-left: 10px solid {CONFIG["primary"]}; padding: 30px; margin-bottom: 30px; transition: 0.3s; position: relative; z-index: 100; }}
    .news-card:hover {{ border-color: {CONFIG["neon_pink"]}; border-left-color: {CONFIG["neon_pink"]}; transform: scale(1.02); box-shadow: 0 0 40px rgba(255,0,224,0.2); }}
    .news-card a {{ color: white !important; font-size: 1.3rem; font-weight: 900; text-decoration: none !important; text-shadow: 0 0 5px {CONFIG["neon_blue"]}; }}
    
    /* ボタン（維持） */
    .stButton > button {{
        background: transparent !important; color: {CONFIG["primary"]} !important; border: 4px solid {CONFIG["primary"]} !important;
        width: 100% !important; max-width: 850px !important; height: 80px !important; font-family: 'Orbitron' !important;
        font-size: 1.8rem !important; transition: 0.3s !important; text-transform: uppercase; margin-top: 20px;
    }}
    .stButton > button:hover {{ background: {CONFIG["neon_pink"]} !important; color: white !important; box-shadow: 0 0 60px {CONFIG["neon_pink"]} !important; }}

    header, footer {{ visibility: hidden !important; }}
</style>

<div class="side-metrics">
    >> LATENCY: 24ms<br>
    >> UPLINK: SECURE<br>
    >> STATUS: MONITORING<br>
    >> SOURCE: G_INTEL
</div>
""", unsafe_allow_html=True)

# --- LOGIC ---
@st.cache_data(ttl=60)
def fetch_news():
    q = urllib.parse.quote(CONFIG["query"])
    f = feedparser.parse(f"https://news.google.com/rss/search?q={q}&hl=ja&gl=JP&ceid=JP:ja")
    entries = f.entries
    unique_entries = []
    seen_fingerprints = set()
    for entry in entries:
        fingerprint = re.sub(r'\s+', '', entry.title)[:20]
        if fingerprint not in seen_fingerprints:
            unique_entries.append(entry)
            seen_fingerprints.add(fingerprint)
    unique_entries.sort(key=lambda x: x.get('published_parsed') or (0,0,0,0,0,0,0,0,0), reverse=True)
    return unique_entries

# --- RENDERING ---
st.markdown(f'<div class="title">{CONFIG["site_name"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="satellite">{CONFIG["editor_avatar"]}</div>', unsafe_allow_html=True)

st.markdown('<div class="news-wrapper">', unsafe_allow_html=True)
all_items = fetch_news()
JST = timezone(timedelta(hours=+9), 'JST')
display_items = all_items[:st.session_state.display_count]

for entry in display_items:
    try:
        ts = time.mktime(entry.published_parsed)
        dt = datetime.fromtimestamp(ts, timezone.utc).astimezone(JST).strftime('%Y/%m/%d %H:%M')
    except: dt = "2026/--/-- --:--"
    
    st.markdown(f"""
    <div class="news-card">
        <div style="color:{CONFIG['neon_pink']}; font-family:'Orbitron'; font-size:1rem; margin-bottom:12px;">
            <span style="animation: blink 1s infinite;">▶</span> SYNC_TS // {dt} JST
        </div>
        <a href="{entry.link}" target="_blank">{entry.title}</a>
        <div style="margin-top:20px; color:{CONFIG['primary']}; opacity:0.8; font-family:'Roboto Mono'; font-size:0.8rem; border-top:1px solid rgba(0,255,65,0.2); padding-top:12px;">
            >> INTEL_STATUS: VERIFIED // ACCESS: UNRESTRICTED
        </div>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.display_count < len(all_items):
    if st.button("[ ADD MORE INTEL ]"):
        st.session_state.display_count += CONFIG["step_display"]
        st.rerun()

st.markdown("""<style>@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }</style>""", unsafe_allow_html=True)
