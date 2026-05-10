from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
from langchain_core.documents import Document
from ollama import chat
from ollama import ChatResponse
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaEmbeddings


embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
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