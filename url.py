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
    Answer the questions ONLY using the provided content

    Find the exact answer from the content.
    If the answer exists, return it directly
    If the answer is not found in the content, say:
    "I could not find the answer in the provided content."

    Do NOT guess or make up the answers.

    {content}

    Question = {question}
    """

    response = llm.invoke(prompt)

    return response.content 
