import streamlit as st
import os
from dotenv import load_dotenv, find_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List, Optional

# Must be the first Streamlit command
st.set_page_config(page_title="GEN-AI Hub", page_icon="🎬", layout="wide", initial_sidebar_state="expanded")

load_dotenv(find_dotenv())

# --- Common Setup ---
@st.cache_resource
def get_model():
    return ChatMistralAI(model="mistral-small-latest", temperature=0.9)

try:
    model = get_model()
except Exception as e:
    model = None
    st.sidebar.error(f"Error initializing model: {e}")

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio(
    "Choose Mode",
    ["🎬 CineIP (Movie Extractor)", "🤖 AI Chatbot"]
)

# ==========================================
# CINE IP - MOVIE EXTRACTOR (Main UI)
# ==========================================
if app_mode == "🎬 CineIP (Movie Extractor)":
    st.markdown("""
    <style>
    /* Static Dark Blue Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #020617 0%, #1e3a8a 50%, #0f172a 100%);
        color: #f8fafc;
    }
    
    /* Glassmorphism for main container */
    .block-container {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 3rem !important;
        margin-top: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }
    
    /* Hide header */
    [data-testid="stHeader"] { background-color: transparent !important; }
    
    /* Beautiful Blue Text & Title styling */
    h1 {
        text-align: center;
        font-family: 'Inter', sans-serif;
        background: -webkit-linear-gradient(#f8fafc, #93c5fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 4px 10px rgba(0,0,0,0.5);
        margin-bottom: 0.5rem;
    }
    
    /* Sleek TextArea */
    .stTextArea > div > div > textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 10px;
    }
    .stTextArea > div > div > textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 10px rgba(59, 130, 246, 0.5) !important;
    }
    
    /* Blue Modern Button */
    .stButton > button {
        background: linear-gradient(90deg, #2563eb, #1d4ed8) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.7rem 2.5rem !important;
        font-weight: bold !important;
        width: 100%;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.6) !important;
        background: linear-gradient(90deg, #1d4ed8, #1e40af) !important;
    }
    
    /* Clean up JSON output */
    [data-testid="stCodeBlock"] {
        background: rgba(0, 0, 0, 0.3) !important;
        border-radius: 10px;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    
    /* Center the button properly */
    [data-testid="column"] {
        display: flex;
        justify-content: center;
    }

    /* Increase Sidebar Icon Visibility and Style as Premium Buttons */
    div[data-testid="stSidebar"] div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.1);
        padding: 12px 15px !important;
        border-radius: 12px;
        margin-bottom: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    div[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
        border-color: #3b82f6;
    }
    div[data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"] p {
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        color: #f8fafc !important;
    }
    </style>
    """, unsafe_allow_html=True)

    class Movie(BaseModel):
        title: str
        release_year: Optional[int]
        genre: List[str]
        director: Optional[str]
        cast: List[str]
        rating: Optional[float]
        summary: str

    parser = PydanticOutputParser(pydantic_object=Movie)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Extract movie information from the paragraph.\n{format_instructions}"),
        ("human", "{paragraph}")
    ])

    st.title("🎬 CineIP Extractor")
    st.markdown("<p style='text-align: center; color: #bfdbfe; margin-bottom: 2rem;'>Paste any movie description and AI will convert it into structured cinematic data.</p>", unsafe_allow_html=True)

    paragraph = st.text_area("Enter Movie Paragraph", height=150)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        extract_pressed = st.button("EXTRACT DATA")
        
    if extract_pressed:
        if not paragraph.strip():
            st.warning("Please enter a paragraph first.")
        elif not model:
            st.error("Model is not initialized.")
        else:
            with st.spinner("Analyzing movie sequence..."):
                try:
                    final_prompt = prompt.invoke({
                        "paragraph": paragraph,
                        "format_instructions": parser.get_format_instructions()
                    })
                    response = model.invoke(final_prompt)
                    movie_data = parser.parse(response.content)
                    
                    st.markdown("<h4 style='color: #60a5fa; margin-top: 1rem;'>Structured Output</h4>", unsafe_allow_html=True)
                    st.json(movie_data.dict())
                    st.success("Extraction Completed Successfully!")
                except Exception as e:
                    st.error("Failed to parse response.")
                    st.exception(e)

# ==========================================
# AI CHATBOT (Sidebar option)
# ==========================================
elif app_mode == "🤖 AI Chatbot":
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    [data-testid="stHeader"] { background-color: transparent !important; }
    .stBottomBlockContainer, [data-testid="stBottom"] { background-color: transparent !important; }
    [data-testid="stBottom"] > div { background-color: transparent !important; }
    [data-testid="stChatInput"] { background-color: #1e293b !important; }
    div[data-testid="stChatMessage"] {
        border-radius: 15px;
        padding: 15px;
        background-color: rgba(30, 41, 59, 0.7);
    }
    h1 { text-align: center; color: #f8fafc; }
    
    /* Increase Sidebar Icon Visibility and Style as Premium Buttons */
    div[data-testid="stSidebar"] div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.1);
        padding: 12px 15px !important;
        border-radius: 12px;
        margin-bottom: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    div[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
        border-color: #3b82f6;
    }
    div[data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"] p {
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        color: #f8fafc !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.divider()
    st.sidebar.subheader("Chat Options")
    
    mode = st.sidebar.selectbox("Choose Personality", ["😂 Funny", "😡 Angry", "😢 Sad", "😊 Friendly"])
    system_prompts = {
        "😂 Funny": "You are a hilarious AI assistant. Always reply with humor and funny jokes.",
        "😡 Angry": "You are an angry AI assistant. Reply aggressively and impatiently.",
        "😢 Sad": "You are a sad AI assistant. Speak emotionally and dramatically.",
        "😊 Friendly": "You are a friendly AI assistant who is warm, helpful and supportive."
    }

    if st.sidebar.button("🧹 Clear Chat"):
        st.session_state.messages = [SystemMessage(content=system_prompts[mode])]
        st.session_state.chat_history = []
        try: st.rerun()
        except AttributeError: st.experimental_rerun()

    if "messages" not in st.session_state or not st.session_state.messages:
        st.session_state.messages = [SystemMessage(content=system_prompts[mode])]
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if st.session_state.messages and getattr(st.session_state.messages[0], 'content', '') != system_prompts[mode]:
        st.session_state.messages = [SystemMessage(content=system_prompts[mode])]
        st.session_state.chat_history = []

    st.title("🤖 AI Mood Chatbot")

    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(message)

    if model:
        if prompt := st.chat_input("Type your message..."):
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.chat_history.append(("user", prompt))
            st.session_state.messages.append(HumanMessage(content=prompt))

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = model.invoke(st.session_state.messages)
                        st.markdown(response.content)
                        st.session_state.messages.append(AIMessage(content=response.content))
                        st.session_state.chat_history.append(("assistant", response.content))
                    except Exception as e:
                        st.error(f"Error calling API: {e}")
