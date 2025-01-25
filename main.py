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

def details():
    try:
        with open("login_data.json", "r") as file:
            login_data = json.load(file)
            
            email = login_data["email"]
            password = login_data["password"]
            name = login_data["Name"]
            lastname = login_data["lastname"]
            contact = login_data["Contact"]
            account_number = login_data["Account Number"]
            balance = login_data["Balance"]
            if balance is None:
                balance = 0
            
            return email, password, name, lastname, contact, account_number, balance
    except FileNotFoundError:
        print("Login data not found. Please log in first.")
        return None, None
    
Email, Password, Name, Lastname, Contact, Account_number, Balance = details()

def update_time():
    time_label.config(text=f"{strftime('%H:%M %p')}")
    top.after(1000, update_time)

def profile(func):
    def check(*args, **kwargs):
        db = sql.connect(host='localhost', user='root', password='7011', db='banking')
        cur = db.cursor()
        acc_num = Account_number
        
        query = """
            SELECT cd.account_number, cd.account_type 
            FROM clients c 
            JOIN clients_details cd ON c.account_number = cd.account_number 
            WHERE c.account_number = %s
        """
        cur.execute(query, (acc_num,))
        result = cur.fetchone()

        if result:
            account_type = result[1]
            if not account_type:
                messagebox.showerror("Error", "Please complete your profile before proceeding.")
            else:
                return func(*args, **kwargs)
        else:
            messagebox.showerror("Error", "No account details found.")
        
        cur.close()
        db.close()
    return check

@profile
def Accounts():
    top.destroy()
    subprocess.call(["python", "accounts&deposits.py"])

@profile
def Deposits():
    top.destroy()
    subprocess.call(["python", "deposit.py"])

@profile
def Loans():
    top.destroy()
    subprocess.call(["python", "Loan.py"])

@profile
def Insurance():
    top.destroy()
    subprocess.call(["python", "Insurance.py"])

@profile
def Investments():
    top.destroy()
    subprocess.call(["python", "Investment.py"])

@profile
def Foriegn():
    top.destroy()
    subprocess.call(["python", "Foriegn_Exchange.py"])

def Profile():
    top.destroy()
    subprocess.call(["python", "Profile.py"])

def Exit():
    top.destroy()


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

frame =LabelFrame(top,width=450,height=800,bg="lightblue")
frame.place(x=1080, y=20)

Heading = Label(top, text=f"Hii! {Name} {Lastname}. \nWelcome to \nABC Bank Corporation.", bg='lightblue', fg='#000000', font=('Bookman Old Style', 30, 'bold'),justify="center")
Heading.place(relx=0.5, y=300, anchor="center")

b1 = Button(frame, cursor="hand2", width=20, pady=7, text='Overview', bg='lightblue', fg='Black', border=5, font=('Bookman Old Style', 15), command=Accounts).place(x=100, y=20)
b2 = Button(frame, cursor="hand2", width=20, pady=7, text='Deposit', bg='lightblue', fg='Black', border=5, font=('Bookman Old Style', 15), command=Deposits).place(x=100, y=120)
b3 = Button(frame, cursor="hand2", width=20, pady=7, text='Loans', bg='lightblue', fg='Black', border=5, font=('Bookman Old Style', 15), command=Loans).place(x=100, y=220)
b4 = Button(frame, cursor="hand2", width=20, pady=7, text='Insurance', bg='lightblue', fg='Black', border=5, font=('Bookman Old Style', 15), command=Insurance).place(x=100, y=320)
b5 = Button(frame, cursor="hand2", width=20, pady=7, text='Investments', bg='lightblue', fg='Black', border=5, font=('Bookman Old Style', 15), command=Investments).place(x=100, y=420)
b6 = Button(frame, cursor="hand2", width=20, pady=7, text='Foriegn Exchange', bg='lightblue', fg='Black', border=5, font=('Bookman Old Style', 15), command=Foriegn).place(x=100, y=520)
b7 = Button(frame, cursor="hand2", width=20, pady=7, text='Profile', bg='lightblue', fg='Black', border=5, font=('Bookman Old Style', 15), command=Profile).place(x=100, y=620)
b8 = Button(frame, cursor="hand2", width=20, pady=7, text='Exit', bg='lightblue', fg='Black', border=5, font=('Bookman Old Style', 15), command=Exit).place(x=100, y=720)

update_time()
top.mainloop()
