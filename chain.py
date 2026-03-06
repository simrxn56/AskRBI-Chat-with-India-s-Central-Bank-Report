from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_classic.prompts import PromptTemplate
from retriever import load_retriever
import os
import warnings
warnings.filterwarnings('ignore')
from dotenv import load_dotenv
load_dotenv()

PROMPT_TEMPLATE = """
You are an expert analyst of RBI Annual Reports.
Use the context below to answer the question as helpfully as possible.
Extract specific numbers, percentages and facts directly from the context.
If the answer is partially in the context, share what you found.
Only say "I couldn't find this" if the context has absolutely nothing related.

Context:
{context}

Question: {question}

Answer:
"""

def build_chain():
    llm = ChatGroq(
        model = "llama-3.1-8b-instant",
        api_key=os.getenv('GROQ_API_KEY'),
        temperature=0.2 # low temp = factual, grounded answers
    )

    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "question"]
    )

    retriever = load_retriever()

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain, retriever

