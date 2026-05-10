from unittest import loader

from fastapi import FastAPI,Query
from client.rq_client import queue
from queues.workers import process_query
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
from langchain_core.documents import Document
from ollama import chat
from ollama import ChatResponse
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaEmbeddings

app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/chat")
def  chat(query:str = Query(..., description="The query to chat with the model")):
    job = queue.enqueue(process_query, query)  # Process the query and generate a response
    return {"status": "queued", "job_id": job.id}

@app.post("/activate-worker")
def activate_worker():
    pdf_path = Path(__file__).parent.parent/ "nodejs.pdf"

    print(f"Loading PDF from path: {pdf_path}")

    # Load this file in python program
    loader = PyPDFLoader(file_path=pdf_path)
    docs = loader.load()

    # Split the docs into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=400
    )

    chunks = text_splitter.split_documents(documents=docs)

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
    )

    vector_stored = QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        url="http://localhost:6333",
        collection_name="learning_rag",
        # force_recreate=True
    )

    return {"status": "worker activated and PDF loaded into vector store"}

@app.get('/job-status')
def get_result(job_id:str = Query(..., description="The ID of the job to retrieve the result for")):
    job = queue.fetch_job(job_id=job_id)
    result = job.return_value()
    
    return { "result":  result}
  
