import streamlit as st
import feedparser
from datetime import datetime

# --- 設定エリア（ここを書き換えるだけでカスタマイズ可能！） ---
CONFIG = {
    "site_name": "Ferment-Logic",
    "editor_name": "Ferment (ファーメント)",
    "editor_avatar": "🔬",
    "theme_color": "#4CAF50",  # お茶の緑
    "accent_color": "#00E5FF", # サイバーブルー
    "bg_color": "#f8fff9",     # ミルキーホワイト
    "news_query": "ヨーグルト OR お茶 OR 飲料 新商品",
    "greeting": "Good morning. 発酵プロセス完了。君の脳内にシナジーを生むニュースをデプロイしたよ。"
}

# ページ基本設定
st.set_page_config(page_title=CONFIG["site_name"], page_icon=CONFIG["editor_avatar"])

# デザインの注入
st.markdown(f"""
    <style>
    .stApp {{ background-color: {CONFIG["bg_color"]}; }}
    .stTitle {{ color: {CONFIG["theme_color"]}; font-weight: 800; }}
    .news-card {{
        background: white; padding: 18px; border-radius: 15px;
        border: 2px solid #eee; margin-bottom: 15px;
        box-shadow: 6px 6px 0px {CONFIG["theme_color"]};
    }}
    .status-tag {{
        background: {CONFIG["accent_color"]}; color: black;
        padding: 3px 10px; border-radius: 20px; font-size: 0.7em; font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)

# ヘッダー
st.title(f"🧬 {CONFIG['site_name']}")
st.caption(f"Status: Fermenting... | {datetime.now().strftime('%Y/%m/%d %H:%M')}")

# AI編集長のメッセージ
with st.chat_message("ai", avatar=CONFIG["editor_avatar"]):
    st.write(f"**{CONFIG['editor_name']}**: {CONFIG['greeting']}")

# ニュース取得
@st.cache_data(ttl=3600) # 1時間はキャッシュを保持して高速化
def fetch_news():
    url = f"https://news.google.com/rss/search?q={CONFIG['news_query']}&hl=ja&gl=JP&ceid=JP:ja"
    feed = feedparser.parse(url)
    return feed.entries[:10]

news_items = fetch_news()

# ニュースカードの生成
for entry in news_items:
    with st.container():
        st.markdown(f"""
        <div class="news-card">
            <span class="status-tag">EXTRACTED</span>
            <h3 style="font-size: 1.1em; margin: 10px 0;">
                <a href="{entry.link}" target="_blank" style="text-decoration:none; color:#333;">{entry.title}</a>
            </h3>
            <p style="font-size:0.85em; color:#666; line-height:1.4;">
                {entry.published}<br>
                🔍 {CONFIG['editor_name']}分析：業界のトレンドを揺るがすポテンシャルを感知。
            </p>
        </div>
        """, unsafe_allow_html=True)

st.markdown(f"<p style='text-align: center; color: silver;'>Stay Fermented. ({CONFIG['site_name']} v1.0)</p>", unsafe_allow_html=True)
