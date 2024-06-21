import pickle
import tkinter as tk
from tkinter import messagebox

class BudgetTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Tracker")
        self.root.minsize(400, 200)
        self.root.maxsize(800, 600)
        
        self.income = 0
        self.expenses = []
        self.categories = {}

        self.load_data()

        # Configure grid for responsiveness
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_rowconfigure(i, weight=1)

        # Create and place widgets
        self.create_widgets()

    def create_widgets(self):
        # Income Widgets
        self.income_label = tk.Label(self.root, text="Income:")
        self.income_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.income_entry = tk.Entry(self.root)
        self.income_entry.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.income_button = tk.Button(self.root, text="Add Income", command=self.add_income)
        self.income_button.grid(row=0, column=2, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Expense Widgets
        self.expense_label = tk.Label(self.root, text="Expense:")
        self.expense_label.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.expense_category_entry = tk.Entry(self.root)
        self.expense_category_entry.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.expense_amount_entry = tk.Entry(self.root)
        self.expense_amount_entry.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        self.expense_button = tk.Button(self.root, text="Add Expense", command=self.add_expense)
        self.expense_button.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")

        # View Expenses Button
        self.view_expenses_button = tk.Button(self.root, text="View Expenses", command=self.view_expenses)
        self.view_expenses_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # View Remaining Budget Button
        self.view_budget_button = tk.Button(self.root, text="View Remaining Budget", command=self.view_budget)
        self.view_budget_button.grid(row=2, column=2, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Save and Quit Button
        self.save_button = tk.Button(self.root, text="Save and Quit", command=self.save_and_quit)
        self.save_button.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

    def add_income(self):
        try:
            amount = float(self.income_entry.get())
            self.income += amount
            self.income_entry.delete(0, tk.END)
            messagebox.showinfo("Income Added", f"Added income: {amount}")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for income.")

    def add_expense(self):
        try:
            category = self.expense_category_entry.get()
            amount = float(self.expense_amount_entry.get())
            self.expenses.append((category, amount))
            self.income -= amount
            self.categories[category] = self.categories.get(category, 0) + amount
            self.expense_category_entry.delete(0, tk.END)
            self.expense_amount_entry.delete(0, tk.END)
            messagebox.showinfo("Expense Added", f"Added expense: {category} - {amount}")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid inputs for expense category and amount.")

    def view_expenses(self):
        expenses_str = "\n".join([f"Category: {category}, Amount: {amount}" for category, amount in self.expenses])
        messagebox.showinfo("Expenses", expenses_str if expenses_str else "No expenses recorded.")

    def view_budget(self):
        remaining_budget = self.income - sum(amount for _, amount in self.expenses)
        messagebox.showinfo("Remaining Budget", f"Remaining Budget: {remaining_budget}")

    def save_and_quit(self):
        self.save_data()
        self.root.quit()

    def save_data(self):
        data = {
            "income": self.income,
            "expenses": self.expenses,
            "categories": self.categories,
        }
        with open("budget_data.pkl", "wb") as file:
            pickle.dump(data, file)

    def load_data(self):
        try:
            with open("budget_data.pkl", "rb") as file:
                data = pickle.load(file)
                self.income = data["income"]
                self.expenses = data["expenses"]
                self.categories = data["categories"]
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetTracker(root)
    root.mainloop()


