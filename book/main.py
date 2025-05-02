from typing import List
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

# API Endpoints

# Register a Borrower
@app.post("/borrowers/")
def register_borrower(borrower: Borrower):
    if any(b.id == borrower.id for b in borrowers):
        raise HTTPException(status_code=400, detail="Borrower already registered")
    borrowers.append(borrower)
    return {"message": "Borrower registered successfully"}

# List All Books
@app.get("/books/", response_model=List[Book])
def list_books():
    return books

# Borrow a Book
@app.post("/borrowings/")
def borrow_book(book_id: int, borrower_id: int, librarian: bool):
    if not librarian:
        raise HTTPException(status_code=403, detail="Only librarian can authorize borrowing")
    
    book = next((b for b in books if b.id == book_id), None)
    if not book or not book.available:
        raise HTTPException(status_code=404, detail="Book not available")
    
    borrower = next((b for b in borrowers if b.id == borrower_id), None)
    if not borrower:
        raise HTTPException(status_code=404, detail="Borrower not found")
    
    return_date = datetime.now() + timedelta(days=14)  # 2 weeks to return
    borrowing = Borrowing(
        book_id=book_id,
        borrower_id=borrower_id,
        borrower_name=borrower.name,
        borrow_date=datetime.now(),
        return_date=return_date
    )
    borrowings.append(borrowing)
    book.available = False  # Mark book as borrowed
    return {"message": "Book borrowed successfully", "return_date": return_date}

# Return a Book
@app.post("/return/")
def return_book(book_id: int, borrower_id: int):
    borrowing = next((b for b in borrowings if b.book_id == book_id and b.borrower_id == borrower_id), None)
    if not borrowing:
        raise HTTPException(status_code=404, detail="Borrowing record not found")
    
    book = next((b for b in books if b.id == book_id), None)
    if book:
        book.available = True  # Mark book as available
    borrowings.remove(borrowing)  # Remove borrowing record
    return {"message": "Book returned successfully"}

# View Borrowed Books
@app.get("/borrowings/{borrower_id}", response_model=List[Borrowing])
def get_borrowed_books(borrower_id: int):
    borrowed_books = [b for b in borrowings if b.borrower_id == borrower_id]
    return borrowed_books 