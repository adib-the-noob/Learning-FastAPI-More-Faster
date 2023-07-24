from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()


class MyBook:
    def __init__(self, id, title, author, year, rating):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.rating = rating


BOOKS = [
    MyBook(1, 'The Great Gatsby', 'F. Scott Fitzgerald', 1925, 4.5),
    MyBook(2, 'The DaVinci Code', 'Dan Brown', 2003, 4.2),
    MyBook(3, 'Angels & Demons', 'Dan Brown', 2000, 4.0),
    MyBook(4, 'The Lost Symbol', 'Dan Brown', 2009, 3.7),
    MyBook(5, 'Old Man\'s War', 'John Scalzi', 2005, 4.1),
    MyBook(6, 'The Lock Artist', 'Steve Hamilton', 2010, 4.0),
    MyBook(7, 'HTML5', 'Remy Sharp', 2010, 4.3),
    MyBook(8, 'Right Ho Jeeves', 'P.D. Woodhouse', 1934, 4.2),
    MyBook(9, 'The Code of the Wooster', 'P.D. Woodhouse', 1938, 4.7),
    MyBook(10, 'Thank You Jeeves', 'P.D. Woodhouse', 1934, 4.2),
    MyBook(11, 'The DaVinci Code', 'Dan Brown', 2003, 4.2),
]


class Book(BaseModel):
    # add id field optional
    id: Optional[int] = Field(title="ID", description="ID of the book")
    title: str = Field(min_length=1, max_length=50) 
    author: str = Field(min_length=1, max_length=50)
    year: int
    rating: float = Field(gt=0, le=5)

    class Config:
        json_schema_extra = {
            'example': {
                'id': 1,
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'year': 1925,
                'rating': 4.5
            }
        }


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/books")
async def create_book(book: Book):
    book1 = MyBook(book.id, book.title, book.author, book.year, book.rating)
    BOOKS.append(find_book_by_id(book1))


def find_book_by_id(book : Book):
    if len(BOOKS) > 1 :
        book.id = BOOKS[:-1].id + 1
    # else:
        # book.id = 1
    return book

@app.get("/books")
async def get_books():
    return BOOKS

@app.get("/get-book/{book_id}")
async def get_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book
    return {"message": "Book not found"}

@app.get("/get-books-by-rating/{rating}")
async def get_books_by_rating(rating: float):
    books = []
    for book in BOOKS:
        if book.rating == rating:
            books.append(book)
    return books


@app.put("/update-book/{book_id}")
async def update_book(book_id: int, book: Book):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS[i] = book
            return {"message": "Book updated successfully"}
        

@app.delete("/delete-book/{book_id}")
async def delete_book(book_id: int):
    for i in BOOKS:
        if i.id == book_id:
            BOOKS.remove(i)
            return {"message": "Book deleted successfully"}