from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector as sql
from mysql.connector.errors import Error
from tkinter import messagebox as msg
from datetime import date


win = Tk()
win.title("Registration Window")
win.geometry("1200x750")
win.configure(bg='#343534')
win.maxsize(width=1200,height=750)
win.minsize(width=1200,height=750)

###########VARIABLES#########
style = ttk.Style()
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
    # pass
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

def on_search():
    if (search_by_combo_var.get()!="") and (enter_name_entry_var.get()!=""):
        con=sql.connect(host='localhost',user='root',password='wadgaonmali')
        cursor=con.cursor()
        cursor.execute("use labmanagement")
        cursor.execute("select * from stud_reg")
        result = cursor.fetchall()
        if (search_by_combo_var.get()=="ID"):
            
            for row in result:
                if (enter_name_entry_var.get() == row[0]):
                    # id_entry_var.set(row[0])
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
        elif (search_by_combo_var.get()=="Name"):
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
                # else:
                #     msg.showerror("Error","Record not found")

        cursor.close()
        con.close()
        

    else:
        msg.showwarning("warning","Both fields required!")

# def on_view():
#     pass
#     # pass_key_entry_var.set(pass_key_entry_var.get())
#     # pass_key_entry.config(show=pass_key_entry_var.get())

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
id_entry = Entry(win,font="cambria 13 bold",bg="#343534",fg="white")


name_lbl = Label(win,text="Name:",font="cambria 18 bold",fg="white",bg="#343534")
name_lbl.place(x=30,y=150)
name_entry = Entry(win,font="cambria 13 bold",bg="#252530",fg="white",textvariable=name_entry_var)
name_entry.focus_set()
name_entry.place(x=190,y=153,width=420,height=30)

gender_lbl = Label(win,text="Gender:",font="cambria 18 bold",fg="white",bg="#343534")
gender_lbl.place(x=30,y=210)
gender_combo = ttk.Combobox(win,justify='left',font="arial 12 bold",textvariable=gender_combo_var)

combostyle = ttk.Style()
combostyle.theme_create('combostyle', parent='alt',
                         settings = {'TCombobox':
                                     {'configure':
                                      {'selectbackground': '#252530',
                                       'fieldbackground': '#252530',
                                       'background': 'green'
                                       }}}
                         )
combostyle.theme_use('combostyle')

gender_combo['state'] = 'readonly'
gender_combo['values'] = ('Male','Female')
gender_combo.place(x=190,y=213,width=420,height=30)

mobile_lbl = Label(win,text="Mobile No.:",font="cambria 18 bold",fg="white",bg="#343534")
mobile_lbl.place(x=30,y=270)
ph1_lbl = Label(win,text="Upto 10 digit",font="cambria 9 bold",fg="#B6AEAE",bg="#343534")
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
ph2_lbl = Label(win,text="Format must be: dd/mm/yyyy",font="cambria 9 bold",fg="#B6AEAE",bg="#343534")
ph2_lbl.place(x=190,y=375)
leave_entry = Entry(win,font="cambria 13 bold",bg="#252530",fg="white",textvariable=leave_entry_var)
leave_entry.place(x=190,y=393,width=420,height=30)

address_lbl = Label(win,text="Address:",font="cambria 18 bold",fg="white",bg="#343534")
address_lbl.place(x=30,y=450)
address_entry = Text(win,font="cambria 13 bold",bg="#252530",fg="white")
address_entry.place(x=190,y=453,width=420,height=80)

pass_key_lbl = Label(win,text="Pass Key:",font="cambria 18 bold",fg="white",bg="#343534")
pass_key_lbl.place(x=30,y=560)
ph3_lbl = Label(win,text="Upto 10 character",font="cambria 9 bold",fg="#B6AEAE",bg="#343534")
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

# load3 = Image.open("Images/PicsArt_05-11-12.47.12.png")
# load3 = load3.resize((140, 45), Image.ANTIALIAS)
# remove_btn_img = ImageTk.PhotoImage(load3)
# remove_btn = Button(win,image=remove_btn_img,bg="#343534",bd=0)
# remove_btn.image = remove_btn_img
# remove_btn.place(x=750,y=605)



win.mainloop()