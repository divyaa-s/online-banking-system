import csv
import tkinter as tk
from tkinter import simpledialog, messagebox

class OnlineBanking:
    def __init__(self):
        self.accounts = {}
        self.load_from_csv()  # Load existing data from CSV during initialization

        self.root = tk.Tk()
        self.root.title("Online Banking System")

        self.display_account_details_button = tk.Button(self.root, text="Display Account Details", command=self.display_account_details)
        self.display_account_details_button.pack()

        self.deposit_money_button = tk.Button(self.root, text="Deposit Money", command=self.deposit_money)
        self.deposit_money_button.pack()

        self.withdraw_money_button = tk.Button(self.root, text="Withdraw Money", command=self.withdraw_money)
        self.withdraw_money_button.pack()

        self.modify_details_button = tk.Button(self.root, text="Modify Account Details", command=self.modify_details)
        self.modify_details_button.pack()

        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit)
        self.exit_button.pack()

    def load_from_csv(self):
        try:
            with open('customers.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 9:
                        account_number, account_type, name, dob, address, email, phone_number, password, balance = row
                        self.accounts[account_number] = {
                            'account_type': account_type,
                            'name': name,
                            'dob': dob,
                            'address': address,
                            'email': email,
                            'phone_number': phone_number,
                            'password': password,
                            'balance': float(balance)
                        }
                    else:
                        print(f"Ignoring invalid row: {row}")
        except FileNotFoundError:
            print("CSV file not found. No existing data loaded.")
        except Exception as e:
            print(f"An error occurred while loading data from CSV: {e}")


    def display_account_details(self):
        account_number = simpledialog.askstring("Display Account Details", "Enter Account Number:")
        if account_number in self.accounts:
            account = self.accounts[account_number]
            result = f"Account Holder: {account['name']}\nAccount Number: {account_number}\n" \
                     f"Account Type: {account['account_type']}\nCurrent Balance: {account['balance']}"
            messagebox.showinfo("Account Details", result)
        else:
            messagebox.showerror("Error", "Account Number does not exist!")

    def deposit_money(self):
        account_number = simpledialog.askstring("Deposit Money", "Enter Account Number:")
        amount = float(simpledialog.askfloat("Deposit Money", "Enter Deposit Amount:"))
        if account_number in self.accounts:
            self.accounts[account_number]['balance'] += amount
            messagebox.showinfo("Deposit Money", f"Deposited amount: {amount}\nCurrent balance: {self.accounts[account_number]['balance']}")
        else:
            messagebox.showerror("Error", "Account Number does not exist!")

    def withdraw_money(self):
        account_number = simpledialog.askstring("Withdraw Money", "Enter Account Number:")
        amount = float(simpledialog.askfloat("Withdraw Money", "Enter Withdrawal Amount:"))
        if account_number in self.accounts:
            account = self.accounts[account_number]
            if amount <= account['balance']:
                account['balance'] -= amount
                messagebox.showinfo("Withdraw Money", f"Withdrawn amount: {amount}\nCurrent balance: {account['balance']}")
            else:
                messagebox.showerror("Error", "Insufficient balance!")
        else:
            messagebox.showerror("Error", "Account Number does not exist!")

    def modify_details(self):
        account_number = simpledialog.askstring("Modify Account Details", "Enter Account Number:")
        if account_number in self.accounts:
            account = self.accounts[account_number]
            new_phone_number = simpledialog.askstring("Modify Account Details", "Enter new phone number:")
            new_email = simpledialog.askstring("Modify Account Details", "Enter new email address:")
            old_email, old_phone_number = account['email'], account['phone_number']
            account['phone_number'] = new_phone_number
            account['email'] = new_email
            messagebox.showinfo("Modify Account Details", "Phone number and email updated successfully.")

            # Read existing data from the CSV file
            with open('customers.csv', 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)

            # Update the specific record with the modified details
            for i in range(len(rows)):
                if rows[i][0] == account_number:
                    rows[i][5] = new_email
                    rows[i][6] = new_phone_number

            # Write back the entire updated data to the CSV file
            with open('customers.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
        else:
            messagebox.showerror("Error", "Account Number does not exist!")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    banking_app = OnlineBanking()
    banking_app.run()
