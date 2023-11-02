from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, Date, Float, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import timedelta

Base = declarative_base()

class Book(Base):
    __tablename__ = "BOOKS"

    isbn = Column("isbn", String(13), primary_key=True)
    title = Column("title", String(255))

    def __init__(self, isbn, title):
        self.isbn = isbn
        self.title = title


class Book_Authors(Base):
    __tablename__ = "BOOK_AUTHORS"

    author_id = Column(Integer, ForeignKey("AUTHORS.author_id"), primary_key=True)
    isbn = Column(String(13), ForeignKey("BOOKS.isbn"), primary_key=True)

    def __init__(self, author_id, isbn):
        self.author_id = author_id
        self.isbn = isbn


class Authors(Base):
    __tablename__ = "AUTHORS"

    author_id = Column(Integer, primary_key=True)
    name = Column(String(100))

    def __init__(self, author_id, name):
        self.author_id = author_id
        self.name = name


class Borrower(Base):
    __tablename__  = "BORROWER"

    card_id = Column(String(8), primary_key=True, nullable=False)
    ssn = Column(String(11), nullable=False, unique=True)
    bname = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    phone = Column(String(15))

    def __init__(self, card_id, ssn, bname, address, phone):
        self.card_id = card_id
        self.ssn = ssn
        self.bname = bname
        self.address = address
        self.phone = phone

class Book_Loans(Base):
    __tablename__ = "BOOK_LOANS"

    loan_id = Column(Integer, primary_key=True)
    isbn = Column(String(13), ForeignKey("BOOKS.isbn"))
    card_id = Column(String(8), ForeignKey("BORROWER.card_id"))
    date_out = Column(Date)
    due_date = Column(Date)
    date_in = Column(Date)

    def __init__(self, loan_id, isbn, card_id, date_out, due_date):
        self.loan_id = loan_id
        self.isbn = isbn
        self.card_id = card_id 
        self.date_out = date_out
        self.due_date = due_date

class Fines(Base):
    __tablename__ = "FINES"

    loan_id = Column(Integer, ForeignKey("BOOK_LOANS.loan_id"), primary_key=True)
    fine_amt = Column(Float)
    paid = Column(Boolean)

    def __init__(self, loan_id, fine_amt, paid):
        self.loan_id = loan_id
        self.fine_amt = fine_amt
        self.paid = paid

db_url = "mysql://root:raahm2304@localhost/library"
engine = create_engine(db_url)

Base.metadata.create_all(engine)
