import smtplib
import json
from time import strftime 
import pymysql as sql
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

Time = strftime('%H:%M %p')
Date = strftime('%d/%m/%y')

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
            print("No Record Found")

    except Exception as error:
        print(error)

    finally:
        cur.close()
        db.close()

getbalance()


def get_credentials(file_path):
    credentials = {}
    with open(file_path, "r") as file:
        for line in file:
            key, value = line.strip().split(":")
            credentials[key.strip()] = value.strip('"').strip()
    return credentials

credentials = get_credentials("password.txt")
sender_email = credentials["email"]
password = credentials["password"]

def Data():
    global Account_type, deposit_type, deposit_amount, deposit_return, deposit_time
    global loan_type, loan_amount, loan_return, loan_time
    global insurance_type, insurance_amount, insurance_return, insurance_time
    global investment_type, investment_amount, investment_purchased
    global foreign_exchange_from, foreign_exchange_amount, foreign_exchange_to, foreign_exchange_converted
    global Loan_due_amount, Loan_paid_amount

    db = sql.connect(host='localhost', user='root', password='7011', db='banking')
    cur = db.cursor()
    query = query = """
            SELECT * FROM clients c
            JOIN clients_details cd ON c.account_number = cd.account_number
            WHERE c.account_number = %s;
        """
    try:
        cur.execute(query, (Account_number))
        result = cur.fetchall()
        if result:
            for col in result:
                Account_type = col[8]
                deposit_type = col[9]
                deposit_amount = col[10]
                deposit_return = col[11]
                deposit_time = col[12]
                loan_type = col[13]
                loan_amount = col[14]
                loan_return = col[15]
                loan_time = col[16]
                insurance_type = col[17]
                insurance_amount = col[18]
                insurance_return = col[19]
                insurance_time = col[20]
                investment_type = col[21]
                investment_amount = col[22]
                investment_purchased = col[23]
                foreign_exchange_from = col[24]
                foreign_exchange_amount = col[25]
                foreign_exchange_to = col[26]
                foreign_exchange_converted = col[27]
                Loan_due_amount = col[28]
                Loan_paid_amount = col[29]
        else:
            print("Error", "No Record Found")
    except Exception as error:
        print("Error", error)
        print(error)

    finally:
        cur.close()
        db.close()

Data()
def send_email(subject, body, receiver_email):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            print("Connecting to SMTP server...")
            server.starttls()
            print("Starting TLS...")
            server.login(sender_email, password)
            print("Logged in as:", sender_email)
            server.send_message(message)
            print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def register_email():
    receiver_email = Email
    subject = "Welcome to ABC Bank Corporation – Thank You for Registering!"
    body = f"""
Dear {Name} {Lastname},

We are delighted to welcome you to the ABC Bank Corporation family! Thank you for choosing us as your trusted partner for your financial needs.
Congratulations on successfully completing your registration with us.

Your account number is: {Account_number}.

Best regards,
The ABC Bank Team
    """
    send_email(subject, body, receiver_email)

def login_email():
    Data()
    receiver_email = Email
    subject = "Login Attempt Warning - ABC Bank Corporation"
    body = f"""
Dear {Name} {Lastname},

We noticed an attempt to log in to your account at ABC Bank Corporation from an unrecognized device or location.

If this was you, there is no action required. If not, please take immediate action to secure your account.

Best regards,
The ABC Bank Team
"""
    send_email(subject, body, receiver_email)

def Profile_Compltion_Email():
    Data()
    receiver_email = Email
    subject = "Your ABC Bank Account Setup and Profile Completion"
    body = f"""
Dear {Name} {Lastname},

We are pleased to inform you that your account with ABC Bank Corporation has been successfully set up. Your profile has been completed, and you are now ready to start using your account.

Account Details:

- Account Type: {Account_type}
- Account Number: {Account_number}
    
To ensure the security and smooth operation of your account, please keep your login credentials safe.

Best regards,
The ABC Bank Team
    """
    send_email(subject, body, receiver_email)

def Loan_Payment_Email():
    Data()
    receiver_email = Email
    subject = "Loan Payment Confirmation - ABC Bank Corporation"
    body = f"""
Dear {Name} {Lastname},

We are writing to confirm the payment of your {loan_type}.

Loan Details:
- Loan Type: {loan_type}
- Loan Amount: {loan_amount}/-
- Loan Repayment: {loan_return}/-
- Loan Time: {loan_time} years
- Loan Due Amount: {Loan_due_amount}/-
- Amount Paid: {Loan_paid_amount}/-
    
Your payment has been successfully processed, and the loan balance has been updated accordingly.

Best regards,
The ABC Bank Team
    """
    send_email(subject, body, receiver_email)

def Loan_approval_Email():
    Data()
    receiver_email = Email
    subject = "Loan Approval/Concession Confirmation"
    body = f"""
Dear {Name} {Lastname},

We are pleased to inform you that your request for a {loan_type} has been successfully accepted, and the terms have been approved as per your request.

Loan Details:
- Loan Type: {loan_type}
- Loan Amount: {loan_amount}/-
- Loan Repayment: {loan_return}/-
- Loan Time: {loan_time} years

Best regards,
The ABC Bank Team
    """
    send_email(subject, body, receiver_email)

def Investment_Email():
    Data()
    receiver_email = Email
    subject = "Investment Confirmation - ABC Bank Corporation"
    body = f"""
Dear {Name} {Lastname},

We are pleased to inform you that your {investment_type} investment has been successfully processed.

Investment Details:
- Investment Type: {investment_type}
- Amount Invested: {investment_amount}/-
- Purchased: {investment_purchased}/-
    
Your investment is now active, and you will start receiving returns as per the terms outlined.

Best regards,
The ABC Bank Team
    """
    send_email(subject, body, receiver_email)

def Insurance_Email():
    Data()
    receiver_email = Email
    subject = "Insurance Purchase Confirmation - ABC Bank Corporation"
    body = f"""
Dear {Name} {Lastname},

We are pleased to confirm that your {insurance_type} has been successfully purchased.

Insurance Details:
- Insurance Type: {insurance_type}
- Coverage Amount: {insurance_amount}/-
- Policy Duration: {insurance_time} years
- Premium Amount: {insurance_return}/-

Your policy is now active, and you are protected under the terms of the purchased insurance.

Best regards,
The ABC Bank Team
    """
    send_email(subject, body, receiver_email)

def Exchange_Email():
    Data()
    receiver_email = Email
    subject = "Exchange Transaction Confirmation - ABC Bank Corporation"
    body = f"""
Dear {Name} {Lastname},

We are pleased to confirm that your foreign exchange transaction has been successfully completed.

Transaction Details:
- From Currency: {foreign_exchange_from}
- To Currency: {foreign_exchange_to}
- Amount Exchanged: {foreign_exchange_amount}/-
- Converted Amount: {foreign_exchange_converted}/-

Best regards,
The ABC Bank Team
    """
    send_email(subject, body, receiver_email)

def Deposit_Email():
    Data()
    receiver_email = Email
    subject = "Deposit Confirmation - ABC Bank Corporation"
    body = f"""
Dear {Name} {Lastname},

We are pleased to confirm that your deposit has been successfully processed.

Deposit Details:
- Deposit Type: {deposit_type}
- Amount Deposited: {deposit_amount}/-
- Return Amount: {deposit_return}/-
- Deposit Duration: {deposit_time} years

Your deposit is now active, and the applicable returns will be credited as per the agreed terms.

Best regards,
The ABC Bank Team
    """
    send_email(subject, body, receiver_email)

def Balance_Email():
    Data()
    getbalance()
    receiver_email = Email
    subject = "Credit Notification"
    body = f"""
Dear {Name} {Lastname},

We are pleased to inform you that your account has been credited.  
Your updated closing balance is {Balance}.

Thank you for banking with us.

Best regards,  
ABC Bank Corporation
"""
    send_email(subject, body, receiver_email)
