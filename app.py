import streamlit as st
import pandas as pd
import time

# 1. 網頁頁面配置
st.set_page_config(page_title="星雲啟示錄", page_icon="🌌", layout="wide")

# 套用深色神祕感 CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTextInput > div > div > input { background-color: #1a1c24; color: #38bdf8; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌌 星雲啟示錄：連結宇宙的指引")
st.write("宇宙由無數的星雲組成，每一顆恆星的誕生與消亡都隱藏著生命的道理。")

# 2. 接收造訪者的問題
user_question = st.text_input("🔮 在心中默念你的困惑，並在此寫下一個問題：", placeholder="例如：我該如何面對下週的挑戰？")

# 3. 讀取你的星雲資料庫 (CSV)
@st.cache_data
def load_nebula_data():
    return pd.read_csv("cards.csv")

try:
    df = load_nebula_data()
except FileNotFoundError:
    st.error("⚠️ 找不到 cards.csv，請確認檔案與 app.py 放在同一層資料夾。")
    st.stop()

# 4. 抽卡觸發邏輯
if st.button("✨ 尋求宇宙的共振"):
    if not user_question:
        st.warning("請先寫下你的問題，讓宇宙能感應你的心聲。")
    else:
        with st.spinner("正在與深空星雲進行能量共振..."):
            time.sleep(2) # 營造神祕感的等待時間
            
            # 隨機抽取一張星雲卡
            card = df.sample(n=1).iloc[0]
            
            st.divider()
            
            # 5. 畫面呈現排版
            col1, col2 = st.columns([1, 1])
            
            with col1:
                # 讀取 image_path 欄位的圖片
                try:
                    st.image(card['image_path'], use_container_width=True)
                except Exception as e:
                    st.error(f"⚠️ 找不到圖片：{card['image_path']}。請確認 image 資料夾與圖片名稱是否正確。")
            
            with col2:
                # 你的 CSV 裡，星雲的名稱是放在 description 欄位
                st.markdown(f"### ✦ 您抽到的星雲：{card['description']}")
                st.write(f"**針對您的問題：** *「{user_question}」*")
                
                # 顯示核心啟示 (對應 revelation 欄位)
                st.markdown("---")
                st.subheader("💡 今日啟示")
                st.info(card['revelation'])
                
                # 顯示完整運勢解析 (對應 fortune 欄位)
                st.write("---")
                st.markdown("### 📜 完整運勢指引")
                # st.write() 會自動處理你 CSV 裡的換行符號 (\n)，讓排版很漂亮
                st.write(card['fortune'])
                
                st.caption("願星辰指引你的方向。")