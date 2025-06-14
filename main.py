import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Title
st.title("📊 GitHub Radar")

# Sidebar input
username = st.sidebar.text_input("🔍 Nhập GitHub Username:", value="hieupham")

if username:
    user_url = f"https://api.github.com/users/{username}"
    repo_url = f"https://api.github.com/users/{username}/repos"

    user_data = requests.get(user_url).json()
    repo_data = requests.get(repo_url).json()

    if 'message' in user_data and user_data['message'] == 'Not Found':
        st.error("❌ Không tìm thấy người dùng.")
    else:
        # Hiển thị thông tin user
        st.image(user_data["avatar_url"], width=100)
        st.subheader(user_data["name"] or username)
        st.write(f"📍 Followers: {user_data['followers']}")
        st.write(f"📦 Public Repos: {user_data['public_repos']}")

        # Xử lý data repo
        if repo_data:
            df = pd.DataFrame(repo_data)
            df = df[['name', 'stargazers_count', 'forks_count', 'html_url']]

            # Biểu đồ stars
            fig = px.bar(df, x='name', y='stargazers_count',
                         labels={'name':'Repository', 'stargazers_count':'Stars'},
                         title="⭐ Stars của từng Repository")
            st.plotly_chart(fig)

            # Danh sách repo
            st.markdown("## 📂 Danh sách Repository:")
            for index, row in df.iterrows():
                st.write(f"- [{row['name']}]({row['html_url']}) ⭐ {row['stargazers_count']} | 🍴 {row['forks_count']}")
        else:
            st.info("Người này chưa có repository công khai nào.")
else:
    st.info("Nhập một username để bắt đầu.")

