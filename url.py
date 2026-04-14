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

def get_relevant_content(content, question):
    keywords = [w for w in question.lower().split() if len(w) > 3]

    sentences = content.split(".")
    relevant = []

    for s in sentences:
        if any(k in s.lower() for k in keywords):
            relevant.append(s)
            
    return ". ".join(relevant[:10])


def process_url_query(url, question):
    content = extract_text(url)

    # limit content
    content = content[:8000]

    # get relevant content
    filtered_content = get_relevant_content(content, question)

    llm = ChatOpenAI(temperature=0)

    prompt = f"""
    You must answer only from the provided content.

    Rules:
    - Do Not guess
    - Do Not use outside language
    - If answer is not clearly present, say:
    "I could not find the answer in the provided content."

    Do NOT guess or make up the answers.

    {filtered_content}

    Question = {question}
    """

    response = llm.invoke(prompt)

    return response.content 
