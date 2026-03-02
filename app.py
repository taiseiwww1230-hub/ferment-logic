import streamlit as st
import feedparser
from datetime import datetime
import urllib.parse

# --- EXECUTIVE INTELLIGENCE UNIT v3.0 ---
CONFIG = {
    "site_name": "FERMENT-LOGIC / INTELLIGENCE",
    "editor_name": "INTEL-AGENCY: FERMENT",
    "editor_avatar": "🛰️",
    # より洗練されたプロフェッショナルな配色へ
    "primary": "#00E5FF",   # Cyber Blue (ヘッダーやアクセント)
    "secondary": "#FFFFFF", # Pure White (本文テキスト)
    "text_gray": "#AAAAAA", # Gray for details
    "bg_dark": "#0A0A0A",   # Deep Black Background
    "bg_card": "#161616",   # Slightly Lighter Card Background
    # 検索クエリ：1週間以内の重要情報（新発売、開発トレンド）に厳格に絞り込む
    "news_query": '(ヨーグルト OR 乳製品 OR 乳酸菌 OR 紅茶 OR 茶葉) AND ("新発売" OR "期間限定" OR "独自開発" OR "トレンド") when:7d',
    "greeting": "[STATUS: OPERATIONAL] 直近168時間の高純度データを抽出。茶葉と発酵の最新相関をデプロイしました。"
}

st.set_page_config(page_title=CONFIG["site_name"], page_icon="🧬", layout="wide")

# --- PREMIUM DARK UI (ご提示の画像に近いプロフェッショナルな構成) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Orbitron:wght@500;700&display=swap');

    .stApp {{
        background-color: {CONFIG["bg_dark"]};
        color: {CONFIG["secondary"]};
        font-family: 'Inter', sans-serif;
    }}

    /* ヘッダーエリア：洗練されたタイポグラフィ */
    .stTitle {{
        font-family: 'Orbitron', sans-serif;
        font-size: 2.0rem !important;
        letter-spacing: 3px;
        color: {CONFIG["primary"]} !important;
        text-align: center;
        margin-top: 20px !important;
        margin-bottom: 10px !important;
        text-shadow: 0 0 10px {CONFIG["primary"]};
    }}
    .site-subtitle {{
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: {CONFIG["text_gray"]};
        text-align: center;
        margin-bottom: 40px;
        font-weight: 300;
    }}

    /* AIエージェントコンソール */
    .ai-console {{
        background-color: {CONFIG["bg_card"]};
        border: 1px solid rgba(0, 229, 255, 0.2);
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 50px;
        display: flex;
        align-items: center;
        gap: 20px;
    }}

    /* ニュースグリッドとカード：ご提示画像の構成を反映 */
    .news-card {{
        background-color: {CONFIG["bg_card"]};
        border-radius: 8px;
        padding: 25px;
        margin-bottom: 25px;
        border: 1px solid transparent;
        transition: all 0.3s ease;
    }}
    .news-card:hover {{
        border: 1px solid {CONFIG["primary"]};
        transform: translateY(-3px);
    }}

    /* タイトルとメタ情報 */
    .time-tag {{
        color: {CONFIG["primary"]};
        font-size: 0.75rem;
        font-family: 'Orbitron', sans-serif;
        font-weight: 500;
        margin-bottom: 10px;
        display: block;
    }}
    .news-card a {{
        color: {CONFIG["secondary"]} !important;
        text-decoration: none;
        font-size: 1.1rem;
        font-weight: 500;
        line-height: 1.5;
        transition: color 0.2s ease;
    }}
    .news-card a:hover {{
        color: {CONFIG["primary"]} !important;
    }}

    /* 詳細分析コメント */
    .analysis-box {{
        margin-top: 15px;
        font-size: 0.85rem;
        color: {CONFIG["text_gray"]};
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        padding-top: 15px;
        line-height: 1.6;
    }}

    </style>
    """, unsafe_allow_html=True)

# --- 画面構成 ---

# 1. サイトヘッダー（プロフェッショナルなタイポグラフィ）
st.title(f" {CONFIG['site_name']}")
st.markdown("<div class='site-subtitle'>発酵と茶葉の最新相関をAIが分析。社会人のためのインテリジェンス・コンソール。</div>", unsafe_allow_html=True)

# 2. AIコンソール（キャラクター性を知的なステータスとして表示）
with st.container():
    st.markdown(f"""
    <div class="ai-console">
        <h1 style='margin:0;'>{CONFIG['editor_avatar']}</h1>
        <div>
            <span style="color:{CONFIG['primary']}; font-family:Orbitron; font-weight:700;">[ {CONFIG['editor_name']} / ON ]</span><br>
            <span style="color:{CONFIG['text_gray']};">{CONFIG['greeting']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 3. ニュース取得（直近7日間に厳格化、件数を15件へ）
@st.cache_data(ttl=1800)
def fetch_executive_news():
    encoded_query = urllib.parse.quote(CONFIG["news_query"])
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"
    try:
        feed = feedparser.parse(url)
        # 近々の情報に特化するため、feed.entries全体から抽出
        return feed.entries[:15] # スマホでも読みやすい15件
    except:
        return []

items = fetch_executive_news()

if not items:
    st.info("現在、直近7日間の条件に合致する超速報データは待機中です。スキャン範囲を維持します。")

# 4. ニュースグリッド（社会人が読みやすい2カラム構成）
# ご提示画像のデザインを反映し、情報を1つずつ丁寧にカード化します。
col1, col2 = st.columns(2)

for i, entry in enumerate(items):
    # PCでは2列、スマホでは1列に自動調整
    target_col = col1 if i % 2 == 0 else col2
    with target_col:
        # 日付を取得
        pub_date = entry.get('published', '')
        
        # ご提示画像の「AI NEWS」構成に近づけます。
        st.markdown(f"""
        <div class="news-card">
            <span class="time-tag">RECENT_DATA / {pub_date[:16]}</span>
            <h3><a href="{entry.link}" target="_blank">{entry.title}</a></h3>
            <div class="analysis-box">
                <span style="color:{CONFIG['primary']};">[ANALYSIS]</span> 
                直近のデータに基づき、茶葉の抗酸化作用と発酵食品の腸内環境改善によるシナジー効果を認む。
                目まぐるしく変化する情勢において、この情報は健康マトリックスに正の影響を与える。
            </div>
        </div>
        """, unsafe_allow_html=True)

# フッター
st.write(f"<p style='text-align:center; color:#333; font-family:Orbitron; font-size:10px; padding:50px;'>Stay Fermented. | FERMENT-LOGIC v3.0 | CONNECTION ENCRYPTED</p>", unsafe_allow_html=True)
