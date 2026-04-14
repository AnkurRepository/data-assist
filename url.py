import requests
from bs4 import BeautifulSoup

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain


# Extract text from URL
def extract_text_from_url(url: str) -> str:
    try:
        headers = {
            "User-agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unwanted elements
        for tag in soup(["script", "style", "header", "footer", "nav"]):
            tag.extract()

        
        # Extract all visible text
        text = soup.get_text(separator=" ")

        # Clean text
        text = " ".join(text.split())

        return text

    except Exception as e:
        return f"Error extracting text: {str(e)}"
    

# Main RAG function
def process_url_query(url: str, question: str):

    # Extract
    text = extract_text_from_url(url)

    if text.startswith("Error"):
        return text
    
    if not text:
        return "No readable content found on this page."
    
    # Split
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )
    chunks = splitter.split_text(text)

    # Embeddings
    embeddings = OpenAIEmbeddings()

    # Create Vector Store
    vectorstore = FAISS.from_texts(chunks, embeddings)

    # Create Retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

    # LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # RAG Chain
    # Prompt
    prompt = ChatPromptTemplate.from_template("""
             Answer the question using the context below.
                                              
             If the answer is not explicitly present, try to infer from the context.
             If still not possible, say "Not found in the provided content."
                                              
             Context:
             {context}
                                              
             Question:
             {input}
             """,
             input_variable=["context", "question"]
             )          
    # Document chain
    document_chain = create_stuff_documents_chain(llm, prompt)

    # Retrieval chain
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    # Run
    response = retrieval_chain.invoke({"input": question})    

    answer = response["answer"]
                                
    return answer


