from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
import pymysql as sql
from time import strftime 
import subprocess
import json

top=Tk()
top.title("Registration Form")
top.state("zoomed")
top.resizable(False,False)
top.iconbitmap("Assests\Bank icon.ico")
top.config(bg='lightblue')

logged_in = False


def update_time():
    time_label.config(text=f"{strftime('%H:%M %p')}")
    top.after(1000, update_time)

def register():
    top.destroy()
    subprocess.call(["python", "Registration.py"])

def Exit():
    top.destroy()

def forget():
    top.destroy()
    subprocess.call(["python", "forget.py"])

def login():
    global logged_in
    k1 = Email.get()
    k2 = Password.get()
    if (not k1 or k1 == "Email" or not k2 or k2 == "Password"):
        messagebox.showerror("Error", "All fields are required. Please fill in all the details.")
        return
    db=sql.connect(host='localhost',user='root',password='7011',db='banking')
    cur=db.cursor()
    s = "SELECT email,password FROM clients WHERE email =%s AND password =%s"
    cur.execute(s, (k1, k2))
    result = cur.fetchone()
    if result:
        s= "SELECT * FROM clients WHERE Email=%s AND password =%s"
        v=cur.execute(s,(k1,k2))
        result = cur.fetchall()
        if v > 0:
            for col in result:
                Accounts_no = col[0]
                Name=col[1]
                Lastname = col[2]
                Contact = col[4]
                Balance = col[6]
        login_data = {"email": k1, "password": k2,"Name": Name, "lastname":Lastname,"Contact": Contact,"Account Number":Accounts_no, "Balance":Balance }
        with open("login_data.json", "w") as file:
            json.dump(login_data, file)
            
        logged_in = True
        messagebox.showinfo("Welcome", f"Your Welcome {Name}")
        from smtpEmail import login_email
        login_email()
        top.destroy()
        subprocess.call(["python", "main.py"])
        
    else:
        messagebox.showerror("Result", "Incorrect Access")
    db.close()

path=r"Assests/Login.png"
img = ImageTk.PhotoImage(Image.open(path))
l0 =Label(top,image=img,border=2,bg="lightblue").place(x=10, y=300)

path2=r"Assests\Bank.png"
img2 = ImageTk.PhotoImage(Image.open(path2))
l2 =Label(top,image=img2,border=2,bg="lightblue").place(x=490, y=-170)

date_label = Label(top, text= f"{strftime('%d/%m/%y')}" ,font=("Bookman Old Style", 15), fg="#000000", bg="lightblue")
date_label.place(x=10,y=80)
time_label = Label(top,font=("Bookman Old Style", 15), fg="#000000", bg="lightblue")
time_label.place(x=10,y=110)

frame =LabelFrame(top,width=450,border=10,height=700,bg="lightblue")
frame.place(x=1050, y=120)

Heading = Label(frame, text='Login', bg='lightblue', fg='#000000', font=('Bookman Old Style', 40, 'bold'))
Heading.place(x=130, y=50)

def on_click1(e):
    Email.delete(0,"end")

def on_focus_out1(e):
    email = Email.get()
    if email == "":
        Email.insert(0,"E-mail")

Email=Entry(frame, width=20,fg='#000000', border=0, bg='lightblue', font=('Bookman Old Style', 20))
Email.place(x=50,y=200)
Email.insert(0,"E-mail")
Email.bind("<FocusIn>", on_click1)
Email.bind("<FocusOut>", on_focus_out1)
Emailframe =Frame(frame,width=342,height=2,bg="#000000").place(x=50, y=232)

def on_click2(e):
    Password.delete(0,"end")
    Password.config(show="*")

def on_focus_out2(e):
    password = Password.get()
    if password == "":
        Password.config(show="")
        Password.insert(0,"Password")

Password=Entry(frame, width=20,fg='#000000', border=0, bg='lightblue', font=('Bookman Old Style', 20))
Password.place(x=50,y=300)
Password.insert(0,"Password")
Password.bind("<FocusIn>", on_click2)
Password.bind("<FocusOut>", on_focus_out2)
Passwordframe =Frame(frame,width=342,height=2,bg="#000000").place(x=50, y=332)

l1 = Label(frame, text='Dont have an account?', bg='lightblue', fg='#000000', font=('Bookman Old Style', 15)).place(x=70, y=510)

b1 = Button(frame, cursor="hand2", width=20, pady=7, text='Submit', bg='#50C878', fg='Black', border=0, font=('Arial', 20, "bold"), command=login).place(x=50, y=420)
b2 = Button(frame, cursor="hand2",  pady=7, text='Forgotten Password?', bg='lightblue', fg='Black', border=0, font=('Bookman Old Style', 10), command=forget).place(x=50, y=340)
b3 = Button(frame, cursor="hand2",  pady=7, text='Sign UP', bg='lightblue', fg='Blue', border=0, font=('Bookman Old Style', 15, 'bold'), command=register).place(x=300, y=500)
b4 = Button(top, cursor="hand2", width=10, pady=7, text='Exit', bg='lightblue', fg='Black', border=5, font=('Bookman Old Style', 15), command=exit).place(x=1380, y=10)

update_time()
top.mainloop()
