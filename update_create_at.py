# /app/update_created_at.py

from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.db.session import SessionLocal
from app.db.models import Form

# Function to update created_at for existing forms
def update_created_at_for_existing_forms(db: Session):
    db.query(Form).filter(Form.created_at.is_(None)).update({Form.created_at: func.now()})
    db.commit()

# Main script to run the update
def main():
    # Create a new database session
    db = SessionLocal()
    try:
        # Call the function to update created_at
        update_created_at_for_existing_forms(db)
        print("Updated created_at for existing forms.")
    finally:
        # Close the database session
        db.close()

if __name__ == "__main__":
    main()
