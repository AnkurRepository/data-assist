import streamlit as st
from langchain_openai import ChatOpenAI
from sqlalchemy import text
from report import generate_report
from db import init_db, engine # import both from db


# Initialize DB, Ensure DB is created BEFORE anything else
init_db()


# Page config
st.set_page_config(page_title="Data Assist", layout="wide")
st.title("⭐ Data Assist ⭐")

# UI content
st.markdown("### Ask questions about your database in natural language.")
st.markdown("---")

st.markdown("### Available Tables & Columns:")

st.markdown("""
- Employee --> Emp_id, Name, City, Salary, Dept_id, Job_id
- Department --> Dept_id, Dept_Name
- Job --> Job_id, Job_Title          
""")

st.write("- Please ask questions related to the above tables only.")


# Initialize LLM 
llm = ChatOpenAI(model="gpt-4o-mini", temperature = 0)

# Input Box
query = st.text_input("Ask your question:")

# Examples Buttons
st.markdown("Try these examples")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Show all employees"):
        query = "Show all employees"

    if st.button("Top salary employee"):
        query = "Who has the highest salary?"

with col2:
    if st.button("Employees in IT"):
        query = "Show all employees in IT department"
    
    if st.button("Salary by department"):
        query = "Show total salary by department"

with col3:
    if st.button("Employee + Department + Job"):
        query = "Show employee name with department and job title"



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

                if rows:
                    # Convert rows to list of dict
                    data = [dict(row._mapping) for row in rows]

                    # Natural Language Conversion
                    nl_prompt = f"""
                    You are a helpful assistant.

                    Convert data result set into a natural language answer.

                    Rules:
                    - Keep it short
                    - Do not show JSON
                    - Answer clearly

                    Question: {query}
                    Data: {data}
                    """

                    final_answer = llm.invoke(nl_prompt).content.strip()

                    # Show Output
                    st.subheader("Answer:")
                    st.write(final_answer)


                    # Report Generation
                    st.divider()
                    generate_report(rows)

                else:
                    st.subheader("Answer:")
                    st.info("No data found.")

               
            except Exception as e:
                st.error(f"Error: {e}")

