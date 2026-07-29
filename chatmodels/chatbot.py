from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI

model = ChatMistralAI(model = "mistral-small-2506", temperature=0.9)

while True:

    prompt = input("You: ")

    if prompt == "0":
        break
    
    if not prompt.strip():
        continue
    
    response = model.invoke(prompt)

    print("Bot : ", response.content)