from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk
import pymysql as sql
import re
import requests
import yfinance as yf
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

Email, Password, Name, Lastname, Contact, Account_number, BalanceInvestment = get_login_data()

def typed():
    global Investment,Balance
    db = sql.connect(host='localhost', user='root', password='7011', db='banking')
    cur = db.cursor()
    query = """SELECT clients_details.Investment_type, clients_details.Investment_amount FROM clients JOIN 
                clients_details ON clients.Account_Number = clients_details.Account_Number
                WHERE clients.Account_Number =%s;"""
    cur.execute(query, (Account_number))
    result = cur.fetchall()
    if result:
        for col in result:
            Investment =col[0] if col[0] else "No Active Investment"
            Balance =col[1] if col[1] else "No Active Investment"
    else:
        messagebox.showerror("Error", "No Record Found")
    cur.close()
    db.close()

typed()

def get_exchange_rate(D1, D2):
    """Fetch the real-time exchange rate from ExchangeRate-API"""
    api_url = f"https://v6.exchangerate-api.com/v6/d0c875e0d34cf178b8d92c7c/latest/{D1}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        if data['result'] == 'success':
            return data['conversion_rates'].get(D2)
        else:
            print(f"Error fetching exchange rates: {data.get('error-type', 'Unknown error')}")
            return None
    except Exception as e:
        print(f"Error connecting to the API: {e}")
        return None

def get_exchange_rate(D1, D2):
    api_url = f"https://v6.exchangerate-api.com/v6/d0c875e0d34cf178b8d92c7c/latest/{D1}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        if data['result'] == 'success':
            return data['conversion_rates'].get(D2)
        else:
            print(f"Error fetching exchange rates: {data.get('error-type', 'Unknown error')}")
            return None
    except Exception as e:
        print(f"Error connecting to the API: {e}")
        return None

import yfinance as yf
import requests
from tkinter import messagebox

def get_exchange_rate(D1, D2):
    """Fetch the real-time exchange rate from ExchangeRate-API"""
    api_url = f"https://v6.exchangerate-api.com/v6/d0c875e0d34cf178b8d92c7c/latest/{D1}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        if data['result'] == 'success':
            return data['conversion_rates'].get(D2)
        else:
            print(f"Error fetching exchange rates: {data.get('error-type', 'Unknown error')}")
            return None
    except Exception as e:
        print(f"Error connecting to the API: {e}")
        return None

def Investmentmarket():
    k1 = PInvestment_type.get()
    k2 = InvestmentA.get() 
    
    try:
        if not k1 or k1 == "Select Your Investment":
            messagebox.showerror("Error", "Please select a valid investment type.")
            return
        
        if k2 == "Investment Amount" or not k2:
            messagebox.showerror("Error", "Please fill in all the required details: Deposit Amount.")
            return

        if k1 == "Reliance Industries Limited (Stocks & Shares)":
            data_reliance = yf.download("RELIANCE.NS")
            if 'Close' in data_reliance.columns and not data_reliance.empty:
                latest_price_reliance = float(data_reliance['Close'].iloc[-1])
                k2f = float(k2)
                num_shares = k2f / latest_price_reliance
                messagebox.showinfo("Reliance Industries Limited (Stocks & Shares)", f"Latest Closing Price of Reliance Industries: ₹{latest_price_reliance:.2f}.\nWith ₹{k2f}, you can buy {num_shares:.6f} shares of Reliance Industries.")
                Closing_Investment.config(state="normal")
                Closing_Investment.delete(0, 'end')
                Closing_Investment.insert(0, f"Purchasing: {num_shares:.6f}")
                Closing_Investment.config(state="readonly")

            else:
                messagebox.showerror("Error", "Could not retrieve closing price for Reliance Industries. Data might be unavailable or empty.")
        
        elif k1 == "Bitcoin (Cryptocurrency)":
            usd_to_inr = get_exchange_rate("USD", "INR")
            if usd_to_inr is None:
                messagebox.showerror("Error", "Could not fetch USD to INR exchange rate.")
                return
            
            data_btc = yf.download("BTC-USD")
            if 'Close' in data_btc.columns and not data_btc.empty:
                latest_price_usd = float(data_btc['Close'].iloc[-1])  
                latest_price_inr = latest_price_usd * usd_to_inr
                k2f = float(k2)
                num_bitcoins = k2f / latest_price_inr
                messagebox.showinfo("Bitcoin (Cryptocurrency)", f"Latest Closing Price of Bitcoin: ₹{latest_price_inr:.2f}\nWith ₹{k2f}, you can buy {num_bitcoins:.6f} Bitcoins.")
                Closing_Investment.config(state="normal")
                Closing_Investment.delete(0, 'end')
                Closing_Investment.insert(0, f"Purchasing: {num_bitcoins:.6f}")
                Closing_Investment.config(state="readonly")
            else:
                messagebox.showerror("Error", "Could not retrieve closing price for Bitcoin. Data might be unavailable or empty.")
        else:
            messagebox.showerror("Error", "Invalid investment type selected or data unavailable.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")


def Investmenttype():
    A0 = Password.get()
    A1 = PInvestment_type.get()
    A2 = Account_number
    A3 = InvestmentA.get()
    A5 = Closing_Investment.get()
    Investmentmarket()
    if A5 == "Latest Closing Price" or not A5:
        messagebox.showerror("Error", "Please fill in all the required details: Return.")
        return
    
    A5_cleaned = re.sub(r'[^\d.]', '', A5).strip()

    try:
        A5 = float(A5_cleaned)
    except ValueError:
        messagebox.showerror("Error", "Invalid Investment return value. Please enter a valid number.")
        return

    
    if not A0 or A0 == "Password":
        messagebox.showerror("Error", "Password cannot be empty.")
        return
    if not A1 or A1 == "Select Your Investment":
        messagebox.showerror("Error", "Select a Investment Type.")
        return
    if not A3 or A3 == "Investment Amount" or not A3.isdigit():
        messagebox.showerror("Error", "Enter a valid Investment Amount.")
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
        
        cur.execute("SELECT Investment_type FROM clients_details WHERE account_number = %s;", (A2,))
        exist_Investment_type = cur.fetchone()

        if exist_Investment_type and exist_Investment_type[0]:
            messagebox.showinfo("Investment Exist",f"Investment already exists: '{exist_Investment_type[0]}'. No update has been performed.")
        else:
            confirm = messagebox.askyesno("Confirm Investment", f"Are you sure you want to invest in {A3}?")
            if not confirm:
                return
            
            cur.execute(
            """
            UPDATE clients_details
            SET Investment_Type = %s, Investment_Amount = %s, Investment_Return = %s
            WHERE Account_Number = %s;
            """,
            (A1, A3, A5, A2),
        )
            db.commit()
            from smtpEmail import Investment_Email
            Investment_Email()
            messagebox.showinfo("Successful",f"Your money has been successfully invested in {A1}. We appreciate your trust in our services.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        db.close()

def update_time():
    time_label.config(text=f"{strftime('%H:%M %p')}")
    top.after(1000, update_time)

def Investmentchoose():
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

LHeading = Label(top, text='Investment Overview', bg='lightblue', fg='Black', font=('Bookman Old Style', 30, 'bold'),justify="center")
LHeading.place(relx=0.5, y=200, anchor="center")


LAHeading = Label(frame, text='Investment', bg='lightblue', fg='Black', font=('Bookman Old Style', 30, 'bold'),justify="center")
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

Investment_account1=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
Investment_account1.place(x=50,y=550)
Investment_account1.insert(0,f"{Investment}")
Investment_account1.config(state="readonly",readonlybackground="lightblue")
frameInvestment_account =Frame(frame,width=342,height=2,bg="black").place(x=50, y=582)

balance1=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
balance1.place(x=50,y=650)
balance1.insert(0,f"{Balance}")
balance1.config(state="readonly",readonlybackground="lightblue")
framebalance =Frame(frame,width=342,height=2,bg="black").place(x=50, y=682)

######################frame2

frame2 =LabelFrame(top,width=450,height=800,bg="lightblue")
frame2.place_forget()

AHeading = Label(top, text='Invest Your Money', bg='lightblue', fg='Black', font=('Bookman Old Style', 30, 'bold'),justify="center")
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


Email1=Entry(frame2, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
Email1.place(x=50,y=260)
Email1.insert(0,f"{Email}")
Email1.config(state="readonly",readonlybackground="lightblue")
frameemail =Frame(frame2,width=342,height=2,bg="black").place(x=50, y=292)

def on_click1(e):
    InvestmentA.delete(0,"end")
    InvestmentA.config(validate="key", validatecommand=Investment_amount)

def on_focus_out1(e):
    investment = InvestmentA.get()
    if investment == "":
        InvestmentA.config(validate="none")
        InvestmentA.insert(0," Amount")

def validate_digit_input(P):
    return P.isdigit() or P == ""

Investment_amount = (top.register(validate_digit_input), '%P')

InvestmentA=Entry(frame2, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
InvestmentA.place(x=50,y=330)
InvestmentA.insert(0,"Investment Amount")
InvestmentA.bind("<FocusIn>", on_click1)
InvestmentA.bind("<FocusOut>", on_focus_out1)
frameamount =Frame(frame2,width=342,height=2,bg="black").place(x=50, y=362)

Investment_type = ["Select Your Investment", "Reliance Industries Limited (Stocks & Shares)", "Bitcoin (Cryptocurrency)"]
PInvestment_type=ttk.Combobox(frame2,values=Investment_type, width=25,font=("Bookman Old Style", 15, "bold"),state="readonly",justify="center")
PInvestment_type.place(x=50,y=400)
PInvestment_type.current(0)
frametype1 =Frame(frame2,width=347,height=2,bg="black").place(x=50, y=430)
frametype2 =Frame(frame2,width=347,height=2,bg="black").place(x=50, y=400)
frametype3 =Frame(frame2,width=2,height=32,bg="black").place(x=50, y=400)
frametype4 =Frame(frame2,width=2,height=32,bg="black").place(x=396, y=400)

Closing_Investment= Entry(frame2, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20),justify="center")
Closing_Investment.place(x=50,y=470)
Closing_Investment.insert(0,"Latest Closing Price")
Closing_Investment.config(state="readonly",readonlybackground="Lightblue")
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
b1 = Button(top, cursor="hand2", width=20, pady=7, text='Apply Now', bg='lightblue', fg='Black', border=10, font=('Bookman Old Style', 15),command=Investmentchoose)
b1.place(x=700, y=750)
b2 = Button(frame2,cursor="hand2", width=20, pady=7, text='Latest Closing Price', bg='#98FF98',fg='Black', border=0, font=('Arial', 20, "bold"),command=Investmentmarket)
b2.place_forget()
b4 = Button(frame2,cursor="hand2", width=20, pady=7, text='Submit', bg='#98FF98',fg='Black', border=0, font=('Arial', 20, "bold"),command=Investmenttype)
b4.place_forget()
b5 = Button(frame2,cursor="hand2", width=5, pady=7, text='←', bg="lightblue",fg='Black', border=0, font=('Arial', 15, "bold"), command=default)
b5.place_forget()

update_time()
top.mainloop()
