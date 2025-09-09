import streamlit as st
from groq import Groq

# --- App Title ---
st.set_page_config(page_title="🤖 Chat with Viper", layout="wide")
st.title("🤖 Chat with Viper (Groq Version)")

# --- Load API Key from Streamlit Secrets ---
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error(
        "❌ GROQ_API_KEY not found!\n"
        "Add it to `.streamlit/secrets.toml` or Streamlit Cloud Secrets."
    )
    st.stop()

# --- Initialize Groq client safely ---
try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    st.error(f"Failed to initialize Groq client: {e}")
    st.stop()

# --- Choose Model ---
model = st.selectbox(
    "Choose a Groq model:",
    [
        "llama-3.1-8b-instant",    # Fast, light, cheap
        "llama-3.3-70b-versatile", # More powerful, higher quality
    ],
    index=0,
)

# --- Initialize Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Clear Chat Button ---
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.experimental_rerun()

# --- Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- User Input ---
if user_input := st.chat_input("Type your message here..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response from Groq
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

            # Save assistant reply to history
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Error while generating response: {e}")
