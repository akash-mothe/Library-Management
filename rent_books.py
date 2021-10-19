from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector as sql
from mysql.connector import Error
from tkinter import messagebox as msg
from datetime import date
from datetime import datetime  
from datetime import timedelta
from dateutil.relativedelta import relativedelta



win = Tk()
win.title("Registration Window")
win.geometry("{0}x{1}+0+0".format(win.winfo_screenwidth(), win.winfo_screenheight()))
# win.geometry("1200x700")
win.configure(bg='#343733')
# win.maxsize(width=1200,height=700)
# win.minsize(width=1200,height=700)

#########################ALL VARIABLES############################
# style = ttk.Style()
# # style.theme_use("clam")
search_combo_var = StringVar()
search_entry_var = StringVar()
stud_id_entry_var = StringVar()
pass_key_entry_var = StringVar()
bor_title_entry_var = StringVar()
borrow_area_var = StringVar()
ret_title_entry_var = StringVar()
rent_book_table_var= StringVar()
l = date.today()+ timedelta(days=30)
renew_date = l.strftime("%d/%m/%Y")
fine = 25
today = date.today().strftime("%d/%m/%Y")

###########ALL FUNCTIONS############
def fetch_data():
    try:
        con = sql.connect(host="localhost",user="root",password='wadgaonmali',database="labmanagement")
        cur = con.cursor()
            # cur.execute("use studentmanagement")
        cur.execute("select * from book_details")
        rows = cur.fetchall()
        if len(rows)!=0:
            rent_book_table.delete(*rent_book_table.get_children())
            for row in rows:
                rent_book_table.insert('',END,values=row)
            con.commit()
        con.close()
    except sql.Error:
        msg.showerror("Error","Something went wrong.\nPlease try again by giving correct inputs.")

def on_search_book():
    # on_search_book.has_been_called = True
    try:
        if (search_combo_var.get()!="") and (search_entry_var.get()!=""):
            con=sql.connect(host='localhost',user='root',password='wadgaonmali')
            cur=con.cursor()
            cur.execute("use labmanagement")
            
            if (search_combo_var.get()=="Book Id"):
                cur.execute(f"select * from book_details where book_id = {search_entry_var.get()}")
                result = cur.fetchone()
                if len(result)!=0:
                    rent_book_table.delete(*rent_book_table.get_children())
                    rent_book_table.insert('',END,values=result)
            elif (search_combo_var.get()=="Book Title"):
                cur.execute(f"select * from book_details")
                result = cur.fetchall()
                x = 1
                for row in result:
                    if str(search_entry_var.get())==row[1]:
                        x+=1
                        rent_book_table.delete(*rent_book_table.get_children())
                        rent_book_table.insert('',END,values=row)
                if x == 1:
                    msg.showerror("Error","Record not found")
            # cur.close()
            # con.close()
        else:
            msg.showwarning("warning","Please select search by option and enter some value")
    except sql.errors.ProgrammingError:
        msg.showerror("Error","Record not found")

# def on_tree_select(event):
#     for item in rent_book_table.selection():
#         # rent_book_table.tag_configure('ttk', background='yellow')
#         item_text = rent_book_table.item(item,'values')
#         print(item_text)

def on_show():
    fetch_data()

def current_date1():
    today = date.today()
    d = today.strftime("%d/%m/%Y")
    return d

def on_validate():
    try:
        y = 1
        if (stud_id_entry_var.get()!="") and (pass_key_entry_var.get()!=""):
            con=sql.connect(host='localhost',user='root',password='wadgaonmali')
            cur=con.cursor()
            cur.execute("use labmanagement")
            cur.execute("select * from stud_reg")
            result = cur.fetchall()
            for row in result:
                if (str(stud_id_entry_var.get())==str(row[0])) and (str(pass_key_entry_var.get())==str(row[7])) and (current_date1()!=row[5]):
                    y+=1
                    student_name = row[1]
                    leave_date = row[5]
                    contact = row[3]
                    msg.showinfo("Success",f"Yes, He is a student with name:{row[1]}.")
                    ans = msg.askyesnocancel("?","If you want to borrow book click on 'Yes' and \nif you want to return book click on 'No'")
                    if (ans == True):
                        # >>>>>>>>>>>>>>BORR0W
                        # on_show_receipt_called = 1
                        def on_show_receipt():
                            
                            if (search_combo_var.get()!="") and (search_entry_var.get()!=""):
                                con = sql.connect(host="localhost",user="root",password='wadgaonmali',database="labmanagement")
                                cur = con.cursor()
                                cur.execute("select * from book_details")
                                # result = cur.fetchall()
                                if search_combo_var.get()=="Book Title":
                                    result = cur.fetchall()
                                    x = 1
                                    for row in result:
                                        if (search_entry_var.get()==row[1]):
                                            x+=1
                                            # on_show_receipt_called += 1
                                            borrow_area.insert(END,"\t\t            !!!STUDYPOINT LIBRARY!!!\n\n")
                                            borrow_area.insert(END,f"\n  Student Name: \t\t     {student_name}")
                                            borrow_area.insert(END,f"\n  Student Contact: \t\t     {contact}")
                                            borrow_area.insert(END,f"\n  Book Title: \t\t     {row[1]}")
                                            borrow_area.insert(END,f"\n  Book Auther: \t\t     {row[3]}")
                                            borrow_area.insert(END,f"\n  Book Price: \t\t     Rs.{row[5]}ru.")
                                            borrow_area.insert(END,f"\n  Borrowed Date: \t\t     {current_date1()}")
                                            borrow_area.insert(END,f"\n  Return/Renew Date: \t{renew_date}")
                                            borrow_area.insert(END,f"\n  Per Day Fine: \t\t      Rs.{fine}ru.")
                                            borrow_area.insert(END,f"\n----------------------------------------------------------------------------------")
                                            borrow_area.insert(END,f"\n\n Please don't forget to return of renew your book on {renew_date}\nOtherwise you will got the fine of Rs.{fine}ru. per day\n")
                                            borrow_area.insert(END,f"\n=======================================================\n\n\n")
                                            borrow_area.insert(END,"\n\n\t\t                 THANKS A LOT")
                                            borrow_area.insert(END,"\n\n\t\t         FOR YOUR MEMBERSHIP")
                                            on_show_receipt.has_been_called = True
                                            
                                    if x==1:
                                        msg.showwarning("warning","Please search a book first.")
                                elif search_combo_var.get()=="Book Id":
                                    result1 = cur.fetchall()
                                    xx = 1
                                    for row in result1:
                                        if (str(search_entry_var.get())==str(row[0])):
                                            xx+=1
                                            borrow_area.insert(END,"\t\t            !!!STUDYPOINT LIBRARY!!!\n\n")
                                            borrow_area.insert(END,f"\n  Student Name: \t\t     {student_name}")
                                            borrow_area.insert(END,f"\n  Student Contact: \t\t     {contact}")
                                            borrow_area.insert(END,f"\n  Book Title: \t\t     {row[1]}")
                                            borrow_area.insert(END,f"\n  Book Auther: \t\t     {row[3]}")
                                            borrow_area.insert(END,f"\n  Book Price: \t\t     Rs.{row[5]}ru.")
                                            borrow_area.insert(END,f"\n  Borrowed Date: \t\t     {current_date1()}")
                                            borrow_area.insert(END,f"\n  Return/Renew Date: \t{renew_date}")
                                            borrow_area.insert(END,f"\n  Per Day Fine: \t\t      Rs.{fine}ru.")
                                            borrow_area.insert(END,f"\n----------------------------------------------------------------------------------")
                                            borrow_area.insert(END,f"\n\n Please don't forget to return of renew your book on {renew_date}\nOtherwise you will got the fine of Rs.{fine}ru. per day\n")
                                            borrow_area.insert(END,f"\n=======================================================\n\n\n")
                                            borrow_area.insert(END,"\n\n\t\t                 THANKS A LOT")
                                            borrow_area.insert(END,"\n\n\t\t         FOR YOUR MEMBERSHIP")
                                            on_show_receipt.has_been_called = True
                                            
                                    if xx==1:
                                        msg.showwarning("warning","Please search a book first.")
                            
                            else:
                                msg.showwarning("warning","Please search a book first.")
                        
                        on_show_receipt.has_been_called = False

                        def on_clear():
                            borrow_area.delete('1.0', END)
                            search_combo_var.set("")
                            search_entry_var.set("")
                        def on_borrow():
                            if on_show_receipt.has_been_called == True:
                                con = sql.connect(host="localhost",user="root",password='wadgaonmali',database="labmanagement")
                                cur = con.cursor()
                                cur.execute("select * from book_details")
                                result = cur.fetchall()
                                z = 1
                                for row in result:
                                    if str(search_entry_var.get())==str(row[0]) or str(search_entry_var.get())==str(row[1]):
                                        z += 1
                                        current_copies = int(row[6]) - 1
                                        sql_query = """Update book_details set copies = %s where book_id = %s"""
                                        data = (current_copies,row[0])
                                        cur.execute(sql_query,data)
                                        con.commit()
                                        con2 = sql.connect(host="localhost",user="root",password='wadgaonmali',database="labmanagement")
                                        cur2 = con2.cursor()
                                        insert_query2 = """INSERT INTO borrowed_book_details (student_name,student_contact,boo_title,book_auther,book_price,borrowed_date,return_date,perday_fine) 
                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """
                                        data2 = (student_name,contact,row[1],row[3],int(row[5]),current_date1(),renew_date,fine)
                                        cur2.execute(insert_query2,data2)
                                        con2.commit()
                                        cur.close()
                                        con.close()
                                        cur2.close()
                                        con2.close()
                                        msg.showinfo("sucess",f"You have successfully borrowed book with title: {row[1]}")
                                if z==1:
                                    msg.showwarning("warning","Please don't enter incorrect value in search entry field.")
                            else:
                                msg.showwarning("warning","Please generate the receipt first.")
                            # print(on_show_receipt_called)


                        borrow_lbl = Label(borrow_frame,text="Borrow Details",font="cambria 25 bold",fg="#FFEF00",bg="#343733")
                        borrow_lbl.place(x=190,y=6)

                        bor_title_lbl = Label(borrow_frame,text="Book Receipt:",font="cambria 17 bold",fg="white",bg="#343733")
                        bor_title_lbl.place(x=10,y=66)
                        # bor_title_entry = Entry(borrow_frame,width=35,font="cambria 13 bold",bg="#3C5B37",fg="white",textvariable=bor_title_entry_var)
                        # bor_title_entry.place(x=140,y=63,width=300,height=25)

                        show_receipt_btn = Button(borrow_frame,text="Show Receipt",font="cambria 11 bold",bg="#FF0033",fg="white",command=on_show_receipt)
                        show_receipt_btn.place(x=250,y=740,width=115,height=35)

                        borrow_area = Text(borrow_frame,font="cambria 13",bg="#343733",fg="white",bd=4)
                        borrow_area.place(x=5,y=115,width=580,height=600)

                        borrow_btn = Button(borrow_frame,text="Borrow Book",font="cambria 16 bold",bg="#FF0033",fg="white",command=on_borrow)
                        borrow_btn.place(x=390,y=740,width=190,height=35)

                        clear_btn = Button(borrow_frame,text="Clear",font="cambria 16 bold",bg="#FF0033",fg="white",command=on_clear)
                        clear_btn.place(x=110,y=740,width=115,height=35)
                    elif (ans==False):
                        # >>>>>>>>>>>>>>RETURN BOOK
                        con = sql.connect(host="localhost",user="root",password='wadgaonmali',database="labmanagement")
                        cur = con.cursor()
                        cur.execute("select * from borrowed_book_details")
                        record = cur.fetchall()
                        a = 1
                        for i in record:
                            if i[0]==student_name:
                                a+=1
                                def gen_fine():
                                    con = sql.connect(host="localhost",user="root",password='wadgaonmali',database="labmanagement")
                                    cur = con.cursor()
                                    cur.execute("select * from borrowed_book_details")
                                    result = cur.fetchall()
                                    for row in result:
                                        c_date = date.today()
                                        d,m,y = row[6].split("/")
                                        ret_date = date(int(y),int(m),int(d))
                                        rdelta = relativedelta(c_date,ret_date)
                                        if int(rdelta.days)>0:
                                            generated_fine = 25*int(rdelta.days)
                                            return generated_fine
                                        else:
                                            return 0
                                    cur.close()
                                    con.close()


                                def on_ret_receipt():
                                    if (ret_title_entry_var.get()!=""):
                                        con = sql.connect(host="localhost",user="root",password='wadgaonmali',database="labmanagement")
                                        cur = con.cursor()
                                        cur.execute("select * from borrowed_book_details")
                                        result = cur.fetchall()
                                        abc = 1
                                        for row in result:
                                            if (str(student_name)==str(row[0])) and (str(contact)==str(row[1])) and (str(ret_title_entry_var.get())==str(row[2])):
                                                abc+=1
                                                return_area.delete('1.0', END)
                                                return_area.insert(END,"\t\t            !!!STUDYPOINT LIBRARY!!!\n\n")
                                                return_area.insert(END,f"\n  Student Name: \t\t     {row[0]}")
                                                return_area.insert(END,f"\n  Student Contact: \t\t     {row[1]}")
                                                return_area.insert(END,f"\n  Book Title: \t\t     {row[2]}")
                                                return_area.insert(END,f"\n  Book Auther: \t\t     {row[3]}")
                                                return_area.insert(END,f"\n  Book Price: \t\t     Rs.{str(row[4])}ru.")
                                                return_area.insert(END,f"\n  Borrowed Date: \t\t     {row[5]}")
                                                return_area.insert(END,f"\n  Return/Renew Date: \t{row[6]}")
                                                return_area.insert(END,f"\n  Returning on: \t             {today}")
                                                return_area.insert(END,f"\n  Per Day Fine: \t\t      Rs.{str(row[7])}ru.")
                                                return_area.insert(END,f"\n  Your Generated fine:   Rs.{str(gen_fine())}ru.")
                                                return_area.insert(END,f"\n----------------------------------------------------------------------------------")
                                                return_area.insert(END,f"\n\n Thanks for your interest.\nDon't share your passkey to anyone.")
                                                return_area.insert(END,f"\n=======================================================\n\n\n")
                                                return_area.insert(END,"\n\n\t\t                 THANKS A LOT")
                                                return_area.insert(END,"\n\n\t\t         FOR YOUR MEMBERSHIP")
                                                on_ret_receipt.has_been_called = True
                                        # else:
                                        #     msg.showinfo("as","Failed")
                                        cur.close()
                                        con.close()
                                        if abc==1:
                                            msg.showwarning("Sorry","You did't borrowed that book.\n Enter your borrowed book title.")
                                    else:
                                        msg.showwarning("Warning","Please enter your book title that you want to return.")

                                on_ret_receipt.has_been_called = False

                                def getting_book_details():
                                    con = sql.connect(host="localhost",user="root",password='wadgaonmali',database="labmanagement")
                                    cur = con.cursor()
                                    cur.execute("select * from borrowed_book_details")
                                    result = cur.fetchall()
                                    for row in result:
                                        if (str(student_name)==str(row[0])) and (str(contact)==str(row[1])):
                                            book_title = row[2]
                                            return book_title

                                def on_ret_clear():
                                    search_combo_var.set("")
                                    search_entry_var.set("")
                                    ret_title_entry_var.set("")
                                    return_area.delete('1.0', END)

                                def on_return():
                                    if (ret_title_entry_var.get()!="") and (on_ret_receipt.has_been_called==True):
                                        con = sql.connect(host="localhost",user="root",password='wadgaonmali',database="labmanagement")
                                        cur = con.cursor()
                                        cur.execute("select * from book_details")
                                        book_result = cur.fetchall()
                                        z = 1
                                        for row in book_result:
                                            if (ret_title_entry_var.get()==row[1]):
                                                z+=1
                                                current_copies = int(row[6]) + 1
                                                sql_query = """Update book_details set copies = %s where title = %s"""
                                                data = (current_copies,ret_title_entry_var.get())
                                                cur.execute(sql_query,data)
                                                con.commit()
                                                sql_Delete_query = """Delete from borrowed_book_details where boo_title = %s"""
                                                data = ret_title_entry_var.get()
                                                cur.execute(sql_Delete_query, (data,))
                                                con.commit()
                                                msg.showinfo("Success",f"You have successfully returned your book with title:{row[1]}")
                                        if z==1:
                                            msg.showwarning("Warning","Your entered book title is not matched\n with your borrowed book title")
                                    else:
                                        msg.showwarning("warning","Please enter your book title and show your receipt first.")

                                ret_lbl = Label(borrow_frame,text="Return Book",font="cambria 25 bold",fg="#FFEF00",bg="#343733")
                                ret_lbl.place(x=190,y=6)

                                ret_title_lbl = Label(borrow_frame,text="Book Title:",font="cambria 15 bold",fg="white",bg="#343733")
                                ret_title_lbl.place(x=10,y=60)
                                ret_title_entry = Entry(borrow_frame,width=35,font="cambria 13 bold",bg="#3C5B37",fg="white",textvariable=ret_title_entry_var)
                                ret_title_entry.place(x=150,y=63,width=400,height=25)

                                return_area = Text(borrow_frame,font="cambria 13",bg="#343733",fg="white")
                                return_area.place(x=5,y=115,width=580,height=600)

                                return_btn = Button(borrow_frame,text="Return Book",font="cambria 16 bold",bg="#FF0080",fg="white",command=on_return)
                                return_btn.place(x=390,y=740,width=180,height=35)

                                ret_receipt_btn = Button(borrow_frame,text="Show Receipt",font="cambria 11 bold",bg="#FF0033",fg="white",command=on_ret_receipt)
                                ret_receipt_btn.place(x=250,y=740,width=115,height=35)

                                ret_clear_btn = Button(borrow_frame,text="Clear",font="cambria 16 bold",bg="#FF0033",fg="white",command=on_ret_clear)
                                ret_clear_btn.place(x=110,y=740,width=115,height=35)
                        cur.close()
                        con.close()
                        if a==1:
                            msg.showwarning("Sorry","Oh..You did't borrowed any book yet.")
                    elif (ans==None):
                        pass
            if y==1:
                msg.showwarning("warning","Sorry! This Id is not registered or maybe your membership is expired.")
        else:
            msg.showwarning("warning","Please fill up both fields.")
    except sql.Error:
        msg.showerror("Error","Something went wrong.\nPlease try again by giving correct inputs.")


detail_frame = Frame(win,bd=5,relief="ridge",bg="#343733")
detail_frame.place(x=0,y=0,width=925,height=830)

head_lbl = Label(detail_frame,text="Search Your Book Below:",font="cambria 25 bold",fg="#D5FF00",bg="#343733")
head_lbl.grid(row=0,columnspan=3,sticky=W,padx=7,pady=10)

search_lbl = Label(detail_frame,text="Search By:",font="cambria 20 bold",fg="white",bg="#343733")
search_lbl.grid(row=1,column=0,sticky=W,padx=10,pady=10)

search_combo = ttk.Combobox(detail_frame,width=10,font="cambria 15 bold",state="readonly",textvariable=search_combo_var)
combostyle = ttk.Style()
combostyle.theme_create('combostyle', parent='alt',
                         settings = {'TCombobox':
                                     {'configure':
                                      {'selectbackground': '#3C5B37',
                                       'fieldbackground': '#3C5B37',
                                       'background': '#4D00FF'
                                       }}}
                         )
combostyle.theme_use('combostyle')
search_combo['values'] = ('Book Id','Book Title')
search_combo.grid(row=1,column=1,sticky=W,pady=10)

search_entry = Entry(detail_frame,width=30,bd=5,font="cambria 13 bold",relief="groove",bg="#3C5B37",fg="white",textvariable=search_entry_var)
search_entry.grid(row=1,column=2,sticky=W,padx=6,pady=10)

load4 = Image.open("Images/search_btn2.png")
load4 = load4.resize((140, 30), Image.ANTIALIAS)
search_btn_img = ImageTk.PhotoImage(load4)
search_btn = Button(detail_frame,image=search_btn_img,font="cambria 12 bold",fg="white",bg="#090A33",bd=0,command=on_search_book)
search_btn.image = search_btn_img
search_btn.grid(row=1,column=3,sticky=W,padx=8,pady=10)

show_btn = Button(detail_frame,text="Show All",width=9,font="cambria 12 bold",fg="white",bg="#00BCFF",command=on_show)
show_btn.grid(row=1,column=4,sticky=W,padx=8,pady=10)

####################Table Frame##############################
table_frame = Frame(detail_frame,bd=2,relief="ridge",bg="#343733")
table_frame.place(x=2,y=120,width=910,height=700)

scroll_x = Scrollbar(table_frame,orient=HORIZONTAL)
scroll_y = Scrollbar(table_frame,orient=VERTICAL)
rent_book_table = ttk.Treeview(table_frame,columns=("1","2","3","4","5","6","7"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
style = ttk.Style()
style.configure("Treeview", background="#343733",foreground="white", fieldbackground="#343733", rowheight=30,font="arial 13 bold")
scroll_x.pack(side=BOTTOM,fill=X)
scroll_y.pack(side=RIGHT,fill=Y)
scroll_x.config(command=rent_book_table.xview)
scroll_y.config(command=rent_book_table.yview)
rent_book_table.heading("1",text="Book ID")
rent_book_table.heading("2",text="Title")
rent_book_table.heading("3",text="Catagory")
rent_book_table.heading("4",text="Auther")
rent_book_table.heading("5",text="Publisher")
rent_book_table.heading("6",text="Price")
rent_book_table.heading("7",text="Copies")
rent_book_table['show'] = 'headings'
rent_book_table.column("1",width=100)
rent_book_table.column("2",width=220)
rent_book_table.column("3",width=160)
rent_book_table.column("4",width=160)
rent_book_table.column("5",width=220)
rent_book_table.column("6",width=90)
rent_book_table.column("7",width=60)
rent_book_table.pack(fill=BOTH,expand=1)
# rent_book_table.bind("<<TreeviewSelect>>", on_tree_select)

###################BORROW FRAME###################
borrow_frame = Frame(win,bd=5,relief="ridge",bg="#343733")
borrow_frame.place(x=926,y=2,width=600,height=830)

#>>>>>>>>>>>WELCOME
borrow_lbl = Label(borrow_frame,text="WELCOME",font="cambria 25 bold",fg="#FFEF00",bg="#343733")
borrow_lbl.place(x=190,y=6)

stud_id_lbl = Label(borrow_frame,text="Enter Student Id:",font="cambria 15 bold",fg="white",bg="#343733")
stud_id_lbl.place(x=100,y=230)
stud_id_entry = Entry(borrow_frame,width=35,font="cambria 13 bold",bg="#3C5B37",fg="white",textvariable=stud_id_entry_var)
stud_id_entry.place(x=100,y=270,width=320,height=25)

pass_key_lbl = Label(borrow_frame,text="Pass Key:",font="cambria 15 bold",fg="white",bg="#343733")
pass_key_lbl.place(x=100,y=320)
pass_key_entry = Entry(borrow_frame,width=35,font="cambria 13 bold",bg="#3C5B37",fg="white",textvariable=pass_key_entry_var)
pass_key_entry.place(x=100,y=360,width=320,height=25)

validate_btn = Button(borrow_frame,text="Validate",font="cambria 16 bold",bg="#FF2247",fg="white",command=on_validate)
validate_btn.place(x=185,y=450,width=150,height=28)


fetch_data()

win.mainloop()