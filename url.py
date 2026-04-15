import streamlit as st

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.document_loaders import WebBaseLoader

import os

api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")


# -----------------------------------
# Extract text using WebBaseLoader
# -----------------------------------
def extract_text_from_url(url: str) -> str:
    try:
        loader = WebBaseLoader(url)
        docs = loader.load()

        text = " ".join([doc.page_content for doc in docs])
        return text

    except Exception as e:
        return f"Error extracting text: {str(e)}"
    

# -----------------------------------
# Main RAG function
# -----------------------------------
def process_url_query(url: str, question: str):

    # Get API key (works for both local + Streamlit Cloud)
    api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

    # Extract content
    text = extract_text_from_url(url)

    if text.startswith("Error"):
        return text

    if not text:
        return "No readable content found on this page."

    # DEBUG (optional - remove later)
    st.write("Text length:", len(text))

    # Split text
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_text(text)

    # Embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)

    # Vector store
    vectorstore = FAISS.from_texts(chunks, embeddings)

    # Retriever (improved)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

    # LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        openai_api_key=api_key
    )

    # Prompt
    prompt = ChatPromptTemplate.from_template("""
    Answer the question using the context below.

    Try your best to answer using available information.
    If not found, say "Not found in the provided content."

    Context:
    {context}

    Question:
    {input}
    """)

    # Chains
    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    # Run
    response = retrieval_chain.invoke({"input": question})

    return response["answer"]