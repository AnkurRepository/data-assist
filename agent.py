from dotenv import load_dotenv
import os

load_dotenv()



from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from db import get_engine


prefix = """
You are a SQL assistant.

Rules:
- Never perform INSERT, UPDATE, DELETE, DROP
- If user asks anything else, politely refuse
- Always use SQL to answer questions
- Never answer from memory
- Always generate a SQL query first
- Only generate and use SELECT statements.
- Even if you know the answer, still query the database

"""

def get_agent():
    engine = get_engine()

    db = SQLDatabase(engine)

    llm = ChatOpenAI(
        temperature=0,
        model="gpt-4o-mini"
    )

    agent = create_sql_agent(
        llm=llm,
        db=db,
        verbose=True,
        handle_parsing_errors=True,
        return_intermediate_steps=True,
        prefix=prefix
    )

    return agent