import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
)

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Mood Chatbot",
    page_icon="🤖",
    layout="wide",
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>
/* Main Background Gradient */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: #f8fafc;
}

/* Make header transparent to remove the top black bar */
[data-testid="stHeader"] {
    background-color: transparent !important;
}

/* Premium Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #0f172a !important;
    border-right: 1px solid #334155;
}

/* Make the bottom chat input area blend with the gradient */
.stBottomBlockContainer, [data-testid="stBottom"] {
    background-color: transparent !important;
}
[data-testid="stBottom"] > div {
    background-color: transparent !important;
}

/* Style the chat input box to look sleek */
[data-testid="stChatInput"] {
    background-color: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
}

/* Beautiful chat messages */
div[data-testid="stChatMessage"] {
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 10px;
    background-color: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(51, 65, 85, 0.5);
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

/* Adjust page title spacing */
h1 {
    text-align: center;
    color: #f8fafc;
    font-weight: 700;
    padding-top: 1rem;
    padding-bottom: 1.5rem;
}

.block-container {
    padding-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------- MODEL ----------------

try:
    model = ChatMistralAI(
        model="mistral-small-latest",
        temperature=0.9,
    )
except Exception as e:
    st.error(f"Error initializing model: {e}")
    model = None

# ---------------- SIDEBAR ----------------

st.sidebar.title("🤖 AI Personalities")

mode = st.sidebar.selectbox(
    "Choose Mode",
    [
        "😂 Funny",
        "😡 Angry",
        "😢 Sad",
        "😊 Friendly",
    ]
)

system_prompts = {
    "😂 Funny":
        "You are a hilarious AI assistant. Always reply with humor and funny jokes.",

    "😡 Angry":
        "You are an angry AI assistant. Reply aggressively and impatiently.",

    "😢 Sad":
        "You are a sad AI assistant. Speak emotionally and dramatically.",

    "😊 Friendly":
        "You are a friendly AI assistant who is warm, helpful and supportive."
}

if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.messages = [
        SystemMessage(content=system_prompts[mode])
    ]
    st.session_state.chat_history = []
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

st.sidebar.divider()

st.sidebar.metric(
    "Messages",
    len(st.session_state.get("chat_history", []))
)

# ---------------- SESSION ----------------

if "messages" not in st.session_state or not st.session_state.messages:
    st.session_state.messages = [
        SystemMessage(content=system_prompts[mode])
    ]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Change system prompt if mode changes
if (
    st.session_state.messages
    and len(st.session_state.messages) > 0
    and getattr(st.session_state.messages[0], 'content', '') != system_prompts[mode]
):
    st.session_state.messages = [
        SystemMessage(content=system_prompts[mode])
    ]
    st.session_state.chat_history = []

# ---------------- TITLE ----------------

st.title("🤖 AI Mood Chatbot")

st.caption("Powered by Mistral AI")

# ---------------- DISPLAY CHAT ----------------

for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# ---------------- INPUT ----------------

if model:
    if prompt := st.chat_input("Type your message..."):

        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.chat_history.append(
            ("user", prompt)
        )

        st.session_state.messages.append(
            HumanMessage(content=prompt)
        )

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = model.invoke(st.session_state.messages)
                    st.markdown(response.content)
                    
                    st.session_state.messages.append(
                        AIMessage(content=response.content)
                    )

                    st.session_state.chat_history.append(
                        ("assistant", response.content)
                    )
                except Exception as e:
                    st.error(f"Error calling API: {e}")
else:
    st.warning("Chat is disabled because the model failed to initialize.")