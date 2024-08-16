import chromadb
import ollama 

DATA_PATH = r"data"
CHROMA_PATH = r"chroma_db"

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = chroma_client.get_or_create_collection(name="Crypto_World")

user_query = input("What do you want to know about crypto & blockchain?\n")

results = collection.query(
    query_texts=[user_query],
    n_results=1
)

system_prompt = """
You are a helpful assistant. You answer questions about crypto & payFi. 
But you only answer based on knowledge I'm providing you. You don't use your internal 
knowledge and you don't make thins up.
If you don't know the answer, just say: I don't know
--------------------
The data:
"""+str(results['documents'])+"""
"""

#print(system_prompt)

response = ollama.chat(
    model="llama3.1",  # Replace with the desired model version (e.g., llama3.1)
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query},
    ]
)

print("\n\n---------------------\n\n")

print(response['message']['content'])

# -------------------------------------

# import chromadb
# from openai import OpenAI
# from dotenv import load_dotenv
# import os
# import ollama
# from langchain_community.chat_models import ChatOllama
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate
# from langchain.chains import RetrievalQA
# from langchain import hub

# desiredModal = 'llama3.1:latest'
# questionTask = "How to solve quadratic equation?"

# response = ollama.chat(model=desiredModal, messages=[
#     {"role": "user", 
#      "content": questionTask
#     }
# ])

# OllamaResponse=response['messages']['content']

# print(OllamaResponse)

# # Suppress tokenizers parallelism warning
# os.environ["TOKENIZERS_PARALLELISM"] = "false"

# # Load environment variables
# load_dotenv()

# # Set OpenAI API key
# # openai.api_key = os.getenv("OPENAI_API_KEY")
# client = OpenAI()

# # Setting the environment
# DATA_PATH = r"data"
# CHROMA_PATH = r"chroma_db"

# chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

# collection = chroma_client.get_or_create_collection(name="growing_vegetables")

# user_query = input("What do you want to know about growing vegetables?\n\n")

# results = collection.query(
#     query_texts=[user_query],
#     n_results=1
# )

# # client = openai

# system_prompt = f"""
# You are a helpful assistant. You answer questions about growing vegetables in Florida. 
# But you only answer based on knowledge I'm providing you. You don't use your internal 
# knowledge and you don't make things up.
# If you don't know the answer, just say: I don't know
# --------------------
# The data:
# {results['documents']}
# """

# print(system_prompt)

# response = client.chat.completions.create(
#     model="gpt-3.5-turbo",  # Use the correct model name
#     messages=[
#         {"role": "system", "content": system_prompt},
#         {"role": "user", "content": user_query}
#     ]
# )

# print("\n\n---------------------\n\n")

# print(response.choices[0].message['content'])

# ---------------------------------------------

# from langchain_community.llms import Ollama
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate

# class MyOutputParser(StrOutputParser):
#     def parse(self, text):
#         return text.replace('Assistant: ', '').strip()

# output_parser = MyOutputParser()

# llm = Ollama(model='llama3.1:latest')
# prompt = ChatPromptTemplate.from_messages([
#     ('user', '{input}'),
# ])

# chain = prompt | llm | output_parser

# input_text = input('>>> ')
# while input_text.lower() != 'bye':
#    print(chain.invoke({'input': input_text}))
#    input_text = input('>>> ')

# ---------------------------------------------

# from langchain_community.document_loaders import TextLoader
# from langchain_community.embeddings import OllamaEmbeddings
# from langchain_community.llms import Ollama
# from langchain_community.embeddings import OllamaEmbeddings
# from langchain_text_splitters import CharacterTextSplitter
# from langchain_chroma import Chroma
# from langchain.prompts import ChatPromptTemplate
# from langchain_ollama import ChatOllama

# llm = Ollama(model='llama3.1:latest')

# chatLlm = ChatOllama(
#     model="llama3.1:latest",
#     temperature=0,
# )

# embeddings = OllamaEmbeddings()
# CHROMA_PATH = "chroma"
# PROMPT_TEMPLATE = """
# Answer the question based only on the following context:

# {context}

# ---

# Answer the question based on the above context: {question}
# """
# def query_rag(query_text):
#   """
#   Query a Retrieval-Augmented Generation (RAG) system using Chroma database and OpenAI.
#   Args:
#     - query_text (str): The text to query the RAG system with.
#   Returns:
#     - formatted_response (str): Formatted response including the generated text and sources.
#     - response_text (str): The generated response text.
#   """
#   # YOU MUST - Use same embedding function as before
#   embedding_function = embeddings

#   # Prepare the database
#   db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
  
#   # Retrieving the context from the DB using similarity search
#   results = db.similarity_search_with_relevance_scores(query_text, k=3)

#   # Check if there are any matching results or if the relevance score is too low
#   if len(results) == 0 or results[0][1] < 0.7:
#     print(f"Unable to find matching results.")

#   # Combine context from matching documents
#   context_text = "\n\n - -\n\n".join([doc.page_content for doc, _score in results])
 
#   # Create prompt template using context and query text
#   prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
#   prompt = prompt_template.format(context=context_text, question=query_text)
  
#   # Initialize OpenAI chat model
#   model = chatLlm()

#   # Generate response text based on the prompt
#   response_text = model.predict(prompt)
 
#    # Get sources of the matching documents
#   sources = [doc.metadata.get("source", None) for doc, _score in results]
 
#   # Format and return response including generated text and sources
#   formatted_response = f"Response: {response_text}\nSources: {sources}"
#   return formatted_response, response_text

# # Let's call our function we have defined
# formatted_response, response_text = query_rag(query_text)
# # and finally, inspect our final response!
# print(response_text)

# ---------------------------------------------

# from langchain_community.document_loaders import TextLoader
# # from langchain_openai import OpenAIEmbeddings
# from langchain_text_splitters import CharacterTextSplitter
# # from langchain_chroma import Chroma
# from langchain.vectorstores import Chroma
# # from langchain_ollama import OllamaEmbeddings
# from langchain_community.document_loaders import PyPDFDirectoryLoader
# from langchain.embeddings import OllamaEmbeddings

# embeddings = OllamaEmbeddings(base_url="http://localhost:11434", model="llama3.1:latest")

# # embeddings = OllamaEmbeddings({
# #     model: "llama3.1:latest",
# #     baseUrl: "http://localhost:11434", 
# # })

# DATA_PATH = r"data"

# # Load the document, split it into chunks, embed each chunk and load it into the vector store.
# raw_documents = TextLoader('PayFi.txt').load()
# # raw_documents = PyPDFDirectoryLoader(DATA_PATH)
# text_splitter = CharacterTextSplitter(chunk_size=10000, chunk_overlap=0)
# documents = text_splitter.split_documents(raw_documents)
# db = Chroma.from_documents(documents, embeddings)

# query = "What is payment finance"
# docs = db.similarity_search(query)
# print(docs[0].page_content)

# ---------------------------------------------

# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.chains import create_retrieval_chain
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_community.llms import Ollama
# from langchain_community.embeddings import OllamaEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain_core.documents import Document


# llm = Ollama(model='llama3.1')
# embeddings = OllamaEmbeddings()

# docs = [
#     Document(page_content='哈利波特', metadata={'作者': 'JK羅琳', '類別': '奇幻類小說'}),
#     Document(page_content='變身水（Polyjuice Potion）可變成其他人的樣貌。不可拿來變身成動物，也對動物產生不了效果（包括半人半動物的生物），誤用動物毛髮的話，則會變成動物的容貌。'),
#     Document(page_content='吐真劑（Veritaserum）出自《火盃的考驗》，特徵為像水一樣清澈無味，使用者只要加入三滴，就能強迫飲用者說出真相。它是現存最強大的吐實魔藥，在《哈利波特》的虛構世界觀中受英國魔法部嚴格控管。J·K·羅琳表示，吐真劑最適合用在毫無戒心、易受傷害、缺乏自保技能的人身上，有些巫師能使用鎖心術等方式保護自己免受吐真劑影響。'),
#     Document(page_content='福來福喜（Felix Felicix）出自《混血王子》，是一種稀有而且難以調製的金色魔藥，能夠給予飲用者好運。魔藥的效果消失之前，飲用者的所有努力都會成功。假如飲用過量，會導致頭暈、魯莽和危險的過度自信，甚至成為劇毒。'),
# ]

# vectordb = FAISS.from_documents(docs, embeddings)
# retriever = vectordb.as_retriever()

# prompt = ChatPromptTemplate.from_messages([
#     ('system',
#      'Answer the user\'s questions in Chinese, based on the context provided below:\n\n{context}'),
#     ('user', 'Question: {input}'),
# ])
# document_chain = create_stuff_documents_chain(llm, prompt)

# retrieval_chain = create_retrieval_chain(retriever, document_chain)

# context = []
# input_text = input('>>> ')
# while input_text.lower() != 'bye':
#     response = retrieval_chain.invoke({
#         'input': input_text,
#         'context': context
#     })
#     print(response['answer'])
#     context = response['context']
#     print(response['context'])
#     input_text = input('>>> ')

# ---------------------------------------------











# context = []
# input_text = input('>>> ')
# while input_text.lower() != 'bye':
#     response = retrieval_chain.invoke({
#         'input': input_text,
#         'context': context
#     })
#     print(response['answer'])
#     context = response['context']
#     print(response['context'])
#     input_text = input('>>> ')