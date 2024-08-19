from langchain_community.document_loaders import PyPDFDirectoryLoader, TextLoader, AsyncHtmlLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb

# setting the environment

DATA_PATH = r"data"
TEXT_PATH = r"text"
CHROMA_PATH = r"chroma_db"

urls = ["https://www.kimkim.com/c/5-days-in-germany-unique-itineraries", "https://www.lartisien.com/blog/5-day-itinerary-in-berlin/"]

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = chroma_client.get_or_create_collection(name="Travel_Germany")

# loading the document

# loader = AsyncHtmlLoader(urls)
# docs = loader.load()
# print(docs)

# loader = PyPDFDirectoryLoader(DATA_PATH) # for single loader

loaders = [
    # PyPDFDirectoryLoader(DATA_PATH),  # First PDF directory
    TextLoader("germany.txt")          # Text files loader (or any other type of loader)
]

# Load all documents from multiple sources
raw_documents = []
for loader in loaders:
    raw_documents.extend(loader.load())  # Combine the loaded documents

# ----- Test for embedded data ---------
# print(len(raw_documents))
# page = raw_documents[len(raw_documents) -1]
# print(page.page_content[0:500])
# print("\n\n---------------------\n\n")

# ----- Test for embedded data ---------
# splitting the document
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", "," ," ", ""],
)

chunks = text_splitter.split_documents(raw_documents)
# chunks = text_splitter.split_documents(docs)

# # preparing to be added in chromadb
documents = []
metadata = []
ids = []

i = 0

# for chunk in chunks:
#     documents.append(chunk.page_content)
#     ids.append("ID"+str(i))
#     metadata.append(chunk.metadata)
#     i += 1

# adding to chromadb
# collection.upsert(
#     documents=documents,
#     metadatas=metadata,
#     ids=ids
# )

# # ----- Test for data already embedded ---------

# # Verify the number of documents in the collection
# num_documents = collection.count()
# print(f"Number of documents in the collection: {num_documents}")
# print("\n\n---------------------\n\n")
# # Retrieve and print a specific document by ID
# retrieved_document = collection.get(ids=["ID0"])
# print(f"Retrieved document: {retrieved_document}")
# print("\n\n---------------------\n\n")
# # List all IDs in the collection
# all_ids = collection.get(ids=[])
# print(f"All document IDs: {all_ids['ids']}")
# print("\n\n---------------------\n\n")
# # Query the collection for documents containing the word "vegetables"
results = collection.query(
    query_texts=["Germany" , "travel", "5-day trip"],
    n_results=2
)

# print(results)
for result in results['documents']:
    print(result)

# ----- Test for data already embedded ---------
