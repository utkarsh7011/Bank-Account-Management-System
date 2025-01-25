from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk
import pymysql as sql
import re
import math
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
            balance = login_data["Balance"]
            
            return email, password, name, lastname, contact, account_number, balance
    except FileNotFoundError:
        print("Login data not found. Please log in first.")
        return None, None
    
Email, Password, Name, Lastname, Contact, Account_number , BalanceAcc= get_login_data()


def typed():
    global Deposit ,Balance
    db = sql.connect(host='localhost', user='root', password='7011', db='banking')
    cur = db.cursor()
    query = query = """SELECT cd.deposit_type,cd.deposit_amount FROM clients c 
                        JOIN clients_details cd ON 
                        c.account_number = cd.account_number 
                        WHERE c.account_number =%s"""
    try:
        cur.execute(query, (Account_number))
        result = cur.fetchall()
        if result:
            for col in result:
                Deposit =col[0] if col[0] else "No Deposit"
                Balance =col[1] if col[1] else "No Deposit"
                
        else:
            messagebox.showerror("Error", "No Record Found")
    except Exception as error:
        messagebox.showerror("Error", error)
        print(error)

    finally:
        cur.close()
        db.close()

typed()


def update_time():
    time_label.config(text=f"{strftime('%H:%M %p')}")
    top.after(1000, update_time)

def default():
    frame.place(x=1050, y=20)
    b0.place(x=5, y=5)
    b2.place(x=700, y=750)
    b5.place_forget()
    b6.place_forget()
    b7.place_forget()
    AHeading.place(relx=0.5, y=200, anchor="center")
    DAHeading.place(relx=0.5, y=80, anchor="center")
    DHeading.place_forget()
    frame3.place_forget()

def deposits():
    AHeading.place_forget()
    frame3.place(x=1050, y=20)
    DHeading.place(relx=0.5, y=200, anchor="center")
    DAHeading.place_forget()
    b5.place(x=50, y=620)
    b6.place(x=50, y=700)
    b7.place(x=5, y=2)
    frame.place_forget()
    b0.place_forget()
    b2.place_forget()
    
def login():
    top.destroy()
    subprocess.call(["python", "main.py"])

def returnamount():
    k1 = deposit_amount1.get()
    k2 = PDeposit_type.get()
    k3 = PDeposit_years.get()

    if k1 == "Deposit Amount" or not k1:
        messagebox.showerror("Error", "Please fill in all the required details: Deposit Amount.")
        return

    if k2 == "Select Your Deposit" or not k2:
        messagebox.showerror("Error", "Please fill in all the required details: Deposit Type.")
        return

    if k3 == "Number of years" or not k3:
        messagebox.showerror("Error", "Please fill in all the required details: Number of years.")
        return

    try:
        interest_rate = next(key for key, value in Deposit_type_dict.items() if value == k2)
    except StopIteration:
        messagebox.showerror("Error", "Invalid deposit type selected.")
        return

    try:
        years = int(k3.split()[0])
    except ValueError:
        messagebox.showerror("Error", "Invalid deposit time value. Please select a valid number of years.")
        return

    try:
        deposit_amount = float(k1)
    except ValueError:
        messagebox.showerror("Error", "Invalid deposit amount. Please enter a valid number.")
        return
    
    if not deposit_amount or not k2 or not years:
        messagebox.showerror("Error", "Please fill in all the required details.")
        return

    if deposit_amount < 10000:
        messagebox.showerror("Error", "Deposit amount must be ₹10,000 or higher.")
        return

    try:
        interest_rate = next(key for key, value in Deposit_type_dict.items() if value == k2)
    except KeyError:
        messagebox.showerror("Error", "Invalid deposit type selected.")
        return

    if interest_rate == 0:
        messagebox.showerror("Error", "Please select a valid deposit type.")
        return

    if k2 == "Recurring Deposit":
        months = years * 12
        monthly_rate = interest_rate / (12 * 100) 
        total_contribution = deposit_amount * months
        final_amount = deposit_amount * ((math.pow(1 + monthly_rate, months) - 1) / monthly_rate) * (1 + monthly_rate)

    elif k2 == "Savings Account Deposit": 
        quarterly_rate = interest_rate / 400
        final_amount = deposit_amount * math.pow(1 + quarterly_rate, 4 * years) 

    elif k2 in ("Fixed Deposit", "Foreign Currency Non-Resident Deposit"):
        annual_rate = interest_rate / 100
        final_amount = deposit_amount * math.pow(1 + annual_rate, years) 

    elif k2 == "Current Account Deposit":
        annual_rate = interest_rate / 100
        interest = deposit_amount * annual_rate * years
        final_amount = deposit_amount + interest

    else:
        messagebox.showerror("Error", "Invalid deposit type.")
        return
    
    total_contribution = deposit_amount * months if k2 == "Recurring Deposit" else deposit_amount 
    interest = final_amount - total_contribution if k2 == "Recurring Deposit" else final_amount - deposit_amount

    messagebox.showinfo(
        "Interest",
        f"Final Amount: ₹{final_amount:.2f}\nInterest Earned: ₹{interest:.2f}\nTotal Contribution: ₹{total_contribution:.2f}\nInterest Rate: {interest_rate}%",
    )

    return_deposit.config(state="normal")
    return_deposit.delete(0, "end")
    return_deposit.insert(0, f"Final Amount: ₹{final_amount:.2f}")
    return_deposit.config(state="readonly", readonlybackground="Lightblue")

def deposittype():
    A0 = Password3.get()
    A1 = PDeposit_type.get()
    A2 = Account_number
    A3 = deposit_amount1.get()
    A5 = return_deposit.get()
    A6 = PDeposit_years.get()
    returnamount()
    
    if A5 == "Return" or not A5:
        messagebox.showerror("Error", "Please fill in all the required details: Return.")
        return

    A5_cleaned = re.sub(r'[^\d.-]', '', A5).strip()

    if A5_cleaned.endswith('-'):
        A5_cleaned = A5_cleaned[:-1]

    try:
        A5 = float(A5_cleaned)
    except ValueError:
        messagebox.showerror("Error", "Invalid deposit return value. Please enter a valid number.")
        return

    try:
        A6_key = [key for key, value in years_dict.items() if value == A6][0]
    except IndexError:
        messagebox.showerror("Error", "Invalid deposit time value. Please select a valid number of years.")
        return
    
    if not A0 or A0 == "Password":
        messagebox.showerror("Error", "Password cannot be empty.")
        return

    try:
        db = sql.connect(host="localhost", user="root", password="7011", db="banking")
        cur = db.cursor()

        cur.execute("SELECT password FROM clients WHERE account_number = %s;", (A2,))
        result = cur.fetchone()
        if not result:
            messagebox.showerror("Error", "Account number not found.")
            return
        db_password = result[0]
        if db_password != A0:
            messagebox.showerror("Error", "Incorrect Password.")
            return

        cur.execute("SELECT Deposit_Type FROM clients_details WHERE Account_Number = %s;", (A2,))
        exist_Deposit_type = cur.fetchone()

        if exist_Deposit_type and exist_Deposit_type[0]:
            messagebox.showinfo("Depsoit Exist",f"Deposit already exists: '{exist_Deposit_type[0]}'. No update performed.")
        else:
            confirm = messagebox.askyesno("Confirm Deposit", f"Are you sure you want to make a deposit of {A3}?")
            if not confirm:
                return
            
            cur.execute(
            """
            UPDATE clients_details
            SET Deposit_Type = %s, Deposit_Amount = %s, Deposit_Time = %s, Deposit_Return = %s
            WHERE Account_Number = %s;
            """,
            (A1, A3, A6_key, A5, A2),
        )
            db.commit()
            from smtpEmail import Deposit_Email
            Deposit_Email()
            messagebox.showinfo("Successful",f"Your {A1} has been successfully approved.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        db.close()


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

AHeading = Label(top, text='Deposit Management', bg='lightblue', fg='Black', font=('Bookman Old Style', 30, 'bold'),justify="center")
AHeading.place(relx=0.5, y=200, anchor="center")

DAHeading = Label(frame, text='Deposit Application', bg='lightblue', fg='Black', font=('Bookman Old Style', 30, 'bold'),justify="center")
DAHeading.place(relx=0.5, y=80, anchor="center")

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

deposit_account=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
deposit_account.place(x=50,y=550)
deposit_account.insert(0,f"{Deposit}")
deposit_account.config(state="readonly",readonlybackground="lightblue")
framedeposit_account =Frame(frame,width=342,height=2,bg="black").place(x=50, y=582)

balance1=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
balance1.place(x=50,y=650)
balance1.insert(0,f"{Balance}")
balance1.config(state="readonly",readonlybackground="lightblue")
framebalance1 =Frame(frame,width=342,height=2,bg="black").place(x=50, y=682)

###############################frame3

frame3 =LabelFrame(top,width=450,height=800,bg="lightblue")
frame3.place_forget()

DHeading = Label(top, text='Apply for a Deposit', bg='lightblue', fg='Black', font=('Bookman Old Style', 30, 'bold'),justify="center")
DHeading.place_forget()

account_number2=Entry(frame3, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
account_number2.place(x=50,y=50)
account_number2.insert(0,f"{Account_number}")
account_number2.config(state="readonly",readonlybackground="lightblue")
frameaccnumber3 =Frame(frame3,width=342,height=2,bg="black").place(x=50, y=82)

Name3=Entry(frame3, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
Name3.place(x=50,y=120)
Name3.insert(0,f"{Name} {Lastname}")
Name3.config(state="readonly",readonlybackground="lightblue")
framename3 =Frame(frame3,width=342,height=2,bg="black").place(x=50, y=152)

contact3=Entry(frame3, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
contact3.place(x=50,y=190)
contact3.insert(0,f"{Contact}")
contact3.config(state="readonly",readonlybackground="lightblue")
framecontact3 =Frame(frame3,width=342,height=2,bg="black").place(x=50, y=222)

def on_click1(e):
    deposit_amount1.delete(0,"end")
    deposit_amount1.config(validate="key", validatecommand=deposit_amount)

def on_focus_out1(e):
    deposit_amount2 = deposit_amount1.get()
    if deposit_amount2 == "":
        deposit_amount1.config(validate="none")
        deposit_amount1.insert(0,"Deposit Amount")

def validate_digit_input(P):
    return P.isdigit() or P == ""

deposit_amount = (top.register(validate_digit_input), '%P')

deposit_amount1=Entry(frame3, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
deposit_amount1.place(x=50,y=260)
deposit_amount1.insert(0,"Deposit Amount")
deposit_amount1.bind("<FocusIn>", on_click1)
deposit_amount1.bind("<FocusOut>", on_focus_out1)
frameamount =Frame(frame3,width=342,height=2,bg="black").place(x=50, y=292)

Deposit_type_dict = {
    0.0: "Select Your Deposit",
    7.0: "Savings Account Deposit",
    7.75: "Fixed Deposit",
    7.25: "Recurring Deposit",
    4.0: "Current Account Deposit",
    3.50: "Foreign Currency Non-Resident Deposit"
}
Deposit_type = list(Deposit_type_dict.values())
PDeposit_type=ttk.Combobox(frame3,values=Deposit_type, width=25,font=("Bookman Old Style", 15, "bold"),state="readonly",justify="center")
PDeposit_type.place(x=50,y=330)
PDeposit_type.current(0)
frametype1 =Frame(frame3,width=347,height=2,bg="black").place(x=50, y=360)
frametype2 =Frame(frame3,width=347,height=2,bg="black").place(x=50, y=330)
frametype3 =Frame(frame3,width=2,height=32,bg="black").place(x=50, y=330)
frametype4 =Frame(frame3,width=2,height=32,bg="black").place(x=396, y=330)

years_dict = {
    0: "Number of Years",
    1: "1 Year",
    2: "2 Years",
    3: "3 Years",
    4: "4 Years",
    5: "5 Years"
}
years_values = list(years_dict.values())
PDeposit_years=ttk.Combobox(frame3,values=years_values, width=25,font=("Bookman Old Style", 15, "bold"),state="readonly",justify="center")
PDeposit_years.place(x=50,y=400)
PDeposit_years.current(0)
frametype1 =Frame(frame3,width=347,height=2,bg="black").place(x=50, y=430)
frametype2 =Frame(frame3,width=347,height=2,bg="black").place(x=50, y=400)
frametype3 =Frame(frame3,width=2,height=32,bg="black").place(x=50, y=400)
frametype4 =Frame(frame3,width=2,height=32,bg="black").place(x=396, y=400)

return_deposit= Entry(frame3, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20),justify="center")
return_deposit.place(x=50,y=470)
return_deposit.insert(0,"Return")
return_deposit.config(state="readonly",readonlybackground="Lightblue")
frametype1 =Frame(frame3,width=347,height=2,bg="black").place(x=50, y=502)

def on_click5(e):
    Password3.delete(0,"end")
    Password3.config(show="*")

def on_focus_out5(e):
    password3 = Password3.get()
    if password3 == "":
        Password3.config(show="")
        Password3.insert(0,"Password")

Password3=Entry(frame3, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20),justify="center")
Password3.place(x=50,y=540)
Password3.insert(0,"Password")
Password3.bind("<FocusIn>", on_click5)
Password3.bind("<FocusOut>", on_focus_out5)
framepass3 =Frame(frame3,width=342,height=2,bg="black").place(x=50, y=572)

b0 = Button(top,cursor="hand2", width=5, pady=7, text='←', bg="lightblue",fg='Black', border=0, font=('Arial', 15, "bold"), command=login)
b0.place(x=5,y=5)
b2 = Button(top, cursor="hand2", width=20, pady=7, text='Deposit Now', bg='lightblue', fg='Black', border=10, font=('Bookman Old Style', 15),command=deposits)
b2.place(x=700, y=750)
b5 = Button(frame3,cursor="hand2", width=20, pady=7, text='Return', bg='#98FF98',fg='Black', border=0, font=('Arial', 20, "bold"),command=returnamount)
b5.place_forget()
b6 = Button(frame3,cursor="hand2", width=20, pady=7, text='Submit', bg='#98FF98',fg='Black', border=0, font=('Arial', 20, "bold"),command=deposittype)
b6.place_forget()
b7 = Button(frame3,cursor="hand2", width=5, pady=7, text='←', bg="lightblue",fg='Black', border=0, font=('Arial', 15, "bold"), command=default)
b7.place_forget()

update_time()
top.mainloop()
