from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///sample.db")

with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS employees (
            name TEXT,
            city TEXT,
            salary INTEGER
        )
    """))

    conn.execute(text("""
        INSERT INTO employees (name, city, salary) VALUES
        ('Amit', 'Mumbai', 50000),
        ('Neha', 'Delhi', 60000),
        ('Raj', 'Delhi', 55000)
    """))

    conn.commit()

    
