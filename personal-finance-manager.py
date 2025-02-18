import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import datetime
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side
from ttkthemes import ThemedTk  # Import themed tk


# --- Data Handling Module ---
class Transaction:
    """Represents a financial transaction with categories and notes, and transaction mode (Online/Cash)."""
    def __init__(self, date, transaction_type, category, reason, amount, notes="", mode="Online"):
        self.date = date
        self.transaction_type = transaction_type
        self.category = category
        self.reason = reason
        self.amount = amount
        self.notes = notes
        self.mode = mode

    def __str__(self):
        return f"{self.date},{self.transaction_type},{self.category},{self.reason},{self.amount},{self.notes},{self.mode}"

def save_transactions_to_csv(transactions, filename="transactions.csv"):
    """Saves transactions to CSV."""
    try:
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Date', 'Type', 'Category', 'Reason', 'Amount', 'Notes', 'Mode'])
            for transaction in transactions:
                csv_writer.writerow([transaction.date, transaction.transaction_type, transaction.category, transaction.reason, transaction.amount, transaction.notes, transaction.mode])
    except Exception as e:
        messagebox.showerror("Error", f"Error saving transactions: {e}")

def load_transactions_from_csv(filename="transactions.csv"):
    """Loads transactions from CSV."""
    transactions = []
    try:
        with open(filename, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            header = next(csv_reader, None)
            expected_header = ['Date', 'Type', 'Category', 'Reason', 'Amount', 'Notes', 'Mode']
            if header != expected_header and header is not None:
                messagebox.showwarning("Warning", f"CSV header mismatch. Expected: {expected_header}, Found: {header}")
            for row in csv_reader:
                if row:
                    try:
                        date, transaction_type, category, reason, amount, *parts = row
                        notes_parts = []
                        mode = "Online"
                        if len(parts) > 1:
                            mode = parts[-1]
                            notes_parts = parts[:-1]
                        elif len(parts) == 1:
                            if parts[0] in ['Online', 'Cash']:
                                mode = parts[0]
                                notes_parts = []
                            else:
                                notes_parts = parts
                        else:
                            notes_parts = []
                        notes = "".join(notes_parts).strip()
                        transactions.append(Transaction(date, transaction_type, category, reason, float(amount), notes, mode))
                    except ValueError as e:
                        messagebox.showerror("Error", f"CSV data error at row: {row}. Error: {e}")
                    except Exception as e:
                        messagebox.showerror("Error", f"CSV read error at row: {row}. Error: {e}")
    except FileNotFoundError:
        pass
    except Exception as e:
        messagebox.showerror("Error", f"Error loading transactions: {e}")
    return transactions

def export_transactions_to_xlsx(transactions, filename):
    """Exports transactions to XLSX."""
    try:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Transaction History"
        headers = ['Date', 'Type', 'Category', 'Reason', 'Amount', 'Notes', 'Mode']
        sheet.append(headers)
        header_font = Font(bold=True)
        header_alignment = Alignment(horizontal='center')
        header_border = Border(bottom=Side(style='thin'))
        for cell in sheet["1:1"]:
            cell.font = header_font
            cell.alignment = header_alignment
            cell.border = header_border
        for transaction in transactions:
            sheet.append([transaction.date, transaction.transaction_type, transaction.category, transaction.reason, transaction.amount, transaction.notes, transaction.mode])
        for column_cells in sheet.columns:
            length = max(len(str(cell.value)) for cell in column_cells)
            sheet.column_dimensions[column_cells[0].column_letter].width = length + 2
        workbook.save(filename)
        messagebox.showinfo("Success", "Transactions exported to XLSX!")
    except Exception as e:
        messagebox.showerror("Error", f"Error exporting to XLSX: {e}")

# --- GUI Application Module ---
class FinanceApp(ThemedTk):  # Inherit from ThemedTk
    def __init__(self):
        super().__init__(theme="clam") # Set the theme here
        self.title("Personal Finance Manager - Advanced")
        self.transactions = load_transactions_from_csv()
        self.current_balance = self.calculate_balance()
        self.categories = self.load_categories()
        self.filtered_transactions = list(self.transactions)

        self.init_styles() # Initialize styles
        self.init_ui()
        self.update_transaction_tree(self.filtered_transactions)

    def init_styles(self):
        """Defines and configures ttk styles for consistent look."""
        style = ttk.Style(self)
        # Configure default font for all ttk widgets
        style.configure('TLabel', font=('Segoe UI', 10))
        style.configure('TButton', font=('Segoe UI', 10))
        style.configure('TRadiobutton', font=('Segoe UI', 10))
        style.configure('TCombobox', font=('Segoe UI', 10))
        style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'))

        # Style for LabelFrames
        style.configure('TLabelframe.Label', font=('Segoe UI', 10, 'bold'))

        # Bold style for summary labels
        style.configure('Bold.TLabel', font=('Segoe UI', 10, 'bold'))


    def load_categories(self, filename="categories.txt"):
        """Loads categories from file or defaults."""
        try:
            with open(filename, 'r') as f:
                categories = [line.strip() for line in f.readlines()]
                return sorted(list(set(categories)))
        except FileNotFoundError:
            default_categories = ["Food", "Utilities", "Salary", "Entertainment", "Transportation", "Other"]
            self.save_categories(default_categories)
            return default_categories
        except Exception as e:
            messagebox.showerror("Error", f"Error loading categories: {e}. Using default.")
            return ["Food", "Utilities", "Salary", "Entertainment", "Transportation", "Other"]

    def save_categories(self, categories, filename="categories.txt"):
        """Saves categories to file."""
        try:
            with open(filename, 'w') as f:
                for category in categories:
                    f.write(category + "\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving categories: {e}")

    def init_ui(self):
        # --- Input Frame ---
        input_frame = ttk.LabelFrame(self, text="Add New Transaction")
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)

        input_field_width = 20  # Consistent width for input fields

        # Date
        ttk.Label(input_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.date_entry = ttk.Entry(input_frame, width=input_field_width)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))

        # Type
        ttk.Label(input_frame, text="Type:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.type_var = tk.StringVar(value="Credit")
        type_frame = ttk.Frame(input_frame) # Frame to group radio buttons
        type_frame.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        type_options = ["Credit", "Debit"]
        for i, option in enumerate(type_options):
            ttk.Radiobutton(type_frame, text=option, variable=self.type_var, value=option).pack(side=tk.LEFT, padx=5)

        # Mode (Online/Cash)
        ttk.Label(input_frame, text="Mode:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.mode_var = tk.StringVar(value="Online")
        mode_frame = ttk.Frame(input_frame) # Frame to group mode radio buttons
        mode_frame.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        mode_options = ["Online", "Cash"]
        for i, option in enumerate(mode_options):
            ttk.Radiobutton(mode_frame, text=option, variable=self.mode_var, value=option).pack(side=tk.LEFT, padx=5)


        # Category
        ttk.Label(input_frame, text="Category:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(input_frame, textvariable=self.category_var, values=self.categories, width=input_field_width-3)
        self.category_combo.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.category_combo.set(self.categories[0] if self.categories else "")

        # Reason
        ttk.Label(input_frame, text="Reason:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.reason_entry = ttk.Entry(input_frame, width=input_field_width)
        self.reason_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        # Amount
        ttk.Label(input_frame, text="Amount:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.amount_entry = ttk.Entry(input_frame, width=input_field_width)
        self.amount_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

        # Notes
        ttk.Label(input_frame, text="Notes:").grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        self.notes_entry = tk.Text(input_frame, height=2, width=input_field_width)
        self.notes_entry.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)

        # Add Transaction Button
        add_button = ttk.Button(input_frame, text="Add Transaction", command=self.add_transaction)
        add_button.grid(row=7, column=0, columnspan=2, pady=10)

        # --- Balance & Summary Frame ---
        summary_frame = ttk.LabelFrame(self, text="Account Summary")
        summary_frame.grid(row=0, column=1, padx=10, pady=10, sticky=tk.N)

        # Balance Labels - using grid for layout
        ttk.Label(summary_frame, text="Total Balance:", style='Bold.TLabel').grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        self.balance_label = ttk.Label(summary_frame, text=f"₹{self.current_balance:.2f}")
        self.balance_label.grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)

        ttk.Label(summary_frame, text="Online Balance:", style='Bold.TLabel').grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
        self.online_balance_label = ttk.Label(summary_frame, text="₹0.00")
        self.online_balance_label.grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)

        ttk.Label(summary_frame, text="Cash Balance:", style='Bold.TLabel').grid(row=2, column=0, padx=5, pady=2, sticky=tk.W)
        self.cash_balance_label = ttk.Label(summary_frame, text="₹0.00")
        self.cash_balance_label.grid(row=2, column=1, padx=5, pady=2, sticky=tk.W)

        ttk.Label(summary_frame, text="Total Credits:", style='Bold.TLabel').grid(row=0, column=2, padx=5, pady=2, sticky=tk.W)
        self.total_credits_label = ttk.Label(summary_frame, text="₹0.00")
        self.total_credits_label.grid(row=0, column=3, padx=5, pady=2, sticky=tk.W)

        ttk.Label(summary_frame, text="Total Debits:", style='Bold.TLabel').grid(row=1, column=2, padx=5, pady=2, sticky=tk.W)
        self.total_debits_label = ttk.Label(summary_frame, text="₹0.00")
        self.total_debits_label.grid(row=1, column=3, padx=5, pady=2, sticky=tk.W)

        ttk.Label(summary_frame, text="Online Credits:", style='Bold.TLabel').grid(row=2, column=2, padx=5, pady=2, sticky=tk.W)
        self.online_credits_label = ttk.Label(summary_frame, text="₹0.00")
        self.online_credits_label.grid(row=2, column=3, padx=5, pady=2, sticky=tk.W)

        ttk.Label(summary_frame, text="Online Debits:", style='Bold.TLabel').grid(row=3, column=2, padx=5, pady=2, sticky=tk.W)
        self.online_debits_label = ttk.Label(summary_frame, text="₹0.00")
        self.online_debits_label.grid(row=3, column=3, padx=5, pady=2, sticky=tk.W)

        ttk.Label(summary_frame, text="Cash Credits:", style='Bold.TLabel').grid(row=4, column=2, padx=5, pady=2, sticky=tk.W)
        self.cash_credits_label = ttk.Label(summary_frame, text="₹0.00")
        self.cash_credits_label.grid(row=4, column=3, padx=5, pady=2, sticky=tk.W)

        ttk.Label(summary_frame, text="Cash Debits:", style='Bold.TLabel').grid(row=5, column=2, padx=5, pady=2, sticky=tk.W)
        self.cash_debits_label = ttk.Label(summary_frame, text="₹0.00")
        self.cash_debits_label.grid(row=5, column=3, padx=5, pady=2, sticky=tk.W)


        self.update_summary_labels()


        # --- Filter Frame ---
        filter_frame = ttk.LabelFrame(self, text="Filter Transactions")
        filter_frame.grid(row=1, column=0, padx=10, pady=5, sticky=tk.NSEW)

        # Date Range Filter
        ttk.Label(filter_frame, text="Start Date:").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        self.filter_start_date_entry = ttk.Entry(filter_frame, width=12)
        self.filter_start_date_entry.grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)
        self.filter_start_date_entry.insert(0, (datetime.date.today() - datetime.timedelta(days=30)).strftime("%Y-%m-%d"))

        ttk.Label(filter_frame, text="End Date:").grid(row=0, column=2, padx=5, pady=2, sticky=tk.W)
        self.filter_end_date_entry = ttk.Entry(filter_frame, width=12)
        self.filter_end_date_entry.grid(row=0, column=3, padx=5, pady=2, sticky=tk.W)
        self.filter_end_date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))

        # Type Filter
        ttk.Label(filter_frame, text="Type:").grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
        self.filter_type_var = tk.StringVar(value="All")
        filter_type_options = ["All", "Credit", "Debit"]
        filter_type_combo = ttk.Combobox(filter_frame, textvariable=self.filter_type_var, values=filter_type_options, width=8)
        filter_type_combo.grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)

        # Mode Filter
        ttk.Label(filter_frame, text="Mode:").grid(row=1, column=2, padx=5, pady=2, sticky=tk.W)
        self.filter_mode_var = tk.StringVar(value="All")
        filter_mode_options = ["All", "Online", "Cash"]
        filter_mode_combo = ttk.Combobox(filter_frame, textvariable=self.filter_mode_var, values=filter_mode_options, width=8)
        filter_mode_combo.grid(row=1, column=3, padx=5, pady=2, sticky=tk.W)

        # Category Filter
        ttk.Label(filter_frame, text="Category:").grid(row=2, column=0, padx=5, pady=2, sticky=tk.W)
        self.filter_category_var = tk.StringVar(value="All")
        filter_category_options = ["All"] + self.categories
        filter_category_combo = ttk.Combobox(filter_frame, textvariable=self.filter_category_var, values=filter_category_options, width=12)
        filter_category_combo.grid(row=2, column=1, padx=5, pady=2, sticky=tk.W)

        # Search Filter
        ttk.Label(filter_frame, text="Search:").grid(row=3, column=0, padx=5, pady=2, sticky=tk.W)
        self.search_entry = ttk.Entry(filter_frame, width=25)
        self.search_entry.grid(row=3, column=1, columnspan=3, padx=5, pady=2, sticky=tk.W+tk.E)

        filter_button = ttk.Button(filter_frame, text="Apply Filters", command=self.apply_filters)
        filter_button.grid(row=4, column=0, columnspan=2, pady=5)

        clear_filter_button = ttk.Button(filter_frame, text="Clear Filters", command=self.clear_filters)
        clear_filter_button.grid(row=4, column=2, columnspan=2, pady=5)


        # --- Transaction History Frame ---
        history_frame = ttk.LabelFrame(self, text="Transaction History")
        history_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky=tk.NSEW)
        self.grid_rowconfigure(2, weight=1) # Allow history frame to expand vertically
        self.grid_columnconfigure(0, weight=1) # Allow history frame to expand horizontally
        self.grid_columnconfigure(1, weight=1) # Allow history frame to expand horizontally

        self.tree = ttk.Treeview(history_frame, columns=('Date', 'Type', 'Category', 'Reason', 'Amount', 'Notes', 'Mode'), show='headings')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Type', text='Type')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Reason', text='Reason')
        self.tree.heading('Amount', text='Amount')
        self.tree.heading('Notes', text='Notes')
        self.tree.heading('Mode', text='Mode')
        self.tree.column('Date', anchor=tk.W, width=100) # Adjust column widths as needed
        self.tree.column('Type', anchor=tk.W, width=80)
        self.tree.column('Category', anchor=tk.W, width=120)
        self.tree.column('Reason', anchor=tk.W, width=150)
        self.tree.column('Amount', anchor=tk.W, width=80)
        self.tree.column('Notes', anchor=tk.W, width=200)
        self.tree.column('Mode', anchor=tk.W, width=80)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # --- Action Buttons Frame ---
        action_buttons_frame = ttk.Frame(self)
        action_buttons_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky=tk.EW)

        edit_button = ttk.Button(action_buttons_frame, text="Edit Transaction", command=self.edit_transaction)
        edit_button.pack(side=tk.LEFT, padx=5, pady=5)
        delete_button = ttk.Button(action_buttons_frame, text="Delete Transaction", command=self.delete_transaction)
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)
        export_button = ttk.Button(action_buttons_frame, text="Export to XLSX", command=self.export_data)
        export_button.pack(side=tk.LEFT, padx=5, pady=5)
        clear_all_button = ttk.Button(action_buttons_frame, text="Clear All Transactions", command=self.clear_all_transactions)
        clear_all_button.pack(side=tk.LEFT, padx=5, pady=5)
        manage_categories_button = ttk.Button(action_buttons_frame, text="Manage Categories", command=self.manage_categories_dialog)
        manage_categories_button.pack(side=tk.LEFT, padx=5, pady=5)


        # --- Status Bar ---
        self.status_bar = tk.StringVar()
        status_label = ttk.Label(self, textvariable=self.status_bar, relief=tk.SUNKEN, anchor=tk.W)
        status_label.grid(row=4, column=0, columnspan=2, sticky=tk.EW, padx=10, pady=5)
        current_year = datetime.datetime.now().year
        self.status_bar.set(f"Ready | Made by Sufyaan | Copyright {current_year}")

        # Make the main window resizable
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)


    def validate_input(self, date_str, amount_str, reason_str, category_str):
        """Validates input fields."""
        if not date_str or not amount_str or not reason_str or not category_str:
            messagebox.showerror("Input Error", "Date, Category, Reason, and Amount are required.")
            return False
        if category_str not in self.categories:
            messagebox.showerror("Input Error", "Invalid Category selected.")
            return False
        try:
            datetime.datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Input Error", "Invalid date format. Use YYYY-MM-DD.")
            return False
        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Input Error", "Amount must be positive.")
                return False
        except ValueError:
            messagebox.showerror("Input Error", "Invalid amount. Enter a numeric value.")
            return True # corrected from return False to True, as it should return True if validation passes
        return True


    def add_transaction(self):
        """Adds a new transaction."""
        date_str = self.date_entry.get()
        transaction_type = self.type_var.get()
        category = self.category_var.get()
        reason = self.reason_entry.get()
        amount_str = self.amount_entry.get()
        notes = self.notes_entry.get("1.0", tk.END).strip()
        mode = self.mode_var.get()

        if self.validate_input(date_str, amount_str, reason, category):
            date = date_str
            amount = float(amount_str)
            new_transaction = Transaction(date, transaction_type, category, reason, amount, notes, mode)
            self.transactions.append(new_transaction)
            self.save_and_update()
            self.clear_input_fields()
            self.status_bar.set("Transaction added successfully.")


    def edit_transaction(self):
        """Edits a selected transaction."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Select a transaction to edit.")
            return

        selected_index = self.tree.index(selected_item)
        old_transaction = self.filtered_transactions[selected_index]

        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Transaction")

        # Date
        ttk.Label(edit_window, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        date_entry_edit = ttk.Entry(edit_window)
        date_entry_edit.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        date_entry_edit.insert(0, old_transaction.date)

        # Type
        ttk.Label(edit_window, text="Type:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        type_var_edit = tk.StringVar(value=old_transaction.transaction_type)
        type_options = ["Credit", "Debit"]
        for i, option in enumerate(type_options):
            ttk.Radiobutton(edit_window, text=option, variable=type_var_edit, value=option).grid(row=1, column=i+1, padx=5, pady=5, sticky=tk.W)

        # Mode
        ttk.Label(edit_window, text="Mode:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        mode_var_edit = tk.StringVar(value=old_transaction.mode)
        mode_options = ["Online", "Cash"]
        for i, option in enumerate(mode_options):
            ttk.Radiobutton(edit_window, text=option, variable=mode_var_edit, value=option).grid(row=2, column=i+1, padx=5, pady=5, sticky=tk.W)

        # Category
        ttk.Label(edit_window, text="Category:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        category_var_edit = tk.StringVar(value=old_transaction.category)
        category_combo_edit = ttk.Combobox(edit_window, textvariable=category_var_edit, values=self.categories)
        category_combo_edit.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)

        # Reason
        ttk.Label(edit_window, text="Reason:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        reason_entry_edit = ttk.Entry(edit_window)
        reason_entry_edit.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        reason_entry_edit.insert(0, old_transaction.reason)

        # Amount
        ttk.Label(edit_window, text="Amount:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        amount_entry_edit = ttk.Entry(edit_window)
        amount_entry_edit.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
        amount_entry_edit.insert(0, str(old_transaction.amount))

        # Notes
        ttk.Label(edit_window, text="Notes:").grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        notes_entry_edit = tk.Text(edit_window, height=2, width=20)
        notes_entry_edit.grid(row=6, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)
        notes_entry_edit.insert("1.0", old_transaction.notes)

        def save_edit():
            date_str = date_entry_edit.get()
            transaction_type = type_var_edit.get()
            category = category_var_edit.get()
            reason = reason_entry_edit.get()
            amount_str = amount_entry_edit.get()
            notes = notes_entry_edit.get("1.0", tk.END).strip()
            mode = mode_var_edit.get()

            if self.validate_input(date_str, amount_str, reason, category):
                date = date_str
                amount = float(amount_str)
                updated_transaction = Transaction(date, transaction_type, category, reason, amount, notes, mode)
                original_index = self.transactions.index(old_transaction)
                self.transactions[original_index] = updated_transaction
                self.save_and_update()
                self.apply_filters()
                edit_window.destroy()
                self.status_bar.set("Transaction edited.")

        ttk.Button(edit_window, text="Save Changes", command=save_edit).grid(row=7, column=0, columnspan=2, pady=10)


    def delete_transaction(self):
        """Deletes a selected transaction."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Select a transaction to delete.")
            return
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this transaction?"):
            selected_index = self.tree.index(selected_item)
            transaction_to_delete = self.filtered_transactions[selected_index]
            original_index_to_delete = self.transactions.index(transaction_to_delete)
            del self.transactions[original_index_to_delete]
            self.save_and_update()
            self.apply_filters()
            self.status_bar.set("Transaction deleted.")

    def clear_all_transactions(self):
        """Clears all transactions after confirmation."""
        if messagebox.askyesno("Confirm Clear All", "Are you sure you want to delete ALL transactions? This cannot be undone."):
            self.transactions = []
            self.save_and_update()
            self.apply_filters()
            self.status_bar.set("All transactions cleared.")

    def export_data(self):
        """Exports data to XLSX."""
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        if filename:
            export_transactions_to_xlsx(self.transactions, filename)
            self.status_bar.set(f"Transactions exported to {filename}")

    def calculate_balance(self, transactions=None, mode=None):
        """Calculates balance, optionally by mode."""
        if transactions is None:
            transactions = self.transactions
        if mode:
            transactions = [t for t in transactions if t.mode == mode]
        balance = 0
        for transaction in transactions:
            if transaction.transaction_type == "Credit":
                balance += transaction.amount
            else:
                balance -= transaction.amount
        return balance

    def calculate_summary(self, transactions=None):
        """Calculates transaction summary."""
        if transactions is None:
            transactions = self.transactions
        total_credits, total_debits = 0, 0
        online_credits, online_debits = 0, 0
        cash_credits, cash_debits = 0, 0

        for transaction in transactions:
            if transaction.transaction_type == "Credit":
                total_credits += transaction.amount
                if transaction.mode == "Online":
                    online_credits += transaction.amount
                else:
                    cash_credits += transaction.amount
            else:
                total_debits += transaction.amount
                if transaction.mode == "Online":
                    online_debits += transaction.amount
                else:
                    cash_debits += transaction.amount
        return total_credits, total_debits, online_credits, online_debits, cash_credits, cash_debits


    def update_summary_labels(self, transactions=None):
        """Updates summary labels in GUI."""
        if transactions is None:
            transactions = self.transactions
        total_credits, total_debits, online_credits, online_debits, cash_credits, cash_debits = self.calculate_summary(transactions)
        current_balance = self.calculate_balance(transactions=transactions)
        online_balance = self.calculate_balance(transactions=transactions, mode="Online")
        cash_balance = self.calculate_balance(transactions=transactions, mode="Cash")

        self.balance_label.config(text=f"₹{current_balance:.2f}")
        self.online_balance_label.config(text=f"₹{online_balance:.2f}")
        self.cash_balance_label.config(text=f"₹{cash_balance:.2f}")
        self.total_credits_label.config(text=f"₹{total_credits:.2f}")
        self.total_debits_label.config(text=f"₹{total_debits:.2f}")
        self.online_credits_label.config(text=f"₹{online_credits:.2f}")
        self.online_debits_label.config(text=f"₹{online_debits:.2f}")
        self.cash_credits_label.config(text=f"₹{cash_credits:.2f}")
        self.cash_debits_label.config(text=f"₹{cash_debits:.2f}")


    def save_and_update(self):
        """Saves, updates balance, summary, and transaction tree."""
        save_transactions_to_csv(self.transactions)
        self.current_balance = self.calculate_balance()
        self.update_summary_labels()
        self.apply_filters()

    def update_transaction_tree(self, transactions_to_display):
        """Updates transaction Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for transaction in transactions_to_display:
            self.tree.insert('', tk.END, values=(transaction.date, transaction.transaction_type, transaction.category, transaction.reason, f"₹{transaction.amount:.2f}", transaction.notes, transaction.mode))

    def clear_input_fields(self):
        """Clears input fields in 'Add Transaction' frame."""
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
        self.category_combo.set(self.categories[0] if self.categories else "")
        self.reason_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.notes_entry.delete("1.0", tk.END)
        self.mode_var.set("Online")

    def apply_filters(self):
        """Applies filters and updates transaction tree."""
        start_date_str = self.filter_start_date_entry.get()
        end_date_str = self.filter_end_date_entry.get()
        filter_type = self.filter_type_var.get()
        filter_category = self.filter_category_var.get()
        search_term = self.search_entry.get().lower()
        filter_mode = self.filter_mode_var.get()

        filtered = self.transactions[:]

        try:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
            filtered = [t for t in filtered if start_date <= datetime.datetime.strptime(t.date, '%Y-%m-%d').date() <= end_date]
        except ValueError:
            messagebox.showwarning("Filter Warning", "Invalid date format. Dates ignored.")

        if filter_type != "All":
            filtered = [t for t in filtered if t.transaction_type == filter_type]
        if filter_mode != "All":
            filtered = [t for t in filtered if t.mode == filter_mode]
        if filter_category != "All":
            filtered = [t for t in filtered if t.category == filter_category]
        if search_term:
            filtered = [t for t in filtered if search_term in t.reason.lower() or search_term in t.category.lower() or search_term in t.notes.lower()]

        self.filtered_transactions = filtered
        self.update_transaction_tree(self.filtered_transactions)
        self.update_summary_labels(self.filtered_transactions)
        self.status_bar.set(f"Showing {len(self.filtered_transactions)} transactions.")

    def clear_filters(self):
        """Clears all filters."""
        self.filter_start_date_entry.delete(0, tk.END)
        self.filter_start_date_entry.insert(0, (datetime.date.today() - datetime.timedelta(days=30)).strftime("%Y-%m-%d"))
        self.filter_end_date_entry.delete(0, tk.END)
        self.filter_end_date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
        self.filter_type_var.set("All")
        self.filter_mode_var.set("All")
        self.filter_category_var.set("All")
        self.search_entry.delete(0, tk.END)
        self.apply_filters()
        self.status_bar.set("Filters cleared. Showing all transactions.")


    def manage_categories_dialog(self):
        """Opens dialog to manage categories."""
        category_window = tk.Toplevel(self)
        category_window.title("Manage Categories")

        category_list_frame = ttk.Frame(category_window)
        category_list_frame.pack(padx=10, pady=10)

        self.category_listbox = tk.Listbox(category_list_frame, height=10, width=30, selectmode=tk.SINGLE)
        self.category_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(category_list_frame, orient=tk.VERTICAL, command=self.category_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.category_listbox.config(yscrollcommand=scrollbar.set)

        for category in self.categories:
            self.category_listbox.insert(tk.END, category)

        input_frame = ttk.Frame(category_window)
        input_frame.pack(padx=10, pady=5, fill=tk.X)

        self.new_category_entry = ttk.Entry(input_frame)
        self.new_category_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        add_category_button = ttk.Button(input_frame, text="Add Category", command=self.add_category)
        add_category_button.pack(side=tk.LEFT, padx=5)
        delete_category_button = ttk.Button(input_frame, text="Delete Category", command=self.delete_category)
        delete_category_button.pack(side=tk.LEFT, padx=5)

    def add_category(self):
        """Adds a new category."""
        new_category = self.new_category_entry.get().strip()
        if new_category and new_category not in self.categories:
            self.categories.append(new_category)
            self.categories.sort()
            self.save_categories(self.categories)
            self.category_combo['values'] = self.categories
            self.filter_category_combo['values'] = ["All"] + self.categories
            self.category_listbox.insert(tk.END, new_category)
            self.new_category_entry.delete(0, tk.END)
        elif not new_category:
            messagebox.showwarning("Category Input", "Category name cannot be empty.")
        else:
            messagebox.showwarning("Category Input", "Category already exists.")

    def delete_category(self):
        """Deletes a category."""
        selected_index = self.category_listbox.curselection()
        if selected_index:
            category_to_delete = self.category_listbox.get(selected_index[0])
            if messagebox.askyesno("Confirm Delete", f"Delete category '{category_to_delete}'?"):
                if category_to_delete in self.categories:
                    self.categories.remove(category_to_delete)
                    self.save_categories(self.categories)
                    self.category_combo['values'] = self.categories
                    self.filter_category_combo['values'] = ["All"] + self.categories
                    self.category_listbox.delete(selected_index[0])
                    self.filter_category_var.set("All")
                    self.category_var.set(self.categories[0] if self.categories else "")
                    self.apply_filters()


# --- Main Application ---
if __name__ == "__main__":
    app = FinanceApp()
    app.mainloop()