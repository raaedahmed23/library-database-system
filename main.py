import tkinter as tk
from search import *
from datetime import date
from ttkthemes import ThemedTk

today_date = date.today()

if __name__ == "__main__":
    # app = tk.Tk()
    app = ThemedTk()
    _ = MainPage(app)
    app.mainloop()
