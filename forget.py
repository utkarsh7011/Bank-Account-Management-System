from tkinter import *
import pymysql as sql
from PIL import Image,ImageTk
from tkinter import messagebox
from time import strftime
import re
import subprocess

top=Tk()
top.title("Forget Password")
top.state("zoomed")
top.resizable(False,False)
top.iconbitmap("Assests\Bank icon.ico")
top.config(bg='lightblue')

def search():
    k1 = Account.get()
    k2 = Email2.get()
    k3 = Contact2.get()
    k4 = Password2.get()
    k5 = Confirm2.get()

    if (not k1 or k1 == "Account No." or not k2 or k2 == "Email" or not k3 or k3 == "Contact" or not k4 or k4 == "New Password" or not k5 or k5 == "Confirm"):
        messagebox.showerror("Error", "All fields are required. Please fill in all the details.")
        return
    if k4 != k5:
        messagebox.showerror("Error", "Passwords do not match")
        return

    if len(k4) < 8:
        messagebox.showerror("Invalid Password", "Password must be at least 8 characters long.")
        return
    elif not re.search(r"[A-Z]", k4):
        messagebox.showerror("Invalid Password", "Password must contain at least one uppercase letter.")
        return
    elif not re.search(r"\d", k4):
        messagebox.showerror("Invalid Password", "Password must contain at least one digit.")
        return
    elif not re.search(r"[!@#$%^&*(),.?\":{}|<>]", k4):
        messagebox.showerror("Invalid Password", "Password must contain at least one special character.")
        return
    
    db = sql.connect(host='localhost', user='root', password='7011', db='banking')
    cur = db.cursor()
    s = "UPDATE clients SET Password=%s WHERE Account_Number=%s AND Email=%s AND Contact=%s"
    value = (k4,k1,k2,k3)
    cur.execute(s, value)
    db.commit()
    print(f"Executing SQL: {s} with values {value}") 
    print(f"Rows affected: {cur.rowcount}")
    if cur.rowcount > 0:
        messagebox.showinfo("Password", "Password reset successfully")
        top.destroy()
        subprocess.call(["python", "login.py"])
    else:
        messagebox.showerror("Error", "Password reset failed. Please check your details.")
        
def back1():
    top.destroy()
    subprocess.call(["python", "login.py"])

def update_time():
    time_label.config(text=f"{strftime('%H:%M %p')}")
    date_label.after(1000, update_time)

path=r"Assests\Login.png"
img = ImageTk.PhotoImage(Image.open(path))
l0 =Label(top,image=img,border=0,bg="lightblue").place(x=10, y=300)

path2=r"Assests\Bank.png"
img2 = ImageTk.PhotoImage(Image.open(path2))
l2 =Label(top,image=img2,border=0,bg="lightblue").place(x=490, y=-170)

frame =Frame(top,width=450,height=730,bg="lightblue")
frame.place(x=1050, y=100)

date_label = Label(top, text= f"{strftime('%d/%m/%y')}" ,font=("Bookman Old Style", 15), fg="black", bg="lightblue")
date_label.place(x=10,y=80)
time_label = Label(top, font=("Bookman Old Style", 15), fg="black", bg="lightblue")
time_label.place(x=10,y=110)

Heading = Label(frame, text='Password Recovery', bg='lightblue', fg='Black', font=('Bookman Old Style', 30, 'bold'))
Heading.place(x=30, y=50)

def on_click1(e):
    Account.delete(0,"end")
    Account.config(validate="key", validatecommand=customeridentity)

def on_focus_out1(e):
    account = Account.get()
    if account == "":
        Account.config(validate="none")
        Account.insert(0,"Account No.")

def validate_digit_input(P):
    return P.isdigit() or P == ""

customeridentity = (top.register(validate_digit_input), '%P')

Account=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20))
Account.place(x=50,y=150)
Account.insert(0,"Account No.")
Account.bind("<FocusIn>", on_click1)
Account.bind("<FocusOut>", on_focus_out1)
frame2 =Frame(frame,width=342,height=2,bg="black").place(x=50, y=182)

def on_click2(e):
    Email2.delete(0,"end")

def on_focus_out2(e):
    email = Email2.get()
    if email == "":
        Email2.insert(0,"Email")

Email2=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20))
Email2.place(x=50,y=250)
Email2.insert(0,"Email")
Email2.bind("<FocusIn>", on_click2)
Email2.bind("<FocusOut>", on_focus_out2)
Emailframe2 =Frame(frame,width=342,height=2,bg="black").place(x=50, y=282)

def on_click3(e):
    Contact2.delete(0,"end")
    Contact2.config(validate="key", validatecommand=phone)

def on_focus_out3(e):
    contact = Contact2.get()
    if contact == "":
        Contact2.config(validate="none")
        Contact2.insert(0,"Contact")

phone = (top.register(validate_digit_input), '%P')

Contact2=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20))
Contact2.place(x=50,y=350)
Contact2.insert(0,"Contact")
Contact2.bind("<FocusIn>", on_click3)
Contact2.bind("<FocusOut>", on_focus_out3)
Contactframe2 =Frame(frame,width=342,height=2,bg="black").place(x=50, y=382)

def on_click4(e):
    Password2.delete(0,"end")
    Password2.config(show="*")

def on_focus_out4(e):
    password = Password2.get()
    if password == "":
        Password2.config(show="")
        Password2.insert(0,"New Password")

Password2=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20))
Password2.place(x=50,y=450)
Password2.insert(0,"New Password")
Password2.bind("<FocusIn>", on_click4)
Password2.bind("<FocusOut>", on_focus_out4)
Passwordframe2 =Frame(frame,width=342,height=2,bg="black").place(x=50, y=482)

def on_click5(e):
    Confirm2.delete(0,"end")
    Confirm2.config(show="*")

def on_focus_out5(e):
    confirm = Confirm2.get()
    if confirm == "":
        Confirm2.config(show="")
        Confirm2.insert(0,"Confirm")

Confirm2=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20))
Confirm2.place(x=50,y=550)
Confirm2.insert(0,"Confirm Password")
Confirm2.bind("<FocusIn>", on_click5)
Confirm2.bind("<FocusOut>", on_focus_out5)
Confirmframe2 =Frame(frame,width=342,height=2,bg="black").place(x=50, y=582)

b1=Button(frame,cursor="hand2", width=20, pady=7, text='Submit', bg='#98FF98',fg='Black', border=0, font=('Arial', 20, "bold"), command=search).place(x=50, y=650)
b2=Button(top,cursor="hand2", width=5, pady=7, text='←', bg="lightblue",fg='Black', border=0, font=('Arial', 15, "bold"), command=back1).place(x=5, y=2)

update_time()
top.mainloop()
