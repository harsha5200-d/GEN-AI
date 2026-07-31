# 🎬 CineIP Extractor

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://cinematic-ip-madhav.streamlit.app/)

CineIP Extractor is an AI-powered web application that takes any unstructured movie description or plot summary and instantly converts it into structured, easy-to-read JSON data. 

Built using **Streamlit**, **LangChain**, and **Mistral AI**, this tool acts as an expert data extractor, intelligently identifying missing information and structuring it beautifully.

## 🚀 Live Demo
You can try the live application right now:
**[https://cinematic-ip-madhav.streamlit.app/](https://cinematic-ip-madhav.streamlit.app/)**

## ✨ Features
* **Intelligent Extraction**: Uses Mistral AI to parse unstructured text into highly accurate structured data.
* **World Knowledge Integration**: If details like Release Year, Director, or Cast are missing from the text, the AI uses its internal knowledge base to fill in the blanks.
* **Beautiful UI**: A sleek, modern, glassmorphism-inspired dark mode interface built natively in Streamlit.
* **Structured Output**: Strictly enforces output formats using Pydantic parsers.

## 🛠️ Technology Stack
* **Frontend**: Streamlit
* **AI Framework**: LangChain
* **LLM**: Mistral AI (`mistral-small-latest`)
* **Data Parsing**: Pydantic

## 💻 Running Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/harsha5200-d/GEN-AI.git
   cd GEN-AI
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Environment Variables**
   Create a `.env` file in the root directory and add your Mistral API key:
   ```toml
   MISTRAL_API_KEY="your_api_key_here"
   ```

4. **Run the Streamlit App**
   ```bash
   cd CineIP
   python -m streamlit run uicore.py
   ```