
import streamlit as st
import requests
from bs4 import BeautifulSoup

def get_tiktok_views(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return "❌ 请求失败"
        soup = BeautifulSoup(res.text, 'html.parser')
        possible_texts = soup.find_all("strong")
        for tag in possible_texts:
            if "views" in tag.text.lower():
                return tag.text
        return "❌ 播放量未找到"
    except Exception as e:
        return f"❌ 错误：{e}"

st.set_page_config(page_title="TikTok 播放量查询器", layout="centered")

st.title("📈 TikTok 播放量查询器")
st.write("粘贴你的视频链接，点击按钮即可查看播放量（自动读取网页）")

url = st.text_input("请输入 TikTok 视频链接：")

if st.button("查看播放量") and url:
    with st.spinner("正在查询中..."):
        result = get_tiktok_views(url)
        st.success(f"🎯 播放量结果：{result}")
