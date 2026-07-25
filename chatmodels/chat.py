from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model

# Using Google Gemini which has a generous free tier!
# Remember to add GOOGLE_API_KEY to your .env file

model = init_chat_model("gpt-4.1")

response = model.invoke("what is cricket?")
print(response.content)