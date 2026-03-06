import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def load_pdf(path):
    doc = fitz.open(path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text

def build_vector_store(path, save_path='vectorstore/rbi_index'):

    # 1. Load PDF
    text = load_pdf(path)

    # 2. Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 50
    )
    chunks = splitter.create_documents([text])
    print(f"Total chunks created: {len(chunks)}")

    # 3. Embed and save to FAISS
    embeddings = HuggingFaceEmbeddings(
        model_name='all-MiniLM-L6-v2'
    )
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(save_path)
    print(f"Vectorstore saved to {save_path}")

def main():
    build_vector_store("data/RBI_annual_report.pdf")

if __name__ == "__main__":
    main()