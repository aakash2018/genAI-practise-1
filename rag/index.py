from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaEmbeddings

# pdf_path = Path(__file__).parent / "nodejs.pdf"
pdf_path = str(Path(__file__).parent / "nodejs.pdf")

# Load this file in python program
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

# print(docs[12])

# Split the docs into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200 
)

chunks = text_splitter.split_documents(documents=docs)

# print(chunks[40])


embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
)

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    url="http://localhost:6333",
    collection_name="learning_rag",
    force_recreate=True
)

print("Indexing of documents done....")