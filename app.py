import streamlit as st
from openai import OpenAI

# Initialize OpenAI client with your secret API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Viper Chatbot", page_icon="🤖", layout="centered")
st.title("Chat with Viper, powered by OpenAI!")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are Viper, a helpful AI chatbot."}]

# User input
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message:")
    submitted = st.form_submit_button("Send")

# Handle conversation
if submitted and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Viper is thinking..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # You can also use "gpt-4o" or "gpt-3.5-turbo"
                messages=st.session_state.messages,
                temperature=0.7,
                max_tokens=300,
            )
            assistant_reply = response.choices[0].message.content.strip()

            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

        except Exception as e:
            st.error(f"Error: {e}")

# Display chat history
for message in st.session_state.messages[1:]:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    else:
        st.markdown(f"**Viper:** {message['content']}")
