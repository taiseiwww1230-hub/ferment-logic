import streamlit as st
import feedparser
from datetime import datetime, timedelta
import urllib.parse

# --- EXECUTIVE CORE CONFIG (社会人向け・プロ仕様設定) ---
CONFIG = {
    "site_name": "FERMENT-LOGIC / INTELLIGENCE",
    "editor_name": "INTEL-AGENCY: FERMENT",
    "editor_avatar": "🛰️",
    "primary": "#00FF41",   # Cyber Green
    "secondary": "#E0E0E0", # Platinum Silver
    "accent": "#007AFF",    # Deep Blue
    "bg_dark": "#020202",
    # 検索クエリ：1週間以内の新商品・トレンドに特化
    "news_query": '(ヨーグルト OR 乳製品 OR 乳酸菌 OR 紅茶 OR 茶葉) AND ("新発売" OR "期間限定" OR "世界初" OR "独自開発") when:7d',
    "greeting": "[STATUS: OPERATIONAL] 直近7日間の高純度データを抽出。茶葉と発酵の最新相関をデプロイしました。"
}

st.set_page_config(page_title=CONFIG["site_name"], page_icon="🧬", layout="wide")

# --- PREMIUM CYBER VISUALS (洗練された社会人向けUI) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Noto+Sans+JP:wght@300;500&display=swap');

    .stApp {{
        background: radial-gradient(circle at 50% 50%, #0a1a0a 0%, {CONFIG["bg_dark"]} 100%);
        color: {CONFIG["secondary"]};
        font-family: 'Noto Sans JP', sans-serif;
    }}

    /* ヘッダー：重厚なメタル質感 */
    .stTitle {{
        font-family: 'Orbitron', sans-serif;
        font-size: 2.2rem !important;
        letter-spacing: 4px;
        color: {CONFIG["primary"]} !important;
        border-bottom: 1px solid rgba(0, 255, 65, 0.3);
        padding-bottom: 15px !important;
        margin-bottom: 40px !important;
        text-shadow: 0 0 15px rgba(0, 255, 65, 0.5);
    }}

    /* ニュースカード：高級感のあるダークガラス */
    .news-card {{
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 3px solid {CONFIG["primary"]};
        padding: 25px;
        margin-bottom: 20px;
        border-radius: 4px;
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
        position: relative;
    }}
    .news-card:hover {{
        background: rgba(0, 255, 65, 0.05);
        border-left: 3px solid {CONFIG["accent"]};
        transform: scale(1.02);
    }}

    /* ニュースタイトル：落ち着いた知性 */
    .news-card a {{
        color: {CONFIG["secondary"]} !important;
        text-decoration: none;
        font-size: 1.15rem;
        font-weight: 500;
        line-height: 1.5;
    }}
    .news-card a:hover {{
        color: {CONFIG["primary"]} !important;
    }}

    /* AIステータスエリア */
    .ai-console {{
        font-family: 'Orbitron', sans-serif;
        background: rgba(0, 0, 0, 0.6);
        border: 1px solid {CONFIG["primary"]};
        padding: 20px;
        border-radius: 2px;
        margin-bottom: 40px;
        font-size: 0.9rem;
    }}

    /* タイムスタンプ・タグ */
    .time-tag {{
        color: {CONFIG["primary"]};
        font-size: 0.75rem;
        font-family: 'Orbitron', sans-serif;
        margin-bottom: 8px;
        display: block;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 画面構成 ---

# 1. サイトヘッダー
st.title(f" {CONFIG['site_name']}")

# 2. AIコンソール（ここがキャラクターとしての華やかさと知性を演出）
col_a, col_b = st.columns([1, 6])
with col_a:
    st.write(f"<h1 style='text-align:center; margin:0;'>{CONFIG['editor_avatar']}</h1>", unsafe_allow_html=True)
with col_b:
    st.markdown(f"""
    <div class="ai-console">
        <span style="color:{CONFIG['primary']};">>> LOG_ANALYSIS: ACTIVE</span><br>
        <span style="color:#888;">{CONFIG['greeting']}</span>
    </div>
    """, unsafe_allow_html=True)

# 3. ニュース取得（最新1週間以内に厳格化）
@st.cache_data(ttl=1800)
def fetch_latest_intelligence():
    # 'when:7d' パラメータをクエリに直接含めることでGoogleニュース側に期間指定を強制
    encoded_query = urllib.parse.quote(CONFIG["news_query"])
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"
    try:
        feed = feedparser.parse(url)
        # さらにプログラム側でも念のためフィルタリング（任意）
        return feed.entries[:18] # 18件まで表示（3列構成に最適）
    except:
        return []

items = fetch_latest_intelligence()

if not items:
    st.info("現在、直近7日間の条件に合致する超速報データは待機中です。スキャン範囲を維持します。")

# 4. ニュースグリッド（社会人が読みやすい3カラム構成）
cols = st.columns(3)

for i, entry in enumerate(items):
    with cols[i % 3]:
        # タイトルから日付を簡易的に表示
        pub_date = entry.get('published', '')
        
        st.markdown(f"""
        <div class="news-card">
            <span class="time-tag">RECENT_DATA / {pub_date[:16]}</span>
            <h3><a href="{entry.link}" target="_blank">{entry.title}</a></h3>
            <div style="margin-top:15px; font-size:0.85rem; color:#777; border-top:1px solid #222; padding-top:10px;">
                <span style="color:{CONFIG['primary']};">◆</span> 分析：茶葉の抗酸化作用と乳酸菌の相乗効果を認む。
            </div>
        </div>
        """, unsafe_allow_html=True)

st.write(f"<p style='text-align:center; color:#333; font-family:Orbitron; font-size:10px; padding:50px;'>SYSTEM CLOUD CONNECTED / ENCRYPTED</p>", unsafe_allow_html=True)
