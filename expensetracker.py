import tkinter as tk
from tkinter import messagebox
from tkinter import ttk 
import json     
import os
from datetime import datetime


FILE_NAME = "expenses.json"

CATEGORIES = [
    "Food & Dining",
    "Shopping",
    "Transportation",
    "Entertainment",
    "Healthcare",
    "Makeup & Skincare",
    "Travel",
    "Education",
    "Bills & Utilities",
    "Others"
]

#load the existing expenses 
def load_expenses():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return {}

#Save the expenses
def save_expenses(expenses):
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file)

def convert_old_data():
    """Convert old data format to new format if needed"""
    global expenses
    converted = False
    
    for category, value in list(expenses.items()):
        if isinstance(value, (int, float)):  # Old format
            # Convert to new format
            expense_entry = {
                "amount": value,
                "date": datetime.now().strftime("%Y-%m-%d") # Default date for old entries
            }
            expenses[category] = [expense_entry]
            converted = True
    
    if converted:
        save_expenses(expenses)
        print("Old data format converted to new format!")
    
#Add a new expense
def add_expenses():
    category = category_entry.get().strip()

    if not category:
        messagebox.showerror("Error", "Please select a category.")
        return
    
    try:
        amount = float(amount_entry.get())

        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Create expense entry with amount and date
        expense_entry = {
            "amount": amount,
            "date": current_date
        }

        if category not in expenses:
            expenses[category] = []

        expenses[category].append(expense_entry)

        save_expenses(expenses)
        update_display()
        category_entry.set('')
        amount_entry.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount.")

#Update expense display
def update_display():
    text_area.delete(1.0, tk.END)
    total = 0

    for category, expense_list in expenses.items():
        if isinstance(expense_list, list):
            category_total = 0
            text_area.insert(tk.END, f"{category}:\n")

            for expense in expense_list:
                amount = expense["amount"]
                date = expense["date"]
                text_area.insert(tk.END, f"  ${amount:.2f} on {date}\n")
                category_total += amount
                total += amount

            text_area.insert(tk.END, f"  Category Total: ${category_total:.2f}\n\n")

        else:
            text_area.insert(tk.END, f"{category}: ${expense_list:.2f}\n")
            total += expense_list
    
    text_area.insert(tk.END, f"GRAND TOTAL: ${total:.2f}")

#Main app
root = tk.Tk()
root.title("PennyPal - Expense Tracker ")
root.state('zoomed')
root.configure(bg="#FFD1F3")

expenses = load_expenses()
convert_old_data()

#Input fields
tk.Label(root, text="Category:", font=('Comic Sans MS',14, 'bold'),
         bg='#FFD1F3', fg='#8B008B').pack(pady=5)
category_entry = ttk.Combobox(root, values=CATEGORIES, state="normal", width=25, font=('Arial',12))
category_entry.pack(pady=5)

style = ttk.Style()
style.configure('TCombobox', 
               fieldbackground='#FFF0F5',  
               background='#FFB6C1')      

tk.Label(root, text="Amount:", font=('Comic Sans MS',14, 'bold'),
         bg='#FFD1F3', fg='#8B008B').pack(pady=5)
amount_entry = tk.Entry(root, font=('Arial',12), width=20)  
amount_entry.pack(pady=5)

tk.Button(root, text="Add Expense", command=add_expenses,
          font=('Comic Sans MS',12,'bold'), bg='#FF69B4',
          fg='white',     
          relief='raised',
          bd=3).pack(pady=10)
          
#Display area
text_area = tk.Text(root, height=25, width=70, font=('Consolas',12), bg='#FFF0F5', fg='black', relief='sunken', bd=2)
text_area.pack(pady=10, padx=20)
update_display()

root.mainloop()