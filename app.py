import streamlit as st
from groq import Groq

# Title
st.title("Chat with Viper (Free Version)")

# Get API Key from Streamlit Secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if user_input := st.chat_input("Type your message:"):
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Error: {e}")
