# app.py
import streamlit as st
import openai

# --- App Configuration ---
st.set_page_config(page_title="Viper — AI Chatbot", page_icon="🦂", layout="centered")
st.title("🦂 Viper — AI Chatbot")
st.markdown("Chat with Viper, powered by OpenAI!")

# --- Retrieve API Key from Streamlit Secrets ---
if "OPENAI_API_KEY" not in st.secrets:
    st.error("⚠️ OpenAI API key is missing! Please add it in Streamlit Cloud → Settings → Secrets.")
    st.stop()

openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- Initialize Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Viper, a friendly and helpful AI assistant."}
    ]

# --- Sidebar Settings ---
with st.sidebar:
    st.header("⚙️ Settings")
    model = st.selectbox("Choose a model", ["gpt-3.5-turbo"], index=0)
    temperature = st.slider("Creativity (temperature)", 0.0, 1.0, 0.3, 0.05)
    if st.button("Clear chat"):
        st.session_state.messages = [
            {"role": "system", "content": "You are Viper, a friendly and helpful AI assistant."}
        ]
        st.experimental_rerun()

# --- Display Chat History ---
for msg in st.session_state.messages[1:]:  # skip system message
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Viper:** {msg['content']}")

# --- User Input ---
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message:", "")
    submitted = st.form_submit_button("Send")

# --- Process Input ---
if submitted and user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Viper is thinking..."):
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=st.session_state.messages,
                temperature=float(temperature),
                max_tokens=1024,
            )
            assistant_reply = response["choices"][0]["message"]["content"].strip()

            # Add assistant message
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
            st.experimental_rerun()

        except Exception as e:
            st.error(f"Error: {e}")
