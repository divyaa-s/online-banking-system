import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import csv
import re 
import random

# Validate phone function 
def validate_phone(char):
    if char.isdigit() and len(phone_var.get() + char) <= 10:
        return True
    else:
        return False
# Validate password function
def validate_password(password):
    # Password should be 8 to 12 characters and contain at least one special character
    pattern = r"^(?=.*[!@#$%^&*()_+}{:;'?/>.<,])(.){8,12}$"
    return re.match(pattern, password)
# Validate email function
def validate_email(email):
    # Regular expression for basic email validation
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(email_regex, email):
        return True
    else:
        return False

    
def submit():
    type_input = type_var.get().strip()
    name_input = name_var.get().strip()
    dob_input = dob_var.get().strip()
    address_input = address_var.get().strip()
    email_input = email_var.get().strip()
    phone_input = phone_var.get().strip()
    password_input = password_var.get().strip()
    confirm_password_input=confirm_password_var.get().strip()
    initial_balance_input = initial_balance_var.get().strip()

    if not (type_input and name_input and dob_input and address_input and email_input and phone_input and password_input and confirm_password_input):
        messagebox.showerror("Error", "All fields are required.")
        return

    if password_input != confirm_password_input:
        messagebox.showerror("Error", "Passwords do not match.")
        return
    
    if not validate_password(password_input):
        messagebox.showerror("Error", "Password should be 8 to 12 characters and contain at least one special character.")
        return
    
    # Validate email
    if not validate_email(email_input):
        messagebox.showerror("Error", "Invalid email address.")
        return
    
    account_number = ''.join(random.choices('0123456789', k=10))
    
    # Show a success message
    messagebox.showinfo('Success', 'Data saved successfully.')

    with open('customers.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([account_number, type_input, name_input, dob_input, address_input, email_input, phone_input, password_input,initial_balance_input])

    # Clear the input fields
    type_var.set('')
    name_var.set('')
    dob_var.set('')
    address_var.set('')
    email_var.set('')
    phone_var.set('')
    password_var.set('')
    confirm_password_var.set('')
    initial_balance_var.set('')

# Create main window
master = tk.Tk()
master.title('Customer Registration')

# Create and grid type label
tk.Label(master, text="Type").grid(row=1, column=0)
type_var = tk.StringVar()
type_var.set("Type Of Account")  # Default value
type_options = ['Savings', 'Current']
type_option_menu = tk.OptionMenu(master, type_var, *type_options)
type_option_menu.grid(row=1, column=1)

# Create and grid name label
tk.Label(master, text="Name").grid(row=3, column=0)
name_var = tk.StringVar()
name_entry = tk.Entry(master, textvariable=name_var)
name_entry.grid(row=3, column=1)

# Create and grid dob label
tk.Label(master, text="D.O.B").grid(row=4, column=0)
dob_var = tk.StringVar()
dob_entry = DateEntry(master, textvariable=dob_var, date_pattern='dd-mm-yyyy')
dob_entry.grid(row=4, column=1)

# Create and grid address label
tk.Label(master, text="Address").grid(row=5, column=0)
address_var = tk.StringVar()
address_entry = tk.Entry(master, textvariable=address_var)
address_entry.grid(row=5, column=1)

# Create and grid email label
tk.Label(master, text="Email").grid(row=6, column=0)
email_var = tk.StringVar()
email_entry = tk.Entry(master, textvariable=email_var)
email_entry.grid(row=6, column=1)

# Create and grid phone label
tk.Label(master, text="Phone").grid(row=7, column=0)
phone_var = tk.StringVar()
phone_entry = tk.Entry(master, textvariable=phone_var, validate='key')
phone_entry['validatecommand'] = (phone_entry.register(validate_phone), '%S')
phone_entry.grid(row=7,column=1)

# Create and grid password label
tk.Label(master, text="Password").grid(row=8, column=0)
password_var = tk.StringVar()
password_entry = tk.Entry(master, textvariable=password_var, show="*")
password_entry.grid(row=8, column=1)

# Create and grid confirm password label and entry
tk.Label(master, text="Confirm Password").grid(row=9, column=0)
confirm_password_var = tk.StringVar()
confirm_password_entry = tk.Entry(master, textvariable=confirm_password_var, show="*")
confirm_password_entry.grid(row=9, column=1)

tk.Label(master, text="Initial Balance").grid(row=10, column=0)
initial_balance_var = tk.StringVar()
initial_balance_entry = tk.Entry(master, textvariable=initial_balance_var)
initial_balance_entry.grid(row=10, column=1)

# Create and grid submit button
submit_button = tk.Button(master, text="Submit", command=submit)
submit_button.grid(row=11, column=0)
quit_button = tk.Button(master, text="Quit", command=master.quit)
quit_button.grid(row=11, column=1)

# Run main loop
master.mainloop()
