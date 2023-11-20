from tkinter import *
from tkinter import messagebox, simpledialog
from tkinter.ttk import Treeview

from schema import *
from pay_fine import *
from borrower import * 
from checkin import *
from main import today_date

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func

from datetime import timedelta

db_url = "mysql://root:raahm2304@localhost/library"
engine = create_engine(db_url)

Session = sessionmaker(engine)

class MainPage():
    def __init__(self, master):
        
        self.parent = master
        # Configure and pack widgets specific to the main page
        self.parent.title("Library Management System")
        self.frame = Frame(self.parent, width=1100, height=550)
        self.frame.grid(row=0, column=0)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_propagate(False)

        # Parameter Initialization
        self.search_string = None
        self.data = None
        self.borrowerId = None
        self.bookForCheckOutIsbn = None

        # Frame for the welcome message and header
        self.HeaderFrame = Frame(self.frame)
        self.HeaderFrame.grid(row=0, column=0, sticky='n')
        self.HeaderFrame.grid_rowconfigure(0, weight=1)
        self.HeaderFrame.grid_columnconfigure(0, weight=1)
        
        # # Label for the welcome message
        self.HeaderLabel = Label(self.HeaderFrame, text='What Book Do You Want?', font="Helvetica")
        self.HeaderLabel.grid(row=0, column=0)
        self.HeaderLabel.grid_rowconfigure(0, weight=10)
        self.HeaderLabel.grid_columnconfigure(0, weight=10)
        
        #Label for the searchbox
        self.SearchLabel = Label(self.HeaderFrame, text='')
        self.SearchLabel.grid(row=1, column=0)
        self.SearchLabel.grid_rowconfigure(1, weight=10)
        self.SearchLabel.grid_columnconfigure(0, weight=10)

        # Search Frame
        self.SearchFrame = Frame(self.frame)
        self.SearchFrame.grid(row=1, column=0, sticky='n')
        self.SearchFrame.grid_rowconfigure(1, weight=1)
        # self.SearchFrame.grid_columnconfigure(0, weight=1)
        self.SearchLabel = Label(self.SearchFrame, text='Search')
        self.SearchLabel.grid(row=0, column=0)
        self.SearchLabel.grid_rowconfigure(0, weight=1)
        # self.SearchLabel.grid_columnconfigure(0, weight=1)
        self.SearchTextBox = Entry(self.SearchFrame, fg='white', width=70)
        self.SearchTextBox.grid(row=1, column=0)
        self.SearchTextBox.grid_rowconfigure(1, weight=1)
        self.SearchButton = Button(self.SearchFrame, text='Search', command=self.search)
        self.SearchButton.grid(row=2, column=0)
        self.SearchButton.grid_rowconfigure(2, weight=1)

        # Search Result Frame
        self.ActiveArea = Frame(self.frame)
        self.ActiveArea.grid(row=2, column=0, sticky='n')
        self.ActiveArea.grid_rowconfigure(2, weight=1)
        self.ResultTreeview = Treeview(self.ActiveArea, columns=["ISBN", "Book Title", "Author(s)", "Availability"])
        self.ResultTreeview.grid(row=1, column=1)
        self.ResultTreeview.grid_rowconfigure(0, weight=1)
        self.ResultTreeview.heading('#0', text="ISBN")
        self.ResultTreeview.heading('#1', text="Book Title")
        self.ResultTreeview.heading('#2', text="Author(s)")
        self.ResultTreeview.heading('#3', text="Availability")
        self.ResultTreeview.bind('<ButtonRelease-1>', self.select_book_for_checkout)

        # Interaction Frame
        self.MajorFunctions = Frame(self.frame)
        self.MajorFunctions.grid(row=3, column=0, sticky='n')
        self.MajorFunctions.grid_rowconfigure(3, weight=1)
        self.checkOutBtn = Button(self.MajorFunctions, text="Check Out Book", command=self.check_out)
        self.checkOutBtn.grid(row=0, column=0, padx=10, pady=10)
        self.checkOutBtn.grid_rowconfigure(0, weight=1)
        self.checkOutBtn.grid_columnconfigure(0, weight=1)
        self.checkInBtn = Button(self.MajorFunctions, text="Check In Book", command=self.check_in)
        self.checkInBtn.grid(row=0, column=1, padx=10, pady=10)
        self.checkOutBtn.grid_rowconfigure(0, weight=1)
        self.checkOutBtn.grid_columnconfigure(1, weight=1)
        self.updateFinesBtn = Button(self.MajorFunctions, text="Updates Fines", command=self.update_fines)
        self.updateFinesBtn.grid(row=1, column=0, padx=10, pady=10)
        self.payFinesBtn = Button(self.MajorFunctions, text="Pay Fines", command=self.pay_fines)
        self.payFinesBtn.grid(row=1, column=1, padx=10, pady=10)
        self.changeDayBtn = Button(self.MajorFunctions, text="Change Day", command=self.change_day)
        self.changeDayBtn.grid(row=1, column=2, padx=10, pady=10)
        self.addBorrowerBtn = Button(self.MajorFunctions, text="Add New Borrower", command=self.add_borrower)
        self.addBorrowerBtn.grid(row=0, column=2, padx=10, pady=10)

    def search(self):
        session = Session()
        self.search_string = self.SearchTextBox.get()
        self.data = session.query(Book.isbn, Book.title, Authors.name)\
            .join(Book_Authors, Book_Authors.isbn == Book.isbn).join(Authors, Authors.author_id == Book_Authors.author_id)\
            .filter(
                (Book.isbn.ilike(f"%{self.search_string}%")) |
                (Book.title.ilike(f"%{self.search_string}%")) |
                (Authors.name.ilike(f"%{self.search_string}%"))
            ).all()

        session.close()
        self.view_results()

    def view_results(self):
        self.ResultTreeview.delete(*self.ResultTreeview.get_children())

        session = Session()
        # Checking for availability of each book before displaying in result
        for res in self.data:
            isbn_to_check = res[0]
            is_present = session.query(Book_Loans.isbn).filter(Book_Loans.isbn == isbn_to_check).count() > 0
            if not is_present:
                availability = "Available"
            else:
                loan_record = session.query(Book_Loans.date_in).filter(Book_Loans.isbn == isbn_to_check).order_by(Book_Loans.date_out).all()
                
                if loan_record[-1][0] is None:
                    availability = "Not Available"
                else:
                    availability = "Available"

            self.ResultTreeview.insert('', 'end', text=str(res[0]),
                                       values=(res[1], res[2], availability))
        
        session.close()

    
    def select_book_for_checkout(self, _):
        selected_item = self.ResultTreeview.focus()
        self.bookForCheckOutIsbn = self.ResultTreeview.item(selected_item)['text']

    def check_out(self):
        if self.bookForCheckOutIsbn is None or len(self.bookForCheckOutIsbn) == 0:
            messagebox.showwarning(title="Attention!", message="Please select a book to check out.")
            return None
        
        self.borrowerId = simpledialog.askstring("Check Out Book", "Enter Borrower ID")

        session = Session()

        is_present = session.query(Borrower.card_id).filter(Borrower.card_id == self.borrowerId).count() > 0
        if not is_present:
            messagebox.showwarning(message="Borrower not in database.")
            session.close()
            return None

        all_loans = session.query(Book_Loans.date_in).filter(Book_Loans.card_id == self.borrowerId).all()
        active_loans = [loan[0] for loan in all_loans].count(None)
        if active_loans >= 3:
            messagebox.showwarning(message="Error: The borrower has 3 active loans")
            session.close()
            return None

        id = session.query(func.max(Book_Loans.loan_id)).scalar() + 1 
        new_loan = Book_Loans(loan_id=id, isbn=self.bookForCheckOutIsbn, card_id=self.borrowerId, date_out=today_date, due_date= today_date + timedelta(days=14))
        session.add(new_loan)
        new_fine = Fines(loan_id=id, fine_amt=0.0, paid=False)
        session.add(new_fine)

        session.commit()
        session.close()

        messagebox.showinfo(message="Book loaned out successfully!")


    def check_in(self):
        self.checkInWindow = Toplevel(self.parent)
        self.app = CheckIn(self.checkInWindow)

    def update_fines(self):
        session = Session()
        result = session.query(Book_Loans.loan_id, Book_Loans.due_date, Book_Loans.date_in).all()

        for res in result:
            due_date = res[1]
            date_in = res[2]

            if date_in is None:
                date_in = today_date

            diff = date_in - due_date
   
            if diff.days > 0:
                fine = int(diff.days) * 0.25
                row_to_update = session.query(Fines).filter(Fines.loan_id == res[0]).all()
                for row in row_to_update:
                    row.fine_amt = fine
            
            session.commit()

        messagebox.showinfo(message=f"Fines updates for today's date: {today_date}")


    def pay_fines(self):
        self.PayFineWindow = Toplevel(self.parent)
        self.fine_app = PayFine(self.PayFineWindow)

    def change_day(self):
        global today_date
        today_date += timedelta(days=1)
        messagebox.showinfo(message=f"Today's date is now: {today_date}")

    def add_borrower(self):
        self.AddBorrowerWindow = Toplevel(self.parent)
        self.borrow_app = AddBorrower(self.AddBorrowerWindow)