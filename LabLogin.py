from tkinter import *
from PIL import Image, ImageTk
import mysql.connector as sql
import webbrowser
from tkinter import ttk


win = Tk()
win.title("Login Window")
# win.geometry("{0}x{1}+0+0".format(win.winfo_screenwidth(), win.winfo_screenheight()))
win.geometry("1000x500")
# win.configure(bg='#610303')


# @@@@@@@@@@@@@@@All FUNCTIONS@@@@@@@@@@@


def books_manage():
    win = Toplevel()
    
def login():
    con = sql.connect(host='localhost', user='root', password='wadgaonmali')
    cursor = con.cursor()
    cursor.execute("use LabManagement")
    cursor.execute("SELECT * FROM member_login")
    result = cursor.fetchall()
    path = "F:/Programming/python/projects/LibraryManagement/navitions.py"
    for row in result:
        if user_entry_var.get() == row[0] and pass_entry_var.get() == row[1]:
            books_manage()
        else:
            print("Failed")


# ALLL VARIABLES@@@@@@@@@@
user_entry_var = StringVar()
pass_entry_var = StringVar()


# load = Image.open("Images/books1.png")
# load = load.resize((330, 400), Image.ANTIALIAS)
# book_img = ImageTk.PhotoImage(load)
# book_img_lbl = Label(win, image=book_img, bg='#610303')
# book_img_lbl.image = book_img
# book_img_lbl.place(x=10, y=50)

load2 = Image.open("Images/door.jpg")
load2 = load2.resize((1000, 500), Image.ANTIALIAS)
book_img = ImageTk.PhotoImage(load2)
book_img_lbl = Label(win, image=book_img, bg='#610303')
book_img_lbl.image = book_img
book_img_lbl.place(x=0, y=0)

login_lbl = Label(win, text="Member Login...",
                  font="forte 32", fg="#00FF80")
login_lbl.place(x=400, y=60)
login_lbl['bg'] = login_lbl.master['bg']

user_lbl = Label(win, text="Username: ", font="arial 20 bold",
                 bg="#610303", fg="white")
user_lbl.place(x=450, y=140)

user_entry = Entry(win, font="arial 16 bold", bg="#3C0A0A",
                   fg="white", textvariable=user_entry_var)
user_entry.focus_set()
user_entry.place(x=450, y=190, width=390, height=25)

pass_lbl = Label(win, text="Password: ", font="arial 20 bold",
                 bg="#610303", fg="white")
pass_lbl.place(x=450, y=240)

pass_entry = Entry(win, font="arial 16 bold", bg="#3C0A0A",
                   fg="white", textvariable=pass_entry_var)
pass_entry.place(x=450, y=290, width=390, height=25)

load1 = Image.open("Images/login_btn.png")
load1 = load1.resize((150, 60), Image.ANTIALIAS)
login_btn_img = ImageTk.PhotoImage(load1)
login_btn = Button(win, image=login_btn_img, bg="#610303", bd=0, command=login)
login_btn.image = login_btn_img
login_btn.place(x=570, y=390)

# load2 = Image.open("Images/reset_btn.png")
# load2 = load2.resize((130, 60), Image.ANTIALIAS)
# reset_btn_img = ImageTk.PhotoImage(load2)
# reset_btn = Button(win,image=reset_btn_img,bg="#610303",bd=0)
# reset_btn.image = reset_btn_img
# reset_btn.place(x=650,y=360)


win.mainloop()
