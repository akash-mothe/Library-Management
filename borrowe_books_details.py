from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import mysql.connector as sql
from tkinter import messagebox as msg
from datetime import date,datetime,timedelta

win = Tk()
win.title("Books borrowed student details")
win.geometry("{0}x{1}+0+0".format(win.winfo_screenwidth(), win.winfo_screenheight()))
win.configure(bg='#41231D')

#########################ALL VARIABLES############################
search_combo_var = StringVar()
search_entry_var = StringVar()
# entry_box_var = StringVar()
today1 = date.today().strftime("%d/%m/%Y")

def fetch_rows():
    try:
        con = sql.connect(host="localhost",user="root",password='wadgaonmali',database="labmanagement")
        cur = con.cursor()
            # cur.execute("use studentmanagement")
        cur.execute("select * from borrowed_book_details")
        rows = cur.fetchall()
        if len(rows)!=0:
            books_table.delete(*books_table.get_children())
            for row in rows:
                books_table.insert('',END,values=row)
            con.commit()
        con.close()
    except sql.Error:
        msg.showerror("Error","Something went wrong.\nPlease try again by giving correct inputs.")

def on_search_record():
    if (search_combo_var.get()!="") and (search_entry_var.get()!=""):
        con = sql.connect(host="localhost",user="root",password='wadgaonmali',database="labmanagement")
        cur = con.cursor()
        if (search_combo_var.get() == "Student Name"):
            cur.execute("select * from borrowed_book_details")
            record = cur.fetchall()
            books_table.delete(*books_table.get_children())
            a = 1
            for row in record:
                if (str(search_entry_var.get())==str(row[0])):
                    books_table.insert('',END,values=row)
                    a+=1
            if a==1:
                msg.showerror("Sorry","Record not found...!")
                fetch_rows()
        elif (search_combo_var.get() == "Book Title"):
            cur.execute("select * from borrowed_book_details")
            record = cur.fetchall()
            books_table.delete(*books_table.get_children())
            b = 1
            for row in record:
                if (str(search_entry_var.get())==str(row[2])):
                    books_table.insert('',END,values=row)
                    b+=1
            if b==1:
                msg.showerror("Sorry","Record not found...!")
                fetch_rows()
        elif (search_combo_var.get() == "Return Date"):
            cur.execute("select * from borrowed_book_details")
            record = cur.fetchall()
            books_table.delete(*books_table.get_children())
            c = 1
            for row in record:
                if (str(search_entry_var.get())==str(row[6])):
                    books_table.insert('',END,values=row)
                    c+=1
            if c==1:
                msg.showerror("Sorry","Record not found...!")
                fetch_rows()
        cur.close()
        con.close()
    else:
        msg.showwarning("Got Empty","Please select option and enter value.")


def todays_return():
    con = sql.connect(host="localhost",user="root",password='wadgaonmali',database="labmanagement")
    cur = con.cursor()
    cur.execute("select * from borrowed_book_details")
    records = cur.fetchall()
    records_list = []
    for row in records:
        if (str(row[6])==str(today1)):
            records_list.append(row)
            l = str(len(records_list))
            t = f"{l} Students have to return their book today."
            label = Label(detail_frame,text="Notification: ",font="cambria 17 bold",fg="White",bg="#41231D")
            label.place(x=886,y=75)
            label = Label(detail_frame,text=t,font="cambria 17 bold",fg="#FF4400",bg="#41231D")
            label.place(x=1025,y=77)
        else:
            pass
    cur.close()
    con.close()           
        

detail_frame = Frame(win,bd=5,relief="ridge",bg="#41231D")
detail_frame.place(x=0,y=0,width=1530,height=830)

head_lbl = Label(detail_frame,text="Books borrowed student details are below:",font="cambria 25 bold",fg="#F243EC",bg="#41231D")
head_lbl.place(x=3,y=0)

search_lbl = Label(detail_frame,text="Search By:",font="cambria 20 bold",fg="white",bg="#41231D")
search_lbl.place(x=3,y=67)

search_combo = ttk.Combobox(detail_frame,width=10,font="cambria 15 bold",state="readonly",textvariable=search_combo_var)
combostyle = ttk.Style()
combostyle.theme_create('combostyle4', parent='alt',
                         settings = {'TCombobox':
                                     {'configure':
                                      {'selectbackground': '#321111',
                                       'fieldbackground': '#321111',
                                       'background': '#4D00FF'
                                       }}}
                         )
combostyle.theme_use('combostyle4')
search_combo['values'] = ('Student Name','Book Title','Return Date')
search_combo.place(x=150,y=75,height=30)

search_entry = Entry(detail_frame,bd=5,font="cambria 13 bold",relief="groove",bg="#321111",fg="white",textvariable=search_entry_var)
search_entry.place(x=296,y=75,width=300,height=30)

load4 = Image.open("Images/search.png")
load4 = load4.resize((45, 40), Image.ANTIALIAS)
search_btn_img = ImageTk.PhotoImage(load4)
search_btn = Button(detail_frame,image=search_btn_img,font="cambria 12 bold",fg="white",bg="#41231D",bd=0,command=on_search_record)
search_btn.image = search_btn_img
search_btn.place(x=610,y=72)

# # show_btn = Button(detail_frame,text="Show All",width=9,font="cambria 12 bold",fg="white",bg="#FF2247")
# # show_btn.grid(row=0,column=4,sticky=W,padx=8,pady=10)

####################Table Frame##############################
table_frame = Frame(detail_frame,bd=2,relief="ridge",bg="#41231D")
table_frame.place(x=2,y=120,width=1530,height=700)

scroll_x = Scrollbar(table_frame,orient=HORIZONTAL)
scroll_y = Scrollbar(table_frame,orient=VERTICAL)
books_table = ttk.Treeview(table_frame,columns=("1","2","3","4","5","6","7"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
# style.configure("Treeview", fieldbackground="#41231D",font="arial 15 bold")
style11 = ttk.Style()
style11.configure("Treeview", background="#41231D",foreground="white", fieldbackground="#41231D", rowheight=30,font="arial 13 bold")
scroll_x.pack(side=BOTTOM,fill=X)
scroll_y.pack(side=RIGHT,fill=Y)
scroll_x.config(command=books_table.xview)
scroll_y.config(command=books_table.yview)
books_table.heading("1",text="Student Name")
books_table.heading("2",text="Student Contact")
books_table.heading("3",text="Book Title")
books_table.heading("4",text="Book Auther")
books_table.heading("5",text="Book Price")
books_table.heading("6",text="Borrowed Date")
books_table.heading("7",text="Return Date")
books_table['show'] = 'headings'
books_table.column("1",width=50)
books_table.column("2",width=125)
books_table.column("3",width=125)
books_table.column("4",width=125)
books_table.column("5",width=125)
books_table.column("6",width=125)
books_table.column("7",width=125)
books_table.pack(fill=BOTH,expand=1)
##########################################################
fetch_rows()
todays_return()

win.mainloop()