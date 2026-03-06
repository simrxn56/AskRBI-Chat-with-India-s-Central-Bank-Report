from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def load_retriever(index_path='vectorstore/rbi_index', k=4):
    embeddings = HuggingFaceEmbeddings(
        model_name='all-MiniLM-L6-v2'
    )
    vectorstore = FAISS.load_local(
        index_path,
        embeddings,
        allow_dangerous_deserialization=True
    )
    # k=4 means retreive top 4 most relevant chunks
    return vectorstore.as_retriever(search_kwargs={'k':k})