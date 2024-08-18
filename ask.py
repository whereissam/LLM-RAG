import chromadb
import ollama 

DATA_PATH = r"data"
CHROMA_PATH = r"chroma_db"
DISTANCE_THRESHOLD = 1.0 

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = chroma_client.get_or_create_collection(name="Crypto_World")

user_query = input("What do you want to know about crypto & blockchain?\n")

results = collection.query(
    query_texts=[user_query],
    n_results=1
)

if results['distances'][0][0] <= DISTANCE_THRESHOLD:
    context = str(results['documents'][0][0])
else:
    context = "No relevant information found in the database."

system_prompt = f"""
You are a helpful assistant specializing in crypto & payFi. Your tasks are:

1. Answer the user's question based on this context from our database:
{context}

2. Suggest 3 related follow-up questions the user might ask next. These should be a mix of questions that can be answered from the context and those that might require broader knowledge.

Instructions:
- For task 1: If the context doesn't provide enough information, say "I don't have enough information to answer that question accurately."
- For task 2: Ensure the related questions are diverse and genuinely relevant to the user's initial query and the provided context.

Respond in this format:
Answer: [Your answer based on the context]

Related questions you might want to ask:
1. [Related question 1]
2. [Related question 2]
3. [Related question 3]
"""

response = ollama.chat(
    model="llama3.1", 
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query},
    ]
)

print("\n\n---------------------\n\n")

print(response['message']['content'])

