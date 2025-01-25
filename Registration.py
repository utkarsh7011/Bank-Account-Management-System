from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
import pymysql as sql
import re
from time import strftime 
import subprocess

top=Tk()
top.title("Registration Form")
top.state("zoomed")
top.resizable(False,False)
top.iconbitmap("Assests\Bank icon.ico")
top.config(bg='lightblue')

def insert():
    k1 = Name1.get()
    k2 = Lastname1.get()
    k3 = Email1.get()
    k4 = Contact1.get()
    k5 = Password1.get()
    
    try:
        db = sql.connect(host='localhost', user='root', password='7011', db='Banking')
        cur = db.cursor()

        query_check = "SELECT email, contact FROM clients WHERE Email=%s OR Contact=%s"
        cur.execute(query_check, (k3, k4))
        checking = cur.fetchone()

        if checking:   
            if checking[0] == k3:
                messagebox.showerror("Error", "Email Already Registered")
            if int(checking[1]) == int(k4):
                messagebox.showerror("Error", "Contact Already Registered")
            return

        if not all([k1, k2, k3, k4, k5]) or k1 == "Name" or k2 == "Lastname" or k3 == "Email" or k4 == "Contact" or k5 == "Password":
            messagebox.showerror("Error", "All fields are mandatory. Please complete all required details.")
            return
        
        if len(k5) < 8:
            messagebox.showerror("Invalid Password", "Password must be at least 8 characters long.")
            return
        elif not re.search(r"[A-Z]", k5):
            messagebox.showerror("Invalid Password", "Password must contain at least one uppercase letter.")
            return
        elif not re.search(r"\d", k5):
            messagebox.showerror("Invalid Password", "Password must contain at least one digit.")
            return
        elif not re.search(r"[!@#$%^&*(),.?\":{}|<>]", k5):
            messagebox.showerror("Invalid Password", "Password must contain at least one special character.")
            return
        
        confirm = messagebox.askyesno("Confirm Registration", f"Are you sure you want to register in ABC Bank Corporation?")
        if not confirm:
            return

        query_insert_client = "INSERT INTO clients (Name, Lastname, Email, Contact, Password, balance) VALUES (%s, %s, %s, %s, %s, %s)"
        values_client = (k1, k2, k3, k4, k5, 0) 
        cur.execute(query_insert_client, values_client)
        db.commit()

        cur.execute("SELECT LAST_INSERT_ID()")
        account_number = cur.fetchone()[0]

        query_insert_details = "INSERT INTO clients_details (account_number) VALUES (%s)"
        cur.execute(query_insert_details, (account_number,))
        db.commit()

        messagebox.showinfo("Registration Complete", f"Your registration has been successfully completed. Your official Account Number is {account_number}.") 
        top.destroy()
        subprocess.call(["python", "login.py"])

    except sql.MySQLError as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
    finally:
        db.close()


def Back2():
    top.destroy()
    subprocess.call(["python", "login.py"])

def update_time():
    time_label.config(text=f"{strftime('%H:%M %p')}")
    date_label.after(1000, update_time)


path=r"Assests/Login.png"
img = ImageTk.PhotoImage(Image.open(path))
l0 =Label(top,image=img,border=2,bg="lightblue").place(x=10, y=300)

path2=r"Assests\Bank.png"
img2 = ImageTk.PhotoImage(Image.open(path2))
l2 =Label(top,image=img2,border=2,bg="lightblue").place(x=490, y=-170)

date_label = Label(top, text= f"{strftime('%d/%m/%y')}" ,font=("Bookman Old Style", 15), fg="black", bg="lightblue")
date_label.place(x=10,y=80)
time_label = Label(top,font=("Bookman Old Style", 15), fg="black", bg="lightblue")
time_label.place(x=10,y=110)

frame =Frame(top,width=450,height=730,bg="lightblue")
frame.place(x=1050, y=100)

Heading = Label(frame, text='Register Yourself', bg='lightblue', fg='Black', font=('Bookman Old Style', 30, 'bold'))
Heading.place(x=30, y=50)

def on_click1(e):
    Name1.delete(0,"end")
    Name1.config(validate="key",validatecommand=Customername)

def on_focus_out1(e):
    name = Name1.get()
    if name == "":
        Name1.config(validate="none")
        Name1.insert(0,"Name")

def validate_name_input(char, value):
    if value == "":
        return True
    if char.isalpha():
        return True
    return False
Customername = (top.register(validate_name_input), "%S", "%P")

Name1=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20))
Name1.place(x=50,y=150)
Name1.insert(0,"Name")
Name1.bind("<FocusIn>", on_click1)
Name1.bind("<FocusOut>", on_focus_out1)
Nameframe1 =Frame(frame,width=342,height=2,bg="black").place(x=50, y=182)

def on_click2(e):
    Lastname1.delete(0,"end")
    Lastname1.config(validate="key",validatecommand=Customername)

def on_focus_out2(e):
    lastname = Lastname1.get()
    if lastname == "":
        Lastname1.config(validate="none")
        Lastname1.insert(0,"Lastname")

Lastname1=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20))
Lastname1.place(x=50,y=250)
Lastname1.insert(0,"Lastname")
Lastname1.bind("<FocusIn>", on_click2)
Lastname1.bind("<FocusOut>", on_focus_out2)
Lastnameframe1 =Frame(frame,width=342,height=2,bg="black").place(x=50, y=282)

def on_click3(e):
    Email1.delete(0,"end")

def on_focus_out3(e):
    email = Email1.get()
    if email == "":
        Email1.insert(0,"Email")

Email1=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20))
Email1.place(x=50,y=350)
Email1.insert(0,"Email")
Email1.bind("<FocusIn>", on_click3)
Email1.bind("<FocusOut>", on_focus_out3)
Emailframe1 =Frame(frame,width=342,height=2,bg="black").place(x=50, y=382)

def on_click4(e):
    Contact1.delete(0,"end")
    Contact1.config(validate="key", validatecommand=phone)

def on_focus_out4(e):
    contact = Contact1.get()
    if contact == "":
        Contact1.config(validate="none")
        Contact1.insert(0,"Contact")

def validate_digit_input(P):
    return P.isdigit() or P == ""

phone = (top.register(validate_digit_input), '%P')

Contact1=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20))
Contact1.place(x=50,y=450)
Contact1.insert(0,"Contact")
Contact1.bind("<FocusIn>", on_click4)
Contact1.bind("<FocusOut>", on_focus_out4)
Contactframe1 =Frame(frame,width=342,height=2,bg="black").place(x=50, y=482)

def on_click5(e):
    Password1.delete(0,"end")
    Password1.config(show="*")

def on_focus_out5(e):
    name = Password1.get()
    if name == "":
        Password1.config(show="")
        Password1.insert(0,"Password")

Password1=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20))
Password1.place(x=50,y=550)
Password1.insert(0,"Password")
Password1.bind("<FocusIn>", on_click5)
Password1.bind("<FocusOut>", on_focus_out5)
Passwordframe1 =Frame(frame,width=342,height=2,bg="black").place(x=50, y=582)

b1=Button(frame,cursor="hand2", width=20, pady=7, text='Submit', bg='#98FF98',fg='Black', border=0, font=('Arial', 20, "bold"), command=insert).place(x=50, y=620)
b2=Button(top,cursor="hand2", width=5, pady=7, text='←', bg="lightblue",fg='Black', border=0, font=('Arial', 15, "bold"), command=Back2).place(x=5, y=2)

update_time()
top.mainloop()
