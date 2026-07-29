import os
# Change the cache directory to a local folder to avoid Windows permission/locking issues
os.environ['HF_HOME'] = './models_cache'
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
)

texts = [ "Hello this is madhav",
         "hello your name is krishna,"
         "your are most beautyful person "]

vector = embedding.embed_documents(texts)

print(vector)