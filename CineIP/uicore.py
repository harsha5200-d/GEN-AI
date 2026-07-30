import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser
from langchain_mistralai import ChatMistralAI

# -------------------- Setup --------------------
load_dotenv()

@st.cache_resource
def get_model():
    return ChatMistralAI(model="mistral-small-latest")

try:
    model = get_model()
except Exception as e:
    model = None
    st.error(f"Error initializing model: {e}")

# -------------------- Schema --------------------
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
    ("system", """
Extract movie information from the paragraph.
{format_instructions}
"""),
    ("human", "{paragraph}")
])

# -------------------- UI --------------------
st.set_page_config(page_title="🎬 Movie Info Extractor", page_icon="🍿", layout="centered")

# Cinematic Glassmorphism CSS
st.markdown("""
<style>
/* Animated background for a cinematic vibe */
@keyframes gradientAnimation {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stApp {
    background: linear-gradient(-45deg, #09090b, #18181b, #4c0519, #27272a);
    background-size: 400% 400%;
    animation: gradientAnimation 15s ease infinite;
    color: #f8fafc;
}

/* Glassmorphism for the main container */
.block-container {
    background: rgba(24, 24, 27, 0.5);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 3rem !important;
    margin-top: 3rem;
    margin-bottom: 3rem;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.7);
}

/* Hide header */
[data-testid="stHeader"] {
    background-color: transparent !important;
}

/* Typography for Title */
h1 {
    text-align: center;
    font-family: 'Inter', sans-serif;
    text-transform: uppercase;
    letter-spacing: 3px;
    background: -webkit-linear-gradient(#f8fafc, #94a3b8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0px 4px 10px rgba(0,0,0,0.5);
    margin-bottom: 0.5rem;
}

/* TextArea Glassmorphism */
.stTextArea > div > div > textarea {
    background-color: rgba(255, 255, 255, 0.05) !important;
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 12px;
}
.stTextArea > div > div > textarea:focus {
    border-color: #e11d48 !important;
    box-shadow: 0 0 10px rgba(225, 29, 72, 0.5) !important;
}

/* Animated Cinematic Button */
.stButton > button {
    background: linear-gradient(90deg, #e11d48, #be123c) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 2.5rem !important;
    font-weight: bold !important;
    letter-spacing: 1px;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(225, 29, 72, 0.4) !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(225, 29, 72, 0.7) !important;
    background: linear-gradient(90deg, #be123c, #9f1239) !important;
}

/* JSON / Code Blocks styling */
[data-testid="stCodeBlock"] {
    background: rgba(0, 0, 0, 0.5) !important;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}
</style>
""", unsafe_allow_html=True)

st.title("🎬 Movie Extractor")
st.markdown("<p style='text-align: center; color: #cbd5e1; margin-bottom: 2rem;'>Paste any movie description and AI will convert it into structured cinematic data.</p>", unsafe_allow_html=True)

paragraph = st.text_area("Enter Movie Paragraph", height=150, placeholder="e.g. In 1999, The Matrix redefined sci-fi...")

if st.button("EXTRACT DATA"):
    if not paragraph.strip():
        st.warning("Please enter a paragraph first.")
    elif not model:
        st.error("Model is not initialized. Please check your API keys.")
    else:
        with st.spinner("Analyzing movie sequence..."):
            try:
                final_prompt = prompt.invoke({
                    "paragraph": paragraph,
                    "format_instructions": parser.get_format_instructions()
                })

                response = model.invoke(final_prompt)

                st.markdown("<h4 style='color: #e11d48; margin-top: 1rem;'>Raw Model Output</h4>", unsafe_allow_html=True)
                st.code(response.content, language="json")

                movie_data = parser.parse(response.content)

                st.markdown("<h4 style='color: #e11d48; margin-top: 1rem;'>Structured Output</h4>", unsafe_allow_html=True)
                st.json(movie_data.dict())

                st.success("Extraction Completed Successfully!")

            except Exception as e:
                st.error("Failed to parse response. Model did not follow schema.")
                st.exception(e)