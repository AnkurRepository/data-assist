import requests
from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI


def extract_text(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        for script in soup(["script", "style"]):
            script.extract()

        return soup.get_text(separator= " ")

    except Exception as e:
        return f"Error: {str(e)}"

def process_url_query(url, question):
    content = extract_text(url)

    # limit content
    content = content[:3000]

    llm = ChatOpenAI(temperature=0)

    prompt = f"""
    Answer the question based on the below content: 

    {content}

    Question = {question}
    """

    response = llm.invoke(prompt)

    return response.content 
