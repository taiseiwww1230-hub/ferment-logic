import streamlit as st
import feedparser
from datetime import datetime
import urllib.parse # 追加：日本語をURL用に変換する道具

# --- 設定エリア ---
CONFIG = {
    "site_name": "発酵論理",
    "editor_name": "Ferment(ファーメント)",
    "editor_avatar": "🔬",
    "theme_color": "#4CAF50",
    "accent_color": "#00E5FF",
    "bg_color": "#f8fff9",
    "news_query": "ヨーグルト OR お茶 OR 飲料 新商品", # ここが原因でした
    "greeting": "おはようございます。発酵プロセス完了。君の脳内にシナジーを生むニュースをデプロイしたよ。"
}

st.set_page_config(page_title=CONFIG["site_name"], page_icon=CONFIG["editor_avatar"])

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

st.title(f"🧬 {CONFIG['site_name']}")
st.caption(f"状態:発酵中... | {datetime.now().strftime('%Y/%m/%d %H:%M')}")

with st.chat_message("ai", avatar=CONFIG["editor_avatar"]):
    st.write(f"**{CONFIG['editor_name']}**: {CONFIG['greeting']}")

@st.cache_data(ttl=3600)
def fetch_news():
    # 日本語をURLで使える形式（%xx...）に変換
    encoded_query = urllib.parse.quote(CONFIG["news_query"])
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"
    
    try:
        feed = feedparser.parse(url)
        return feed.entries[:10]
    except Exception as e:
        return []

news_items = fetch_news()

if not news_items:
    st.warning("ニュースの抽出に一時的に失敗しました。しばらく待ってから再読み込みしてください。")

for entry in news_items:
    with st.container():
        st.markdown(f"""
        <div class="news-card">
            <span class="status-tag">EXTRACTED</span>
            <h3 style="font-size: 1.1em; margin: 10px 0;">
                <a href="{entry.link}" target="_blank" style="text-decoration:none; color:#333;">{entry.title}</a>
            </h3>
            <p style="font-size:0.85em; color:#666; line-height:1.4;">
                🔍 {CONFIG['editor_name']}分析：業界のトレンドを揺るがすポテンシャルを感知。
            </p>
        </div>
        """, unsafe_allow_html=True)

st.markdown(f"<p style='text-align: center; color: silver;'>Stay Fermented. ({CONFIG['site_name']} v1.0)</p>", unsafe_allow_html=True)
