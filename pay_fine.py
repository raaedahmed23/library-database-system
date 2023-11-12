from main import * 
from schema import *

from tkinter import * 
from tkinter import messagebox

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url = "mysql://root:raahm2304@localhost/library"
engine = create_engine(db_url)

Session = sessionmaker(engine)

class PayFine:
    def __init__(self, master):
        self.parent = master

        self.fine_amt = StringVar()

        self.borrowerLabel = Label(self.parent, text="Enter Borrower ID").grid(row=0, column=0, padx=20, pady=20)
        self.borrowerEntry = Entry(self.parent)
        self.borrowerEntry.grid(row=1, column=0, padx=20, pady=20)
        self.showFineBtn = Button(self.parent, text="Show Fines", command=self.show_fines).grid(row=2, column=0, padx=20, pady=20)
        self.fineLabel = Label(self.parent, textvariable=self.fine_amt)
        self.fineLabel.grid(row=3, column=0, padx=20, pady=20)
        self.payFineBtn = Button(self.parent, text="Pay Complete Fine", command=self.pay_fine).grid(row=4, column=0, padx=20, pady=20)


    def show_fines(self):
        borrower_id = self.borrowerEntry.get()
        total_fine = 0

        session = Session()
        is_present = session.query(Borrower.card_id).filter(Borrower.card_id == borrower_id).count() > 0 
        if not is_present:
            messagebox.showwarning(message="Borrower does not exist in database. Make sure card ID is correct.")
            return None
        
        result = session.query(Fines.fine_amt, Fines.paid)\
            .join(Book_Loans, Book_Loans.loan_id == Fines.loan_id)\
            .filter(Book_Loans.card_id == borrower_id).all()
        
        session.close() 

        for res in result:
            if res[1] is False:
                total_fine += float(res[0])

        self.fine_amt.set(f"Unpaid Fine: ${total_fine}")


    def pay_fine(self):
        borrower_id = self.borrowerEntry.get()

        session = Session()
        is_present = session.query(Borrower.card_id).filter(Borrower.card_id == borrower_id).count() > 0 
        if not is_present:
            messagebox.showwarning(message="Borrower does not exist in database. Make sure card ID is correct.")
            return None

        # Setting Fines.paid to True
        result = session.query(Fines)\
            .join(Book_Loans, Book_Loans.loan_id == Fines.loan_id)\
            .filter(Book_Loans.card_id == borrower_id).all()
        
        for res in result:
            res.paid = 1
        
        session.commit()
        messagebox.showinfo(message="Fine Paid Successfully!")
        self.parent.destroy()


        
        



