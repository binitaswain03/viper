import streamlit as st
from groq import Groq

# --- App Title ---
st.title("🤖 Chat with Viper (Free Groq Version)")

# --- Load API Key from Streamlit Secrets ---
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY not found in Streamlit Secrets. Please add it in your Streamlit Cloud settings.")
    st.stop()

# --- Initialize Groq client ---
client = Groq(api_key=GROQ_API_KEY)

# --- Initialize Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Clear Chat Button ---
if st.button("Clear Chat"):
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
                model="llama3-8b-8192",  # Free & fast model
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

            # Save assistant reply to history
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Error while generating response: {e}")
