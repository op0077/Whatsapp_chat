from tkinter import VERTICAL
from wordcloud import WordCloud
import streamlit as st
import preprocessing as pre
import front
import time
import base64
main_bg = "night.jpg"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/png;base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
        position: fixed;
        background-repeat : no-repeat;
        background-size: 100% 100%;
        margin:auto;
        min-width:100%;
        min-height:100%;
        z-index:-1;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
text = "Welcome to whatsapp chat analyser"
#ss = SessionState.get(k=0)
# if ss.k==0:
#     t = st.empty()
#     for i in range(len(text) + 1):
#         t.markdown("## %s..." % text[0:i])
#         time.sleep(0.05)

st.sidebar.title("whatsapp_chat_analyzer")
uploaded_file = st.sidebar.file_uploader("chose a file")
if uploaded_file is not None:
    # ss.k=1
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    dframe = pre.preprocess(data)
    st.dataframe(dframe)

    #fetchin unique users using unique
    user_list = dframe['user'].unique().tolist()
    user_list.remove('kargo_notification')
    n1_user_list = user_list.copy()
    user_list.insert(0,'Overall')
    
    selected_user = st.sidebar.selectbox("show analysis with respect to user",user_list)
    
    

    if st.sidebar.button("show analysis"):
        front.show_analysis(selected_user,dframe)
    #compare two user
    with st.sidebar:
        st.title("compare two user")
    selected_user1 = st.sidebar.selectbox("User 1",n1_user_list)
    selected_user2 = st.sidebar.selectbox("User 2",n1_user_list)
    tab = st.sidebar.button('compare')
    if selected_user1 == selected_user2 and tab:
        st = st.empty()
        front.show_analysis(selected_user2,dframe)

    if selected_user1 != selected_user2 and tab:
        st= st.empty()
        front.compare(selected_user1,selected_user2,dframe)
