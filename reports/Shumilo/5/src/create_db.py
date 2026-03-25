from db import engine, Base
from models import Company, Account, Counterparty, Document, Posting

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tables created")
