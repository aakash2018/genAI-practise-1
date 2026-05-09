from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
from langchain_core.documents import Document
from ollama import chat
from ollama import ChatResponse
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaEmbeddings


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
    force_recreate=True
)

vector_store = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    url="http://localhost:6333",
    collection_name="learning_rag"
)


async def process_query(query:str):
    print(f"Processing query: {query}")
    # Simulate processing the query
    search_results = vector_store.similarity_search(query=query)
    context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])

    SYSTEM_PROMPT = f"""
    You are a helpfull AI Assistant who answeres user query based on the available context retrieved from a PDF file along with page_contents and page number.

    You should only ans the user based on the following context and navigate the user to open the right page number to know more.

    Context:
    {context}
    """
    ressponse:ChatResponse = chat(
    model="llama3",
    messages=[
        { "role": "system", "content":SYSTEM_PROMPT  },
        { "role": "user", "content":query  },
    ]
    )

    print(f"🤖: {ressponse.message.content}")
    return ressponse.message.content