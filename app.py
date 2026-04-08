import streamlit as st
from langchain_openai import ChatOpenAI
from sqlalchemy import text

# import os
# st.write("FILES:", os.listdir())

from db import init_db, engine # import both from db


# Initialize DB, Ensure DB is created BEFORE anything else
init_db()


# Page config
st.set_page_config(page_title="Data Assist", layout="wide")
st.title("⭐ Data Assist ⭐")

# UI content
st.markdown("### Ask questions about your database in natural language.")
st.markdown("---")
st.markdown("### Querying table and its columns:")
st.write("- Table: employee Columns: emp_id, name, city, salary, dept_id, job_id")
st.write("- Table: department Columns: dept_id, dept_name")
st.write("- Table: job Columns: job_id, job_title")


# Initialize LLM 
llm = ChatOpenAI(model="gpt-4o-mini", temperature = 0)

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
                employee(emp_id, name, city, salary, dept_id, job_id)
                department(dept_id, dept_name)
                job(job_id, job_title)

                Relationships:
                employee.dept_id = department.dept_id
                employee.job_id = job.job_id


                Note:
                - "location", "place", "staying" all mean city

                Convert the following question into SQL query.

                Rules:
                - Use JOIN when needed
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

