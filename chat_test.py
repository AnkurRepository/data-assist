from dotenv import load_dotenv
import os

load_dotenv()


from agent import get_agent

agent = get_agent()

while True:
    query = input("Ask something: ")

    if query.lower() in ["exit", "quit", "bye"]:
        print("Goodbye!")
        break

    response = agent.run(query)
    print(response)