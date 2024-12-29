from sqlalchemy import create_engine, text
import os

DATABASE_URL = "postgresql://postgres:post123@localhost:5433/mydatabase"

def test_connection():
    try:
        # Create a new database session and return a new connection
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            for row in result:
                print("Connection to database successful:", row)
    except Exception as e:
        print("Error connecting to database:", str(e))

if __name__ == "__main__":
    test_connection()
