rom typing import List
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Data Models
class Book(BaseModel):
    id: int
    title: str
    author: str
    available: bool = True

class Borrower(BaseModel):
    id: int
    name: str
    registered: bool = True

class Borrowing(BaseModel):
    book_id: int
    borrower_id: int
    borrower_name: str
    borrow_date: datetime
    return_date: datetime

# In-memory storage
books = [Book(id=i, title=f"Book {i}", author=f"Author {i}") for i in range(1, 10)]
borrowers = []
borrowings = []
