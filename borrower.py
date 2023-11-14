from main import * 
from schema import *

from tkinter import *
from tkinter import messagebox

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func

db_url = "mysql://root:raahm2304@localhost/library"
engine = create_engine(db_url)

Session = sessionmaker(engine)

class AddBorrower:
    def __init__(self, master):
        self.parent = master

        self.titleLabel = Label(self.parent, text="Please Enter Details")
        self.titleLabel.grid(row=0, column=0, padx=20, pady=20)

        self.nameLabel = Label(self.parent, text="Full Name").grid(row=1, column=0, padx=10, pady=5)
        self.nameTB = Entry(self.parent)
        self.nameTB.grid(row=2, column=0, padx=10, pady=5)

        self.ssnLabel = Label(self.parent, text="SSN xxx-xx-xxxx").grid(row=3, column=0, padx=10, pady=5)
        self.ssnTB = Entry(self.parent)
        self.ssnTB.grid(row=4, column=0, padx=10, pady=5)

        self.addressLabel = Label(self.parent, text="Street Address").grid(row=5, column=0, padx=10, pady=5)
        self.addressTB = Entry(self.parent)
        self.addressTB.grid(row=6, column=0, padx=10, pady=5)

        self.cityLabel = Label(self.parent, text="City").grid(row=7, column=0, padx=10, pady=5)
        self.cityTB = Entry(self.parent)
        self.cityTB.grid(row=8, column=0, padx=10, pady=5)

        self.stateLabel = Label(self.parent, text="State").grid(row=9, column=0, padx=10, pady=5)
        self.stateTB = Entry(self.parent)
        self.stateTB.grid(row=10, column=0, padx=10, pady=5)

        self.numberLabel = Label(self.parent, text="Phone Number (xxx) xxx-xxxx").grid(row=11, column=0, padx=10, pady=5)
        self.numberTB = Entry(self.parent)
        self.numberTB.grid(row=12, column=0, padx=10, pady=5)

        self.addBtn = Button(self.parent, text="Add", command=self.add_borrower)
        self.addBtn.grid(row=13, column=0, padx=10, pady=5)

    def add_borrower(self):
        ssn = self.ssnTB.get()

        if len(self.ssnTB.get()) == 0 or len(self.cityTB.get()) == 0 or len(self.nameTB.get()) == 0 or len(self.addressTB.get()) == 0 or len(self.stateTB.get()) == 0:
            messagebox.showwarning(message="Error: SSN, Name and Address must be specified")
            return None

        session = Session()
        is_present = session.query(Borrower).filter(Borrower.ssn == ssn).count() > 0
        if is_present:
            messagebox.showwarning(message="Borrower already exists in database")
            return None
        
        str_id = session.query(func.max(Borrower.card_id)).scalar() 
        new_num = int(str_id[2:]) + 1
        id = f"ID{new_num:06d}"
        address = ', '.join([self.addressTB.get(), self.cityTB.get(), self.stateTB.get()])
        phone_num = None

        if len(self.numberTB.get()) > 0:
            phone_num = self.numberTB.get()
            
        new_borrower = Borrower(card_id=id, ssn=ssn, bname=self.nameTB.get(), address= address, phone=phone_num)
        # session.add(new_borrower)
        # session.commit()
        session.close()

        messagebox.showinfo(message="Borrower added successfully!")
        self.parent.destroy()







        