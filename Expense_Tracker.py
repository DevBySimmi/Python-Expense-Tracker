import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime


class ExpenseTracker:

    def __init__(self, root):
        self.root = root
        self.root.title("📊 Simple Expense Tracker")
        self.root.geometry("850x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#10151c")

        self.data_file = "expenses.json"
        self.transactions = []

        self.load_data()
        self.create_ui()
        self.refresh_table()
        self.update_summary()

    # =====================================================
    # DATA
    # =====================================================

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as file:
                    self.transactions = json.load(file)
            except (json.JSONDecodeError, OSError):
                self.transactions = []

    def save_data(self):
        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump(
                self.transactions,
                file,
                indent=4,
                ensure_ascii=False
            )

    # =====================================================
    # UI
    # =====================================================

    def create_ui(self):

        # Header
        header = tk.Frame(
            self.root,
            bg="#10151c"
        )
        header.pack(
            fill="x",
            padx=25,
            pady=(20, 10)
        )

        tk.Label(
            header,
            text="📊 Expense Tracker",
            font=("Consolas", 24, "bold"),
            fg="#63e6be",
            bg="#10151c"
        ).pack(side="left")

        tk.Label(
            header,
            text="Track your money easily",
            font=("Consolas", 9),
            fg="#7d8794",
            bg="#10151c"
        ).pack(
            side="right",
            pady=10
        )

        # =================================================
        # SUMMARY
        # =================================================

        summary = tk.Frame(
            self.root,
            bg="#10151c"
        )
        summary.pack(
            fill="x",
            padx=25,
            pady=10
        )

        self.balance_label = self.create_summary_card(
            summary,
            "💰 Balance",
            "#63e6be"
        )
        self.income_label = self.create_summary_card(
            summary,
            "📈 Income",
            "#7dd3fc"
        )
        self.expense_label = self.create_summary_card(
            summary,
            "💸 Expenses",
            "#fb7185"
        )

        # =================================================
        # ADD TRANSACTION
        # =================================================

        form = tk.Frame(
            self.root,
            bg="#181f28"
        )
        form.pack(
            fill="x",
            padx=25,
            pady=10
        )

        tk.Label(
            form,
            text="ADD TRANSACTION",
            font=("Consolas", 10, "bold"),
            fg="#63e6be",
            bg="#181f28"
        ).grid(
            row=0,
            column=0,
            columnspan=5,
            sticky="w",
            padx=15,
            pady=(12, 8)
        )

        # Type
        tk.Label(
            form,
            text="Type",
            font=("Consolas", 9),
            fg="#aeb7c3",
            bg="#181f28"
        ).grid(row=1, column=0, padx=8)

        self.type_var = tk.StringVar(
            value="Expense"
        )

        self.type_box = ttk.Combobox(
            form,
            textvariable=self.type_var,
            values=["Expense", "Income"],
            state="readonly",
            width=10
        )
        self.type_box.grid(
            row=2,
            column=0,
            padx=8,
            pady=(0, 15)
        )

        # Amount
        tk.Label(
            form,
            text="Amount",
            font=("Consolas", 9),
            fg="#aeb7c3",
            bg="#181f28"
        ).grid(row=1, column=1, padx=8)

        self.amount_entry = tk.Entry(
            form,
            font=("Consolas", 10),
            bg="#252e39",
            fg="white",
            insertbackground="white",
            relief="flat",
            width=15
        )
        self.amount_entry.grid(
            row=2,
            column=1,
            padx=8,
            pady=(0, 15),
            ipady=6
        )

        # Category
        tk.Label(
            form,
            text="Category",
            font=("Consolas", 9),
            fg="#aeb7c3",
            bg="#181f28"
        ).grid(row=1, column=2, padx=8)

        self.category_entry = tk.Entry(
            form,
            font=("Consolas", 10),
            bg="#252e39",
            fg="white",
            insertbackground="white",
            relief="flat",
            width=15
        )
        self.category_entry.grid(
            row=2,
            column=2,
            padx=8,
            pady=(0, 15),
            ipady=6
        )

        # Description
        tk.Label(
            form,
            text="Description",
            font=("Consolas", 9),
            fg="#aeb7c3",
            bg="#181f28"
        ).grid(row=1, column=3, padx=8)

        self.description_entry = tk.Entry(
            form,
            font=("Consolas", 10),
            bg="#252e39",
            fg="white",
            insertbackground="white",
            relief="flat",
            width=20
        )
        self.description_entry.grid(
            row=2,
            column=3,
            padx=8,
            pady=(0, 15),
            ipady=6
        )

        # Add button
        tk.Button(
            form,
            text="＋ ADD",
            command=self.add_transaction,
            font=("Consolas", 10, "bold"),
            bg="#63e6be",
            fg="#10151c",
            activebackground="#80f0ce",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=7
        ).grid(
            row=2,
            column=4,
            padx=10,
            pady=(0, 15)
        )

        # =================================================
        # TABLE
        # =================================================

        table_frame = tk.Frame(
            self.root,
            bg="#181f28"
        )
        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(5, 10)
        )

        columns = (
            "date",
            "type",
            "amount",
            "category",
            "description"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=9
        )

        self.table.heading(
            "date",
            text="Date"
        )
        self.table.heading(
            "type",
            text="Type"
        )
        self.table.heading(
            "amount",
            text="Amount"
        )
        self.table.heading(
            "category",
            text="Category"
        )
        self.table.heading(
            "description",
            text="Description"
        )

        self.table.column(
            "date",
            width=125
        )
        self.table.column(
            "type",
            width=90
        )
        self.table.column(
            "amount",
            width=100
        )
        self.table.column(
            "category",
            width=130
        )
        self.table.column(
            "description",
            width=260
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # =================================================
        # BOTTOM BUTTONS
        # =================================================

        bottom = tk.Frame(
            self.root,
            bg="#10151c"
        )
        bottom.pack(
            fill="x",
            padx=25,
            pady=(0, 15)
        )

        tk.Button(
            bottom,
            text="🗑 Delete Selected",
            command=self.delete_transaction,
            font=("Consolas", 9, "bold"),
            bg="#a85f68",
            fg="white",
            activebackground="#bd7079",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=7
        ).pack(side="left")

        tk.Button(
            bottom,
            text="🧹 Clear All",
            command=self.clear_all,
            font=("Consolas", 9, "bold"),
            bg="#303946",
            fg="white",
            activebackground="#414d5c",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=7
        ).pack(
            side="left",
            padx=8
        )

        self.status_label = tk.Label(
            bottom,
            text="Ready",
            font=("Consolas", 9),
            fg="#687585",
            bg="#10151c"
        )
        self.status_label.pack(
            side="right"
        )

    # =====================================================
    # SUMMARY CARD
    # =====================================================

    def create_summary_card(
        self,
        parent,
        title,
        text_color
    ):

        card = tk.Frame(
            parent,
            bg="#181f28",
            width=245,
            height=80
        )

        card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )

        card.pack_propagate(False)

        tk.Label(
            card,
            text=title,
            font=("Consolas", 9, "bold"),
            fg="#788493",
            bg="#181f28"
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 0)
        )

        value_label = tk.Label(
            card,
            text="₹0.00",
            font=("Consolas", 17, "bold"),
            fg=text_color,
            bg="#181f28"
        )

        value_label.pack(
            anchor="w",
            padx=15,
            pady=3
        )

        return value_label

    # =====================================================
    # ADD TRANSACTION
    # =====================================================

    def add_transaction(self):

        transaction_type = self.type_var.get()
        amount_text = self.amount_entry.get().strip()
        category = self.category_entry.get().strip()
        description = self.description_entry.get().strip()

        # Validate amount
        try:
            amount = float(amount_text)

            if amount <= 0:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Invalid Amount",
                "Please enter a valid positive amount."
            )
            return

        if not category:
            category = "General"

        if not description:
            description = "No description"

        transaction = {
            "date": datetime.now().strftime(
                "%d-%m-%Y"
            ),
            "type": transaction_type,
            "amount": amount,
            "category": category,
            "description": description
        }

        self.transactions.append(
            transaction
        )

        self.save_data()
        self.refresh_table()
        self.update_summary()
        self.clear_form()

        self.status_label.config(
            text="Transaction added ✓"
        )

    # =====================================================
    # REFRESH TABLE
    # =====================================================

    def refresh_table(self):

        for item in self.table.get_children():
            self.table.delete(item)

        for transaction in self.transactions:

            amount = f"₹{transaction['amount']:.2f}"

            self.table.insert(
                "",
                "end",
                values=(
                    transaction["date"],
                    transaction["type"],
                    amount,
                    transaction["category"],
                    transaction["description"]
                )
            )

    # =====================================================
    # UPDATE SUMMARY
    # =====================================================

    def update_summary(self):

        income = 0
        expenses = 0

        for transaction in self.transactions:

            if transaction["type"] == "Income":
                income += transaction["amount"]

            else:
                expenses += transaction["amount"]

        balance = income - expenses

        self.income_label.config(
            text=f"₹{income:.2f}"
        )

        self.expense_label.config(
            text=f"₹{expenses:.2f}"
        )

        self.balance_label.config(
            text=f"₹{balance:.2f}"
        )

    # =====================================================
    # DELETE TRANSACTION
    # =====================================================

    def delete_transaction(self):

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a transaction first."
            )
            return

        item = selected[0]
        index = self.table.index(item)

        confirm = messagebox.askyesno(
            "Delete Transaction",
            "Are you sure you want to delete this transaction?"
        )

        if not confirm:
            return

        del self.transactions[index]

        self.save_data()
        self.refresh_table()
        self.update_summary()

        self.status_label.config(
            text="Transaction deleted"
        )

    # =====================================================
    # CLEAR ALL
    # =====================================================

    def clear_all(self):

        if not self.transactions:
            return

        confirm = messagebox.askyesno(
            "Clear All",
            "Delete all transactions?"
        )

        if not confirm:
            return

        self.transactions = []

        self.save_data()
        self.refresh_table()
        self.update_summary()

        self.status_label.config(
            text="All transactions cleared"
        )

    # =====================================================
    # CLEAR FORM
    # =====================================================

    def clear_form(self):

        self.amount_entry.delete(
            0,
            tk.END
        )

        self.category_entry.delete(
            0,
            tk.END
        )

        self.description_entry.delete(
            0,
            tk.END
        )

        self.type_var.set(
            "Expense"
        )


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = ExpenseTracker(root)

    root.mainloop()