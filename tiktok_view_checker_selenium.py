
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def get_tiktok_views_with_selenium(url):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("window-size=1920,1080")
        chrome_options.add_argument("user-agent=Mozilla/5.0")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        time.sleep(5)  # 等待页面加载，可根据需要调整时间

        # 播放量可能在 aria-label 或 <strong> 标签内
        try:
            spans = driver.find_elements(By.TAG_NAME, "strong")
            for span in spans:
                if span.text and "次观看" in span.text:
                    return span.text
        except:
            pass

        # 尝试其他结构
        try:
            views_element = driver.find_element(By.XPATH, '//span[contains(text(),"次观看")]')
            return views_element.text
        except:
            pass

        driver.quit()
        return "❌ 未找到播放量"
    except Exception as e:
        return f"❌ 错误：{e}"

st.set_page_config(page_title="TikTok 播放量查询器（Selenium）", layout="centered")

st.title("📈 TikTok 播放量查询器（升级版）")
st.write("粘贴你的视频链接，点击按钮即可查看播放量（使用 Selenium 动态加载页面）")

url = st.text_input("请输入 TikTok 视频链接：")

if st.button("查看播放量") and url:
    with st.spinner("正在启动浏览器并抓取数据，请稍候..."):
        result = get_tiktok_views_with_selenium(url)
        st.success(f"🎯 播放量结果：{result}")
