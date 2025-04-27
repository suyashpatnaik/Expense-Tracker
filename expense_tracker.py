import csv
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import pandas as pd

FILE_NAME = "expenses.csv"
CATEGORIES = ["Food", "Transport", "Utilities", "Entertainment", "Shopping", "Others"]

def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Description", "Category", "Amount"])

def add_expense(): 
    desc = desc_entry.get()
    category = category_var.get()
    amount = amount_entry.get()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not desc or not amount:
        messagebox.showerror("Input Error", "Please fill all fields!")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Input Error", "Amount must be a number!")
        return

    with open(FILE_NAME, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, desc, category, amount])

    messagebox.showinfo("Success", "Expense added successfully!")
    desc_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

def view_expenses():
    try:
        df = pd.read_csv(FILE_NAME)
        if df.empty:
            messagebox.showinfo("Info", "No expenses recorded yet.")
            return
        show_dataframe(df, "All Expenses")
    except Exception as e:
        messagebox.showerror("Error", f"Could not read file: {e}")

def filter_by_date():
    start = start_entry.get()
    end = end_entry.get()
    try:
        df = pd.read_csv(FILE_NAME)
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        mask = (df["Date"] >= pd.to_datetime(start)) & (df["Date"] <= pd.to_datetime(end))
        filtered = df.loc[mask]
        if filtered.empty:
            messagebox.showinfo("Result", "No expenses found in this range.")
        else:
            show_dataframe(filtered, f"Filtered Expenses ({start} to {end})")
    except Exception as e:
        messagebox.showerror("Error", f"Invalid date format or data: {e}")

def monthly_report():
    try:
        df = pd.read_csv(FILE_NAME)
        if df.empty:
            messagebox.showinfo("Info", "No expenses recorded yet.")
            return
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["Month"] = df["Date"].dt.to_period("M")
        report = df.groupby(["Month", "Category"])["Amount"].sum().unstack(fill_value=0)
        show_dataframe(report, "Monthly Report")
    except Exception as e:
        messagebox.showerror("Error", f"Could not generate report: {e}")

def plot_expenses():
    try:
        df = pd.read_csv(FILE_NAME)
        if df.empty:
            messagebox.showinfo("Info", "No expenses recorded yet.")
            return
        df.groupby("Category")["Amount"].sum().plot(kind="pie", autopct="%1.1f%%")
        plt.title("Expenses by Category")
        plt.ylabel("")
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Could not plot expenses: {e}")

def show_dataframe(df, title="Data"):
    win = tk.Toplevel(root)
    win.title(title)

    frame = tk.Frame(win)
    frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(frame)
    tree["columns"] = list(df.columns)
    tree["show"] = "headings"

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    for _, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))

    tree.pack(expand=True, fill="both")

root = tk.Tk()
root.title("Expense Tracker")

initialize_file()

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

tk.Label(frame, text="Description:").grid(row=0, column=0)
desc_entry = tk.Entry(frame)
desc_entry.grid(row=0, column=1)

tk.Label(frame, text="Category:").grid(row=1, column=0)
category_var = tk.StringVar(value=CATEGORIES[0])
category_menu = ttk.Combobox(frame, textvariable=category_var, values=CATEGORIES)
category_menu.grid(row=1, column=1)

tk.Label(frame, text="Amount:").grid(row=2, column=0)
amount_entry = tk.Entry(frame)
amount_entry.grid(row=2, column=1)

tk.Button(frame, text="Add Expense", command=add_expense).grid(row=3, columnspan=2, pady=5)

filter_frame = tk.Frame(root, padx=10, pady=10)
filter_frame.pack()

tk.Label(filter_frame, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0)
start_entry = tk.Entry(filter_frame)
start_entry.grid(row=0, column=1)

tk.Label(filter_frame, text="End Date (YYYY-MM-DD):").grid(row=1, column=0)
end_entry = tk.Entry(filter_frame)
end_entry.grid(row=1, column=1)

tk.Button(filter_frame, text="Filter by Date", command=filter_by_date).grid(row=2, columnspan=2, pady=5)

btn_frame = tk.Frame(root, padx=10, pady=10)
btn_frame.pack()

tk.Button(btn_frame, text="View All Expenses", width=20, command=view_expenses).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Monthly Report", width=20, command=monthly_report).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Plot Expenses", width=20, command=plot_expenses).grid(row=0, column=2, padx=5)

root.mainloop()