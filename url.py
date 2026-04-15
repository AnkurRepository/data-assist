import streamlit as st
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import WebBaseLoader


# -----------------------------------
# Extract text
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

    # API key (local + cloud)
    api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

    # Extract
    text = extract_text_from_url(url)

    if text.startswith("Error"):
        return text

    if not text:
        return "No readable content found on this page."

    # Split
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_text(text)

    # Embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)

    # Vector store
    vectorstore = FAISS.from_texts(chunks, embeddings)

    # Retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

    # LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        openai_api_key=api_key
    )

    # RAG chain (stable)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever
    )

    return qa_chain.run(question)