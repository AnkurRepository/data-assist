import streamlit as st
from langchain_openai import ChatOpenAI
from sqlalchemy import text
from sqlalchemy import create_engine
from db import get_engine
from agent import get_agent

# Page config
st.set_page_config(page_title="Data Assist", layout="wide")

st.title("⭐ Data Assist ⭐")

# UI content
st.markdown("### Ask questions about your database in natural language.")
st.markdown("---")
st.markdown("### Example questions:")
st.write("- Show all employees")
st.write("- Employees in HR department")
st.write("- Top 3 highest salaries")


# Initialize LLM and DB
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
# engine = get_engine()
engine = create_engine("sqlite:///sample.db")


# Input Box
query = st.text_input("Ask your question:")

# Button
if st.button("Submit"):
    if query:
        with st.spinner("Thinking....."):
            try:
                # Generate SQL
                sql_prompt = f"""
                You are a SQL Expert.

                Database Schema: 
                employees(name, city, salary)

                Note:
                - "location", "place", "staying" all mean city

                Convert the following question into SQL query.

                Rules:
                - Use only SELECT statements
                - Do not explain anything
                - Return only SQL query

                Question: {query}
                """

                sql_query = llm.invoke(sql_prompt).content.strip()
                sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
                sql_query = sql_query.replace('"', '').strip()

                # Execute SQL
                with engine.connect() as conn:
                    result = conn.execute(text(sql_query))
                    rows = result.fetchall()

                # Show SQL
                st.subheader("Generated SQL:")
                st.code(sql_query, language="sql")

                st.subheader("Answer:")

                if rows:
                    for row in rows:
                        try:
                            st.write(dict(row._mapping))
                        except:
                            st.write(row)
                else:
                    st.info("No data found.")

               
            except Exception as e:
                st.error(f"Error: {e}")
