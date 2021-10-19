from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector as sql
from mysql.connector import Error
from mysql.connector.errors import Error
import webbrowser
from tkinter import messagebox as msg
from datetime import date,datetime,timedelta
from dateutil.relativedelta import relativedelta



win = Tk()
win.title("Login Window")
# win.geometry("{0}x{1}+0+0".format(win.winfo_screenwidth(), win.winfo_screenheight()))
win.geometry("1000x500")
win.configure(bg='#610303')

style = ttk.Style()
style.theme_create('combostyle', parent='alt',
                            settings = {'TCombobox':
                                        {'configure':
                                        {'selectbackground': '#252530',
                                        'fieldbackground': '#252530',
                                        'background': 'white'
                                        }}}
                            )
# style.theme_use('combostyle')



# @@@@@@@@@@@@@@@All FUNCTIONS@@@@@@@@@@@

def navigations():
    win = Toplevel()
    win.title("Navigations Window")
    win.geometry("1000x570")
    win.maxsize(width=1000,height=570)
    win.minsize(width=1000,height=570)
    ########FUNCTIONS#####
    def go_to_registration():
        registration()
    def go_to_manage_books():
        books_management()
    def go_to_rent_books():
        rent_books()
    def go_to_books_borrowed():
        borrow_books_details()
    #######DESIGNS########
    load = Image.open("Images/books.jpg")
    load = load.resize((1000, 570), Image.ANTIALIAS)
    book_img = ImageTk.PhotoImage(load)
    book_img_lbl = Label(win,image=book_img,bg='#251B1B')
    book_img_lbl.image = book_img
    book_img_lbl.place(x=0,y=0)

    nav_lbl = Label(win,text="Navigations",font="forte 65 bold",fg="#2E04FF",bg="white")
    nav_lbl.place(x=5,y=200)

    stud_reg_btn = Button(win,text="Register Students",font="cambria 16 bold",bg="#FF0471",fg="white",command=go_to_registration)
    stud_reg_btn.place(x=750,y=80,width=220,height=40)

    manage_books_btn = Button(win,text="Manage Books",font="cambria 16 bold",bg="#FF0471",fg="white",command=go_to_manage_books)
    manage_books_btn.place(x=750,y=166,width=220,height=40)

    rent_books_btn = Button(win,text="Rent Books",font="cambria 16 bold",bg="#FF0471",fg="white",command=go_to_rent_books)
    rent_books_btn.place(x=750,y=260,width=220,height=40)

    books_borrowed_btn = Button(win,text="Books Borrowed",font="cambria 16 bold",bg="#FF0471",fg="white",command=go_to_books_borrowed)
    books_borrowed_btn.place(x=750,y=360,width=220,height=40)

def registration():
    win = Toplevel()
    win.title("Registration Window")
    win.geometry("1200x750")
    win.configure(bg='#343534')
    win.maxsize(width=1200,height=750)
    win.minsize(width=1200,height=750)

    ###########VARIABLES#########
    ###style = ttk.Style()
    style.theme_use("clam")
    id_entry_var = StringVar()
    name_entry_var = StringVar()
    gender_combo_var = StringVar()
    mobile_entry_var = StringVar()
    join_entry_var = StringVar()
    leave_entry_var = StringVar()
    address_entry_var = StringVar()
    pass_key_entry_var = StringVar()
    search_by_combo_var = StringVar()
    enter_name_entry_var = StringVar()


    ##################FUNCTIONS###########
    def current_date():
        today = date.today()
        d = today.strftime("%d/%m/%Y")
        return d

    def gen_id():

        con=sql.connect(host='localhost',user='root',password='wadgaonmali')
        cursor=con.cursor()
        cursor.execute("use labmanagement")
        cursor.execute("select * from stud_reg")
        result = cursor.fetchall()

        val = result[-1][0]
        return str(int(val)+1)

    id_entry_var.set(gen_id())


    def on_register():
        try:
            con=sql.connect(host='localhost',user='root',password='wadgaonmali')
            cursor=con.cursor()
            cursor.execute("use labmanagement")
            cursor.execute("select * from stud_reg")
            result = cursor.fetchall()
            if (id_entry_var.get()!="") and (name_entry_var.get()!="") and (gender_combo_var.get()!="") and (mobile_entry_var.get()!="") and (join_entry_var.get()!="") and (leave_entry_var.get()!="") and (address_entry.get("1.0","end-1c")!="") and (pass_key_entry_var.get()!=""):

                if str(result[-1][0]) != str(id_entry_var.get()):
                    insert_query = """INSERT INTO stud_reg (student_id,name,gender,mobile_no,joindate,leavedate,address,passkey) 
                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """
                    data = (id_entry_var.get(),name_entry_var.get(),gender_combo_var.get(),mobile_entry_var.get(),join_entry_var.get(),leave_entry_var.get(),address_entry.get("1.0","end-1c"),pass_key_entry_var.get())
                    cursor.execute(insert_query,data)
                    con.commit()
                    cursor.close()
                    con.close()
                    ans = msg.askyesno("Success",f"You have successfully registred {name_entry_var.get()}.\nWant to register one more student?")
                    if ans == True:
                        on_clear()
                        id_entry.delete(0,END)
                        id_entry.insert(0,gen_id())
                        id_entry_var.set(gen_id())
                    else:
                        on_clear()
                else:
                    msg.showerror("Error","This ID is already registered.")

            else:
                msg.showwarning("Warning","All fields are required..!")
        except sql.Error:
            msg.showerror("Sorry","Something went wrong.\nTry again by giving correct inputs")

    def on_search():
        if (search_by_combo_var.get()!="") and (enter_name_entry_var.get()!=""):
            con=sql.connect(host='localhost',user='root',password='wadgaonmali')
            cursor=con.cursor()
            cursor.execute("use labmanagement")
            cursor.execute("select * from stud_reg")
            result = cursor.fetchall()
            if (search_by_combo_var.get()=="ID"):
                a = 1
                for row in result:
                    if (int(enter_name_entry_var.get()) == row[0]):
                        id_entry.delete(0,END)
                        id_entry.insert(0,row[0])
                        id_entry_var.set(row[0])
                        name_entry_var.set(row[1])
                        gender_combo_var.set(row[2])
                        mobile_entry_var.set(row[3])
                        join_entry.delete(0,END)
                        join_entry.insert(0,row[4])
                        leave_entry_var.set(row[5])
                        address_entry.delete("1.0","end")
                        address_entry.insert("1.0",row[6])
                        pass_key_entry_var.set(row[7])
                        a+=1
                if a==1:
                    msg.showerror("Sorry","Record not found....!")

            elif (search_by_combo_var.get()=="Name"):
                b = 1
                for row in result:
                    if (enter_name_entry_var.get() == row[1]):
                        id_entry.delete(0,END)
                        id_entry.insert(0,row[0])
                        id_entry_var.set(row[0])
                        name_entry_var.set(row[1])
                        gender_combo_var.set(row[2])
                        mobile_entry_var.set(row[3])
                        join_entry.delete(0,END)
                        join_entry.insert(0,row[4])
                        leave_entry_var.set(row[5])
                        address_entry.delete("1.0","end")
                        address_entry.insert("1.0",row[6])
                        pass_key_entry_var.set(row[7])
                        b+=1
                if b==1:
                    msg.showerror("Sorry","Record not found....!")
            cursor.close()
            con.close()
        else:
            msg.showwarning("warning","Both fields required!")


    def on_update():
        if (str(id_entry_var.get())!=gen_id()):
            con = sql.connect(host="localhost",user="root",password='wadgaonmali',database="labmanagement")
            cur = con.cursor()
            cur.execute("UPDATE stud_reg set name = %s, gender = %s, mobile_no = %s, joindate = %s, leavedate = %s, address = %s, passkey = %s WHERE student_id = %s",(name_entry_var.get(), gender_combo_var.get(), mobile_entry_var.get(), join_entry_var.get(), leave_entry_var.get(), address_entry.get("1.0","end-1c"), pass_key_entry_var.get(), id_entry_var.get()))
            con.commit()
            con.close()
            msg.showinfo("Info",f"Record of ID:{id_entry_var.get()} has been updated successfully. ")
        else:
            msg.showwarning("Warning","Given id is not registered.")

    def on_remove():
        if (str(id_entry_var.get())!=gen_id()):
            ans = msg.askyesno("YesOrNo",f"Do you really want to delete record of ID:{id_entry_var.get()}")
            if ans==True:
                con = sql.connect(host="localhost",user="root",password='wadgaonmali',database="labmanagement")
                cur = con.cursor()
                sql_query = '''delete from stud_reg where student_id = %s'''
                data = id_entry_var.get()
                # cur.execute("delete from stud_reg where student_id = %s",(id_entry_var.get()))
                cur.execute(sql_query,(data,))
                con.commit()
                con.close()
                msg.showinfo("Success",f"Student record of ID:{id_entry_var.get()} removed successfully.")
            else:
                pass
        else:
            msg.showwarning("Warning","Given id is not registered.")

    def on_clear():
        name_entry_var.set("")
        gender_combo_var.set("")
        mobile_entry_var.set("")
        leave_entry_var.set("")
        pass_key_entry_var.set("")
        address_entry.delete("1.0","end")
        search_by_combo_var.set("")
        enter_name_entry_var.set("")
        id_entry.delete(0,END)
        id_entry.insert(0,gen_id())
        id_entry_var.set(gen_id())


    head_lbl = Label(win,text="Manage Students",font="elephant 24 bold",fg="#D7FF14",bg="#343534")
    head_lbl.pack()

    id_lbl = Label(win,text="Student Id:",font="cambria 18 bold",fg="white",bg="#343534")
    id_lbl.place(x=30,y=90)
    ph_lbl = Label(win,text="Auto increment",font="cambria 9",fg="#B6AEAE",bg="#343534")
    ph_lbl.place(x=190,y=75)
    id_entry = Entry(win,font="cambria 13 bold",bg="#343534",fg="white")
    id_entry.insert(0,gen_id())
    id_entry.place(x=190,y=93,width=140,height=30)

    name_lbl = Label(win,text="Name:",font="cambria 18 bold",fg="white",bg="#343534")
    name_lbl.place(x=30,y=150)
    name_entry = Entry(win,font="cambria 13 bold",bg="#252530",fg="white",textvariable=name_entry_var)
    name_entry.focus_set()
    name_entry.place(x=190,y=153,width=420,height=30)

    gender_lbl = Label(win,text="Gender:",font="cambria 18 bold",fg="white",bg="#343534")
    gender_lbl.place(x=30,y=210)
    gender_combo = ttk.Combobox(win,justify='left',font="arial 12 bold",textvariable=gender_combo_var)

    # combostyle = ttk.Style()
    # style.theme_create('combostyle1', parent='alt',
    #                         settings = {'TCombobox':
    #                                     {'configure':
    #                                     {'selectbackground': '#252530',
    #                                     'fieldbackground': '#252530',
    #                                     'background': 'green'
    #                                     }}}
    #                         )
    style.theme_use('combostyle')

    gender_combo['state'] = 'readonly'
    gender_combo['values'] = ('Male','Female')
    gender_combo.place(x=190,y=213,width=420,height=30)

    mobile_lbl = Label(win,text="Mobile No.:",font="cambria 18 bold",fg="white",bg="#343534")
    mobile_lbl.place(x=30,y=270)
    ph1_lbl = Label(win,text="Upto 10 digit",font="cambria 9",fg="#B6AEAE",bg="#343534")
    ph1_lbl.place(x=190,y=255)
    mobile_entry = Entry(win,font="cambria 13 bold",bg="#252530",fg="white",textvariable=mobile_entry_var)
    mobile_entry.place(x=190,y=273,width=420,height=30)

    join_lbl = Label(win,text="join Date:",font="cambria 18 bold",fg="white",bg="#343534")
    join_lbl.place(x=30,y=330)
    join_entry = Entry(win,font="cambria 13 bold",bg="#252530",fg="white",textvariable=join_entry_var)
    join_entry.insert(0,current_date())
    join_entry.place(x=190,y=333,width=420,height=30)

    leave_lbl = Label(win,text="Leave Date:",font="cambria 18 bold",fg="white",bg="#343534")
    leave_lbl.place(x=30,y=390)
    ph2_lbl = Label(win,text="Format must be: dd/mm/yyyy",font="cambria 9",fg="#B6AEAE",bg="#343534")
    ph2_lbl.place(x=190,y=375)
    leave_entry = Entry(win,font="cambria 13 bold",bg="#252530",fg="white",textvariable=leave_entry_var)
    leave_entry.place(x=190,y=393,width=420,height=30)

    address_lbl = Label(win,text="Address:",font="cambria 18 bold",fg="white",bg="#343534")
    address_lbl.place(x=30,y=450)
    address_entry = Text(win,font="cambria 13 bold",bg="#252530",fg="white")
    address_entry.place(x=190,y=453,width=420,height=80)

    pass_key_lbl = Label(win,text="Pass Key:",font="cambria 18 bold",fg="white",bg="#343534")
    pass_key_lbl.place(x=30,y=560)
    ph3_lbl = Label(win,text="Upto 12 Characters",font="cambria 9",fg="#B6AEAE",bg="#343534")
    ph3_lbl.place(x=190,y=545)
    pass_key_entry = Entry(win,font="cambria 13 bold",bg="#252530",fg="white",show="*",textvariable=pass_key_entry_var)
    pass_key_entry.place(x=190,y=563,width=240,height=30)

    # view_btn = Button(win,text="View",font="cambria 14 bold",bg="#FF0080",fg="white",command=on_view)
    # view_btn.place(x=460,y=563,width=100,height=30)

    load = Image.open("Images/register_btn.png")
    load = load.resize((210, 50), Image.ANTIALIAS)
    reg_btn_img = ImageTk.PhotoImage(load)
    reg_btn = Button(win,image=reg_btn_img,bg="#343534",bd=0,command=on_register)
    reg_btn.image = reg_btn_img
    reg_btn.place(x=280,y=660)

    frame1 = Frame(win,bd=2,relief="ridge",bg="#343534")
    frame1.place(x=680,y=120,width=450,height=300)

    search_lbl = Label(frame1,text="Search Student:",font="cambria 22 bold",fg="white",bg="#343534")
    search_lbl.place(x=3,y=3)

    search_by_lbl = Label(frame1,text="Search By:",font="cambria 13 bold",fg="white",bg="#343534")
    search_by_lbl.place(x=12,y=60)

    search_by_combo = ttk.Combobox(frame1,justify='left',font="arial 12 bold",textvariable=search_by_combo_var)
    search_by_combo['state'] = 'readonly'
    search_by_combo['values'] = ["ID","Name"]
    search_by_combo.place(x=12,y=90,width=200,height=27)

    enter_name_lbl = Label(frame1,text="Enter Name/Id:",font="cambria 13 bold",fg="white",bg="#343534")
    enter_name_lbl.place(x=12,y=130)
    enter_name_entry = Entry(frame1,font="cambria 13 bold",bg="#252530",fg="white",textvariable=enter_name_entry_var)
    enter_name_entry.place(x=12,y=160,width=330,height=30)

    load2 = Image.open("Images/search_btn3.png")
    load2 = load2.resize((50, 50), Image.ANTIALIAS)
    search_btn_img = ImageTk.PhotoImage(load2)
    search_btn = Button(frame1,image=search_btn_img,bg="#343534",bd=0,command=on_search)
    search_btn.image = search_btn_img
    search_btn.place(x=360,y=150)

    update_btn = Button(frame1,text="Update",font="cambria 16 bold",bg="#C10AAF",fg="white",command=on_update)
    update_btn.place(x=40,y=250,width=130,height=30)

    remove_btn = Button(frame1,text="Remove",font="cambria 16 bold",bg="#C10AAF",fg="white",command=on_remove)
    remove_btn.place(x=190,y=250,width=130,height=30)

    clear_btn = Button(win,text="Clear",font="cambria 16 bold",bg="#0AB6FF",fg="white",command=on_clear)
    clear_btn.place(x=790,y=490,width=200,height=33)

def books_management():
    win = Toplevel()
    win.title("Books Mangement")
    win.geometry("{0}x{1}+0+0".format(win.winfo_screenwidth(), win.winfo_screenheight()))
    win.configure(bg='#030314')

    #########################ALL VARIABLES############################
    ###style = ttk.Style()
    style.theme_use("clam")
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
    mng_title.grid(row=0,columnspan=2,ipadx=155,ipady=20)

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
    # combostyle = ttk.Style()
    # style.theme_create('combostyle2', parent='alt',
    #                         settings = {'TCombobox':
    #                                     {'configure':
    #                                     {'selectbackground': '#06144D',
    #                                     'fieldbackground': '#06144D',
    #                                     'background': '#4D00FF'
    #                                     }}}
    #                         )
    style.theme_use('combostyle')
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
    ###style = ttk.Style()
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
##############BOOK MANAGEMENT END##############

def rent_books():
    win = Toplevel()
    win.title("Registration Window")
    win.geometry("{0}x{1}+0+0".format(win.winfo_screenwidth(), win.winfo_screenheight()))
    # win.geometry("1200x700")
    win.configure(bg='#343733')
    # win.maxsize(width=1200,height=700)
    # win.minsize(width=1200,height=700)

    #########################ALL VARIABLES############################
    # ###style = ttk.Style()
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
            msg.showerror("None","Record not found")
        except TypeError:
            msg.showerror("None","Record not found")

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
                                                borrow_area.insert(END,f"\n\n Please don't forget to return or renew your book on {renew_date}\nOtherwise you will got the fine of Rs.{fine}ru. per day\n")
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
                                            on_clear()
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
    # combostyle = ttk.Style()
    # style.theme_create('combostyle3', parent='alt',
    #                         settings = {'TCombobox':
    #                                     {'configure':
    #                                     {'selectbackground': '#3C5B37',
    #                                     'fieldbackground': '#3C5B37',
    #                                     'background': '#4D00FF'
    #                                     }}}
    #                         )
    style.theme_use('combostyle')
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
    ###style = ttk.Style()
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
    pass_key_entry = Entry(borrow_frame,width=35,font="cambria 13 bold",bg="#3C5B37",fg="white",textvariable=pass_key_entry_var,show="*")
    pass_key_entry.place(x=100,y=360,width=320,height=25)

    validate_btn = Button(borrow_frame,text="Validate",font="cambria 16 bold",bg="#FF2247",fg="white",command=on_validate)
    validate_btn.place(x=185,y=450,width=150,height=28)
    fetch_data()

def borrow_books_details():
    win = Toplevel()
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
    # combostyle = ttk.Style()
    # style.theme_create('combostyle4', parent='alt',
    #                         settings = {'TCombobox':
    #                                     {'configure':
    #                                     {'selectbackground': '#321111',
    #                                     'fieldbackground': '#321111',
    #                                     'background': '#4D00FF'
    #                                     }}}
    #                         )
    style.theme_use('combostyle')
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
    # style11 = ttk.Style()
    style.configure("Treeview", background="#41231D",foreground="white", fieldbackground="#41231D", rowheight=30,font="arial 13 bold")
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

    
def login():
    if (user_entry_var.get()!="") and (pass_entry_var.get()!=""):
        con = sql.connect(host='localhost', user='root', password='wadgaonmali')
        cursor = con.cursor()
        cursor.execute("use LabManagement")
        cursor.execute("SELECT * FROM member_login")
        result = cursor.fetchall()
        for row in result:
            if user_entry_var.get() == row[0] and pass_entry_var.get() == row[1]:
                navigations()
            else:
                msg.showerror("Error","You given wrong username or password")
    else:
        msg.showwarning("Warning","Please enter username and password.")
    
# ALLL VARIABLES@@@@@@@@@@
user_entry_var = StringVar()
pass_entry_var = StringVar()

load = Image.open("Images/books1.png")
load = load.resize((330, 400), Image.ANTIALIAS)
book_img = ImageTk.PhotoImage(load)
book_img_lbl = Label(win, image=book_img, bg='#610303')
book_img_lbl.image = book_img
book_img_lbl.place(x=10, y=50)

login_lbl = Label(win, text="Owener Login...",font="forte 32", bg="#610303", fg="#00FF80")
login_lbl.place(x=400, y=60)

user_lbl = Label(win, text="Username: ", font="arial 20 bold",bg="#610303", fg="white")
user_lbl.place(x=450, y=140)

user_entry = Entry(win, font="arial 16 bold", bg="#3C0A0A",fg="white", textvariable=user_entry_var)
user_entry.focus_set()
user_entry.place(x=450, y=190, width=390, height=25)

pass_lbl = Label(win, text="Password: ", font="arial 20 bold",bg="#610303", fg="white")
pass_lbl.place(x=450, y=240)

pass_entry = Entry(win, font="arial 16 bold", bg="#3C0A0A",fg="white", textvariable=pass_entry_var,show="*")
pass_entry.place(x=450, y=290, width=390, height=25)

load1 = Image.open("Images/login_btn.png")
load1 = load1.resize((150, 60), Image.ANTIALIAS)
login_btn_img = ImageTk.PhotoImage(load1)
login_btn = Button(win, image=login_btn_img, bg="#610303", bd=0, command=login)
login_btn.image = login_btn_img
login_btn.place(x=570, y=390)


win.mainloop()
