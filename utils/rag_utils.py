from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from models.embeddings import get_embedding_model

def setup_rag_pipeline(document_path="data/"):
    """
    Sets up the RAG pipeline by loading PDF and TXT documents,
    creating embeddings, and building a vector store.
    """
    try:
        # --- 1. Load PDF files ---
        pdf_loader = DirectoryLoader(document_path, glob="**/*.pdf", loader_cls=PyPDFLoader, show_progress=True)
        pdf_documents = pdf_loader.load()

        # --- 2. NEW: Load TXT files ---
        txt_loader = DirectoryLoader(document_path, glob="**/*.txt", loader_cls=TextLoader, show_progress=True)
        txt_documents = txt_loader.load()

        # --- 3. NEW: Combine all documents ---
        all_documents = pdf_documents + txt_documents

        # Split documents into manageable chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(all_documents)

        # Get the embedding model
        embedding_model = get_embedding_model()

        # Create a vector store using FAISS
        print("Creating vector store with all documents...")
        vector_store = FAISS.from_documents(texts, embedding_model)
        print("Vector store created successfully.")
        
        return vector_store.as_retriever(search_kwargs={'k': 3})

    except Exception as e:
        print(f"Error setting up RAG pipeline: {e}")
        raise

def query_rag_pipeline(retriever, query: str):
    """
    Queries the RAG pipeline to retrieve relevant document chunks.
    """
    return retriever.invoke(query)