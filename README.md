# Personal Finance Manager - Advanced

## Description

This is a personal finance management application designed to help you track your income and expenses effectively. It allows you to record transactions, categorize them, add notes, and filter them based on various criteria. The application provides a clear overview of your financial status, including balances, total credits, and debits, broken down by online and cash transactions.

## Features

*   **Transaction Management:**
    *   Add new transactions with date, type (credit/debit), category, reason, amount, notes, and transaction mode (Online/Cash).
    *   Edit and delete existing transactions.
    *   Clear all transactions (with confirmation).
*   **Categorization:**
    *   Categorize transactions for better expense tracking.
    *   Manage and customize transaction categories.
*   **Transaction Modes:**
    *   Option to specify transaction mode as Online or Cash.
    *   Filter transactions by Online or Cash mode.
*   **Filtering and Searching:**
    *   Filter transactions by date range, type (credit/debit), mode (Online/Cash), and category.
    *   Search transactions by reason, category, or notes.
    *   Clear all applied filters to view all transactions.
*   **Balance and Summary:**
    *   View current total balance, online balance, and cash balance.
    *   Summary of total credits, debits, online credits, online debits, cash credits, and cash debits.
*   **Data Export:**
    *   Export transaction data to an XLSX (Excel) file.
*   **User-Friendly Interface:**
    *   Graphical user interface built with Tkinter for ease of use.
    *   Modern and refined look with a professional theme.

## Installation (Linux - .deb Package)

These instructions are for installing the application on Debian-based Linux distributions (like Ubuntu, Debian, Linux Mint, Kali Linux, etc.) using the provided `.deb` package.

1.  **Download the `.deb` package:** Download the `personal-finance-manager.deb` file to your computer.

2.  **Open a terminal:** Navigate to the directory where you downloaded the `.deb` file. For example, if it's in your `Downloads` folder:

    ```bash
    cd Downloads
    ```

3.  **Install the application using `apt`:** Run the following command to install the `.deb` package. You will need to enter your administrator password.

    ```bash
    sudo apt install ./personal-finance-manager.deb
    ```

4.  **Wait for installation to complete:** `apt` will install the application and handle any dependencies.

5.  **Run the application:** Once installed, you can find "Personal Finance Manager" in your application menu (usually under "Office" or "Finance"). You can also run it from the terminal by typing:

    ```bash
    personal-finance-manager
    ```

## Usage

After installation, launch "Personal Finance Manager" from your application menu or using the terminal command.

*   **Adding Transactions:** Use the "Add New Transaction" section to enter transaction details: Date, Type (Credit/Debit), Mode (Online/Cash), Category, Reason, Amount, and Notes. Click "Add Transaction" to save.
*   **Viewing Transactions:** Transaction history is displayed in the "Transaction History" section.
*   **Filtering Transactions:** Use the "Filter Transactions" section to apply filters based on date range, type, mode, category, and search terms. Click "Apply Filters" to see filtered transactions or "Clear Filters" to remove filters.
*   **Managing Categories:** Click "Manage Categories" to add, delete, or modify transaction categories.
*   **Exporting Data:** Click "Export to XLSX" to save your transaction data to an Excel file.

## Built With

*   **Python:** Programming language
*   **Tkinter:**  GUI toolkit
*   **ttkthemes:**  Themed Tkinter widgets for a modern look
*   **csv:**  For CSV file handling
*   **datetime:** For date and time operations
*   **openpyxl:** For exporting data to XLSX files

## License

## Author

Made by Sufyaan

## Copyright

Copyright © 2025 Sufyaan. All rights reserved.

---

**Note:** Replace `2025` in the Copyright section with the current year. You can also customize the description, features, and license sections as needed to better reflect your application.
