from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk
import pymysql as sql
from time import strftime 
import subprocess
import json


top=Tk()
style = ttk.Style()
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
    global Account, loan_type, loan_amount, loan_return, loan_time, Loan_due_amount, Loan_paid_amount

    db = sql.connect(host='localhost', user='root', password='7011', db='banking')
    cur = db.cursor()

    query = """SELECT clients_details.account_type, 
                      clients_details.loan_type, 
                      clients_details.loan_amount, 
                      clients_details.loan_return, 
                      clients_details.loan_time, 
                      clients_details.Loan_due_amount, 
                      clients_details.Loan_paid_amount
               FROM clients 
               JOIN clients_details 
               ON clients.Account_Number = clients_details.Account_Number
               WHERE clients.Account_Number = %s;"""
    
    cur.execute(query, (Account_number,))
    result = cur.fetchall()
    
    if result:
        for col in result:
            Account = col[0] if col[0] is not None and col[0] != "NULL" else "Not Active"
        loan_type = col[1] if col[1] is not None and col[1] != "NULL" else "Not Active"
        loan_amount = col[2] if col[2] is not None and col[2] != "NULL" else "Not Active"
        loan_return = col[3] if col[3] is not None and col[3] != "NULL" else "Not Active"
        loan_time = col[4] if col[4] is not None and col[4] != "NULL" else "Not Active"
        Loan_due_amount = col[5] if col[5] is not None and col[5] != "NULL" else "Not Active"
        Loan_paid_amount = col[6] if col[6] is not None and col[6] != "NULL" else "Not Active"

    else:
        messagebox.showerror("Error", "No Record Found")
    
    cur.close()
    db.close()

typed()


def update_time():
    time_label.config(text=f"{strftime('%H:%M %p')}")
    top.after(1000, update_time)

def login():
    top.destroy()
    subprocess.call(["python", "main.py"])

def default():
    frame.place(x=1080, y=20)
    frame2.place_forget()
    frame3.place_forget()
    frame4.place_forget()
    frame5.place_forget()
    frame6.place_forget()
    FHeading1.place(relx=0.5, y=200, anchor="center")
    FHeading2.place_forget()
    FHeading3.place_forget()
    FHeading4.place_forget()
    FHeading5.place_forget()
    FHeading6.place_forget()
    b0.place(x=5, y=5)
    b8.place(x=700, y=750)
    b1.place_forget()
    b2.place_forget()
    b3.place_forget()
    b4.place_forget()
    b5.place_forget()
    b6.place_forget()
    b11.place_forget()
    b12.place_forget()
    b13.place_forget()
    b12.place_forget()
    b20.place_forget()
    b21.place_forget()
    b22.place_forget()

def frame2place():
    frame2.place(x=1080, y=20)
    frame.place_forget()
    frame3.place_forget()
    frame4.place_forget()
    frame5.place_forget()
    frame6.place_forget()
    FHeading2.place(relx=0.5, y=200, anchor="center")
    FHeading1.place_forget()
    FHeading3.place_forget()
    FHeading4.place_forget()
    FHeading5.place_forget()
    FHeading6.place_forget()
    b1.place(x=50, y=150)
    b2.place(x=50, y=250)
    b3.place(x=50, y=350)
    b4.place(x=5, y=5)
    b12.place(x=50, y=450)
    b0.place_forget()
    b8.place_forget()
    b5.place_forget()
    b6.place_forget()
    b13.place_forget()
    b11.place_forget()
    b20.place_forget()
    b21.place_forget()
    b22.place_forget()

def frame3place():
    frame3.place(x=1080, y=20)
    frame2.place_forget()
    frame.place_forget()
    frame4.place_forget()
    frame5.place_forget()
    frame6.place_forget()
    FHeading3.place(relx=0.5, y=200, anchor="center")
    FHeading1.place_forget()
    FHeading2.place_forget()
    FHeading4.place_forget()
    FHeading5.place_forget()
    FHeading6.place_forget()
    b5.place(x=50,y=690)
    b6.place(x=5,y=5)
    b1.place_forget()
    b2.place_forget()
    b3.place_forget()
    b4.place_forget()
    b0.place_forget()
    b8.place_forget()
    b10.place_forget()
    b11.place_forget()
    b13.place_forget()
    b12.place_forget()
    b20.place_forget()
    b21.place_forget()
    b22.place_forget()

def frame4place():
    frame4.place(x=1050, y=20)
    frame.place_forget()
    frame2.place_forget()
    frame3.place_forget()
    frame5.place_forget()
    frame6.place_forget()
    FHeading4.place(relx=0.5, y=200, anchor="center")
    FHeading1.place_forget()
    FHeading2.place_forget()
    FHeading3.place_forget()
    FHeading5.place_forget()
    FHeading6.place_forget()
    b7.place(x=50,y=690)
    b9.place(x=5,y=5)
    b13.place(x=50, y=600)
    b1.place_forget()
    b2.place_forget()
    b3.place_forget()
    b4.place_forget()
    b5.place_forget()
    b6.place_forget()
    b0.place_forget()
    b8.place_forget()
    b10.place_forget()
    b11.place_forget()
    b12.place_forget()
    b20.place_forget()
    b21.place_forget()
    b22.place_forget()

def frame5place():
    frame5.place(x=1050, y=20)
    frame.place_forget()
    frame2.place_forget()
    frame3.place_forget()
    frame4.place_forget()
    frame6.place_forget()
    FHeading5.place(relx=0.5, y=200, anchor="center")
    FHeading1.place_forget()
    FHeading2.place_forget()
    FHeading3.place_forget()
    FHeading4.place_forget()
    FHeading6.place_forget()
    b10.place(x=50,y=650)
    b11.place(x=5,y=5)
    b1.place_forget()
    b2.place_forget()
    b3.place_forget()
    b4.place_forget()
    b5.place_forget()
    b6.place_forget()
    b0.place_forget()
    b8.place_forget()
    b7.place_forget()
    b9.place_forget()
    b13.place_forget()
    b12.place_forget()
    b20.place_forget()
    b21.place_forget()
    b22.place_forget()

def frame6place():
    frame6.place(x=1050, y=20)
    frame5.place_forget()
    frame.place_forget()
    frame2.place_forget()
    frame3.place_forget()
    frame4.place_forget()
    FHeading6.place(relx=0.5, y=200, anchor="center")
    FHeading5.place_forget()
    FHeading1.place_forget()
    FHeading2.place_forget()
    FHeading3.place_forget()
    FHeading4.place_forget()
    b20.place(x=50, y=700)
    b21.place(x=5, y=5)
    b22.place(x=50, y=620)
    b10.place_forget()
    b11.place_forget()
    b1.place_forget()
    b2.place_forget()
    b3.place_forget()
    b4.place_forget()
    b5.place_forget()
    b6.place_forget()
    b0.place_forget()
    b8.place_forget()
    b7.place_forget()
    b9.place_forget()
    b13.place_forget()
    b12.place_forget()

def accounttype():
    A0 = Password2.get()
    A1 = PAccounts_type2.get() 
    A2 = Account_number

    if not A0 or A0 == "Password":
        messagebox.showerror("Error", "Password cannot be empty.")
        return
    if not A1 or A1 == "Accounts":
        messagebox.showerror("Error", "Select a Account Type.")
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
        
        cur.execute("SELECT account_type FROM clients_details WHERE account_number = %s;", (A2,))
        exist_account = cur.fetchone()

        if exist_account:
            exist = exist_account[0]
            if exist:
                messagebox.showerror("Error", f"The account is already set to '{exist}'.")
                return
            
        confirm = messagebox.askyesno("Confirm Account", f"Are you sure you want to set the account to {A1}?")
        if not confirm:
            return

        s = "UPDATE clients_details SET account_type = %s WHERE account_number = %s;"
        value = (A1, A2)
        cur.execute(s, value)
        db.commit()
        messagebox.showinfo("Success", f"Your Account has been set to '{A1}' successfully.")
        from smtpEmail import Profile_Compltion_Email
        Profile_Compltion_Email()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to insert Account type: {e}")

    finally:
        db.close()

def Repay():
    global Due_amount
    G1 = Loan_due_amount
    G2 = LoansA.get()
    H5d = PLoans_type.get()

    if not H5d or H5d == "Not Active":
            messagebox.showerror("Error", "You Don't Have a Running Loan")
            return

    if not G2 or G2 == "Payment Amount":
        G2 = 0.0
        messagebox.showerror(0,"Enter a Valid Amount.")
        return

    try:
        G1s = float(G1) 
        G2s = float(G2) 
    except ValueError:
        messagebox.showerror("Error", "Invalid amount entered.") 
        return
    
    if G2s < 10000:
        messagebox.showerror("Error", "Payment amount must be at least 10,000. Please enter a higher amount.")
        return
    
    if G2s > G1s:
        messagebox.showerror("Error", "Payment amount exceeds the outstanding loan amount. Please enter a valid amount.")
        return

    Due_amount = G1s - G2s
    messagebox.showinfo("Loan Due Amount", f"The outstanding loan amount is: {Due_amount}")

    PLoans_due.config(state="normal")
    PLoans_due.delete(0,"end")
    PLoans_due.insert(0,f"{Due_amount}")
    PLoans_due.config(state="readonly",readonlybackground="Lightblue")

def loanpayment():
    H1ds = PLoans_due.get()
    H2ds = LoansA.get()
    H3s = Account_number
    H4s = Password3.get() 
    H5s = PLoans_type.get()
    Repay()
        
    if not H5s or H5s == "Not Active":
        messagebox.showerror("Error", "You Don't Have a Running Loan")
        return
    if not H4s or H4s == "Password":
        messagebox.showerror("Error", "Password cannot be empty.")
        return
    if not H2ds or H2ds == "Payment Amount":
        messagebox.showerror(0,"Enter a Valid Amount.")
        return
    try:
        H1d = float(H1ds) 
        H2d = float(H2ds) 
    except ValueError:
        messagebox.showerror("Error", "Invalid amount entered.") 
        return
    if H2d < 10000:
        messagebox.showerror("Error", "Payment amount must be at least 10,000. Please enter a higher amount.")
        return
    
    try:
        db = sql.connect(host="localhost", user="root", password="7011", db="banking")
        cur = db.cursor()
        
        cur.execute("SELECT password FROM clients WHERE account_number = %s;", (H3s,))
        result = cur.fetchone()
        if not result:
            messagebox.showerror("Error", "Account number not found.")
            return

        db_password = result[0]
        if db_password != H4s:
            messagebox.showerror("Error", "Incorrect Password.")
            return

        cur.execute("SELECT Loan_paid_amount FROM clients_details WHERE account_number = %s;", (H3s,))
        result = cur.fetchone()
        previous_paid = float(result[0]) if result and result[0] else 0.0
        new_paid_amount = previous_paid + float(H2d)

        confirm = messagebox.askyesno("Confirm Payment", f"Are you sure you want to pay {H2d}?")
        if not confirm:
            return
        
        s = "UPDATE clients_details SET Loan_due_amount = %s,Loan_paid_amount=%s  WHERE account_number = %s;"
        value = (H1d,new_paid_amount, H3s)
        cur.execute(s, value)
        db.commit()
        messagebox.showinfo("Loan Amount Paid", f"The loan amount of {H2d} has been successfully paid.")
        from smtpEmail import Loan_Payment_Email
        Loan_Payment_Email()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to update Due Amount: {e}")

    finally:
        db.close()

def CheckStatus():
    top.destroy()
    subprocess.call(["python", "checkstatus.py"])

def Closing():
    global balance_amount
    C1ss = Balance
    C2ss = BalanceA.get()

    if not C2ss or C2ss == "Credit":
        messagebox.showerror(0,"Enter a Valid Amount.")
        return

    try:
        C1s = float(C1ss) 
        C2s = float(C2ss) 
    except ValueError:
        messagebox.showerror("Error", "Invalid amount entered.") 
        return
    
    if C2s < 100:
        messagebox.showerror("Error", "Payment amount must be at least 100. Please enter a higher amount.")
        return

    balance_amount = C1s + C2s
    messagebox.showinfo("Transaction Notification:", f" Your closing balance will be {balance_amount}.")

    closingbalance6.config(state="normal")
    closingbalance6.delete(0,"end")
    closingbalance6.insert(0,f"{balance_amount}")
    closingbalance6.config(state="readonly",readonlybackground="Lightblue")

def TopUP():
    TUs = closingbalance6.get()
    TUs2 = BalanceA.get()
    TUs3 = Account_number
    TUs4 = Password6.get()
    Closing()

    if not TUs4 or TUs4 == "Password":
        messagebox.showerror("Error", "Password cannot be empty.")
        return
    if not TUs2 or TUs2 == "Credit":
        messagebox.showerror(0,"Enter a Valid Amount.")
        return
    try:
        TUs21 = float(TUs2) 
    except ValueError:
        messagebox.showerror("Error", "Invalid amount entered.") 
        return
    
    if TUs21 < 100:
        messagebox.showerror("Error", "Payment amount must be at least 100. Please enter a higher amount.")
        return
    
    try:
        db = sql.connect(host="localhost", user="root", password="7011", db="banking")
        cur = db.cursor()
        
        cur.execute("SELECT password FROM clients WHERE account_number = %s;", (TUs3,))
        result = cur.fetchone()
        if not result:
            messagebox.showerror("Error", "Account number not found.")
            return

        db_password = result[0]
        if db_password != TUs4:
            messagebox.showerror("Error", "Incorrect Password.")
            return
        
        cur.execute("SELECT balance FROM clients WHERE account_number = %s;", (TUs3,))
        result = cur.fetchone()
        previous_paid = float(result[0]) if result and result[0] else 0.0
        new_paid_amount = previous_paid + float(TUs21)

        confirm = messagebox.askyesno("Payment Confirmation:",f" Are you sure you want to top up with {TUs21}?")
        if not confirm:
            return
        
        s = "UPDATE clients SET balance = %s WHERE account_number = %s;"
        value = (new_paid_amount, TUs3)
        cur.execute(s, value)
        db.commit()
        from smtpEmail import Balance_Email
        Balance_Email()
        messagebox.showinfo("Credit Notification:",f" Your account has been credited with an amount of {TUs21}.")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to update Due Amount: {e}")

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

FHeading1 = Label(top, text='Your Profile', bg='lightblue', fg='Black', font=('Bookman Old Style', 30, 'bold'),justify="center")
FHeading1.place_forget()

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

account2=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
account2.place(x=50,y=550)
account2.insert(0,f"{Account}")
account2.config(state="readonly",readonlybackground="lightblue")
frameaccount =Frame(frame,width=342,height=2,bg="black").place(x=50, y=582)

balance1=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
balance1.place(x=50,y=650)
balance1.insert(0,f"{Balance}/-")
balance1.config(state="readonly",readonlybackground="lightblue")
framebalance =Frame(frame,width=342,height=2,bg="black").place(x=50, y=682)

##############################frame3####################################################################################################################################################################################

frame2 =LabelFrame(top,width=450,height=800,bg="lightblue")
frame2.place_forget()

FHeading2 = Label(top, text='More Detail About \nYour profile', bg='lightblue', fg='Black', font=('Bookman Old Style', 30, 'bold'),justify="center")
FHeading2.place_forget()

##############################frame3####################################################################################################################################################################################

frame3 =LabelFrame(top,width=450,height=800,bg="lightblue")
frame3.place_forget()

FHeading3 = Label(top, text='Set Your Account', bg='lightblue', fg='Black', font=('Bookman Old Style', 30, 'bold'),justify="center")
FHeading3.place_forget()

account_number11=Entry(frame3, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
account_number11.place(x=50,y=100)
account_number11.insert(0,f"{Account_number}")
account_number11.config(state="readonly",readonlybackground="lightblue")
frameaccnumber1 =Frame(frame3,width=342,height=2,bg="black").place(x=50, y=132)

Name2=Entry(frame3, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
Name2.place(x=50,y=200)
Name2.insert(0,f"{Name} {Lastname}")
Name2.config(state="readonly",readonlybackground="lightblue")
framename2 =Frame(frame3,width=342,height=2,bg="black").place(x=50, y=232)

Email2=Entry(frame3, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
Email2.place(x=50,y=300)
Email2.insert(0,f"{Email}")
Email2.config(state="readonly",readonlybackground="lightblue")
frameemail2 =Frame(frame3,width=342,height=2,bg="black").place(x=50, y=332)

contact2=Entry(frame3, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
contact2.place(x=50,y=400)
contact2.insert(0,f"{Contact}")
contact2.config(state="readonly",readonlybackground="lightblue")
framecontact2 =Frame(frame3,width=342,height=2,bg="black").place(x=50, y=432)

def on_click0(e):
    Password2.delete(0,"end")
    Password2.config(show="*")

def on_focus_out0(e):
    password2 = Password2.get()
    if password2 == "":
        Password2.config(show="")
        Password2.insert(0,"Password")

Password2 = Entry(frame3, width=20, fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
Password2.place(x=50, y=500)
Password2.insert(0, "Password")
Password2.bind("<FocusIn>", on_click0)
Password2.bind("<FocusOut>", on_focus_out0)
framepass1 = Frame(frame3, width=342, height=2, bg="black")
framepass1.place(x=50, y=532)

Accounts_type2 = ["Accounts","Savings Account","Current Account","Business Account","Joint Account","Student Account"]
PAccounts_type2=ttk.Combobox(frame3,values=Accounts_type2, width=25,font=("Bookman Old Style", 15, "bold"),state="readonly",justify="center")
PAccounts_type2.place(x=50,y=600)
PAccounts_type2.current(0)
frametype1 =Frame(frame3,width=347,height=2,bg="black").place(x=50, y=630)
frametype2 =Frame(frame3,width=347,height=2,bg="black").place(x=50, y=600)
frametype3 =Frame(frame3,width=2,height=32,bg="black").place(x=50, y=600)
frametype4 =Frame(frame3,width=2,height=32,bg="black").place(x=396, y=600)

##############################frame4######################################################################################################################################################

frame4 =LabelFrame(top,width=450,height=800,bg="lightblue")
frame4.place_forget()

FHeading4 = Label(top, text='Repay Your loan', bg='lightblue', fg='Black', font=('Bookman Old Style', 30, 'bold'),justify="center")
FHeading4.place_forget()

account_number2=Entry(frame4, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
account_number2.place(x=50,y=50)
account_number2.insert(0,f"{Account_number}")
account_number2.config(state="readonly",readonlybackground="lightblue")
frameaccnumber2 =Frame(frame4,width=342,height=2,bg="black").place(x=50, y=82)

Name3=Entry(frame4, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
Name3.place(x=50,y=120)
Name3.insert(0,f"{Name} {Lastname}")
Name3.config(state="readonly",readonlybackground="lightblue")
framename =Frame(frame4,width=342,height=2,bg="black").place(x=50, y=152)

contact3=Entry(frame4, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
contact3.place(x=50,y=190)
contact3.insert(0,f"{Contact}")
contact3.config(state="readonly",readonlybackground="lightblue")
framecontact =Frame(frame4,width=342,height=2,bg="black").place(x=50, y=222)

PLoans_type=Entry(frame4, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
PLoans_type.place(x=50,y=260)
PLoans_type.insert(0,f"{loan_type}")
PLoans_type.config(state="readonly",readonlybackground="Lightblue")
frametype1 =Frame(frame4,width=347,height=2,bg="black").place(x=50, y=292)


Total_loan= Entry(frame4, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20),justify="center")
Total_loan.place(x=50,y=330)
Total_loan.insert(0,f"{loan_return}")
Total_loan.config(state="readonly",readonlybackground="Lightblue")
frametype1 =Frame(frame4,width=347,height=2,bg="black").place(x=50, y=362)


def on_click1(e):
    LoansA.delete(0,"end")
    LoansA.config(validate="key", validatecommand=loans_amount)

def on_focus_out1(e):
    loans = LoansA.get()
    if loans == "":
        LoansA.config(validate="none")
        LoansA.insert(0,"Payment Amount")

def validate_digit_input(P):
    return P.isdigit() or P == ""

loans_amount = (top.register(validate_digit_input), '%P')

LoansA=Entry(frame4, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
LoansA.place(x=50,y=400)
LoansA.insert(0,"Payment Amount")
LoansA.bind("<FocusIn>", on_click1)
LoansA.bind("<FocusOut>", on_focus_out1)
frameamount =Frame(frame4,width=342,height=2,bg="black").place(x=50, y=432)

PLoans_due=Entry(frame4, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
PLoans_due.place(x=50,y=470)
PLoans_due.insert(0,f"{Loan_due_amount}")
PLoans_due.config(state="readonly",readonlybackground="Lightblue")
frametype1 =Frame(frame4,width=347,height=2,bg="black").place(x=50, y=502)

def on_click5(e):
    Password3.delete(0,"end")
    Password3.config(show="*")

def on_focus_out5(e):
    password3 = Password3.get()
    if password3 == "":
        Password3.config(show="")
        Password3.insert(0,"Password")

Password3=Entry(frame4, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20),justify="center")
Password3.place(x=50,y=540)
Password3.insert(0,"Password")
Password3.bind("<FocusIn>", on_click5)
Password3.bind("<FocusOut>", on_focus_out5)
framepass3 =Frame(frame4,width=342,height=2,bg="black").place(x=50, y=572)

##############################frame5######################################################################################################################################################

frame5 =LabelFrame(top,width=450,height=800,bg="lightblue")
frame5.place_forget()

FHeading5 = Label(top, text='Check Complete Status \nof your Account', bg='lightblue', fg='Black', font=('Bookman Old Style', 30, 'bold'),justify="center")
FHeading5.place_forget()

account_number5=Entry(frame5, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
account_number5.place(x=50,y=50)
account_number5.insert(0,f"{Account_number}")
account_number5.config(state="readonly",readonlybackground="lightblue")
frameaccnumber5 =Frame(frame5,width=342,height=2,bg="black").place(x=50, y=82)

Name5=Entry(frame5, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
Name5.place(x=50,y=150)
Name5.insert(0,f"{Name} {Lastname}")
Name5.config(state="readonly",readonlybackground="lightblue")
framename5 =Frame(frame5,width=342,height=2,bg="black").place(x=50, y=182)

Email5=Entry(frame5, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
Email5.place(x=50,y=250)
Email5.insert(0,f"{Email}")
Email5.config(state="readonly",readonlybackground="lightblue")
frameemail1 =Frame(frame5,width=342,height=2,bg="black").place(x=50, y=282)

contact5=Entry(frame5, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
contact5.place(x=50,y=350)
contact5.insert(0,f"{Contact}")
contact5.config(state="readonly",readonlybackground="lightblue")
framecontact5 =Frame(frame5,width=342,height=2,bg="black").place(x=50, y=382)

account_type5=Entry(frame5, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
account_type5.place(x=50,y=450)
account_type5.insert(0,f"{Account}")
account_type5.config(state="readonly",readonlybackground="lightblue")
frameaccount_type5 =Frame(frame5,width=342,height=2,bg="black").place(x=50, y=482)

def on_click5(e):
    Password5.delete(0,"end")
    Password5.config(show="*")

def on_focus_out5(e):
    password5 = Password5.get()
    if password5 == "":
        Password5.config(show="")
        Password5.insert(0,"Password")

Password5=Entry(frame5, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20),justify="center")
Password5.place(x=50,y=550)
Password5.insert(0,"Password")
Password5.bind("<FocusIn>", on_click5)
Password5.bind("<FocusOut>", on_focus_out5)
framepass3 =Frame(frame5,width=342,height=2,bg="black").place(x=50, y=582)

##############################frame6######################################################################################################################################################

frame6 =LabelFrame(top,width=450,height=800,bg="lightblue")
frame6.place_forget()

FHeading6 = Label(top, text='Top Up your Account', bg='lightblue', fg='Black', font=('Bookman Old Style', 30, 'bold'),justify="center")
FHeading6.place_forget()

account_number6=Entry(frame6, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
account_number6.place(x=50,y=50)
account_number6.insert(0,f"{Account_number}")
account_number6.config(state="readonly",readonlybackground="lightblue")
frameaccnumber =Frame(frame6,width=342,height=2,bg="black").place(x=50, y=82)

Name6=Entry(frame6, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
Name6.place(x=50,y=120)
Name6.insert(0,f"{Name} {Lastname}")
Name6.config(state="readonly",readonlybackground="lightblue")
framename =Frame(frame6,width=342,height=2,bg="black").place(x=50, y=152)

contact6=Entry(frame6, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
contact6.place(x=50,y=190)
contact6.insert(0,f"{Contact}")
contact6.config(state="readonly",readonlybackground="lightblue")
framecontact =Frame(frame6,width=342,height=2,bg="black").place(x=50, y=222)

account6=Entry(frame6, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
account6.place(x=50,y=260)
account6.insert(0,f"{Account}")
account6.config(state="readonly",readonlybackground="lightblue")
frameaccount =Frame(frame6,width=342,height=2,bg="black").place(x=50, y=292)

balance6=Entry(frame6, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
balance6.place(x=50,y=330)
balance6.insert(0,f"{Balance}/-")
balance6.config(state="readonly",readonlybackground="lightblue")
framebalance =Frame(frame6,width=342,height=2,bg="black").place(x=50, y=362)

def on_click1(e):
    BalanceA.delete(0,"end")
    BalanceA.config(validate="key", validatecommand=loans_amount)

def on_focus_out1(e):
    loans = BalanceA.get()
    if loans == "":
        BalanceA.config(validate="none")
        BalanceA.insert(0,"Credit")

def validate_digit_input(P):
    return P.isdigit() or P == ""

loans_amount = (top.register(validate_digit_input), '%P')

BalanceA=Entry(frame6, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
BalanceA.place(x=50,y=400)
BalanceA.insert(0,"Credit")
BalanceA.bind("<FocusIn>", on_click1)
BalanceA.bind("<FocusOut>", on_focus_out1)
frameamount =Frame(frame6,width=342,height=2,bg="black").place(x=50, y=432)

closingbalance6=Entry(frame6, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
closingbalance6.place(x=50,y=470)
closingbalance6.insert(0,"Closing Balance")
closingbalance6.config(state="readonly",readonlybackground="lightblue")
framebalance =Frame(frame6,width=342,height=2,bg="black").place(x=50, y=502)

def on_click5(e):
    Password6.delete(0,"end")
    Password6.config(show="*")

def on_focus_out5(e):
    password6 = Password6.get()
    if password6 == "":
        Password6.config(show="")
        Password6.insert(0,"Password")

Password6=Entry(frame6, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20),justify="center")
Password6.place(x=50,y=550)
Password6.insert(0,"Password")
Password6.bind("<FocusIn>", on_click5)
Password6.bind("<FocusOut>", on_focus_out5)
framepass3 =Frame(frame6,width=342,height=2,bg="black").place(x=50, y=582)

###########frame buttons
b0 = Button(top,cursor="hand2", width=5, pady=7, text='←', bg="lightblue",fg='Black', border=0, font=('Arial', 15, "bold"), command=login)
b0.place(x=5,y=5)
b8 = Button(top, cursor="hand2", width=20, pady=7, text='More', bg='lightblue', fg='Black', border=10, font=('Bookman Old Style', 15),command=frame2place)
b8.place(x=700, y=750)

###########frame2 buttons
b1 = Button(frame2, cursor="hand2", width=20, pady=7, text='Profile', bg='lightblue', fg='Black', border=10, font=('Bookman Old Style', 15),command=frame3place)
b1.place_forget()
b2 = Button(frame2, cursor="hand2", width=20, pady=7, text='Loan Repay', bg='lightblue', fg='Black', border=10, font=('Bookman Old Style', 15),command=frame4place)
b2.place_forget()
b3 = Button(frame2, cursor="hand2", width=20, pady=7, text='Check Status', bg='lightblue', fg='Black', border=10, font=('Bookman Old Style', 15),command=frame5place)
b3.place_forget()
b12 = Button(frame2, cursor="hand2", width=20, pady=7, text='Top UP', bg='lightblue', fg='Black', border=10, font=('Bookman Old Style', 15),command=frame6place)
b12.place_forget()
b4 = Button(frame2,cursor="hand2", width=5, pady=7, text='←', bg="lightblue",fg='Black', border=0, font=('Arial', 15, "bold"), command=default)
b4.place_forget()

###########frame3 buttons
b5 = Button(frame3,cursor="hand2", width=20, pady=7, text='Submit', bg='#98FF98',fg='Black', border=0, font=('Arial', 20, "bold"),command=accounttype)
b5.place_forget()
b6 = Button(frame3,cursor="hand2", width=5, pady=7, text='←', bg="lightblue",fg='Black', border=0, font=('Arial', 15, "bold"), command=frame2place)
b6.place_forget()

###########frame4 buttons
b7 = Button(frame4,cursor="hand2", width=20, pady=7, text='Submit', bg='#98FF98',fg='Black', border=0, font=('Arial', 20, "bold"), command=loanpayment)
b7.place_forget()
b13 = Button(frame4,cursor="hand2", width=20, pady=7, text='Repay', bg='#98FF98',fg='Black', border=0, font=('Arial', 20, "bold"), command=Repay)
b13.place_forget()
b9 = Button(frame4,cursor="hand2", width=5, pady=7, text='←', bg="lightblue",fg='Black', border=0, font=('Arial', 15, "bold"), command=frame2place)
b9.place_forget()

#################frame 5 buttons
b10 = Button(frame5,cursor="hand2", width=20, pady=7, text='Submit', bg='#98FF98',fg='Black', border=0, font=('Arial', 20, "bold"), command=CheckStatus)
b10.place_forget()
b11 = Button(frame5,cursor="hand2", width=5, pady=7, text='←', bg="lightblue",fg='Black', border=0, font=('Arial', 15, "bold"), command=frame2place)
b11.place_forget()

#################frame 6 buttons
b20 = Button(frame6,cursor="hand2", width=20, pady=7, text='Submit', bg='#98FF98',fg='Black', border=0, font=('Arial', 20, "bold"), command=TopUP)
b20.place_forget()
b21 = Button(frame6,cursor="hand2", width=5, pady=7, text='←', bg="lightblue",fg='Black', border=0, font=('Arial', 15, "bold"), command=frame2place)
b21.place_forget()
b22 = Button(frame6,cursor="hand2", width=20, pady=7, text='Closing', bg='#98FF98',fg='Black', border=0, font=('Arial', 20, "bold"), command=Closing)
b22.place_forget()

update_time()
top.mainloop()
