from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///sample.db", connect_args={"check_same_thread": False})

def init_db():
    with engine.connect() as conn:

        # Employee table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS employee (
                emp_id INTEGER PRIMARY KEY, 
                name TEXT,
                city TEXT,
                salary INTEGER,
                dept_id INTEGER,
                job_id INTEGER
            )
        """))


        # Job table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS department (
                dept_id INTERGER PRIMARY KEY,
                dept_name TEXT               
            )
        """))

        # Department table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS job (
                job_id INTERGER PRIMARY KEY,
                job_title TEXT               
            )
        """))


        # Insert Employees 
        result = conn.execute(text("SELECT COUNT(*) FROM employee"))
        count = result.scalar()

        if count == 0:
            conn.execute(text("""
                INSERT INTO employee (emp_id, name, city, salary, dept_id, job_id) VALUES
                (1,  'Amit',   'Mumbai',    50000, 1, 1),
                (2,  'Neha',   'Delhi',     60000, 2, 2),
                (3,  'Raj',    'Bangalore', 55000, 2, 2),
                (4,  'Priya',  'Chennai',   52000, 3, 3),
                (5,  'Karan',  'Mumbai',    58000, 1, 1),
                (6,  'Sneha',  'Delhi',     61000, 2, 2),
                (7,  'Vikram', 'Pune',      53000, 3, 3),
                (8,  'Anjali', 'Hyderabad', 59000, 2, 2),
                (9,  'Rohit',  'Mumbai',    62000, 1, 1),
                (10, 'Meena',  'Chennai',   54000, 3, 3)
            """))


        # Insert Department 
        result = conn.execute(text("SELECT COUNT(*) FROM department"))
        count = result.scalar()

        if count == 0:
            conn.execute(text("""
                INSERT INTO department (dept_id, dept_name) VALUES
                (1,  'HR'),
                (2,  'IT'),
                (3,  'Finance')
            """))

        # Insert Job 
        result = conn.execute(text("SELECT COUNT(*) FROM job"))
        count = result.scalar()

        if count == 0:
            conn.execute(text("""
                INSERT INTO job (job_id, job_title) VALUES
                (1,  'Manager'),
                (2,  'Developer'),
                (3,  'Analyst')
            """))

        conn.commit()


# def get_engine():
#     server = "localhost"
#     database = "PracticeDB"
#     driver = "ODBC Driver 17 for SQL Server"

#     connection_string = f"mssql+pyodbc://@{server}/{database}?driver={driver}"

#     engine = create_engine(connection_string)
#     return engine