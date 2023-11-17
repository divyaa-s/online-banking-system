import csv  
import tkinter as tk
from tkinter import messagebox
import re
import random
from tkcalendar import DateEntry
from tkinter import simpledialog, messagebox



from admin_homepage import main_application

# Define a global flag to track whether the admin homepage is open
admin_homepage_open = False


####################### ADMIN LOGIN ##########################
def open_admin_login():
    admin_login_window()

admin_window = None
def admin_login_window():
    global admin_window  # Declare admin_window as global  
    admin_window = tk.Toplevel()
    admin_window.title("Admin Page")
    admin_window.geometry("400x300")
    label = tk.Label(admin_window, text="Welcome to the Admin Page", font=("Helvetica", 16))
    label.pack()
    login_button = tk.Button(admin_window, text="Login", command=login_as_admin)
    login_button.pack()

def login_as_admin():
    # Use tkinter to create a simple login dialog for admin
    login_dialog = tk.Toplevel()
    login_dialog.title("Admin Login")
    label = tk.Label(login_dialog, text="Admin Login", font=("Helvetica", 14))
    label.pack()
    admin_username_label = tk.Label(login_dialog, text="Enter admin username:")
    admin_username_label.pack()
    admin_username_entry = tk.Entry(login_dialog)
    admin_username_entry.pack()
    admin_password_label = tk.Label(login_dialog, text="Enter admin password:")
    admin_password_label.pack()
    admin_password_entry = tk.Entry(login_dialog, show="*")
    admin_password_entry.pack()
    login_button = tk.Button(login_dialog, text="Login", command=lambda: validate_admin_login(login_dialog, admin_username_entry.get(), admin_password_entry.get()))
    login_button.pack()
   
def validate_admin_login(login_dialog, admin_username, admin_password):
    global admin_homepage_open
    if admin_homepage_open:
        return  # Prevent opening multiple admin homepage windows

    try:
        with open('admin_data.csv', 'r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if row and row[0] == admin_username and row[1] == admin_password:
                    messagebox.showinfo("Login Successful", "Logged in as an admin.")
                    login_dialog.destroy()   # Closes input window
                    admin_window.destroy()   # Closes admin page
                    main_application()  # Call the main_application function
                    admin_homepage_open = True  # Set the flag to indicate the admin homepage is open
                    return
    except FileNotFoundError:
        pass  # Handle file not found error or other exceptions
    messagebox.showerror("Login Failed", "Invalid username or password.")
 
################# CUSTOMER WINDOW ##########################

def open_customer_login():
    customer_login_window()


def customer_login_window():
    customer_window = tk.Toplevel()
    customer_window.title("Customer Page")
    customer_window.geometry("400x300")
    label = tk.Label(customer_window, text="Welcome to the Customer Page", font=("Helvetica", 16))
    label.pack()
    login_button = tk.Button(customer_window, text="Login", command=login_as_customer)
    login_button.pack()
    register_button = tk.Button(customer_window, text="Register", command=register_customer)
    register_button.pack()


def login_as_customer():
    # Use tkinter to create a simple login dialog
    login_dialog = tk.Toplevel()
    login_dialog.title("Customer Login")
    label = tk.Label(login_dialog, text="Customer Login", font=("Helvetica", 14))
    label.pack()
    cust_acc_label = tk.Label(login_dialog, text="Enter account number:")
    cust_acc_label.pack()
    cust_acc_entry = tk.Entry(login_dialog)
    cust_acc_entry.pack()
    cust_password_label = tk.Label(login_dialog, text="Enter account Password:")
    cust_password_label.pack()
    cust_password_entry = tk.Entry(login_dialog, show="*")
    cust_password_entry.pack()
    login_button = tk.Button(login_dialog, text="Login", command=lambda: validate_customer_login(login_dialog, cust_acc_entry.get(), cust_password_entry.get()))
    login_button.pack()

def validate_customer_login(login_dialog, cust_acc, cust_password):
    try:
        with open('customers.csv', 'r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if row and row[0] == str(cust_acc) and row[5] == str(cust_password):  # Assuming password is in the 6th column (index 5)
                    messagebox.showinfo("Login Successful", "Logged in as a customer.")
                    login_dialog.destroy()
                    run_bank_app()
                    return
    except FileNotFoundError:
        pass  # Handle file not found error or other exceptions
    messagebox.showerror("Login Failed", "Invalid account number or password.")



############ CUSTOMER REGISTER WINDOW ########

def register_customer():
    used_account_numbers = set()

    def generate_unique_account_number():
        while True:
            account_number = str(random.randint(10000, 99999))
            if account_number not in used_account_numbers:
                return account_number

    fieldnames = ['name', 'account_number']

    def add_user():
        name = name_entry.get()
        if name:
            account_number = generate_unique_account_number()
            user_data = {"name": name, "account_number": account_number}  # Include 'account_number' field
            used_account_numbers.add(account_number)
            save_to_csv(user_data)
            name_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "User Added Successfully")
            type_var.set('')
            name_var.set('')
            dob_var.set('')
            address_var.set('')
            email_var.set('')
            phone_var.set('')
            password_var.set('')
            confirm_password_var.set('')

    def save_to_csv(user_data):
        with open('customers.csv', mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(user_data)

    def validate_phone(char):
        if char.isdigit() and len(phone_var.get() + char) <= 10:
            return True
        return False

    def validate_password():
        password = password_var.get()
        pattern = r"^(?=.*[!@#$%^&*()_+}{:;'?/>.<,])(.){8,12}$"
        return bool(re.match(pattern, password))

    def confirm():
        type_input = type_var.get().strip()
        name_input = name_var.get().strip()
        dob_input = dob_var.get().strip()
        address_input = address_var.get().strip()
        email_input = email_var.get().strip()
        phone_input = phone_var.get().strip()
        password_input = password_var.get().strip()
        confirm_password_input = confirm_password_var.get().strip()
        if not (type_input and name_input and dob_input and address_input and email_input and phone_input and password_input and confirm_password_input):
            messagebox.showerror("Error", "All fields are required.")
            return
        if password_input != confirm_password_input:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        if not validate_password():
            messagebox.showerror("Error", "Password should be 8 to 12 characters and contain at least one special character.")
            return
        messagebox.showinfo('Confirmation', 'Kindly confirm the details')

    master = tk.Tk()
    master.title('Customer Registration')
    tk.Label(master, text="Type").grid(row=1, column=0)
    type_var = tk.StringVar()
    type_var.set("Type Of Account")  # Default value
    type_options = ['Savings', 'Current']
    type_option_menu = tk.OptionMenu(master, type_var, *type_options)
    type_option_menu.grid(row=1, column=1)
    tk.Label(master, text="Name").grid(row=2, column=0)
    name_var = tk.StringVar()
    name_entry = tk.Entry(master, textvariable=name_var)
    name_entry.grid(row=2, column=1)
    tk.Label(master, text="D.O.B").grid(row=3, column=0)
    dob_var = tk.StringVar()
    dob_entry = DateEntry(master, textvariable=dob_var, date_pattern='dd-mm-yyyy')
    dob_entry.grid(row=3, column=1)
    tk.Label(master, text="Address").grid(row=4, column=0)
    address_var = tk.StringVar()
    address_entry = tk.Entry(master, textvariable=address_var)
    address_entry.grid(row=4, column=1)
    tk.Label(master, text="Email").grid(row=5, column=0)
    email_var = tk.StringVar()
    email_entry = tk.Entry(master, textvariable=email_var)
    email_entry.grid(row=5, column=1)
    tk.Label(master, text="Phone").grid(row=6, column=0)
    phone_var = tk.StringVar()
    phone_entry = tk.Entry(master, textvariable=phone_var, validate='key')
    phone_entry['validatecommand'] = (phone_entry.register(validate_phone), '%S')
    phone_entry.grid(row=6, column=1)
    tk.Label(master, text="Password").grid(row=7, column=0)
    password_var = tk.StringVar()
    password_entry = tk.Entry(master, textvariable=password_var, show="*", validate="key")
    password_entry['validatecommand'] = (master.register(validate_password), '%P')
    password_entry.grid(row=7, column=1)
    tk.Label(master, text="Confirm Password").grid(row=8, column=0)
    confirm_password_var = tk.StringVar()
    confirm_password_entry = tk.Entry(master, textvariable=confirm_password_var, show="*")
    confirm_password_entry.grid(row=8, column=1)
    confirm_button = tk.Button(master, text="Confirm", command=confirm)
    confirm_button.grid(row=9, column=0)
    submit_button = tk.Button(master, text="Submit", command=add_user)
    submit_button.grid(row=9, column=1)
    quit_button = tk.Button(master, text="Quit", command=master.quit)
    quit_button.grid(row=9, column=2)
    master.mainloop()




class Bank:
    def __init__(self):
        self.admin_credentials = {'username': 'admin', 'password': 'admin_password'}
        self.customer_credentials = {'username': 'customer', 'password': 'customer_password'}
        self.current_user = None
    def create_account(self, id, name, initial_deposit=0):
        if id in self.accounts:
            return "Account ID already exists!"
        else:
            self.accounts[id] = {'name': name, 'balance': initial_deposit}
            return "Account created successfully!"

    def display_account_details(self, id):
        if id not in self.accounts:
            return "Account ID does not exist!"
        else:
            account = self.accounts[id]
            return f"Account Holder: {account['name']}\nAccount Number: {id}\nCurrent Balance: {account['balance']}"

    def deposit_money(self, id, amount):
        if id not in self.accounts:
            return "Account ID does not exist!"
        if not amount or amount <= 0:
            return "Invalid deposit amount. Amount must be a positive number."
        self.accounts[id]['balance'] += amount
        return f"Deposited amount: {amount}\nCurrent balance: {self.accounts[id]['balance']}"

    def withdraw_money(self, id, amount):
        if id not in self.accounts:
            return "Account ID does not exist!"
        if not amount or amount <= 0:
            return "Invalid withdrawal amount. Amount must be a positive number."
        account = self.accounts[id]
        if amount > account['balance']:
            return "Insufficient balance!"
        account['balance'] -= amount
        return f"Withdrawn amount: {amount}\nCurrent balance: {account['balance']}"

def run_bank_app():
    root = tk.Tk()
    root.title("Banking Application")
    bank = Bank()

    def display_account_details():
        id = simpledialog.askstring("Display Account Details", "Enter Account ID:")
        result = bank.display_account_details(id)
        messagebox.showinfo("Account Details", result)

    def deposit_money():
        id = simpledialog.askstring("Deposit Money", "Enter Account ID:")
        amount = float(simpledialog.askfloat("Deposit Money", "Enter Deposit Amount:"))
        result = bank.deposit_money(id, amount)
        messagebox.showinfo("Deposit Money", result)

    def withdraw_money():
        id = simpledialog.askstring("Withdraw Money", "Enter Account ID:")
        amount = float(simpledialog.askfloat("Withdraw Money", "Enter Withdrawal Amount:"))
        result = bank.withdraw_money(id, amount)
        messagebox.showinfo("Withdraw Money", result)


    display_account_details_button = tk.Button(root, text="Display Account Details", command=display_account_details)
    display_account_details_button.pack()

    deposit_money_button = tk.Button(root, text="Deposit Money", command=deposit_money)
    deposit_money_button.pack()

    withdraw_money_button = tk.Button(root, text="Withdraw Money", command=withdraw_money)
    withdraw_money_button.pack()

    exit_button = tk.Button(root, text="Exit", command=root.quit)
    exit_button.pack()
    root.mainloop()

def home_window():
    login_window = tk.Tk()
    login_window.title("Welcome to DJN Bank")


    label = tk.Label(login_window, text="Welcome to DJN Bank", font=("Helvetica", 16))
    label.pack()


    admin_button = tk.Button(login_window, text="Admin", command=open_admin_login)
    admin_button.pack()

    customer_button = tk.Button(login_window, text="Customer", command=open_customer_login)
    customer_button.pack()
    exit_button = tk.Button(login_window, text="Exit", command=login_window.destroy)
    exit_button.pack()


    login_window.mainloop()


home_window()





