from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import mysql.connector as sql
from tkinter import messagebox as msg

win = Tk()
win.title("Books Mangement")
win.geometry("{0}x{1}+0+0".format(win.winfo_screenwidth(), win.winfo_screenheight()))
win.configure(bg='#030314')

#########################ALL VARIABLES############################
# style = ttk.Style()
# style.theme_use("clam")
id_entry_var = StringVar()
title_entry_var = StringVar()
catagory_entry_var = StringVar()
auther_entry_var = StringVar()
publisher_entry_var = StringVar()
price_entry_var = StringVar()
copies_entry_var = StringVar()
search_combo_var = StringVar()
search_entry_var = StringVar()

###########ALL FUNCTIONS##############
def show_id():
    con=sql.connect(host='localhost',user='root',password='wadgaonmali')
    cur=con.cursor()
    cur.execute("use labmanagement")
    cur.execute("select * from book_details")
    result = cur.fetchall()
    new_id = str((result[-1][0])+1)
    return new_id
id_entry_var.set(show_id())

def on_add():
    # pass
    try:
        con=sql.connect(host='localhost',user='root',password='wadgaonmali')
        cur=con.cursor()
        cur.execute("use labmanagement")
        if (id_entry_var.get()!="") and (title_entry_var.get()!="") and (catagory_entry_var.get()!="") and (auther_entry_var.get()!="") and (publisher_entry_var.get()!="") and (price_entry_var.get()!="") and copies_entry_var.get():
            insert_query = """INSERT INTO book_details (book_id,title,catagory,Auther,publisher,price,copies) 
                                        VALUES (%s, %s, %s, %s, %s, %s, %s) """
            data = (int(id_entry_var.get()),title_entry_var.get(),catagory_entry_var.get(),auther_entry_var.get(),publisher_entry_var.get(),int(price_entry_var.get()),int(copies_entry_var.get()))
            cur.execute(insert_query,data)
            con.commit()
            cur.close()
            con.close()
            msg.showinfo("success",f"Record of book with ID:{id_entry_var.get()} has been added successfully.")
            fetch_data()
            on_reset()
            id_entry_var.set(show_id())

        else:
            msg.showwarning("warning","Please fill up all fields.")
    except ValueError as e:
        msg.showerror("Error","Please enter price and copies in integer format.")
    except sql.errors.IntegrityError:
        msg.showerror("Sorry","Got already registred ID.\nPlease click on reset button and try again.")
        # ans = msg.askyesno("?","Got already registred ID")

def fetch_data():
    con = sql.connect(host="localhost",user="root",password='wadgaonmali',database="labmanagement")
    cur = con.cursor()
        # cur.execute("use studentmanagement")
    cur.execute("select * from book_details")
    rows = cur.fetchall()
    if len(rows)!=0:
        book_table.delete(*book_table.get_children())
        for row in rows:
            book_table.insert('',END,values=row)
        con.commit()
    con.close()


def on_update():
    if (str(id_entry_var.get())!=show_id()):
        con = sql.connect(host="localhost",user="root",password='wadgaonmali',database="labmanagement")
        cur = con.cursor()
        cur.execute("UPDATE book_details set title = %s, catagory = %s, Auther = %s, publisher = %s, price = %s, copies = %s WHERE book_id = %s",(title_entry_var.get(), catagory_entry_var.get(), auther_entry_var.get(), publisher_entry_var.get(), int(price_entry_var.get()), int(copies_entry_var.get()), int(id_entry_var.get())))
        con.commit()
        con.close()
        msg.showinfo("Info",f"Record of book with ID:{id_entry_var.get()} has been updated successfully. ")
        fetch_data()
        on_reset()
    else:
        msg.showwarning("Warning","Given id is not registered.")


def on_delete():
    # pass
    if (str(id_entry_var.get())!=show_id()):
        ans = msg.askyesno("YesOrNo",f"Do you really want to delete book record of ID:{id_entry_var.get()}")
        if ans==True:
            con = sql.connect(host="localhost",user="root",password='wadgaonmali',database="labmanagement")
            cur = con.cursor()
            sql_query = '''delete from book_details where book_id = %s'''
            data = id_entry_var.get()
            cur.execute(sql_query,(data,))
            con.commit()
            con.close()
            msg.showinfo("Success",f"Book record of ID:{id_entry_var.get()} deleted successfully.")
            fetch_data()
        else:
            pass
    else:
        msg.showwarning("Warning","Given id is not registered.")

def on_reset():
    # pass
    id_entry_var.set(show_id())
    title_entry_var.set("")
    catagory_entry_var.set("")
    auther_entry_var.set("")
    publisher_entry_var.set("")
    price_entry_var.set("")
    copies_entry_var.set("")

def on_search():
    if (search_combo_var.get()!="") and (search_entry_var.get()!=""):
        con=sql.connect(host='localhost',user='root',password='wadgaonmali')
        cur=con.cursor()
        cur.execute("use labmanagement")
        cur.execute("select * from book_details")
        result = cur.fetchall()
        if (search_combo_var.get()=="Book Id"):
            for row in result:
                if (str(search_entry_var.get())==str(row[0])):
                    id_entry_var.set(row[0])
                    title_entry_var.set(row[1])
                    catagory_entry_var.set(row[2])
                    auther_entry_var.set(row[3])
                    publisher_entry_var.set(row[4])
                    price_entry_var.set(row[5])
                    copies_entry_var.set(row[6])
        elif (search_combo_var.get()=="Book Title"):
            for row in result:
                if (str(search_entry_var.get())==str(row[1])):
                    id_entry_var.set(row[0])
                    title_entry_var.set(row[1])
                    catagory_entry_var.set(row[2])
                    auther_entry_var.set(row[3])
                    publisher_entry_var.set(row[4])
                    price_entry_var.set(row[5])
                    copies_entry_var.set(row[6])
                # else:
                #     msg.showerror("Not found","Record not found!")
        con.close()
    else:
        msg.showwarning("Warning","Please fill both fields.")
        
    


head_frame = Label(win,text="Books Mangement",font="algerian 24 bold",fg="#3CFF00",bg="#090A33",bd=8,relief="groove")
head_frame.pack(side=TOP,fill=X)

# ********************MANAGE FRAME**********************
manage_frame = Frame(win,bd=8,relief="ridge",bg="#090A33")

mng_title = Label(manage_frame,text="Manage Books",font="elephant 24 underline",fg="#FF0077",bg="#090A33")
mng_title.grid(row=0,columnspan=2,ipadx=155,ipadyS=20)

id_lbl = Label(manage_frame,text="Book ID:",font="cambria 18 bold",fg="white",bg="#090A33")
id_lbl.grid(row=1,column=0,sticky=W,padx=10)
id_entry = Entry(manage_frame,width=14,font="cambria 13 bold",bg="#090A33",bd=0,fg="white",textvariable=id_entry_var)
id_entry.grid(row=1,column=1,sticky=W,pady=20)

title_lbl = Label(manage_frame,text="Book Title:",font="cambria 18 bold",fg="white",bg="#090A33")
title_lbl.grid(row=2,column=0,sticky=W,padx=10)
title_entry = Entry(manage_frame,width=35,font="cambria 13 bold",bg="#06144D",fg="white",textvariable=title_entry_var)
title_entry.grid(row=2,column=1,sticky=W,pady=20)

catagory_lbl = Label(manage_frame,text="Catagory:",font="cambria 18 bold",fg="white",bg="#090A33")
catagory_lbl.grid(row=3,column=0,sticky=W,padx=10)
catagory_entry = Entry(manage_frame,width=35,font="cambria 13 bold",bg="#06144D",fg="white",textvariable=catagory_entry_var)
catagory_entry.grid(row=3,column=1,sticky=W,pady=20)

auther_lbl = Label(manage_frame,text="Auther:",font="cambria 18 bold",fg="white",bg="#090A33")
auther_lbl.grid(row=4,column=0,sticky=W,padx=10)
auther_entry = Entry(manage_frame,width=35,font="cambria 13 bold",bg="#06144D",fg="white",textvariable=auther_entry_var)
auther_entry.grid(row=4,column=1,sticky=W,pady=20)

publisher_lbl = Label(manage_frame,text="Publisher:",font="cambria 18 bold",fg="white",bg="#090A33")
publisher_lbl.grid(row=5,column=0,sticky=W,padx=10)
publisher_entry = Entry(manage_frame,width=35,font="cambria 13 bold",bg="#06144D",fg="white",textvariable=publisher_entry_var)
publisher_entry.grid(row=5,column=1,sticky=W,pady=20)

price_lbl = Label(manage_frame,text="Book Price:",font="cambria 18 bold",fg="white",bg="#090A33")
price_lbl.grid(row=6,column=0,sticky=W,padx=10)
price_entry = Entry(manage_frame,width=35,font="cambria 13 bold",bg="#06144D",fg="white",textvariable=price_entry_var)
price_entry.grid(row=6,column=1,sticky=W,pady=20)

copies_lbl = Label(manage_frame,text="Copies:",font="cambria 18 bold",fg="white",bg="#090A33")
copies_lbl.grid(row=7,column=0,sticky=W,padx=10)
copies_entry = Entry(manage_frame,width=35,font="cambria 13 bold",bg="#06144D",fg="white",textvariable=copies_entry_var)
copies_entry.grid(row=7,column=1,sticky=W,pady=20)

load = Image.open("Images/add_btn2.png")
load = load.resize((110, 50), Image.ANTIALIAS)
add_btn_img = ImageTk.PhotoImage(load)
add_btn = Button(win,image=add_btn_img,bg="#090A33",bd=0,command=on_add)
add_btn.image = add_btn_img
add_btn.place(x=30,y=657)

load1 = Image.open("Images/update_btn.png")
load1 = load1.resize((110, 55), Image.ANTIALIAS)
update_btn_img = ImageTk.PhotoImage(load1)
update_btn = Button(win,image=update_btn_img,bg="#090A33",bd=0,command=on_update)
update_btn.image = update_btn_img
update_btn.place(x=155,y=655)

load2 = Image.open("Images/delete_btn2.png")
load2 = load2.resize((110, 55), Image.ANTIALIAS)
delete_btn_img = ImageTk.PhotoImage(load2)
delete_btn = Button(win,image=delete_btn_img,bg="#090A33",bd=0,command=on_delete)
delete_btn.image = delete_btn_img
delete_btn.place(x=280,y=655)

load3 = Image.open("Images/reset-btn.png")
load3 = load3.resize((110, 40), Image.ANTIALIAS)
reset_btn_img = ImageTk.PhotoImage(load3)
reset_btn = Button(win,image=reset_btn_img,bg="#090A33",bd=0,command=on_reset)
reset_btn.image = reset_btn_img
reset_btn.place(x=410,y=665)


manage_frame.place(x=5,y=60,width=570,height=770)



#################DETAILS FRAMES########################
detail_frame = Frame(win,bd=8,relief="ridge",bg="#090A33")
detail_frame.place(x=580,y=60,width=942,height=770)

search_lbl = Label(detail_frame,text="Search By:",font="cambria 20 bold",fg="white",bg="#090A33")
search_lbl.grid(row=0,column=0,sticky=W,pady=10,padx=10)

search_combo = ttk.Combobox(detail_frame,width=10,font="cambria 15 bold",state="readonly",textvariable=search_combo_var)
combostyle = ttk.Style()
combostyle.theme_create('combostyle', parent='alt',
                         settings = {'TCombobox':
                                     {'configure':
                                      {'selectbackground': '#06144D',
                                       'fieldbackground': '#06144D',
                                       'background': '#4D00FF'
                                       }}}
                         )
combostyle.theme_use('combostyle')
search_combo['values'] = ('Book Id','Book Title')
search_combo.grid(row=0,column=1,sticky=W,pady=10)

search_entry = Entry(detail_frame,width=30,bd=5,font="cambria 13 bold",relief="groove",bg="#06144D",fg="white",textvariable=search_entry_var)
search_entry.grid(row=0,column=2,sticky=W,padx=12,pady=10)

load4 = Image.open("Images/search_btn2.png")
load4 = load4.resize((210, 30), Image.ANTIALIAS)
search_btn_img = ImageTk.PhotoImage(load4)
search_btn = Button(detail_frame,image=search_btn_img,font="cambria 12 bold",fg="white",bg="#090A33",bd=0,command=on_search)
search_btn.image = search_btn_img
search_btn.grid(row=0,column=3,sticky=W,padx=8,pady=10)

# show_btn = Button(detail_frame,text="Show All",width=9,font="cambria 12 bold",fg="white",bg="#FF2247")
# show_btn.grid(row=0,column=4,sticky=W,padx=8,pady=10)

####################Table Frame##############################
table_frame = Frame(detail_frame,bd=8,relief="ridge",bg="crimson")
table_frame.place(x=8,y=60,width=910,height=690)

scroll_x = Scrollbar(table_frame,orient=HORIZONTAL)
scroll_y = Scrollbar(table_frame,orient=VERTICAL)
book_table = ttk.Treeview(table_frame,columns=("1","2","3","4","5","6","7"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
style = ttk.Style()
style.configure("Treeview", background="#090A33",foreground="white", fieldbackground="#090A33", rowheight=30,font="arial 13 bold")
# style.configure("Treeview", fieldbackground="#090A33",font="arial 15 bold")
scroll_x.pack(side=BOTTOM,fill=X)
scroll_y.pack(side=RIGHT,fill=Y)
scroll_x.config(command=book_table.xview)
scroll_y.config(command=book_table.yview)
book_table.heading("1",text="Book ID")
book_table.heading("2",text="Title")
book_table.heading("3",text="Catagory")
book_table.heading("4",text="Auther")
book_table.heading("5",text="Publisher")
book_table.heading("6",text="Price")
book_table.heading("7",text="Copies")
book_table['show'] = 'headings'
book_table.column("1",width=100)
book_table.column("2",width=220)
book_table.column("3",width=160)
book_table.column("4",width=160)
book_table.column("5",width=220)
book_table.column("6",width=90)
book_table.column("7",width=60)
book_table.pack(fill=BOTH,expand=1)

fetch_data()

win.mainloop()