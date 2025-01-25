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

def update_time():
    time_label.config(text=f"{strftime('%H:%M %p')}")
    top.after(1000, update_time)

def Back2():
    top.destroy()
    subprocess.call(["python", "Profile.py"])

def Exit():
    top.destroy()

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

Account = None

Email, Password, Name, Lastname, Contact, Account_number, Balance = get_login_data()

path2=r"Assests\Bank.png"
img2 = ImageTk.PhotoImage(Image.open(path2))
l2 =Label(top,image=img2,border=2,bg="lightblue")
l2.place(x=490, y=-170)

date_label = Label(top, text= f"{strftime('%d/%m/%y')}" ,font=("Bookman Old Style", 15), fg="#000000", bg="lightblue")
date_label.place(x=10,y=80)
time_label = Label(top,font=("Bookman Old Style", 15), fg="#000000", bg="lightblue")
time_label.place(x=10,y=110)

frame =LabelFrame(top,width=450,height=800,bg="lightblue")
frame.place(x=1080, y=20)

Heading = Label(top, text=f"Hii! {Name} {Lastname}.", bg='lightblue', fg='#000000', font=('Bookman Old Style', 30, 'bold'),justify="center")
Heading.place(relx=0.5, y=200, anchor="center")

def Back1():
    tv.place_forget()
    tv1.place_forget()
    tv2.place_forget()
    tv3.place_forget()
    tv4.place_forget()
    b8.place_forget()

def deposites():
    tv.place(x=50, y=300, height=100, width=900)
    b8.place(x=5, y=2)
    tv1.place_forget()
    tv2.place_forget()
    tv3.place_forget()
    tv4.place_forget()
    
    for i in tv.get_children():
        tv.delete(i)

    db = sql.connect(host='localhost', user='root', password='7011', db='banking')
    cur = db.cursor()
    query = query = """SELECT cd.deposit_type, cd.deposit_amount, cd.deposit_return, cd.deposit_time  FROM clients c 
                        JOIN clients_details cd ON 
                        c.account_number = cd.account_number 
                        WHERE c.account_number =%s"""
    try:
        cur.execute(query, (Account_number))
        result = cur.fetchall()
        if result:
            for col in result:
                Deposit =col[0] if col[0] else "No Deposit"
                Deposit_Amount =col[1] if col[1] else "No Deposit"
                Deposit_Return =col[2] if col[2] else "No Deposit"
                Deposit_Time =col[3] if col[3] else "No Deposit"
                tv.insert("", "end", values=("","","",""))
                tv.insert("", "end", values=(Account_number , Deposit, Deposit_Amount, Deposit_Return, Deposit_Time))

                
        else:
            messagebox.showerror("Error", "No Record Found")
    except Exception as error:
        messagebox.showerror("Error", error)
        print(error)

    finally:
        cur.close()
        db.close()

def Insurance():
    tv1.place(x=50, y=300, height=100, width=900)
    b8.place(x=5, y=2)
    tv.place_forget()
    tv2.place_forget()
    tv3.place_forget()
    tv4.place_forget()
    
    for i in tv1.get_children():
        tv1.delete(i)

    db = sql.connect(host='localhost', user='root', password='7011', db='banking')
    cur = db.cursor()
    query = query = """SELECT cd.insurance_type, cd.insurance_amount, cd.insurance_return, cd.insurance_time  FROM clients c 
                        JOIN clients_details cd ON 
                        c.account_number = cd.account_number 
                        WHERE c.account_number =%s"""
    try:
        cur.execute(query, (Account_number))
        result = cur.fetchall()
        if result:
            for col in result:
                Insurance =col[0] if col[0] else "No Insurance"
                Insurance_Amount =col[1] if col[1] else "No Insurance"
                Insurance_Return =col[2] if col[2] else "No Insurance"
                Insurance_Time =col[3] if col[3] else "No Insurance"
                tv1.insert("", "end", values=("","","",""))
                tv1.insert("", "end", values=(Account_number, Insurance, Insurance_Amount, Insurance_Return, Insurance_Time))

                
        else:
            messagebox.showerror("Error", "No Record Found")
    except Exception as error:
        messagebox.showerror("Error", error)
        print(error)

    finally:
        cur.close()
        db.close()
    
def Investments():
    tv2.place(x=50, y=300, height=100, width=900)
    b8.place(x=5, y=2)
    tv1.place_forget()
    tv.place_forget()
    tv3.place_forget()
    tv4.place_forget()
    
    for i in tv2.get_children():
        tv2.delete(i)
        
    db = sql.connect(host='localhost', user='root', password='7011', db='banking')
    cur = db.cursor()
    query = query = """SELECT cd.investment_type, cd.investment_amount, cd.investment_return  FROM clients c 
                        JOIN clients_details cd ON 
                        c.account_number = cd.account_number 
                        WHERE c.account_number =%s"""
    try:
        cur.execute(query, (Account_number))
        result = cur.fetchall()
        if result:
            for col in result:
                Investment =col[0] if col[0] else "No Investment"
                Investment_Amount =col[1] if col[1] else "No Investment"
                Investment_Return =col[2] if col[2] else "No Investment"
                tv2.insert("", "end", values=("","","",""))
                tv2.insert("", "end", values=(Account_number, Investment, Investment_Amount, Investment_Return))

                
        else:
            messagebox.showerror("Error", "No Record Found")
    except Exception as error:
        messagebox.showerror("Error", error)
        print(error)

    finally:
        cur.close()
        db.close()

def Foriegn():
    tv3.place(x=50, y=300, height=100, width=900)
    b8.place(x=5, y=2)
    tv1.place_forget()
    tv2.place_forget()
    tv.place_forget()
    tv4.place_forget()

    for i in tv3.get_children():
        tv3.delete(i)

    db = sql.connect(host='localhost', user='root', password='7011', db='banking')
    cur = db.cursor()
    query = query = """SELECT cd.foreign_exchange_from, cd.foreign_exchange_amount, cd.foreign_exchange_to, cd.foreign_exchange_converted  FROM clients c 
                        JOIN clients_details cd ON 
                        c.account_number = cd.account_number 
                        WHERE c.account_number =%s"""
    try:
        cur.execute(query, (Account_number))
        result = cur.fetchall()
        if result:
            for col in result:
                foreign_exchange_from =col[0] if col[0] else "No Foreign Exchange"
                foreign_exchange_to =col[1] if col[1] else "No Foreign Exchange"
                foreign_exchange_converted =col[2] if col[2] else "No Foreign Exchange"
                foreign_exchange_amount =col[3] if col[3] else "No Foreign Exchange"
                tv3.insert("", "end", values=("","","",""))
                tv3.insert("", "end", values=(Account_number , foreign_exchange_from,foreign_exchange_to,foreign_exchange_converted,foreign_exchange_amount))
  
        else:
            messagebox.showerror("Error", "No Record Found")
    except Exception as error:
        messagebox.showerror("Error", error)
        print(error)

    finally:
        cur.close()
        db.close()

def Loans():
    tv4.place(x=50, y=300, height=100, width=900)
    b8.place(x=5, y=2)
    tv1.place_forget()
    tv2.place_forget()
    tv3.place_forget()
    tv.place_forget()

    for i in tv4.get_children():
        tv4.delete(i)

    db = sql.connect(host='localhost', user='root', password='7011', db='banking')
    cur = db.cursor()
    query = query = """SELECT cd.loan_type , cd.loan_amount, cd.loan_return, cd.loan_time, cd.loan_due_amount, cd.loan_paid_amount  FROM clients c 
                        JOIN clients_details cd ON 
                        c.account_number = cd.account_number 
                        WHERE c.account_number =%s"""
    try:
        cur.execute(query, (Account_number))
        result = cur.fetchall()
        if result:
            for col in result:
                Loan_type  =col[0] if col[0] else "No Foreign Exchange"
                Loan_return =col[1] if col[1] else "No Foreign Exchange"
                Loan_time =col[2] if col[2] else "No Foreign Exchange"
                Loan_amount =col[3] if col[3] else "No Foreign Exchange"
                Loan_due_amount =col[4] if col[4] else "No Foreign Exchange"
                Loan_paid_amount =col[5] if col[5] else "No Foreign Exchange"
                tv4.insert("", "end", values=("","","",""))
                tv4.insert("", "end", values=(Account_number , Loan_type , Loan_return, Loan_time, Loan_amount, Loan_due_amount, Loan_paid_amount))
  
        else:
            messagebox.showerror("Error", "No Record Found")
    except Exception as error:
        messagebox.showerror("Error", error)
        print(error)

    finally:
        cur.close()
        db.close()
    

tv = ttk.Treeview(top)
tv['column'] = ("A/C","Deposit Type", "Deposit Amount", "Deposit Returns", "Deposit Maturity")
tv.column("#0", width=0,stretch=0)
tv.column("A/C", anchor=CENTER,width=50)
tv.column("Deposit Type", anchor=CENTER,width=150)
tv.column("Deposit Amount", anchor=CENTER, width=150)
tv.column("Deposit Returns", anchor=CENTER,width=150)
tv.column("Deposit Maturity", anchor=CENTER,width=50)

tv.heading("A/C", text="A/C",anchor=CENTER)
tv.heading("Deposit Type", text="Deposit Type",anchor=CENTER)
tv.heading("Deposit Amount", text="Deposit Amount",anchor=CENTER)
tv.heading("Deposit Returns", text="Deposit Returns",anchor=CENTER)
tv.heading("Deposit Maturity", text="Deposit Maturity",anchor=CENTER)
tv.place_forget()

tv1 = ttk.Treeview(top)
tv1['column'] = ("A/C","Insurance Type", "Insurance Amount", "Insurance Returns", "Insurance Valid")
tv1.column("#0", width=0,stretch=0)
tv1.column("A/C", anchor=CENTER,width=50)
tv1.column("Insurance Type", anchor=CENTER,width=150)
tv1.column("Insurance Amount", anchor=CENTER, width=150)
tv1.column("Insurance Returns", anchor=CENTER,width=150)
tv1.column("Insurance Valid", anchor=CENTER,width=50)

tv1.heading("A/C", text="A/C",anchor=CENTER)
tv1.heading("Insurance Type", text="Insurance Type",anchor=CENTER)
tv1.heading("Insurance Amount", text="Insurance Amount",anchor=CENTER)
tv1.heading("Insurance Returns", text="Insurance Returns",anchor=CENTER)
tv1.heading("Insurance Valid", text="Insurance Valid",anchor=CENTER)
tv1.place_forget()

tv2 = ttk.Treeview(top)
tv2['column'] = ("A/C","Investment Type", "Investment Amount", "Investment Returns")
tv2.column("#0", width=0,stretch=0)
tv2.column("A/C", anchor=CENTER,width=50)
tv2.column("Investment Type", anchor=CENTER,width=150)
tv2.column("Investment Amount", anchor=CENTER, width=150)
tv2.column("Investment Returns", anchor=CENTER,width=150)

tv2.heading("A/C", text="A/C",anchor=CENTER)
tv2.heading("Investment Type", text="Investment Type",anchor=CENTER)
tv2.heading("Investment Amount", text="Investment Amount",anchor=CENTER)
tv2.heading("Investment Returns", text="Investment Returns",anchor=CENTER)
tv2.place_forget()

tv3 = ttk.Treeview(top)
tv3['column'] = ("A/C","Foreign Exchange From", "Foreign Exchange Amount", "Foreign Exchange To", "Foreign Exchange Conversion")
tv3.column("#0", width=0,stretch=0)
tv3.column("A/C", anchor=CENTER,width=50)
tv3.column("Foreign Exchange From", anchor=CENTER,width=150)
tv3.column("Foreign Exchange Amount", anchor=CENTER, width=150)
tv3.column("Foreign Exchange To", anchor=CENTER,width=150)
tv3.column("Foreign Exchange Conversion", anchor=CENTER,width=150)

tv3.heading("A/C", text="A/C",anchor=CENTER)
tv3.heading("Foreign Exchange From", text="Foreign Exchange From",anchor=CENTER)
tv3.heading("Foreign Exchange Amount", text="Foreign Exchange Amount",anchor=CENTER)
tv3.heading("Foreign Exchange To", text="Foreign Exchange To",anchor=CENTER)
tv3.heading("Foreign Exchange Conversion", text="Foreign Exchange Conversion",anchor=CENTER)
tv3.place_forget()

tv4 = ttk.Treeview(top)
tv4['column'] = ("A/C","Loan Type", "Loan Amount", "Repayment", "Tenure", "Paid Amount", "Due Amount")
tv4.column("#0", width=0,stretch=0)
tv4.column("A/C", anchor=CENTER,width=50)
tv4.column("Loan Type", anchor=CENTER,width=150)
tv4.column("Loan Amount", anchor=CENTER, width=150)
tv4.column("Repayment", anchor=CENTER,width=150)
tv4.column("Tenure", anchor=CENTER,width=50)
tv4.column("Paid Amount", anchor=CENTER,width=150)
tv4.column("Due Amount", anchor=CENTER,width=150)

tv4.heading("A/C", text="A/C",anchor=CENTER)
tv4.heading("Loan Type", text="Loan Type",anchor=CENTER)
tv4.heading("Loan Amount", text="Loan Amount",anchor=CENTER)
tv4.heading("Repayment", text="Repayment",anchor=CENTER)
tv4.heading("Tenure", text="Tenure",anchor=CENTER)
tv4.heading("Paid Amount", text="Paid Amount",anchor=CENTER)
tv4.heading("Due Amount", text="Due Amount",anchor=CENTER)
tv4.place_forget()

b1=Button(top,cursor="hand2", width=5, pady=7, text='←', bg="lightblue",fg='Black', border=0, font=('Arial', 15, "bold"), command=Back2).place(x=5, y=2)
b2 = Button(frame, cursor="hand2", width=20, pady=7, text='Deposit', bg='lightblue', fg='Black', border=5, font=('Bookman Old Style', 15), command=deposites).place(x=100, y=150)
b3 = Button(frame, cursor="hand2", width=20, pady=7, text='Loans', bg='lightblue', fg='Black', border=5, font=('Bookman Old Style', 15), command=Loans).place(x=100, y=250)
b4 = Button(frame, cursor="hand2", width=20, pady=7, text='Insurance', bg='lightblue', fg='Black', border=5, font=('Bookman Old Style', 15), command=Insurance).place(x=100, y=350)
b5 = Button(frame, cursor="hand2", width=20, pady=7, text='Investments', bg='lightblue', fg='Black', border=5, font=('Bookman Old Style', 15), command=Investments).place(x=100, y=450)
b6 = Button(frame, cursor="hand2", width=20, pady=7, text='Foriegn Exchange', bg='lightblue', fg='Black', border=5, font=('Bookman Old Style', 15), command=Foriegn).place(x=100, y=550)
b7=Button(frame, cursor="hand2", width=20, pady=7, text='Exit', bg='lightblue', fg='Black', border=5, font=('Bookman Old Style', 15), command=Exit).place(x=100, y=650)
b8=Button(frame,cursor="hand2", width=5, pady=7, text='←', bg="lightblue",fg='Black', border=0, font=('Arial', 15, "bold"), command=Back1)
b8.place_forget()

update_time()
top.mainloop()
