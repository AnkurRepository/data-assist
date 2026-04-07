from sqlalchemy import create_engine

def get_engine():
    server = "localhost"
    database = "PracticeDB"
    driver = "ODBC Driver 17 for SQL Server"

    connection_string = f"mssql+pyodbc://@{server}/{database}?driver={driver}"

    engine = create_engine(connection_string)
    return engine