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

Email, Password, Name, Lastname, Contact, Account_number, BalanceLoan = get_login_data()

def typed():
    global Loans,Balance
    db = sql.connect(host='localhost', user='root', password='7011', db='banking')
    cur = db.cursor()
    query = """SELECT clients_details.loan_type, clients_details.loan_amount FROM clients JOIN 
                clients_details ON clients.Account_Number = clients_details.Account_Number
                WHERE clients.Account_Number =%s;"""
    cur.execute(query, (Account_number))
    result = cur.fetchall()
    if result:
        for col in result:
            Loans = col[0] if col[0] else "No Active loan"
            Balance = col[1] if col[1] else "No Active loan"
    else:
        messagebox.showerror("Error", "No Record Found")
    cur.close()
    db.close()

typed()

def loanreturn():
    L1 = LoansA.get()
    L2 = PLoans_type.get()
    L3 = Ploan_years.get()

    if L1 == "Loan Amount" or not L1:
        messagebox.showerror("Error", "Please fill in all the required details: Loan Amount.")
        return

    if L2 == "Select Your loan" or not L2:
        messagebox.showerror("Error", "Please fill in all the required details: Loan Type.")
        return

    if L3 == "Number of Years" or not L3:
        messagebox.showerror("Error", "Please fill in all the required details: Number of Years.")
        return

    try:
        loan_amount = float(L1)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid loan amount.")
        return
    
    if loan_amount < 10000.00:
        messagebox.showerror("Error", "The loan amount must be ₹10,000 or higher to be eligible for approval.")
        return
    
    for key, value in loan_type_dict.items():
        if value == L2:
            interest_rate = key

    try:
        years = int(L3.split()[0])
    except ValueError:
        messagebox.showerror("Error", "Invalid number of years. Please enter a valid number.")
        return
    
    monthly_rate = interest_rate / 100 / 12 
    num_payments = years * 12 
    if monthly_rate == 0:
        monthly_payment = loan_amount / num_payments 
    else:
        monthly_payment = (loan_amount * monthly_rate * (1 + monthly_rate) ** num_payments) / \
                          ((1 + monthly_rate) ** num_payments - 1)

    total_repayment = monthly_payment * num_payments  
    total_interest = total_repayment - loan_amount  

    formatted_monthly_payment = "₹{:,.2f}".format(monthly_payment)
    formatted_total_repayment = "₹{:,.2f}".format(total_repayment)
    formatted_total_interest = "₹{:,.2f}".format(total_interest)
    messagebox.showinfo("Success", f"Monthly Payment: {formatted_monthly_payment}\nTotal Repayment: {formatted_total_repayment}\nTotal Interest: {formatted_total_interest}\n Interest Rate :- {interest_rate}%")

    return_loan.config(state="normal")
    return_loan.delete(0, 'end')
    return_loan.insert(0, f"Repayment: {formatted_total_repayment}")
    return_loan.config(state="readonly")


def loanstype():
    A0 = Password.get()
    A1 = PLoans_type.get()
    A2 = Account_number
    A3 = LoansA.get()
    A4 = Ploan_years.get()
    A5 = return_loan.get()
    loanreturn()

    if A5 == "Return" or not A5:
        messagebox.showerror("Error", "Please fill in all the required details: Return.")
        return
    
    A5_cleaned = re.sub(r'[^\d.-]', '', A5).strip()

    if A5_cleaned.endswith('-'):
        A5_cleaned = A5_cleaned[:-1]

    try:
        A5 = float(A5_cleaned)
    except ValueError:
        messagebox.showerror("Error", "Invalid loan return value. Please enter a valid number.")
        return

    try:
        A4_key = [key for key, value in years_dict.items() if value == A4][0]
    except IndexError:
        messagebox.showerror("Error", "Invalid loan time value. Please select a valid number of years.")
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
        
        cur.execute("SELECT loan_type FROM clients_details WHERE account_number = %s;", (A2,))
        exist_loan_type = cur.fetchone()

        if exist_loan_type and exist_loan_type[0]:
            messagebox.showinfo("loan Exist",f"The '{exist_loan_type[0]}' already exists. No update has been performed.")
        else:
            confirm = messagebox.askyesno("Confirm Loan", f"Are you sure you want to take a loan of {A3}?")
            if not confirm:
                return
            
            cur.execute(
            """
            UPDATE clients_details
            SET loan_Type = %s, loan_Amount = %s, loan_Time = %s, loan_Return = %s, Loan_due_amount=%s, Loan_paid_amount=%s
            WHERE Account_Number = %s;
            """,
            (A1, A3, A4_key, A5, A5, 0.00, A2),
        )
            db.commit()
            messagebox.showinfo("Successful",f"Your '{A1}' has been successfully approved. We appreciate your trust in our services and look forward to supporting your financial goals.")
            from smtpEmail import Loan_approval_Email
            Loan_approval_Email()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        db.close()


def update_time():
    time_label.config(text=f"{strftime('%H:%M %p')}")
    top.after(1000, update_time)

def loanschoose():
    frame2.place(x=1050, y=20)
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
    frame.place(x=1050, y=20)
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
frame.place(x=1050, y=20)

LHeading = Label(top, text='Loan Overview', bg='lightblue', fg='Black', font=('Bookman Old Style', 30, 'bold'),justify="center")
LHeading.place(relx=0.5, y=200, anchor="center")

LAHeading = Label(frame, text='Loan Application', bg='lightblue', fg='Black', font=('Bookman Old Style', 30, 'bold'),justify="center")
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

Loan_account=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
Loan_account.place(x=50,y=550)
Loan_account.insert(0,f"{Loans}")
Loan_account.config(state="readonly",readonlybackground="lightblue")
frameLoan_account =Frame(frame,width=342,height=2,bg="black").place(x=50, y=582)

balance1=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
balance1.place(x=50,y=650)
balance1.insert(0,f"{Balance}")
balance1.config(state="readonly",readonlybackground="lightblue")
framebalance =Frame(frame,width=342,height=2,bg="black").place(x=50, y=682)

######################frame2

frame2 =LabelFrame(top,width=450,height=800,bg="lightblue")
frame2.place_forget()

AHeading = Label(top, text='Apply for a Loan', bg='lightblue', fg='Black', font=('Bookman Old Style', 30, 'bold'),justify="center")
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
    LoansA.delete(0,"end")
    LoansA.config(validate="key", validatecommand=loans_amount)

def on_focus_out1(e):
    loans = LoansA.get()
    if loans == "":
        LoansA.config(validate="none")
        LoansA.insert(0,"Loan Amount")

def validate_digit_input(P):
    return P.isdigit() or P == ""

loans_amount = (top.register(validate_digit_input), '%P')

LoansA=Entry(frame2, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
LoansA.place(x=50,y=260)
LoansA.insert(0,"Loan Amount")
LoansA.bind("<FocusIn>", on_click1)
LoansA.bind("<FocusOut>", on_focus_out1)
frameamount =Frame(frame2,width=342,height=2,bg="black").place(x=50, y=292)

loan_type_dict = {
    0.0: "Select Your loan",
    10.49: "Personal Loan",
    6.50: "Home Loan",
    24.00: "Business Loan",
    11.00: "Gold Loan",
    8.00: "Education Loan"
}
Loans_type = list(loan_type_dict.values())
PLoans_type=ttk.Combobox(frame2,values=Loans_type, width=25,font=("Bookman Old Style", 15, "bold"),state="readonly",justify="center")
PLoans_type.place(x=50,y=330)
PLoans_type.current(0)
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
Ploan_years=ttk.Combobox(frame2,values=years_values, width=25,font=("Bookman Old Style", 15, "bold"),state="readonly",justify="center")
Ploan_years.place(x=50,y=400)
Ploan_years.current(0)
frametype1 =Frame(frame2,width=347,height=2,bg="black").place(x=50, y=430)
frametype2 =Frame(frame2,width=347,height=2,bg="black").place(x=50, y=400)
frametype3 =Frame(frame2,width=2,height=32,bg="black").place(x=50, y=400)
frametype4 =Frame(frame2,width=2,height=32,bg="black").place(x=396, y=400)

return_loan= Entry(frame2, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20),justify="center")
return_loan.place(x=50,y=470)
return_loan.insert(0,"Return")
return_loan.config(state="readonly",readonlybackground="Lightblue")
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
b1 = Button(top, cursor="hand2", width=20, pady=7, text='Apply Now', bg='lightblue', fg='Black', border=10, font=('Bookman Old Style', 15),command=loanschoose)
b1.place(x=700, y=750)
b2 = Button(frame2,cursor="hand2", width=20, pady=7, text='Return', bg='#98FF98',fg='Black', border=0, font=('Arial', 20, "bold"),command=loanreturn)
b2.place_forget()
b4 = Button(frame2,cursor="hand2", width=20, pady=7, text='Submit', bg='#98FF98',fg='Black', border=0, font=('Arial', 20, "bold"),command=loanstype)
b4.place_forget()
b5 = Button(frame2,cursor="hand2", width=5, pady=7, text='←', bg="lightblue",fg='Black', border=0, font=('Arial', 15, "bold"), command=default)
b5.place_forget()

update_time()
top.mainloop()
