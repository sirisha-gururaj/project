from langchain_community.embeddings import HuggingFaceEmbeddings

def get_embedding_model():
    """Initializes and returns the embedding model."""
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model_kwargs = {'device': 'cpu'}

    # Set normalize_embeddings to True to get reliable 0-1 scores
    encode_kwargs = {'normalize_embeddings': True} 

    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs 
    )

    return embeddings