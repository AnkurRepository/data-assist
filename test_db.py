from db import get_engine

try:
    engine = get_engine()

    with engine.connect() as conn:
        print("Database connected successfully!")

except Exception as e:
    print("Connection failed:")
    print(e)
