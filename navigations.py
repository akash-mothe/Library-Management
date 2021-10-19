from tkinter import *
from PIL import Image, ImageTk


win = Tk()
win.title("Login Window")
win.geometry("1000x570")

#################FUNCTIONS##############


load = Image.open("Images/books.jpg")
load = load.resize((1000, 570), Image.ANTIALIAS)
book_img = ImageTk.PhotoImage(load)
book_img_lbl = Label(win,image=book_img,bg='#251B1B')
book_img_lbl.image = book_img
book_img_lbl.place(x=0,y=0)

nav_lbl = Label(win,text="Navigations",font="forte 65 bold",fg="#2E04FF",bg="white")
nav_lbl.place(x=5,y=200)

stud_reg_btn = Button(win,text="Register Students",font="cambria 16 bold",bg="#FF0471",fg="white")
stud_reg_btn.place(x=750,y=80,width=220,height=40)

manage_books_btn = Button(win,text="Manage Books",font="cambria 16 bold",bg="#FF0471",fg="white")
manage_books_btn.place(x=750,y=166,width=220,height=40)

rent_books_btn = Button(win,text="Rent Books",font="cambria 16 bold",bg="#FF0471",fg="white")
rent_books_btn.place(x=750,y=260,width=220,height=40)

books_borrowed_btn = Button(win,text="Books Borrowed",font="cambria 16 bold",bg="#FF0471",fg="white")
books_borrowed_btn.place(x=750,y=360,width=220,height=40)


win.mainloop()