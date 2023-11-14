from schema import * 
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

db_url = "mysql://root:raahm2304@localhost/library"
engine = create_engine(db_url)

Session = sessionmaker(engine)
session = Session()

fileObj = open('borrowers.csv', 'r', encoding="utf-8")
text_file = list(fileObj)

for line in text_file[1:]:
    row = line.strip().split(',')

    id = row[0]
    ssn = row[1]
    name = row[2] + " " + row[3]
    address = row[5] + ", " + row[6] + ", " + row[7]
    phone = row[8]

    new_borrower = Borrower(card_id=id, ssn=ssn, bname= name, address=address, phone=phone)
    session.add(new_borrower)
    session.commit()

session.close()