import chromadb
from openai import OpenAI
from dotenv import load_dotenv
import os

# Suppress tokenizers parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Load environment variables
load_dotenv()

# Set OpenAI API key
# openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# Setting the environment
DATA_PATH = r"data"
CHROMA_PATH = r"chroma_db"

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = chroma_client.get_or_create_collection(name="growing_vegetables")

user_query = input("What do you want to know about growing vegetables?\n\n")

results = collection.query(
    query_texts=[user_query],
    n_results=1
)

# client = openai

system_prompt = f"""
You are a helpful assistant. You answer questions about growing vegetables in Florida. 
But you only answer based on knowledge I'm providing you. You don't use your internal 
knowledge and you don't make things up.
If you don't know the answer, just say: I don't know
--------------------
The data:
{results['documents']}
"""

print(system_prompt)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",  # Use the correct model name
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ]
)

print("\n\n---------------------\n\n")

print(response.choices[0].message['content'])
