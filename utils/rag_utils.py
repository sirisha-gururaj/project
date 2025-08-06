from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.prompts import PromptTemplate
from models.embeddings import get_embedding_model
from models.llm import get_chatgroq_model

QUERY_PROMPT_TEMPLATE = """You are an AI language model assistant for the Global University of Innovation helpdesk.
Your task is to generate 3 different versions of the given user question to retrieve relevant documents from a vector database.
By generating multiple perspectives on the user question, your goal is to help the user overcome some of the limitations of distance-based similarity search.
If the user provides keywords, turn them into a full, natural-sounding question.
Provide these alternative questions separated by newlines.
Original question: {question}"""

QUERY_PROMPT = PromptTemplate(
    input_variables=["question"],
    template=QUERY_PROMPT_TEMPLATE,
)

def setup_rag_pipeline(document_path="data/"):
    """
    Sets up the final, robust RAG pipeline.
    """
    try:
        # Load and split documents 
        pdf_loader = DirectoryLoader(document_path, glob="**/*.pdf", loader_cls=PyPDFLoader, show_progress=True)
        txt_loader = DirectoryLoader(document_path, glob="**/*.txt", loader_cls=TextLoader, show_progress=True)
        all_documents = pdf_loader.load() + txt_loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=750, chunk_overlap=150)
        texts = text_splitter.split_documents(all_documents)

        embedding_model = get_embedding_model()
        vector_store = FAISS.from_documents(texts, embedding_model)

        # 1. Create a strict base retriever with a similarity score threshold.
        base_retriever = vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={'score_threshold': 0.3, 'k': 5}
        )

        # 2. Get the LLM to power the query generation
        llm = get_chatgroq_model()

        # 3. Create the Multi-Query Retriever using the STRICT base retriever
        multi_query_retriever = MultiQueryRetriever.from_llm(
            retriever=base_retriever, 
            llm=llm,
            prompt=QUERY_PROMPT
        )
        print("Final Multi-Query Retriever with score threshold is complete.")
        return multi_query_retriever

    except Exception as e:
        print(f"Error setting up RAG pipeline: {e}")
        raise

def query_rag_pipeline(retriever, query: str):
    """Queries the RAG pipeline to retrieve relevant document chunks."""
    return retriever.invoke(query)