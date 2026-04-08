from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///sample.db")

def init_db():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS employees (
                name TEXT,
                city TEXT,
                salary INTEGER
            )
        """))

        result = conn.execute(text("SELECT COUNT(*) FROM employees"))
        count = result.scalar()

        if count == 0:
            conn.execute(text("""
                INSERT INTO employees (name, city, salary) VALUES
                ('Amit', 'Mumbai', 50000),
                ('Neha', 'Delhi', 60000),
                ('Raj', 'Delhi', 55000)
            """))

        conn.commit()


# def get_engine():
#     server = "localhost"
#     database = "PracticeDB"
#     driver = "ODBC Driver 17 for SQL Server"

#     connection_string = f"mssql+pyodbc://@{server}/{database}?driver={driver}"

#     engine = create_engine(connection_string)
#     return engine