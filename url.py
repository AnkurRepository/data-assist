import requests
from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI


def extract_text(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text() for p in paragraphs])

        return text

    except Exception as e:
        return f"Error: {str(e)}"

def process_url_query(url, question):
    content = extract_text(url)

    # limit content
    content = content[:8000]

    llm = ChatOpenAI(temperature=0)

    prompt = f"""
    You are answering based on the webpage content.

    Find the exact answer from the content.
    If the answer exists, return it directly
    Do Not say information is missing unless truly absent

    {content}

    Question = {question}
    """

    response = llm.invoke(prompt)

    return response.content 
