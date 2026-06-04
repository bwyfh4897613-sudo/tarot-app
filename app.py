import streamlit as st
import pandas as pd
import time
import base64

# --- 1. 網頁頁面基礎配置 (已移除小圖標) ---
st.set_page_config(page_title="Oracle", layout="wide")

# 讀取本地背景圖片並自動轉換為 base64 格式
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded_string}"
    except FileNotFoundError:
        return ""

bg_image_base64 = get_base64_image("photo.jpg")

# --- 2. 注入自訂高級美編 CSS 樣式 ---
st.markdown(f"""
    <style>
    /* 強制將全站所有元素的字體改為文鼎白玉書體 */
    html, body, [class*="css"], .stMarkdown, .stButton button, div[data-baseweb="input"] input, h1, h2, h3, p, span, div {{
        font-family: "文鼎白玉書體", "AR PL Baoyu", serif !important;
    }}
    
    /* 全局背景設定 */
    .stApp {{
        background-image: linear-gradient(rgba(15, 23, 42, 0.75), rgba(15, 23, 42, 0.75)), url("{bg_image_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* 強制將所有 Markdown 標題與文字改為純白色 */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown p {{
        color: #ffffff !important;
    }}
    
    /* 自訂「今日啟示框」 */
    .custom-info-box {{
        background-color: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid #38bdf8 !important;
        border-left: 5px solid #38bdf8 !important;
        border-radius: 8px !important;
        padding: 15px 20px !important;
        color: #ffffff !important;
        font-size: 18px !important;
        line-height: 1.6 !important;
        margin-bottom: 20px !important;
        box-shadow: 0px 4px 15px rgba(56, 189, 248, 0.2);
    }}
    
    /* 專屬的運勢指引文字區塊 */
    .custom-fortune-text {{
        color: #ffffff !important;
        font-size: 17px !important;
        line-height: 1.8 !important;
        white-space: pre-wrap; 
    }}
    
    /* 核心視覺區塊置中 */
    .centered-container {{
        text-align: center;
        margin-top: 70px;
        margin-bottom: 10px;
    }}
    
    .main-title {{
        font-size: 80px !important;
        font-weight: 800;
        color: #ffffff !important;
        letter-spacing: 2px;
        text-shadow: 0px 0px 30px rgba(56, 189, 248, 0.6);
        margin-bottom: 5px;
    }}
    
    .sub-title {{
        font-size: 26px !important;
        color: #e2e8f0 !important;
        margin-bottom: 60px;
    }}
    
    /* 🔥 終極修復：提問框完美置中比例 🔥 */
    div[data-baseweb="input"] {{
        background-color: rgba(248, 250, 252, 0.95) !important;
        border-radius: 16px !important;
        border: 2px solid #38bdf8 !important;
        box-shadow: 0px 0px 25px rgba(56, 189, 248, 0.4) !important;
        padding: 0px !important; /* 將外層的 padding 歸零，避免上下受力不均 */
        overflow: hidden !important; 
    }}
    
    div[data-baseweb="input"] input {{
        color: #0f172a !important; 
        font-size: 26px !important;
        font-weight: 500 !important;
        padding: 20px 20px !important; /* 讓內層文字自己撐出完美均勻的上下間距 */
        height: auto !important;       
        line-height: 1.5 !important;
    }}
    
    /* 放大按鈕 */
    .stButton > button {{
        font-size: 22px !important;
        font-weight: 600 !important;
        padding: 12px 30px !important;
        border-radius: 14px !important;
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #38bdf8 !important;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        background-color: #38bdf8 !important;
        color: #0f172a !important;
        box-shadow: 0px 0px 15px rgba(56, 189, 248, 0.6) !important;
    }}
    
    /* 抽卡結果的星雲標題 */
    .result-nebula-title {{
        font-size: 34px !important;
        color: #ffffff !important;
        font-weight: 700;
        text-shadow: 0px 0px 15px rgba(56, 189, 248, 0.8);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 網站主標題 ---
st.markdown("""
    <div class="centered-container">
        <h1 class="main-title">Oracle</h1>
        <p class="sub-title">連結宇宙的指引，聆聽星辰的啟示</p>
    </div>
    """, unsafe_allow_html=True)

# --- 4. 讀取星雲資料庫 ---
@st.cache_data
def load_nebula_data():
    return pd.read_csv("cards.csv")

try:
    df = load_nebula_data()
except FileNotFoundError:
    st.error("找不到 cards.csv，請確認檔案位置。")
    st.stop()

# --- 5. 置中互動版面配置 ---
col_left, col_mid, col_right = st.columns([1, 4, 1])

with col_mid:
    st.markdown('<p style="font-size: 26px; font-weight: 600; color: #ffffff; text-align: center; margin-bottom: 20px;">在心中默念你的困惑，並在此寫下一個問題：</p>', unsafe_allow_html=True)
    user_question = st.text_input("question_input", placeholder="", label_visibility="collapsed")
    st.write("") 
    
    btn_space1, btn_mid, btn_space2 = st.columns([1, 2, 1])
    with btn_mid:
        draw_button = st.button("尋求宇宙的共振", use_container_width=True)

# --- 6. 隨機抽卡觸發與結果展示 ---
if draw_button:
    if not user_question:
        st.warning("請先寫下你的問題，讓宇宙能感應你的心聲。")
    else:
        with st.spinner("正在與深空星雲進行能量共振..."):
            time.sleep(2) 
            
            card = df.sample(n=1).iloc[0]
            
            st.markdown("<br><hr><br>", unsafe_allow_html=True)
            
            result_col1, result_col2 = st.columns([1, 1])
            
            with result_col1:
                try:
                    st.image(card['image_path'], use_container_width=True)
                except Exception as e:
                    st.error(f"找不到圖片：{card['image_path']}")
            
            with result_col2:
                st.markdown(f'<p class="result-nebula-title">您抽到的星雲：{card["description"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p style="color:#ffffff !important; font-size:18px;">針對您的問題：「{user_question}」</p>', unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown("### 今日啟示")
                st.markdown(f'<div class="custom-info-box">{card["revelation"]}</div>', unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown("### 完整運勢指引")
                st.markdown(f'<div class="custom-fortune-text">{card["fortune"]}</div>', unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<p style="color:#94a3b8; font-size:14px; text-align:right;">願星辰指引你的方向。</p>', unsafe_allow_html=True)