import streamlit as st
import feedparser
from datetime import datetime
import urllib.parse
import random # 追加：AIチックな演出用

# --- EXECUTIVE INTELLIGENCE TERMINAL v4.0 ---
CONFIG = {
    "site_name": "FERMENT-LOGIC // INTEL",
    "editor_name": "CORE-AI: FERMENT",
    "editor_avatar": "🛰️",
    # ネオンの鮮やかさと儚さを両立させる配色
    "neon_green": "#00FF41", # Matrix Green
    "neon_blue": "#00E5FF",  # Cyber Blue
    "neon_pink": "#FF00E0",  # 儚さを演出するアクセント
    "text_base": "#E0E0E0",  # Base Text
    "bg_deep": "#020502",    # 深い緑を含んだ黒
    # 検索クエリ：直近7日間の重要情報
    "news_query": '(ヨーグルト OR 乳製品 OR 乳酸菌 OR 紅茶 OR 茶葉) AND ("新発売" OR "期間限定" OR "独自開発" OR "トレンド") when:7d',
    "greeting": "[SYSTEM: ONLINE] 直近168時間の高純度データを抽出。茶葉と発酵の最新相関をデプロイしました。"
}

st.set_page_config(page_title=CONFIG["site_name"], page_icon="🧬", layout="wide")

# --- HYPER NEON VISUALS (ネオン管の滲みとAI要素の融合) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&family=Orbitron:wght@500;700&family=Roboto+Mono:wght@300&display=swap');

    .stApp {{
        background-color: {CONFIG["bg_deep"]};
        /* 背景に深い霧と滲むネオンのエフェクト */
        background-image: 
            radial-gradient(at 10% 10%, rgba(0, 255, 65, 0.05) 0px, transparent 50%),
            radial-gradient(at 90% 90%, rgba(0, 229, 255, 0.05) 0px, transparent 50%),
            radial-gradient(at 50% 50%, rgba(255, 0, 224, 0.02) 0px, transparent 50%);
        color: {CONFIG["text_base"]};
        font-family: 'Inter', sans-serif;
    }}
    /* 全体に薄く走る走査線（メカメカしさ） */
    .stApp::before {{
        content: " ";
        position: fixed; top: 0; left: 0; bottom: 0; right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.1) 50%);
        z-index: 9999;
        background-size: 100% 4px;
        pointer-events: none;
        opacity: 0.3;
    }}

    /* ヘッダー：ネオン管の滲みを表現 */
    .stTitle {{
        font-family: 'Orbitron', sans-serif;
        font-size: 2.5rem !important;
        letter-spacing: 5px;
        color: {CONFIG["secondary"]} !important;
        text-align: center;
        margin-top: 30px !important;
        margin-bottom: 5px !important;
        text-shadow: 
            0 0 5px {CONFIG["secondary"]},
            0 0 10px {CONFIG["secondary"]},
            0 0 20px {CONFIG["neon_blue"]},
            0 0 40px {CONFIG["neon_blue"]};
    }}
    .site-subtitle {{
        font-family: 'Roboto Mono', monospace;
        font-size: 0.8rem;
        color: {CONFIG["neon_green"]};
        text-align: center;
        margin-bottom: 50px;
        font-weight: 300;
        text-transform: uppercase;
        opacity: 0.8;
    }}

    /* AIコンソール：余白を埋めるメカニカルな装飾 */
    .ai-console {{
        background: rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(0, 255, 65, 0.3);
        padding: 25px;
        border-radius: 4px;
        margin-bottom: 60px;
        position: relative;
        overflow: hidden;
    }}
    .ai-console::before {{
        content: "SYSTEM_STATUS: OK // CODENAME: FERMENT_LOGIC // AUTH: EXEC_USER";
        position: absolute; bottom: 5px; right: 10px;
        font-family: 'Roboto Mono', monospace;
        font-size: 10px; color: {CONFIG["neon_green"]}; opacity: 0.2;
    }}

    /* ニュースカード：儚さと鮮やかさの融合 */
    .news-card {{
        background: rgba(255, 255, 255, 0.01);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-left: 2px solid {CONFIG["neon_green"]};
        padding: 30px;
        margin-bottom: 30px;
        border-radius: 2px;
        transition: all 0.4s ease;
        position: relative;
    }}
    .news-card:hover {{
        background: rgba(0, 229, 255, 0.03);
        border-left: 2px solid {CONFIG["neon_pink"]}; /* 儚いピンクへ変化 */
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.2);
        transform: translateY(-2px);
    }}

    /* タイトルとメタ情報 */
    .time-tag {{
        color: {CONFIG["neon_pink"]};
        font-size: 0.7rem;
        font-family: 'Orbitron', sans-serif;
        font-weight: 500;
        letter-spacing: 1px;
        margin-bottom: 12px;
        display: block;
        opacity: 0.8;
    }}
    .news-card a {{
        color: {CONFIG["secondary"]} !important;
        text-decoration: none;
        font-size: 1.2rem;
        font-weight: 400;
        line-height: 1.6;
    }}
    .news-card a:hover {{
        color: {CONFIG["neon_blue"]} !important;
        text-shadow: 0 0 5px {CONFIG["neon_blue"]};
    }}

    /* 詳細分析：余白を意味のある情報で埋める */
    .analysis-box {{
        margin-top: 20px;
        font-size: 0.85rem;
        color: #999;
        border-top: 1px solid rgba(255, 255, 255, 0.03);
        padding-top: 20px;
        line-height: 1.7;
        position: relative;
    }}
    .analysis-box::before {{
        content: "AI_LOGIC_PREDICTION";
        position: absolute; top: -10px; left: 10px;
        background: {CONFIG["bg_deep"]};
        padding: 0 5px;
        font-family: 'Roboto Mono', monospace;
        font-size: 9px; color: {CONFIG["neon_green"]};
    }}

    </style>
    """, unsafe_allow_html=True)

# --- 画面構成 ---

# 1. サイトヘッダー（ネオンの滲み効果）
st.title(f"{CONFIG['site_name']}")
st.markdown(f"<div class='site-subtitle'>// Accessing Global Fermentation & Tea Intelligence Grid //</div>", unsafe_allow_html=True)

# 2. AIコンソール（余白をメカニカルに埋める）
with st.container():
    col_a, col_b = st.columns([1, 5])
    with col_a:
        # AIエージェントのアイコンをネオンブルーに
        st.write(f"<h1 style='text-align:center; color:{CONFIG['neon_blue']}; text-shadow: 0 0 10px {CONFIG['neon_blue']};'>{CONFIG['editor_avatar']}</h1>", unsafe_allow_html=True)
    with col_b:
        # AIチックなダミーコードを生成して余白に配置
        dummy_code = f"0x{random.randint(1000, 9999)}_FILTER_ACTIVE // [A: {random.random():.2f}] [B: {random.random():.2f}]"
        st.markdown(f"""
        <div class="ai-console">
            <div style="font-family:'Roboto Mono', monospace; font-size:10px; color:{CONFIG['neon_green']}; opacity:0.5; margin-bottom:10px;">>> {dummy_code}</div>
            <span style="color:{CONFIG['secondary']}; font-family:Orbitron; font-weight:700; font-size:1.1rem; letter-spacing:2px;">[ {CONFIG['editor_name']} / ACTIVE ]</span><br>
            <span style="color:#888; font-size:0.9rem; font-weight:300;">{CONFIG['greeting']}</span>
        </div>
        """, unsafe_allow_html=True)

# 3. ニュース取得（直近7日間に厳格化、18件）
@st.cache_data(ttl=1800)
def fetch_executive_news_v4():
    encoded_query = urllib.parse.quote(CONFIG["news_query"])
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"
    try:
        feed = feedparser.parse(url)
        return feed.entries[:18] # 3列構成に最適な18件
    except:
        return []

items = fetch_executive_news_v4()

if not items:
    st.info("現在、直近7日間の条件に合致する超速報データは待機中です。スキャン範囲を維持します。")

# 4. ニュースグリッド（情報の密度を高めた3カラム構成）
cols = st.columns(3)

for i, entry in enumerate(items):
    with cols[i % 3]:
        pub_date = entry.get('published', '')
        
        st.markdown(f"""
        <div class="news-card">
            <span class="time-tag">RECENT_DATA // {pub_date[:16]}</span>
            <h3><a href="{entry.link}" target="_blank">{entry.title}</a></h3>
            <div class="analysis-box">
                <span style="color:{CONFIG['neon_green']};">◆◆◆</span> 
                直近のデータに基づき、茶葉の抗酸化作用と発酵食品の腸内環境改善によるシナジー効果を認む。
                目まぐるしく変化する情勢において、この情報は健康マトリックスに正の影響を与える。
                [推論精度: {random.randint(95, 99)}%]
            </div>
        </div>
        """, unsafe_allow_html=True)

# フッター
st.write(f"<p style='text-align:center; color:#222; font-family:Orbitron; font-size:10px; padding:50px;'>Stay Fermented. | FERMENT-LOGIC v4.0 | ENCRYPTION_LEVEL: ALPHA</p>", unsafe_allow_html=True)
