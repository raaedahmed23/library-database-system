#!/usr/bin/python3
from schema import * 
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

db_url = "mysql://root:raahm2304@localhost/library"
engine = create_engine(db_url)

Session = sessionmaker(engine)
session = Session()

fileObj = open('books.csv', 'r', encoding="utf-8")
text_file = list(fileObj)
author_id = 0
author_list = {}

for line in text_file[1:]:
    line = line.strip()
    column_list = line.split('\t')

    isbn13 = column_list[1]
    title = column_list[2]
    title = title.replace("&amp;", "&")
    authors = column_list[3]

    # print("INSERT INTO Books VALUES (\"" + isbn13 + "\",\"" + title + "\");")
    new_book = Book(isbn=isbn13, title=title)
    session.add(new_book)

    authors = authors.split(',')
    for author in authors:
        if (author in author_list):
            # Deal with duplicate author
            pass
            # Lookup existing author_id and populate author_id variable
        else:
            # Add author to list
            author_id += 1
            author_list[author] = author_id
            # Be sure to look up existing author if applicable
    
            # print("INSERT INTO Authors VALUES (\"" + str(author_id) + "\",\"" + author + "\");")
            id = author_list[author]
            new_author = Authors(author_id=id, name=author)
            session.add(new_author)

        # print("INSERT INTO Book_authors VALUES (\"" + str(author_id) + "\",\"" + isbn13 + "\");")
        new_ba = Book_Authors(author_id=author_list[author], isbn=isbn13)
        session.add(new_ba)
        try:
            session.commit()
        except IntegrityError as e:
            print(e)
            session.rollback()


session.close()

fileObj.close()
