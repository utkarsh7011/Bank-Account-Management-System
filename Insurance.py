from tkinter import *
from tkinter import ttk
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
            balance = login_data["Balance"]
            if balance is None:
                balance = 0
            
            return email, password, name, lastname, contact, account_number, balance
    except FileNotFoundError:
        print("Login data not found. Please log in first.")
        return None, None

Account = None

Email, Password, Name, Lastname, Contact, Account_number, BalanceInsurance = get_login_data()

def typed():
    global Insurances,Balance
    db = sql.connect(host='localhost', user='root', password='7011', db='banking')
    cur = db.cursor()
    query = """SELECT clients_details.insurance_type, clients_details.insurance_amount FROM clients JOIN 
                clients_details ON clients.Account_Number = clients_details.Account_Number
                WHERE clients.Account_Number =%s;"""
    cur.execute(query, (Account_number))
    result = cur.fetchall()
    if result:
        for col in result:
            Insurances =col[0] if col[0] else "No Active Insurance"
            Balance =col[1] if col[1] else "No Active Insurance"
    else:
        messagebox.showerror("Error", "No Record Found")
    cur.close()
    db.close()

typed()

def InsuranceClaim():
    L1 = InsuranceA.get()
    L2 = PInsurance_type.get()
    L3 = PInsurance_years.get()

    if L1 == "Insurance Amount" or not L1:
        messagebox.showerror("Error", "Please fill in all the required details: Insurance Amount.")
        return

    if L2 == "Select Your Insurance" or not L2:
        messagebox.showerror("Error", "Please fill in all the required details: Insurance Type.")
        return

    if L3 == "Number of Years" or not L3:
        messagebox.showerror("Error", "Please fill in all the required details: Number of Years.")
        return

    try:
        Insurance_amount = float(L1)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid Insurance amount.")
        return
    
    if Insurance_amount < 10000.00:
        messagebox.showerror("Error", "The insurance amount must be ₹10,000 or higher to be eligible for coverage.")
        return
    
    for key, value in Insurance_type_dict.items():
        if value == L2:
            interest_rate = key

    try:
        years = int(L3.split()[0])
    except ValueError:
        messagebox.showerror("Error", "Invalid number of years. Please enter a valid number.")
        return
    
    formatted_Claim_amount = "₹{:,.2f}".format(interest_rate)
    messagebox.showinfo("Success", f"Monthly Payment: {L1}\nInsurance: {L2}\nNumber of Years: {years}\nClaim upto:- {formatted_Claim_amount}")
    Claim_Insurance.config(state="normal")
    Claim_Insurance.delete(0, 'end')
    Claim_Insurance.insert(0, f"Claim upto:- {formatted_Claim_amount}")
    Claim_Insurance.config(state="readonly")

def Insurancetype():
    A0 = Password.get()
    A1 = PInsurance_type.get()
    A2 = Account_number
    A3 = InsuranceA.get()
    A4 = PInsurance_years.get()
    A5 = Claim_Insurance.get()
    InsuranceClaim()

    if A5 == "Return" or not A5:
        messagebox.showerror("Error", "Please fill in all the required details: Return.")
        return
    
    A5_cleaned = re.sub(r'[^\d.]', '', A5).strip()

    try:
        A5 = float(A5_cleaned)
    except ValueError:
        messagebox.showerror("Error", "Invalid Insurance return value. Please enter a valid number.")
        return

    try:
        A4_key = [key for key, value in years_dict.items() if value == A4][0]
    except IndexError:
        messagebox.showerror("Error", "Invalid Insurance time value. Please select a valid number of years.")
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
        
        cur.execute("SELECT Insurance_type FROM clients_details WHERE account_number = %s;", (A2,))
        exist_Insurance_type = cur.fetchone()

        if exist_Insurance_type and exist_Insurance_type[0]:
            messagebox.showinfo("Insurance Exist",f"Insurance already exists: '{exist_Insurance_type[0]}'. No update has been performed.")
        else:    
            confirm = messagebox.askyesno("Confirm Insurance", f"Are you sure you want to purchase insurance of {A3}?")
            if not confirm:
                return
            
            cur.execute(
            """
            UPDATE clients_details
            SET Insurance_Type = %s, Insurance_Amount = %s, Insurance_Time = %s, Insurance_Return = %s
            WHERE Account_Number = %s;
            """,
            (A1, A3, A4_key, A5, A2),
        )
            db.commit()
            from smtpEmail import Insurance_Email
            Insurance_Email()
            messagebox.showinfo("Successful",f"Your '{A1}' has been successfully purchased. We appreciate your trust in our services.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        db.close()

def update_time():
    time_label.config(text=f"{strftime('%H:%M %p')}")
    top.after(1000, update_time)

def Insurancechoose():
    frame2.place(x=1080, y=20)
    AHeading.place(relx=0.5, y=200, anchor="center")
    LHeading.place_forget()
    LAHeading.place_forget()
    b2.place(x=50 ,y=620)
    b4.place(x=50, y=700)
    b5.place(x=5, y=2)
    frame.place_forget()
    b0.place_forget()
    b1.place_forget()

def default():
    LHeading.place(relx=0.5, y=200, anchor="center")
    LAHeading.place(relx=0.5, y=80, anchor="center")
    frame.place(x=1080, y=20)
    b2.place_forget()
    b0.place(x=5, y=5)
    b1.place(x=700, y=750)
    b4.place_forget()
    b5.place_forget()
    AHeading.place_forget()
    frame2.place_forget()


def main():
    top.destroy()
    subprocess.call(["python", "main.py"])

path=r"Assests/Login.png"
img = ImageTk.PhotoImage(Image.open(path))
l0 =Label(top,image=img,border=2,bg="lightblue")
l0.place(x=10, y=300)

path2=r"Assests\Bank.png"
img2 = ImageTk.PhotoImage(Image.open(path2))
l2 =Label(top,image=img2,border=2,bg="lightblue").place(x=490, y=-170)

date_label = Label(top, text= f"{strftime('%d/%m/%y')}" ,font=("Bookman Old Style", 15), fg="#000000", bg="lightblue")
date_label.place(x=10,y=80)
time_label = Label(top,font=("Bookman Old Style", 15), fg="#000000", bg="lightblue")
time_label.place(x=10,y=110)

frame =LabelFrame(top,width=450,height=800,bg="lightblue")
frame.place(x=1080, y=20)

LHeading = Label(top, text='Insurance Overview', bg='lightblue', fg='Black', font=('Bookman Old Style', 30, 'bold'),justify="center")
LHeading.place(relx=0.5, y=200, anchor="center")


LAHeading = Label(frame, text='Insurance', bg='lightblue', fg='Black', font=('Bookman Old Style', 30, 'bold'),justify="center")
LAHeading.place(relx=0.5, y=80, anchor="center")

account_number1=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
account_number1.place(x=50,y=150)
account_number1.insert(0,f"{Account_number}")
account_number1.config(state="readonly",readonlybackground="lightblue")
frameaccnumber =Frame(frame,width=342,height=2,bg="black").place(x=50, y=182)

Name1=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
Name1.place(x=50,y=250)
Name1.insert(0,f"{Name} {Lastname}")
Name1.config(state="readonly",readonlybackground="lightblue")
framename =Frame(frame,width=342,height=2,bg="black").place(x=50, y=282)

Email1=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
Email1.place(x=50,y=350)
Email1.insert(0,f"{Email}")
Email1.config(state="readonly",readonlybackground="lightblue")
frameemail =Frame(frame,width=342,height=2,bg="black").place(x=50, y=382)

contact1=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
contact1.place(x=50,y=450)
contact1.insert(0,f"{Contact}")
contact1.config(state="readonly",readonlybackground="lightblue")
framecontact =Frame(frame,width=342,height=2,bg="black").place(x=50, y=482)

Insurance_account1=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
Insurance_account1.place(x=50,y=550)
Insurance_account1.insert(0,f"{Insurances}")
Insurance_account1.config(state="readonly",readonlybackground="lightblue")
frameInsurance_account =Frame(frame,width=342,height=2,bg="black").place(x=50, y=582)

balance1=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
balance1.place(x=50,y=650)
balance1.insert(0,f"{Balance}")
balance1.config(state="readonly",readonlybackground="lightblue")
framebalance =Frame(frame,width=342,height=2,bg="black").place(x=50, y=682)

######################frame2

frame2 =LabelFrame(top,width=450,height=800,bg="lightblue")
frame2.place_forget()

AHeading = Label(top, text='Apply for a Insurance', bg='lightblue', fg='Black', font=('Bookman Old Style', 30, 'bold'),justify="center")
AHeading.place_forget()

account_number2=Entry(frame2, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
account_number2.place(x=50,y=50)
account_number2.insert(0,f"{Account_number}")
account_number2.config(state="readonly",readonlybackground="lightblue")
frameaccnumber2 =Frame(frame2,width=342,height=2,bg="black").place(x=50, y=82)

Name1=Entry(frame2, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
Name1.place(x=50,y=120)
Name1.insert(0,f"{Name} {Lastname}")
Name1.config(state="readonly",readonlybackground="lightblue")
framename =Frame(frame2,width=342,height=2,bg="black").place(x=50, y=152)

contact1=Entry(frame2, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
contact1.place(x=50,y=190)
contact1.insert(0,f"{Contact}")
contact1.config(state="readonly",readonlybackground="lightblue")
framecontact =Frame(frame2,width=342,height=2,bg="black").place(x=50, y=222)

def on_click1(e):
    InsuranceA.delete(0,"end")
    InsuranceA.config(validate="key", validatecommand=Insurance_amount)

def on_focus_out1(e):
    insurance = InsuranceA.get()
    if insurance == "":
        InsuranceA.config(validate="none")
        InsuranceA.insert(0," Amount")

def validate_digit_input(P):
    return P.isdigit() or P == ""

Insurance_amount = (top.register(validate_digit_input), '%P')

InsuranceA=Entry(frame2, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
InsuranceA.place(x=50,y=260)
InsuranceA.insert(0,"Insurance Amount")
InsuranceA.bind("<FocusIn>", on_click1)
InsuranceA.bind("<FocusOut>", on_focus_out1)
frameamount =Frame(frame2,width=342,height=2,bg="black").place(x=50, y=292)

Insurance_type_dict = {
    0.0: "Select Your Insurance",
    10000000.00: "Life Insurance",
    7500000.00: "Health Insurance",
    5000000.00: "Pet Insurance",
    100000000.00: "Property Insurance",
    1000000000.00: "Business Insurance"
}
Insurance_type = list(Insurance_type_dict.values())
PInsurance_type=ttk.Combobox(frame2,values=Insurance_type, width=25,font=("Bookman Old Style", 15, "bold"),state="readonly",justify="center")
PInsurance_type.place(x=50,y=330)
PInsurance_type.current(0)
frametype1 =Frame(frame2,width=347,height=2,bg="black").place(x=50, y=360)
frametype2 =Frame(frame2,width=347,height=2,bg="black").place(x=50, y=330)
frametype3 =Frame(frame2,width=2,height=32,bg="black").place(x=50, y=330)
frametype4 =Frame(frame2,width=2,height=32,bg="black").place(x=396, y=330)

years_dict = {
    0: "Number of Years",
    5: "5 Year",
    10: "10 Years",
    15: "15 Years",
    25: "25 Years",
    30: "30 Years"
}
years_values = list(years_dict.values())
PInsurance_years=ttk.Combobox(frame2,values=years_values, width=25,font=("Bookman Old Style", 15, "bold"),state="readonly",justify="center")
PInsurance_years.place(x=50,y=400)
PInsurance_years.current(0)
frametype1 =Frame(frame2,width=347,height=2,bg="black").place(x=50, y=430)
frametype2 =Frame(frame2,width=347,height=2,bg="black").place(x=50, y=400)
frametype3 =Frame(frame2,width=2,height=32,bg="black").place(x=50, y=400)
frametype4 =Frame(frame2,width=2,height=32,bg="black").place(x=396, y=400)

Claim_Insurance= Entry(frame2, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20),justify="center")
Claim_Insurance.place(x=50,y=470)
Claim_Insurance.insert(0,"Claim")
Claim_Insurance.config(state="readonly",readonlybackground="Lightblue")
frametype1 =Frame(frame2,width=347,height=2,bg="black").place(x=50, y=502)

def on_click5(e):
    Password.delete(0,"end")
    Password.config(show="*")

def on_focus_out5(e):
    password = Password.get()
    if password == "":
        Password.config(show="")
        Password.insert(0,"Password")

Password=Entry(frame2, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20),justify="center")
Password.place(x=50,y=540)
Password.insert(0,"Password")
Password.bind("<FocusIn>", on_click5)
Password.bind("<FocusOut>", on_focus_out5)
framepass3 =Frame(frame2,width=342,height=2,bg="black").place(x=50, y=572)

b0 = Button(top,cursor="hand2", width=5, pady=7, text='←', bg="lightblue",fg='Black', border=0, font=('Arial', 15, "bold"), command=main)
b0.place(x=5,y=5)
b1 = Button(top, cursor="hand2", width=20, pady=7, text='Apply Now', bg='lightblue', fg='Black', border=10, font=('Bookman Old Style', 15),command=Insurancechoose)
b1.place(x=700, y=750)
b2 = Button(frame2,cursor="hand2", width=20, pady=7, text='Claim', bg='#98FF98',fg='Black', border=0, font=('Arial', 20, "bold"),command=InsuranceClaim)
b2.place_forget()
b4 = Button(frame2,cursor="hand2", width=20, pady=7, text='Submit', bg='#98FF98',fg='Black', border=0, font=('Arial', 20, "bold"),command=Insurancetype)
b4.place_forget()
b5 = Button(frame2,cursor="hand2", width=5, pady=7, text='←', bg="lightblue",fg='Black', border=0, font=('Arial', 15, "bold"), command=default)
b5.place_forget()

update_time()
top.mainloop()
