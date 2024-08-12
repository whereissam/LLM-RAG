from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb

# setting the environment

DATA_PATH = r"data"
CHROMA_PATH = r"chroma_db"

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = chroma_client.get_or_create_collection(name="growing_vegetables")

# loading the document

loader = PyPDFDirectoryLoader(DATA_PATH)

raw_documents = loader.load()

# splitting the document

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
)

chunks = text_splitter.split_documents(raw_documents)

# preparing to be added in chromadb

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
    query_texts=["vegetables"],
    n_results=5
)

for result in results['documents']:
    print(result)