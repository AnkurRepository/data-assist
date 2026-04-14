import requests
from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI


def extract_text(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.select("p")
        text = " ".join([p.get_text() for p in paragraphs])

        return text

    except Exception as e:
        return f"Error: {str(e)}"

def get_relevant_content(content, question):
    keywords = [w.lower() for w in question.split() if len(w) > 3]

    sentences = content.split(".")
    scored_sentences = []

    for s in sentences:
        score = sum(1 for k in keywords if k in s.lower())
        if score > 0:
            scored_sentences.append((score, s))

    # sort by relevance
    scored_sentences.sort(reverse=True, key=lambda x: x[0])

    top_sentences = [s for _, s in scored_sentences[:5]]

    return ". ".join(top_sentences)


def process_url_query(url, question):
    content = extract_text(url)

    # limit content
    content = content[:8000]

    # get relevant content
    filtered_content = get_relevant_content(content, question)
    print("FILTERED:", filtered_content[:500])

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
