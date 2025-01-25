from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk
import pymysql as sql
import re
import requests
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

Email, Password, Name, Lastname, Contact, Account_number, BalanceExchange = get_login_data()

def typed():
    global Foreign_exchange,Balance
    db = sql.connect(host='localhost', user='root', password='7011', db='banking')
    cur = db.cursor()
    query = """SELECT clients_details.foreign_exchange_from,clients_details.foreign_exchange_amount  FROM clients JOIN 
                clients_details ON clients.Account_Number = clients_details.Account_Number
                WHERE clients.Account_Number =%s;"""
    cur.execute(query, (Account_number))
    result = cur.fetchall()
    if result:
        for col in result:
            Foreign_exchange =col[0] if col[0] else "No Foreign Exchange"
            Balance =col[1] if col[1] else "No Foreign Exchange"
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
            messagebox.showerror("Error", f"Error fetching exchange rates: {data.get('error-type', 'Unknown error')}")
            return None
    except Exception as e:
        messagebox.showerror("Error", f"Error connecting to the API: {e}")
        return None

def Foreign_Exchange_price():
    D1s = PForeign_Exchange_type.get() 
    D2s = PForeign_Exchange_values.get() 
    A1f = Foreign_ExchangeA.get()
    
    if not A1f or A1f == "Exchange Amount":
        messagebox.showerror("Error", "Enter a valid Exchange Amount.")
        return

    if not D1s or D1s == "Exchange From":
        messagebox.showerror("Error", "Select a currency from which you want to change.")
        return
    if not D2s or D2s == "Exchange To":
        messagebox.showerror("Error", "Select a currency to exchange into.")
        return
    
    A1 = float(A1f)

    try:
        D1 = [key for key, value in Exchange_to.items() if value == D1s][0]
    except IndexError:
        messagebox.showerror("Error", "Invalid Exchange Currency. Please select a valid number of years.")
        return
    
    try:
        D2 = [key for key, value in Exchange_to.items() if value == D2s][0]
    except IndexError:
        messagebox.showerror("Error", "Invalid Exchange Currency. Please select a valid number of years.")
        return
    
    if A1 < 10000:
        messagebox.showerror("Error", "Exchange amount must be ₹10,000 or higher.")
        return

    if not D1 or not D2 or not A1:
        messagebox.showerror("Error", "Please fill in all the required fields: Currency type, Amount.")
        return

    rate = get_exchange_rate(D1, D2)
    
    if rate is None:
        return 
    converted_amount = A1 * rate

    messagebox.showinfo("Conversion Result", f"{A1} {D1} = {converted_amount:.2f} {D2}")
    Market_Foreign_Exchange.config(state="normal")
    Market_Foreign_Exchange.delete(0, 'end')
    Market_Foreign_Exchange.insert(0, f"{D2}: ₹{converted_amount:.2f}")
    Market_Foreign_Exchange.config(state="readonly")

def Foreign_Exchange_type():
        A0 = Password.get()
        D2 = PForeign_Exchange_type.get() 
        A2 = Account_number
        A3 = Foreign_ExchangeA.get()
        D1 = PForeign_Exchange_values.get()
        A5 = Market_Foreign_Exchange.get()
        Foreign_Exchange_price()

        if not A3 or A3 == "Exchange Amount":
            messagebox.showerror("Error", "Enter a valid Exchange Amount.")
            return

        if A5 == "Market Value" or not A5:
            messagebox.showerror("Error", "Please fill in all the required details: Market Value.")
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
            A4 = [key for key, value in Exchange_from.items() if value == D1][0]
        except IndexError:
            messagebox.showerror("Error", "Invalid Exchange Currency. Please select a valid number of years.")
            return
        try:
            A1 = [key for key, value in Exchange_to.items() if value == D2][0]
        except IndexError:
            messagebox.showerror("Error", "Invalid Exchange Currency. Please select a valid number of years.")
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

            cur.execute("SELECT  foreign_exchange_from FROM clients_details WHERE account_number = %s;", (A2,))
            exist_foreign_exchange_from = cur.fetchone()

            if exist_foreign_exchange_from and exist_foreign_exchange_from[0]:
                messagebox.showinfo("Depsoit Exist",f"Foreign Exchange already exists: '{exist_foreign_exchange_from[0]}'. No update performed.")
            else:
                confirm = messagebox.askyesno("Confirm Foreign Exchange", f"Are you sure you want to exchange {A3}?")
                if not confirm:
                    return
                
                cur.execute(
                """
                UPDATE clients_details
                SET  foreign_exchange_from = %s,  foreign_exchange_Amount = %s, foreign_exchange_to = %s, foreign_exchange_converted = %s
                WHERE Account_Number = %s;
                """,
                (A1, A3, A4, A5, A2),
            )
                db.commit()
                from smtpEmail import Exchange_Email
                Exchange_Email()
                messagebox.showinfo("Successful",f"The exchange from {A1} to {A4} has been successfully completed.")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            db.close()

def update_time():
    time_label.config(text=f"{strftime('%H:%M %p')}")
    top.after(1000, update_time)

def Foreign_Exchange_Choose():
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

LHeading = Label(top, text='Foreign Exchange\nOverview', bg='lightblue', fg='Black', font=('Bookman Old Style', 30, 'bold'),justify="center")
LHeading.place(relx=0.5, y=200, anchor="center")


LAHeading = Label(frame, text='Foreign Exchange', bg='lightblue', fg='Black', font=('Bookman Old Style', 30, 'bold'),justify="center")
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

Foreign_Exchange_account1=Entry(frame, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
Foreign_Exchange_account1.place(x=50,y=550)
Foreign_Exchange_account1.insert(0,f"{Foreign_exchange}")
Foreign_Exchange_account1.config(state="readonly",readonlybackground="lightblue")
frameForeign_Exchange_account =Frame(frame,width=342,height=2,bg="black").place(x=50, y=582)

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

def on_click1(e):
    Foreign_ExchangeA.delete(0,"end")
    Foreign_ExchangeA.config(validate="key", validatecommand=Foreign_Exchange_amount)

def on_focus_out1(e):
    foreign_exchange = Foreign_ExchangeA.get()
    if foreign_exchange == "":
        Foreign_ExchangeA.config(validate="none")
        Foreign_ExchangeA.insert(0," Amount")

def validate_digit_input(P):
    return P.isdigit() or P == ""

Foreign_Exchange_amount = (top.register(validate_digit_input), '%P')

Foreign_ExchangeA=Entry(frame2, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20), justify="center")
Foreign_ExchangeA.place(x=50,y=260)
Foreign_ExchangeA.insert(0,"Exchange Amount")
Foreign_ExchangeA.bind("<FocusIn>", on_click1)
Foreign_ExchangeA.bind("<FocusOut>", on_focus_out1)
frameamount =Frame(frame2,width=342,height=2,bg="black").place(x=50, y=292)

Exchange_from = {
    0.0: "Exchange From",
    "RUB" :"Russian Ruble",
    "JPY" :"Japanese Yen",
    "AED" :"United Arab Emirates Dirham, Dubai",
    "EUR" :"Euro",
    "USD" :"United States Dollar",
    "INR" :"Indian Rupee"
}
Foreign_Exchange_type1 = list(Exchange_from.values())
PForeign_Exchange_type=ttk.Combobox(frame2,values=Foreign_Exchange_type1, width=25,font=("Bookman Old Style", 15, "bold"),state="readonly",justify="center")
PForeign_Exchange_type.place(x=50,y=330)
PForeign_Exchange_type.current(0)
frametype1 =Frame(frame2,width=347,height=2,bg="black").place(x=50, y=360)
frametype2 =Frame(frame2,width=347,height=2,bg="black").place(x=50, y=330)
frametype3 =Frame(frame2,width=2,height=32,bg="black").place(x=50, y=330)
frametype4 =Frame(frame2,width=2,height=32,bg="black").place(x=396, y=330)

Exchange_to = {
    0.0: "Exchange To",
    "RUB" :"Russian Ruble",
    "JPY" :"Japanese Yen",
    "AED" :"United Arab Emirates Dirham, Dubai",
    "EUR" :"Euro",
    "USD" :"United States Dollar",
    "INR" :"Indian Rupee"
}
Exchange_values = list(Exchange_to.values())
PForeign_Exchange_values=ttk.Combobox(frame2,values=Exchange_values, width=25,font=("Bookman Old Style", 15, "bold"),state="readonly",justify="center")
PForeign_Exchange_values.place(x=50,y=400)
PForeign_Exchange_values.current(0)
frametype1 =Frame(frame2,width=347,height=2,bg="black").place(x=50, y=430)
frametype2 =Frame(frame2,width=347,height=2,bg="black").place(x=50, y=400)
frametype3 =Frame(frame2,width=2,height=32,bg="black").place(x=50, y=400)
frametype4 =Frame(frame2,width=2,height=32,bg="black").place(x=396, y=400)

Market_Foreign_Exchange= Entry(frame2, width=20,fg='Black', border=0, bg='lightblue', font=('Bookman Old Style', 20),justify="center")
Market_Foreign_Exchange.place(x=50,y=470)
Market_Foreign_Exchange.insert(0,"Market Value")
Market_Foreign_Exchange.config(state="readonly",readonlybackground="Lightblue")
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
b1 = Button(top, cursor="hand2", width=20, pady=7, text='Apply Now', bg='lightblue', fg='Black', border=10, font=('Bookman Old Style', 15),command=Foreign_Exchange_Choose)
b1.place(x=700, y=750)
b2 = Button(frame2,cursor="hand2", width=20, pady=7, text='Market Value', bg='#98FF98',fg='Black', border=0, font=('Arial', 20, "bold"),command=Foreign_Exchange_price)
b2.place_forget()
b4 = Button(frame2,cursor="hand2", width=20, pady=7, text='Submit', bg='#98FF98',fg='Black', border=0, font=('Arial', 20, "bold"),command=Foreign_Exchange_type)
b4.place_forget()
b5 = Button(frame2,cursor="hand2", width=5, pady=7, text='←', bg="lightblue",fg='Black', border=0, font=('Arial', 15, "bold"), command=default)
b5.place_forget()

update_time()
top.mainloop()
