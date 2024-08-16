from langchain_community.document_loaders import PyPDFDirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb

# setting the environment

DATA_PATH = r"data"
TEXT_PATH = r"text"
CHROMA_PATH = r"chroma_db"

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = chroma_client.get_or_create_collection(name="Crypto_World")

# loading the document

# loader = PyPDFDirectoryLoader(DATA_PATH)
loaders = [
    PyPDFDirectoryLoader(DATA_PATH),  # First PDF directory
    TextLoader("PayFi.txt")          # Text files loader (or any other type of loader)
]
# Load all documents from multiple sources
raw_documents = []
for loader in loaders:
    raw_documents.extend(loader.load())  # Combine the loaded documents

# Test for embedded data
print(len(raw_documents))
page = raw_documents[len(raw_documents) -1]
print(page.page_content[0:2000])

# splitting the document

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
)

chunks = text_splitter.split_documents(raw_documents)

# # preparing to be added in chromadb

documents = []
metadata = []
ids = []

i = 0

for chunk in chunks:
    documents.append(chunk.page_content)
    ids.append("ID"+str(i))
    metadata.append(chunk.metadata)

    i += 1

# adding to chromadb


collection.upsert(
    documents=documents,
    metadatas=metadata,
    ids=ids
)

# Test for data already embedded

# Verify the number of documents in the collection
num_documents = collection.count()
print(f"Number of documents in the collection: {num_documents}")

# Retrieve and print a specific document by ID
retrieved_document = collection.get(ids=["ID0"])
print(f"Retrieved document: {retrieved_document}")

# List all IDs in the collection
all_ids = collection.get(ids=[])
print(f"All document IDs: {all_ids['ids']}")

# Query the collection for documents containing the word "vegetables"
results = collection.query(
    query_texts=["payfi"],
    n_results=5
)

for result in results['documents']:
    print(result)