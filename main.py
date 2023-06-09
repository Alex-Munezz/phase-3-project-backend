from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import Users, Books, Purchases, Reviews, Base
from typing import Optional, List
import uvicorn

app = FastAPI()
origins = [
    "http://127.0.0.1:8000",
]
  

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = create_engine("sqlite:///books.db", echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email_address: str
    phone_number: int
    gender: str
    age: int

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str]

class UserInDB(UserBase):
    id: int

    class Config:
        orm_mode = True

class BookBase(BaseModel):
    title: str
    author: str
    description: str
    year:int
    publisher:str
    quantity:int
    pages:int
    price:int
    cover: str

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class BookInDB(BookBase):
    id: int

    class Config:
        orm_mode = True

class PurchaseBase(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email_address: str
    phone_number: int
    gender: str
    age: int

class PurchaseCreate(PurchaseBase):
    pass

class PurchaseInDB(PurchaseBase):
    id: int

    class Config:
        orm_mode = True

class ReviewBase(BaseModel):
    book_id: int
    first_name: str
    last_name: str
    email_address: str
    phone_number: int
    gender: str
    age: int

class ReviewCreate(ReviewBase):
    pass

class ReviewInDB(ReviewBase):
    id: int

    class Config:
        orm_mode = True

@app.post("/users/", response_model=UserInDB)
def create_user(user: UserCreate):
    db_user = Users(
        first_name=user.first_name,
        last_name=user.last_name,
        email_address=user.email_address,
        phone_number=user.phone_number,
        gender=user.gender,
        age=user.age,
        password=user.password,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[UserInDB])
def get_all_users():
    users = session.query(Users).all()
    return users   

@app.get("/users/{user_id}", response_model=UserInDB)
def read_user(user_id: int):
    db_user = session.query(Users).filter(Users.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=UserInDB)
def update_user(user_id: int, user: UserUpdate):
    db_user = session.query(Users).filter(Users.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for attr, value in user.dict(exclude_unset=True).items():
        setattr(db_user, attr, value)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    db_user = session.query(Users).filter(Users.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(db_user)
    session.commit()
    return {"message": "User deleted"}

@app.get("/books/", response_model=List[BookInDB])
def get_all_books():
    books = session.query(Books).all()
    return books


@app.post("/books/", response_model=BookInDB)
def create_book(book: BookCreate):
    db_book = Books(
        title=book.title,
        author=book.author,
        publisher=book.publisher,
        year=book.year,
        description=book.description,
        pages=book.pages,
        cover=book.cover,
        price=book.price,
        quantity=book.quantity
    )
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

@app.get("/books/{book_id}", response_model=BookInDB)
def read_book(book_id: int):
    db_book = session.query(Books).filter(Books.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.put("/books/{book_id}", response_model=BookInDB)
def update_book(book_id: int, book: BookUpdate):
    db_book = session.query(Books).filter(Books.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    for attr, value in book.dict(exclude_unset=True).items():
        setattr(db_book, attr, value)
    session.commit()
    session.refresh(db_book)
    return db_book

@app.delete("/deletebooks/{book_id}")
def delete_book(book_id: int):
    db_book = session.query(Books).filter(Books.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(db_book)
    session.commit()
    return {"message": "Book deleted"}

@app.get("/purchasess/", response_model=List[PurchaseInDB])
def get_all_purchases():
    Purhases = session.query(Purchases).all()
    return Purchases   

@app.post("/purchases/", response_model=PurchaseInDB)
def create_purchase(purchase: PurchaseCreate):
    db_purchase = Purchases(
        user_id=purchase.user_id,
        first_name=purchase.first_name,
        last_name=purchase.last_name,
        email_address=purchase.email_address,
        phone_number=purchase.phone_number,
        gender=purchase.gender,
        age=purchase.age,
    )
    session.add(db_purchase)
    session.commit()
    session.refresh(db_purchase)
    return db_purchase

@app.get("/purchases/{purchase_id}", response_model=PurchaseInDB)
def read_purchase(purchase_id: int):
    db_purchase = session.query(Purchases).filter(Purchases.id == purchase_id).first()
    if db_purchase is None:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return db_purchase

@app.put("/purchases/{purchase_id}", response_model=PurchaseInDB)
def update_purchase(purchase_id: int, purchase: PurchaseCreate):
    db_purchase = session.query(Purchases).filter(Purchases.id == purchase_id).first()
    if db_purchase is None:
        raise HTTPException(status_code=404, detail="Purchase not found")
    for attr, value in purchase.dict(exclude_unset=True).items():
        setattr(db_purchase, attr, value)
    session.commit()
    session.refresh(db_purchase)
    return db_purchase

@app.delete("/purchases/{purchase_id}")
def delete_purchase(purchase_id: int):
    db_purchase = session.query(Purchases).filter(Purchases.id == purchase_id).first()
    if db_purchase is None:
        raise HTTPException(status_code=404, detail="Purchase not found")
    session.delete(db_purchase)
    session.commit()
    return {"message": "Purchase deleted"}

@app.get("/reviews/", response_model=List[ReviewInDB])
def get_all_reviews():
    reviews = session.query(Reviews).all()
    return reviews    

@app.post("/reviews/", response_model=ReviewInDB)
def create_review(review: ReviewCreate):
    db_review = Reviews(
        book_id=review.book_id,
        first_name=review.first_name,
        last_name=review.last_name,
        email_address=review.email_address,
        phone_number=review.phone_number,
        gender=review.gender,
        age=review.age,
    )
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review

@app.get("/reviews/{review_id}", response_model=ReviewInDB)
def read_review(review_id: int):
    db_review = session.query(Reviews).filter(Reviews.id == review_id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review

@app.put("/reviews/{review_id}", response_model=ReviewInDB)
def update_review(review_id: int, review: ReviewCreate):
    db_review = session.query(Reviews).filter(Reviews.id == review_id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    for attr, value in review.dict(exclude_unset=True).items():
        setattr(db_review, attr, value)
    session.commit()
    session.refresh(db_review)
    return db_review

@app.delete("/reviews/{review_id}")
def delete_review(review_id: int):
    db_review = session.query(Reviews).filter(Reviews.id == review_id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    session.delete(db_review)
    session.commit()
    return {"message": "Review deleted"}
