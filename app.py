import streamlit as st
import pandas as pd
import openai
from streamlit_chat import message
openai.api_key = st.secrets['OPENAI_API_KEY']


def chat_with_csv(df, prompt):
    df_str = df.to_csv(index=False)
    messages = [
        {"role": "system", "content": "You are a helpful and polite assistant."},
        {"role": "user", "content": f"Data:\n{df_str}\n\nQuery: {prompt}"}
    ]
    for attempt in range(3):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=80,
                temperature=0.5,
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            st.error(f"Error: {e}")
            if attempt < 2:
                st.warning("Retrying...")
            else:
                return "Failed to get a response from the model."


def reset_session_state():
    for key in st.session_state.keys():
        del st.session_state[key]


st.set_page_config(
    page_title="ibexstack Chatbot (own data)(only csv)", layout='wide')
# st.markdown("<a href='/'><img src='http://dev.ibexstack.com/stagging/assets/images/creative/logo_white.png' alt='Img not found' style='width: 182px;margin-top: 0px;'/></a>", unsafe_allow_html=True)
st.image('./logo_white.png', width=150)
hide_fullscreen_icon = """<style>button[title="View fullscreen"] {display: none;}</style>"""
st.markdown(hide_fullscreen_icon, unsafe_allow_html=True)
st.markdown(
    "<div style='display:flex'><h4 style='font-size:30px'>ibexstack Chatbot</h4><h5 style='font-size: 15px;font-weight:bold;margin-left: -22px;margin-top: 24px;color:#ff4b4b'>(own data)(only csv)</h5></div>",
    unsafe_allow_html=True
)

input_csv = st.file_uploader("Upload your CSV file", type=['csv'])
if input_csv is not None:
    reset_session_state()
    col1, col2 = st.columns([1, 1])
    with col1:
        st.success("Your CSV Data")
        data = pd.read_csv(input_csv)
        data = data.head(50)
        st.dataframe(data, use_container_width=True)
    with col2:
        st.success("Enter your Query Below")
        input_text = st.chat_input("Enter your query")
        if input_text:
            message(input_text, is_user=True)
            result = chat_with_csv(data, input_text)
            message(result)
