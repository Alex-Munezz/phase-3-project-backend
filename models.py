from sqlalchemy import Column, Integer, String, Table, create_engine, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, backref

Base = declarative_base()

books_user = Table(
    'books_user ',
    Base.metadata,
    Column('book_id',Integer, ForeignKey('books.id'), primary_key=True),
    Column('user_id',Integer, ForeignKey('users.id'), primary_key=True),
    extend_existing=True,
)

class Books(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(), nullable=False)
    author = Column(String(), nullable=False)
    price = Column(Integer(), nullable=False)
    quantity = Column(Integer(), nullable=False)
    publisher = Column(String(), nullable=False)
    pages = Column(Integer(), nullable=False)
    year = Column(Integer(), nullable=False)
    cover = Column(String(), nullable=False)
    description = Column(String(), nullable=False)
    # users = relationship('Users', backref='books', foreign_keys=[user_id])
 

    def __repr__(self):
        return f"{self.id}, {self.title}" 

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(), nullable=False)
    last_name = Column(String(), nullable=False)
    email_address = Column(String(), nullable=False)
    phone_number = Column(Integer, nullable=False)
    gender = Column(String(), nullable=False)
    age = Column(Integer, nullable=False)
    password = Column(Integer, nullable= False)
    # users = relationship('Users', backref='reviews', foreign_keys=[user_id])

    def __repr__(self):
        return f"{self.id}, {self.first_name, self.last_name}"

class Purchases(Base):
    __tablename__ = 'purchases'
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String(), nullable=False)
    last_name = Column(String(), nullable=False)
    email_address = Column(String(), nullable=False)
    phone_number = Column(Integer, nullable=False)
    gender = Column(String(), nullable=False)
    age = Column(Integer, nullable=False)
    # users = relationship('Users', backref='purchases', foreign_keys=[user_id])
    
class Reviews(Base):
    __tablename__ = 'reviews'
    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
    first_name = Column(String(), nullable=False)
    last_name = Column(String(), nullable=False)
    email_address = Column(String(), nullable=False)
    phone_number = Column(Integer, nullable=False)
    gender = Column(String(), nullable=False)
    age = Column(Integer, nullable=False)
     
    def __repr__(self):
        return f"{self.name}"
    

engine = create_engine('sqlite:///books.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()