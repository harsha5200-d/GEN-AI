from dotenv import load_dotenv

load_dotenv()

# from langchain_openai import ChatOpenAI
# from langchain_groq import ChatGroq
from langchain.chat_models import init_chat_model

model = init_chat_model(model="gpt-4.1")

response = model.invoke("where is ikson abids")
print(response.content)