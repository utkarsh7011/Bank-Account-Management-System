from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
import pymysql as sql
import re
from time import strftime 
import subprocess
import json

top=Tk()
top.title("Registration Form")
top.state("zoomed")
top.resizable(False,False)
top.iconbitmap("Assests\Bank icon.ico")
top.config(bg='lightblue')

def get_login_data():
    try:
        with open("login_data.json", "r") as file:
            login_data = json.load(file)
            
            email = login_data["email"]
            password = login_data["password"]
            name = login_data["Name"]
            lastname = login_data["lastname"]
            contact = login_data["Contact"]
            account_number = login_data["Account Number"]
            
            return email, password, name, lastname, contact, account_number 
    except FileNotFoundError:
        print("Login data not found. Please log in first.")
        return None, None
    
Email, Password, Name, Lastname, Contact, Account_number = get_login_data()

def getbalance():
    global Balance
    db = sql.connect(host='localhost', user='root', password='7011', db='banking')
    cur = db.cursor()
    query = query = """SELECT balance from clients where account_number =%s"""
    try:
        cur.execute(query, (Account_number))
        result = cur.fetchall()
        if result:
            for col in result:
                Balance =col[0]
                
        else:
            messagebox.showerror("Error", "No Record Found")

    except Exception as error:
        messagebox.showerror("Error", error)
        print(error)

    finally:
        cur.close()
        db.close()

getbalance()

def typed():
    global Account
    db = sql.connect(host='localhost', user='root', password='7011', db='banking')
    cur = db.cursor()
    query = query = """SELECT cd.account_number, cd.account_type FROM clients c 
                        JOIN clients_details cd ON 
                        c.account_number = cd.account_number 
                        WHERE c.account_number =%s"""
    try:
        cur.execute(query, (Account_number))
        result = cur.fetchall()
        if result:
            for col in result:
                Account =col[1]
                
        else:
            messagebox.showerror("Error", "No Record Found")

    except Exception as error:
        messagebox.showerror("Error", error)
        print(error)

    finally:
        cur.close()
        db.close()

typed()



def Details():
    global Account, Deposit, Loan, Insurance, Investment
    db = sql.connect(host='localhost', user='root', password='7011', db='banking')
    cur = db.cursor()
    query = """select cd.account_number, cd.deposit_type, cd.loan_type, cd.insurance_type, cd.investment_type 
                from clients c JOIN clients_details cd 
                on c.account_number = cd.account_number 
                where c.account_number =%s;"""
    try:
        cur.execute(query, (Account_number))
        result = cur.fetchone()
        if result:
            Deposit = result[1] if result[1] else "No Deposit"
            Loan = result[2] if result[2] else "No Loan"
            Insurance = result[3] if result[3] else "No Insurance"
            Investment = result[4] if result[4] else "No Investment"
        else:
            messagebox.showerror("Error","No Record Found")
    except Exception as error:
        messagebox.showerror("Error", error)
        print(error)
    finally:
        cur.close()
        db.close()

Details()

def Detailsamount():
    global Account, A_Deposit, A_Loan, A_Insurance, A_Investment
    db = sql.connect(host='localhost', user='root', password='7011', db='banking')
    cur = db.cursor()
    query = """select cd.account_number, cd.deposit_amount, cd.loan_amount, cd.insurance_amount, cd.investment_amount 
                from clients c JOIN clients_details cd 
                on c.account_number = cd.account_number 
                where c.account_number =%s;"""
    try:
        cur.execute(query, (Account_number))
        result = cur.fetchone()
        if result:
            A_Deposit = result[1] if result[1] else "0"
            A_Loan = result[2] if result[2] else "0"
            A_Insurance = result[3] if result[3] else "0"
            A_Investment = result[4] if result[4] else "0"
        else:
            messagebox.showerror("Error","No Record Found")
    except Exception as error:
        messagebox.showerror("Error", error)
        print(error)
    finally:
        cur.close()
        db.close()

Detailsamount()

def update_time():
    time_label.config(text=f"{strftime('%H:%M %p')}")
    top.after(1000, update_time)

def accountdetails():
    frame2.place(x=1050, y=20)
    AHeading.place(relx=0.5, y=200, anchor="center")
    b5.place(x=5, y=2)
    frame.place_forget()
    DHeading.place_forget()
    b0.place_forget()
    b1.place_forget()
    b2.place_forget()
    b7.place_forget()

def default():
    frame.place(x=1050, y=20)
    b0.place(x=5, y=5)
    b1.place(x=30, y=210)
    b2.place(x=315, y=210)
    b5.place_forget()
    b7.place_forget()
    AHeading.place_forget()
    DHeading.place_forget()
    frame2.place_forget()
    frame3.place_forget()

def deposits():
    frame3.place(x=1050, y=20)
    DHeading.place(relx=0.5, y=200, anchor="center")
    b7.place(x=5, y=2)
    AHeading.place_forget()
    frame.place_forget()
    frame2.place_forget()
    b0.place_forget()
    b1.place_forget()
    b2.place_forget()
    b5.place_forget()
    
def login():
    top.destroy()
    subprocess.call(["python", "main.py"])


path=r"Assests/Login.png"
img = ImageTk.PhotoImage(Image.open(path))
l0 =Label(top,image=img,border=2,bg="lightblue")
l0.place(x=10, y=300)

path2=r"Assests\Bank.png"
img2 = ImageTk.PhotoImage(Image.open(path2))
l2 =Label(top,image=img2,border=2,bg="lightblue")
l2.place(x=490, y=-170)

date_label = Label(top, text= f"{strftime('%d/%m/%y')}" ,font=("Bookman Old Style", 15), fg="#000000", bg="lightblue")
date_label.place(x=10,y=80)
time_label = Label(top,font=("Bookman Old Style", 15), fg="#000000", bg="lightblue")
time_label.place(x=10,y=110)

frame =LabelFrame(top,width=450,height=800,bg="lightblue")
frame.place(x=1050, y=20)

account_number1=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
account_number1.place(x=50,y=150)
account_number1.insert(0,f"{Account_number}")
account_number1.config(state="readonly",readonlybackground="lightblue")
frameaccnumber1 =Frame(frame,width=342,height=2,bg="black").place(x=50, y=182)

Name1=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
Name1.place(x=50,y=250)
Name1.insert(0,f"{Name} {Lastname}")
Name1.config(state="readonly",readonlybackground="lightblue")
framename1 =Frame(frame,width=342,height=2,bg="black").place(x=50, y=282)

Email1=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
Email1.place(x=50,y=350)
Email1.insert(0,f"{Email}")
Email1.config(state="readonly",readonlybackground="lightblue")
frameemail1 =Frame(frame,width=342,height=2,bg="black").place(x=50, y=382)

contact1=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
contact1.place(x=50,y=450)
contact1.insert(0,f"{Contact}")
contact1.config(state="readonly",readonlybackground="lightblue")
framecontact1 =Frame(frame,width=342,height=2,bg="black").place(x=50, y=482)

account1=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
account1.place(x=50,y=550)
account1.insert(0,f"{Account}")
account1.config(state="readonly",readonlybackground="lightblue")
frameaccount1 =Frame(frame,width=342,height=2,bg="black").place(x=50, y=582)

balance1=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
balance1.place(x=50,y=650)
balance1.insert(0,f"{Balance}/-")
balance1.config(state="readonly",readonlybackground="lightblue")
framebalance1 =Frame(frame,width=342,height=2,bg="black").place(x=50, y=682)



##############################frame2####################################################################################################################################################################################



frame2 =LabelFrame(top,width=450,height=800,bg="lightblue")
frame2.place_forget()

AHeading = Label(top, text='My Subscribed Services', bg='lightblue', fg='Black', font=('Bookman Old Style', 30, 'bold'),justify="center")
AHeading.place_forget()

account_number2 = Entry(frame2, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
account_number2.place(x=50,y=50)
account_number2.insert(0,f"{Account_number}")
account_number2.config(state="readonly",readonlybackground="lightblue")
frameaccnumber2 =Frame(frame2,width=342,height=2,bg="black").place(x=50, y=82)

Name2=Entry(frame2, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
Name2.place(x=50,y=150)
Name2.insert(0,f"{Name} {Lastname}")
Name2.config(state="readonly",readonlybackground="lightblue")
framename2 =Frame(frame2,width=342,height=2,bg="black").place(x=50, y=182)

contact2=Entry(frame2, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
contact2.place(x=50,y=250)
contact2.insert(0,f"{Contact}")
contact2.config(state="readonly",readonlybackground="lightblue")
framecontact2 =Frame(frame2,width=342,height=2,bg="black").place(x=50, y=282)

account_type2=Entry(frame2, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
account_type2.place(x=50,y=350)
account_type2.insert(0,f"{Account}")
account_type2.config(state="readonly",readonlybackground="lightblue")
frameaccount_type2 =Frame(frame2,width=342,height=2,bg="black").place(x=50, y=382)

deposite_type2=Entry(frame2, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
deposite_type2.place(x=50,y=450)
deposite_type2.insert(0,f"{Deposit}")
deposite_type2.config(state="readonly",readonlybackground="lightblue")
framedeposite_type2 =Frame(frame2,width=342,height=2,bg="black").place(x=50, y=482)

loan_type=Entry(frame2, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
loan_type.place(x=50,y=550)
loan_type.insert(0,f"{Loan}")
loan_type.config(state="readonly",readonlybackground="lightblue")
frameloan_type =Frame(frame2,width=342,height=2,bg="black").place(x=50, y=582)

insurance_Type =Entry(frame2, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
insurance_Type .place(x=50,y=650)
insurance_Type .insert(0,f"{Insurance}")
insurance_Type .config(state="readonly",readonlybackground="lightblue")
frameinsurance_Type  =Frame(frame2,width=342,height=2,bg="black").place(x=50, y=682)

investment_Type=Entry(frame2, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
investment_Type.place(x=50,y=750)
investment_Type.insert(0,f"{Investment}")
investment_Type.config(state="readonly",readonlybackground="lightblue")
frameinvestment_Type =Frame(frame2,width=342,height=2,bg="black").place(x=50, y=782)



##############################frame3############################################################################################################################################################



frame3 =LabelFrame(top,width=450,height=800,bg="lightblue")
frame3.place_forget()

DHeading = Label(top, text='My Financial Profile', bg='lightblue', fg='Black', font=('Bookman Old Style', 30, 'bold'),justify="center")
DHeading.place_forget()

account_number3=Entry(frame3, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
account_number3.place(x=50,y=50)
account_number3.insert(0,f"{Account_number}")
account_number3.config(state="readonly",readonlybackground="lightblue")
frameaccnumber3 =Frame(frame3,width=342,height=2,bg="black").place(x=50, y=82)

Name3=Entry(frame3, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
Name3.place(x=50,y=150)
Name3.insert(0,f"{Name} {Lastname}")
Name3.config(state="readonly",readonlybackground="lightblue")
framename3 =Frame(frame3,width=342,height=2,bg="black").place(x=50, y=182)

contact3=Entry(frame3, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
contact3.place(x=50,y=250)
contact3.insert(0,f"{Contact}")
contact3.config(state="readonly",readonlybackground="lightblue")
framecontact3 =Frame(frame3,width=342,height=2,bg="black").place(x=50, y=282)

balance2=Entry(frame3, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
balance2.place(x=50,y=350)
balance2.insert(0,f"Balance :- {Balance}/-")
balance2.config(state="readonly",readonlybackground="lightblue")
framebalance2 =Frame(frame3,width=342,height=2,bg="black").place(x=50, y=382)

deposite_amount=Entry(frame3, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
deposite_amount.place(x=50,y=450)
deposite_amount.insert(0,f"{Deposit} :- {A_Deposit}/-")
deposite_amount.config(state="readonly",readonlybackground="lightblue")
framedeposite_amount =Frame(frame3,width=342,height=2,bg="black").place(x=50, y=482)

loan_amount=Entry(frame3, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
loan_amount.place(x=50,y=550)
loan_amount.insert(0,f"{Loan} :- {A_Loan}/-")
loan_amount.config(state="readonly",readonlybackground="lightblue")
frameloan_amount =Frame(frame3,width=342,height=2,bg="black").place(x=50, y=582)

insurance_amount =Entry(frame3, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
insurance_amount .place(x=50,y=650)
insurance_amount .insert(0,f"{Insurance} :- {A_Insurance}/-")
insurance_amount .config(state="readonly",readonlybackground="lightblue")
frameinsurance_amount  =Frame(frame3,width=342,height=2,bg="black").place(x=50, y=682)

investment_amount=Entry(frame3, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
investment_amount.place(x=50,y=750)
investment_amount.insert(0,f"{Investment} :- {A_Investment}/-")
investment_amount.config(state="readonly",readonlybackground="lightblue")
frameinvestment_amount =Frame(frame3,width=342,height=2,bg="black").place(x=50, y=782)


b0 = Button(top,cursor="hand2", width=5, pady=7, text='←', bg="lightblue",fg='Black', border=0, font=('Arial', 15, "bold"), command=login)
b0.place(x=5,y=5)
b1 = Button(top, cursor="hand2", width=20, pady=7, text='Services Overview', bg='lightblue', fg='Black', border=10, font=('Bookman Old Style', 15),command=accountdetails)
b1.place(x=50, y=250)
b2 = Button(top, cursor="hand2", width=20, pady=7, text='Financial Dashboard', bg='lightblue', fg='Black', border=10, font=('Bookman Old Style', 15),command=deposits)
b2.place(x=335, y=250)
b5 = Button(frame2,cursor="hand2", width=5, pady=7, text='←', bg="lightblue",fg='Black', border=0, font=('Arial', 15, "bold"), command=default)
b5.place_forget()
b7 = Button(frame3,cursor="hand2", width=5, pady=7, text='←', bg="lightblue",fg='Black', border=0, font=('Arial', 15, "bold"), command=default)
b7.place_forget()

update_time()
top.mainloop()
