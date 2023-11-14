from tkinter import * 
from tkinter import messagebox
from tkinter.ttk import Treeview

from schema import * 
from main import today_date

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func

db_url = "mysql://root:raahm2304@localhost/library"
engine = create_engine(db_url)

Session = sessionmaker(engine)

class CheckIn:
    def __init__(self, master):
        self.parent = master
        self.parent.title("Book Check-In")

        self.checkInBookID = None
        self.search_string = None
        self.data = None

        self.searchLabel = Label(self.parent, text="Search here: Borrower ID, Borrower Name or ISBN")
        self.searchLabel.grid(row=0, column=0, padx=20, pady=20)
        self.searchTextBox = Entry(self.parent)
        self.searchTextBox.grid(row=1, column=0)
        self.searchBtn = Button(self.parent, text="Search", command=self.search_book_loans)
        self.searchBtn.grid(row=2, column=0)
        self.table = Treeview(self.parent, columns=["Loan ID", "ISBN", "Borrower ID", "Title"])
        self.table.grid(row=3, column=0)
        self.table.heading('#0', text="Loan ID")
        self.table.heading('#1', text="ISBN")
        self.table.heading('#2', text="Borrower ID")
        self.table.heading('#3', text="Book Title")
        self.table.bind('<ButtonRelease-1>', self.select_book_for_checkin)
        self.checkInBtn = Button(self.parent, text="Check In", command=self.check_in)
        self.checkInBtn.grid(row=4, column=0)

    def select_book_for_checkin(self, _):
        selected_item = self.table.focus()
        self.checkInBookID = self.table.item(selected_item)['text']

    def search_book_loans(self):
        self.search_string = self.searchTextBox.get()
        session = Session()
        self.data = session.query(Book_Loans.loan_id, Book_Loans.isbn, Book_Loans.card_id, Book.title, Book_Loans.date_in)\
                        .join(Borrower, Borrower.card_id == Book_Loans.card_id).join(Book, Book.isbn == Book_Loans.isbn)\
                        .filter(
                            (Book.isbn.ilike(f"%{self.search_string}%")) |
                            (Borrower.bname.ilike(f"%{self.search_string}%")) |
                            (Book_Loans.card_id.ilike(f"%{self.search_string}%"))
                        )\
                        .all()

        session.close()
        self.view_data()

    def view_data(self):
        self.table.delete(*self.table.get_children())
        for elem in self.data:
            if elem[4] is None:
                self.table.insert('', 'end', text=str(elem[0]), values=(elem[1], elem[2], elem[3]))

    def check_in(self):
        if self.checkInBookID is None or len(self.checkInBookID) == 0:
            messagebox.showwarning(message="Warning: Please select a book to check-in")
            return None
        
        session = Session()
        result = session.query(Book_Loans).filter(Book_Loans.loan_id == self.checkInBookID).all()

        for res in result:
            res.date_in = today_date

        session.commit()
        messagebox.showinfo(message="Book checked in successfully!")

        session.close()
        return None

