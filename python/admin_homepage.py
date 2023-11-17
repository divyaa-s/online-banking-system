import csv
import tkinter as tk
from tkinter import messagebox

def main_application():
    root = tk.Tk()
    root.title("Admin Application")

    def search_account():
        search_window = tk.Toplevel(root)
        search_window.title("Search Account")

        label = tk.Label(search_window, text="Search Account", font=("Helvetica", 16))
        label.pack()

        search_label = tk.Label(search_window, text="Enter account number to search:")
        search_label.pack()
        search_entry = tk.Entry(search_window)
        search_entry.pack()

        result_text = tk.Text(search_window, height=10, width=40)
        result_text.pack()

        search_button = tk.Button(search_window, text="Search", command=lambda: perform_search(search_entry.get(), result_text))
        search_button.pack()

    def perform_search(account_number, result_text):
        try:
            with open('customers.csv', 'r', newline='') as csv_file:
                csv_reader = csv.reader(csv_file)
                found = False
                for row in csv_reader:
                    if row and row[0] == account_number:
                        result_text.delete('1.0', tk.END)
                        result_text.insert(tk.END, "Account Number: " + row[0] + "\n")
                        result_text.insert(tk.END, "Account Type: " + row[1] + "\n")
                        result_text.insert(tk.END, "Account Holder: " + row[2] + "\n")
                        result_text.insert(tk.END, "Email id: " + row[5] + "\n")
                        result_text.insert(tk.END, "Phone number: " + row[6] + "\n")
                        result_text.insert(tk.END, "Balance: " + row[2] + "\n")
                        found = True
                        break
                if not found:
                    result_text.delete('1.0', tk.END)
                    result_text.insert(tk.END, "Account not found.")
        except FileNotFoundError:
            pass

    def delete_account():
        delete_window = tk.Toplevel(root)
        delete_window.title("Delete Account")

        label = tk.Label(delete_window, text="Delete Account", font=("Helvetica", 16))
        label.pack()

        delete_label = tk.Label(delete_window, text="Enter account number to delete:")
        delete_label.pack()
        delete_entry = tk.Entry(delete_window)
        delete_entry.pack()

        delete_button = tk.Button(delete_window, text="Delete", command=lambda: confirm_delete(delete_entry.get()))
        delete_button.pack()

    def confirm_delete(account_number):
        confirm_window = tk.Toplevel(root)
        confirm_window.title("Confirm Deletion")

        confirm_label = tk.Label(confirm_window, text="Are you sure you want to delete this account?")
        confirm_label.pack()

        confirm_button = tk.Button(confirm_window, text="Yes", command=lambda: perform_delete(account_number))
        confirm_button.pack()

        cancel_button = tk.Button(confirm_window, text="No", command=confirm_window.destroy)
        cancel_button.pack()

    def perform_delete(account_number):
        try:
            with open('customers.csv', 'r', newline='') as csv_file:
                rows = list(csv.reader(csv_file))

            found = False
            updated_rows = []

            for row in rows:
                if row and row[0] == account_number:
                    found = True
                else:
                    updated_rows.append(row)

            if found:
                with open('customers.csv', 'w', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerows(updated_rows)

                messagebox.showinfo("Account Deleted", f"Account {account_number} has been deleted.")
            else:
                messagebox.showerror("Account Not Found", f"Account {account_number} not found.")

        except FileNotFoundError:
            pass

    label = tk.Label(root, text="Admin Homepage", font=("Helvetica", 16))
    label.pack()
    search_button = tk.Button(root, text="Search Account", command=search_account)
    search_button.pack()
    delete_button = tk.Button(root, text="Delete Account", command=delete_account)
    delete_button.pack()
    exit_button = tk.Button(root, text="Exit", command=root.destroy)
    exit_button.pack()

    root.mainloop()


