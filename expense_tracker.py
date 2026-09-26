import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime


# ============================================================
# DATABASE
# ============================================================

DATABASE = "expenses.db"


def connect_db():
    return sqlite3.connect(DATABASE)


def create_tables():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budget (
            id INTEGER PRIMARY KEY,
            amount REAL NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# ============================================================
# DATABASE OPERATIONS
# ============================================================

def add_expense_db(amount, category, description):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (amount, category, description, date)
        VALUES (?, ?, ?, ?)
    """, (
        amount,
        category,
        description,
        date.today().isoformat()
    ))

    connection.commit()
    connection.close()


def get_expenses(search=""):
    connection = connect_db()
    cursor = connection.cursor()

    if search:
        search_value = f"%{search}%"

        cursor.execute("""
            SELECT id, amount, category, description, date
            FROM expenses
            WHERE category LIKE ?
               OR description LIKE ?
               OR date LIKE ?
            ORDER BY id DESC
        """, (
            search_value,
            search_value,
            search_value
        ))

    else:

        cursor.execute("""
            SELECT id, amount, category, description, date
            FROM expenses
            ORDER BY id DESC
        """)

    data = cursor.fetchall()

    connection.close()

    return data


def delete_expense_db(expense_id):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    connection.commit()
    connection.close()


def get_total():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
    """)

    total = cursor.fetchone()[0]

    connection.close()

    return total


def get_category_data():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """)

    data = cursor.fetchall()

    connection.close()

    return data


def get_highest_expense():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT amount, category, description
        FROM expenses
        ORDER BY amount DESC
        LIMIT 1
    """)

    result = cursor.fetchone()

    connection.close()

    return result


def get_budget():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT amount
        FROM budget
        WHERE id = 1
    """)

    result = cursor.fetchone()

    connection.close()

    return result[0] if result else 0


def save_budget(amount):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO budget
        (id, amount)
        VALUES (1, ?)
    """, (amount,))

    connection.commit()
    connection.close()


# ============================================================
# MAIN WINDOW
# ============================================================

create_tables()

root = tk.Tk()

root.title("SmartSpend - Personal Expense Manager")
root.geometry("1250x760")
root.minsize(1050, 650)
root.configure(bg="#f4f7fb")


# ============================================================
# COLORS
# ============================================================

SIDEBAR = "#111827"
PRIMARY = "#4f46e5"
PRIMARY_DARK = "#3730a3"
BACKGROUND = "#f4f7fb"
WHITE = "#ffffff"
TEXT = "#111827"
SECONDARY_TEXT = "#6b7280"
LIGHT = "#eef2ff"
DANGER = "#dc2626"


# ============================================================
# STYLE
# ============================================================

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Treeview",
    background="white",
    foreground="#1f2937",
    rowheight=38,
    fieldbackground="white",
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    background="#eef2ff",
    foreground="#1e1b4b",
    font=("Segoe UI", 10, "bold"),
    padding=8
)

style.map(
    "Treeview",
    background=[
        ("selected", "#c7d2fe")
    ],
    foreground=[
        ("selected", "#111827")
    ]
)

style.configure(
    "TCombobox",
    padding=5
)


# ============================================================
# MAIN LAYOUT
# ============================================================

sidebar = tk.Frame(
    root,
    bg=SIDEBAR,
    width=220
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)


main_area = tk.Frame(
    root,
    bg=BACKGROUND
)

main_area.pack(
    side="left",
    fill="both",
    expand=True
)


# ============================================================
# SIDEBAR HEADER
# ============================================================

tk.Label(
    sidebar,
    text="SmartSpend",
    font=("Segoe UI", 22, "bold"),
    bg=SIDEBAR,
    fg=WHITE
).pack(
    anchor="w",
    padx=25,
    pady=(30, 2)
)


tk.Label(
    sidebar,
    text="PERSONAL FINANCE",
    font=("Segoe UI", 8, "bold"),
    bg=SIDEBAR,
    fg="#9ca3af"
).pack(
    anchor="w",
    padx=27,
    pady=(0, 30)
)


# ============================================================
# PAGE CONTAINER
# ============================================================

page_container = tk.Frame(
    main_area,
    bg=BACKGROUND
)

page_container.pack(
    fill="both",
    expand=True
)


# ============================================================
# PAGE SWITCHING
# ============================================================

pages = {}


def show_page(page_name):

    for page in pages.values():
        page.pack_forget()

    pages[page_name].pack(
        fill="both",
        expand=True
    )

    if page_name == "Dashboard":
        refresh_dashboard()

    elif page_name == "Expenses":
        refresh_expenses()

    elif page_name == "Analytics":
        refresh_analytics()

    elif page_name == "Budget":
        refresh_budget()


# ============================================================
# SIDEBAR BUTTON
# ============================================================

def create_sidebar_button(text, page_name):

    button = tk.Button(
        sidebar,
        text=text,
        command=lambda: show_page(page_name),
        font=("Segoe UI", 11),
        bg=SIDEBAR,
        fg="#d1d5db",
        activebackground="#1f2937",
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        anchor="w",
        padx=28,
        pady=13,
        cursor="hand2"
    )

    button.pack(
        fill="x",
        pady=2
    )


create_sidebar_button(
    "▣   Dashboard",
    "Dashboard"
)

create_sidebar_button(
    "₹   Expenses",
    "Expenses"
)

create_sidebar_button(
    "▤   Analytics",
    "Analytics"
)

create_sidebar_button(
    "◉   Budget",
    "Budget"
)

create_sidebar_button(
    "+   Add Expense",
    "Add Expense"
)


tk.Label(
    sidebar,
    text="",
    bg=SIDEBAR
).pack(
    expand=True
)


tk.Label(
    sidebar,
    text="SmartSpend v1.0",
    font=("Segoe UI", 9),
    bg=SIDEBAR,
    fg="#6b7280"
).pack(
    pady=(0, 5)
)


tk.Label(
    sidebar,
    text="Python + SQLite",
    font=("Segoe UI", 9),
    bg=SIDEBAR,
    fg="#6b7280"
).pack(
    pady=(0, 25)
)


# ============================================================
# COMMON PAGE HEADER
# ============================================================

def page_header(parent, title, subtitle):

    header = tk.Frame(
        parent,
        bg=BACKGROUND
    )

    header.pack(
        fill="x",
        padx=30,
        pady=(25, 15)
    )

    tk.Label(
        header,
        text=title,
        font=("Segoe UI", 24, "bold"),
        bg=BACKGROUND,
        fg=TEXT
    ).pack(
        anchor="w"
    )

    tk.Label(
        header,
        text=subtitle,
        font=("Segoe UI", 10),
        bg=BACKGROUND,
        fg=SECONDARY_TEXT
    ).pack(
        anchor="w",
        pady=(3, 0)
    )


# ============================================================
# DASHBOARD PAGE
# ============================================================

dashboard_page = tk.Frame(
    page_container,
    bg=BACKGROUND
)

pages["Dashboard"] = dashboard_page


page_header(
    dashboard_page,
    "Dashboard",
    datetime.now().strftime("%d %B %Y")
)


welcome = tk.Frame(
    dashboard_page,
    bg=PRIMARY,
    height=105
)

welcome.pack(
    fill="x",
    padx=30,
    pady=5
)


tk.Label(
    welcome,
    text="Good to see you! 👋",
    font=("Segoe UI", 20, "bold"),
    bg=PRIMARY,
    fg=WHITE
).pack(
    anchor="w",
    padx=25,
    pady=(20, 3)
)


tk.Label(
    welcome,
    text="Track your expenses and manage your monthly budget easily.",
    font=("Segoe UI", 10),
    bg=PRIMARY,
    fg="#e0e7ff"
).pack(
    anchor="w",
    padx=25
)


# ============================================================
# DASHBOARD CARDS
# ============================================================

cards = tk.Frame(
    dashboard_page,
    bg=BACKGROUND
)

cards.pack(
    fill="x",
    padx=30,
    pady=15
)


def create_card(parent, title):

    frame = tk.Frame(
        parent,
        bg=WHITE,
        height=105
    )

    frame.pack(
        side="left",
        fill="both",
        expand=True,
        padx=5
    )

    tk.Label(
        frame,
        text=title,
        font=("Segoe UI", 9, "bold"),
        bg=WHITE,
        fg=SECONDARY_TEXT
    ).pack(
        anchor="w",
        padx=18,
        pady=(15, 3)
    )

    value = tk.Label(
        frame,
        text="₹0.00",
        font=("Segoe UI", 20, "bold"),
        bg=WHITE,
        fg=TEXT
    )

    value.pack(
        anchor="w",
        padx=18
    )

    return value


dashboard_total = create_card(
    cards,
    "TOTAL SPENDING"
)

dashboard_budget = create_card(
    cards,
    "MONTHLY BUDGET"
)

dashboard_remaining = create_card(
    cards,
    "REMAINING"
)

dashboard_highest = create_card(
    cards,
    "HIGHEST EXPENSE"
)


# ============================================================
# DASHBOARD LOWER SECTION
# ============================================================

dashboard_lower = tk.Frame(
    dashboard_page,
    bg=BACKGROUND
)

dashboard_lower.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=(0, 20)
)


# Recent transactions

recent_frame = tk.LabelFrame(
    dashboard_lower,
    text="  Recent Transactions  ",
    font=("Segoe UI", 11, "bold"),
    bg=WHITE,
    fg=TEXT
)

recent_frame.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 8)
)


recent_table = ttk.Treeview(
    recent_frame,
    columns=("Category", "Description", "Amount"),
    show="headings",
    height=7
)

recent_table.heading(
    "Category",
    text="Category"
)

recent_table.heading(
    "Description",
    text="Description"
)

recent_table.heading(
    "Amount",
    text="Amount"
)

recent_table.column(
    "Category",
    width=110,
    anchor="center"
)

recent_table.column(
    "Description",
    width=180,
    anchor="w"
)

recent_table.column(
    "Amount",
    width=110,
    anchor="center"
)

recent_table.pack(
    fill="both",
    expand=True,
    padx=8,
    pady=8
)


# Insights

dashboard_insight_frame = tk.LabelFrame(
    dashboard_lower,
    text="  Smart Insights  ",
    font=("Segoe UI", 11, "bold"),
    bg=WHITE,
    fg=TEXT
)

dashboard_insight_frame.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(8, 0)
)


dashboard_insights = tk.Frame(
    dashboard_insight_frame,
    bg=WHITE
)

dashboard_insights.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)


# ============================================================
# DASHBOARD REFRESH
# ============================================================

def refresh_dashboard():

    total = get_total()
    budget = get_budget()
    highest = get_highest_expense()
    categories = get_category_data()

    dashboard_total.config(
        text=f"₹{total:,.2f}"
    )

    dashboard_budget.config(
        text=f"₹{budget:,.2f}"
    )

    remaining = budget - total

    if budget == 0:
        dashboard_remaining.config(
            text="Not set"
        )
    else:
        dashboard_remaining.config(
            text=f"₹{remaining:,.2f}"
        )

    if highest:
        dashboard_highest.config(
            text=f"₹{highest[0]:,.2f}"
        )
    else:
        dashboard_highest.config(
            text="₹0.00"
        )

    # Recent transactions
    for item in recent_table.get_children():
        recent_table.delete(item)

    expenses = get_expenses()

    for expense in expenses[:6]:

        recent_table.insert(
            "",
            "end",
            values=(
                expense[2],
                expense[3],
                f"₹{expense[1]:,.2f}"
            )
        )

    # Insights
    for widget in dashboard_insights.winfo_children():
        widget.destroy()

    if total == 0:

        create_dashboard_insight(
            "Add your first expense to start tracking your spending."
        )

    else:

        if categories:

            create_dashboard_insight(
                f"Highest spending category: "
                f"{categories[0][0]} "
                f"(₹{categories[0][1]:,.2f})"
            )

        if budget == 0:

            create_dashboard_insight(
                "Set a monthly budget to monitor your spending."
            )

        elif total > budget:

            create_dashboard_insight(
                f"Budget exceeded by ₹{total - budget:,.2f}."
            )

        elif total >= budget * 0.8:

            create_dashboard_insight(
                "You have used more than 80% of your budget."
            )

        else:

            create_dashboard_insight(
                "Your spending is currently within your budget."
            )


def create_dashboard_insight(text):

    frame = tk.Frame(
        dashboard_insights,
        bg="#f8fafc"
    )

    frame.pack(
        fill="x",
        pady=5
    )

    tk.Label(
        frame,
        text="•",
        font=("Segoe UI", 13, "bold"),
        bg="#f8fafc",
        fg=PRIMARY
    ).pack(
        side="left",
        padx=8
    )

    tk.Label(
        frame,
        text=text,
        font=("Segoe UI", 10),
        bg="#f8fafc",
        fg="#374151",
        wraplength=300,
        justify="left"
    ).pack(
        side="left",
        fill="x",
        expand=True,
        padx=3,
        pady=8
    )


# ============================================================
# EXPENSES PAGE
# ============================================================

expenses_page = tk.Frame(
    page_container,
    bg=BACKGROUND
)

pages["Expenses"] = expenses_page


page_header(
    expenses_page,
    "Expenses",
    "View, search and manage your transactions"
)


# Search section

search_frame = tk.Frame(
    expenses_page,
    bg=WHITE
)

search_frame.pack(
    fill="x",
    padx=30,
    pady=5
)


tk.Label(
    search_frame,
    text="Search",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=TEXT
).pack(
    side="left",
    padx=(15, 5),
    pady=15
)


search_entry = tk.Entry(
    search_frame,
    font=("Segoe UI", 10),
    width=35
)

search_entry.pack(
    side="left",
    pady=15
)


def search_expenses():

    refresh_expenses(
        search_entry.get().strip()
    )


def clear_search():

    search_entry.delete(
        0,
        tk.END
    )

    refresh_expenses()


tk.Button(
    search_frame,
    text="Search",
    command=search_expenses,
    bg=PRIMARY,
    fg=WHITE,
    relief="flat",
    padx=15,
    pady=5,
    cursor="hand2"
).pack(
    side="left",
    padx=7
)


tk.Button(
    search_frame,
    text="Clear",
    command=clear_search,
    bg="#e5e7eb",
    fg=TEXT,
    relief="flat",
    padx=15,
    pady=5,
    cursor="hand2"
).pack(
    side="left"
)


def delete_selected_expense():

    selected = expense_table.selection()

    if not selected:

        messagebox.showwarning(
            "No Selection",
            "Please select an expense first."
        )

        return

    item = expense_table.item(
        selected[0]
    )

    expense_id = item["values"][0]

    confirm = messagebox.askyesno(
        "Delete Expense",
        "Are you sure you want to delete this expense?"
    )

    if confirm:

        delete_expense_db(
            expense_id
        )

        refresh_expenses()
        refresh_dashboard()

        messagebox.showinfo(
            "Deleted",
            "Expense deleted successfully."
        )


tk.Button(
    search_frame,
    text="Delete Selected",
    command=delete_selected_expense,
    bg="#fee2e2",
    fg=DANGER,
    relief="flat",
    padx=15,
    pady=5,
    cursor="hand2"
).pack(
    side="right",
    padx=15
)


# Expense table

expense_table_frame = tk.Frame(
    expenses_page,
    bg=WHITE
)

expense_table_frame.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=10
)


expense_table = ttk.Treeview(
    expense_table_frame,
    columns=(
        "ID",
        "Amount",
        "Category",
        "Description",
        "Date"
    ),
    show="headings"
)


for column in (
    "ID",
    "Amount",
    "Category",
    "Description",
    "Date"
):

    expense_table.heading(
        column,
        text=column
    )


expense_table.column(
    "ID",
    width=70,
    anchor="center"
)

expense_table.column(
    "Amount",
    width=150,
    anchor="center"
)

expense_table.column(
    "Category",
    width=150,
    anchor="center"
)

expense_table.column(
    "Description",
    width=300,
    anchor="w"
)

expense_table.column(
    "Date",
    width=150,
    anchor="center"
)


expense_table.pack(
    side="left",
    fill="both",
    expand=True
)


expense_scroll = ttk.Scrollbar(
    expense_table_frame,
    orient="vertical",
    command=expense_table.yview
)

expense_scroll.pack(
    side="right",
    fill="y"
)

expense_table.configure(
    yscrollcommand=expense_scroll.set
)


def refresh_expenses(search=""):

    for item in expense_table.get_children():
        expense_table.delete(item)

    expenses = get_expenses(search)

    for expense in expenses:

        expense_table.insert(
            "",
            "end",
            values=(
                expense[0],
                f"₹{expense[1]:,.2f}",
                expense[2],
                expense[3],
                expense[4]
            )
        )


# ============================================================
# ANALYTICS PAGE
# ============================================================

analytics_page = tk.Frame(
    page_container,
    bg=BACKGROUND
)

pages["Analytics"] = analytics_page


page_header(
    analytics_page,
    "Analytics",
    "Understand where your money is going"
)


analytics_top = tk.Frame(
    analytics_page,
    bg=BACKGROUND
)

analytics_top.pack(
    fill="x",
    padx=30,
    pady=5
)


analytics_total_frame = tk.Frame(
    analytics_top,
    bg=WHITE,
    height=100
)

analytics_total_frame.pack(
    fill="x"
)


tk.Label(
    analytics_total_frame,
    text="TOTAL SPENDING",
    font=("Segoe UI", 9, "bold"),
    bg=WHITE,
    fg=SECONDARY_TEXT
).pack(
    anchor="w",
    padx=20,
    pady=(15, 2)
)


analytics_total_label = tk.Label(
    analytics_total_frame,
    text="₹0.00",
    font=("Segoe UI", 22, "bold"),
    bg=WHITE,
    fg=TEXT
)

analytics_total_label.pack(
    anchor="w",
    padx=20
)


analytics_body = tk.Frame(
    analytics_page,
    bg=BACKGROUND
)

analytics_body.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=15
)


# Category table

analytics_table_frame = tk.LabelFrame(
    analytics_body,
    text="  Category Breakdown  ",
    font=("Segoe UI", 11, "bold"),
    bg=WHITE,
    fg=TEXT
)

analytics_table_frame.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 10)
)


analytics_table = ttk.Treeview(
    analytics_table_frame,
    columns=(
        "Category",
        "Amount",
        "Percentage"
    ),
    show="headings",
    height=10
)


analytics_table.heading(
    "Category",
    text="Category"
)

analytics_table.heading(
    "Amount",
    text="Amount"
)

analytics_table.heading(
    "Percentage",
    text="Share"
)


for column in (
    "Category",
    "Amount",
    "Percentage"
):

    analytics_table.column(
        column,
        width=140,
        anchor="center"
    )


analytics_table.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)


# Simple visual bars

chart_frame = tk.LabelFrame(
    analytics_body,
    text="  Spending Distribution  ",
    font=("Segoe UI", 11, "bold"),
    bg=WHITE,
    fg=TEXT
)

chart_frame.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(10, 0)
)


chart_canvas = tk.Canvas(
    chart_frame,
    bg=WHITE,
    highlightthickness=0
)

chart_canvas.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=15
)


def refresh_analytics():

    total = get_total()

    analytics_total_label.config(
        text=f"₹{total:,.2f}"
    )

    for item in analytics_table.get_children():
        analytics_table.delete(item)

    chart_canvas.delete("all")

    categories = get_category_data()

    for category, amount in categories:

        percentage = (
            amount / total * 100
            if total > 0
            else 0
        )

        analytics_table.insert(
            "",
            "end",
            values=(
                category,
                f"₹{amount:,.2f}",
                f"{percentage:.1f}%"
            )
        )

    if not categories:

        chart_canvas.create_text(
            220,
            120,
            text="No expense data available",
            font=("Segoe UI", 12),
            fill=SECONDARY_TEXT
        )

        return

    max_amount = categories[0][1]

    y = 35

    for category, amount in categories[:6]:

        percentage = amount / total * 100

        chart_canvas.create_text(
            10,
            y,
            text=category,
            anchor="w",
            font=("Segoe UI", 10, "bold"),
            fill=TEXT
        )

        bar_width = (
            amount / max_amount * 280
            if max_amount > 0
            else 0
        )

        chart_canvas.create_rectangle(
            120,
            y - 8,
            120 + bar_width,
            y + 10,
            fill=PRIMARY,
            outline=""
        )

        chart_canvas.create_text(
            420,
            y,
            text=f"₹{amount:,.0f}",
            anchor="e",
            font=("Segoe UI", 9),
            fill=SECONDARY_TEXT
        )

        y += 45


# ============================================================
# BUDGET PAGE
# ============================================================

budget_page = tk.Frame(
    page_container,
    bg=BACKGROUND
)

pages["Budget"] = budget_page


page_header(
    budget_page,
    "Budget",
    "Set and monitor your monthly spending limit"
)


budget_card = tk.Frame(
    budget_page,
    bg=WHITE
)

budget_card.pack(
    fill="x",
    padx=30,
    pady=10
)


tk.Label(
    budget_card,
    text="Monthly Budget",
    font=("Segoe UI", 12, "bold"),
    bg=WHITE,
    fg=TEXT
).pack(
    anchor="w",
    padx=25,
    pady=(20, 5)
)


budget_input = tk.Entry(
    budget_card,
    font=("Segoe UI", 12),
    width=25
)

budget_input.pack(
    anchor="w",
    padx=25,
    pady=5
)


def update_budget():

    text = budget_input.get().strip()

    try:

        amount = float(text)

        if amount <= 0:
            raise ValueError

    except ValueError:

        messagebox.showerror(
            "Invalid Budget",
            "Please enter a valid positive amount."
        )

        return

    save_budget(amount)

    budget_input.delete(
        0,
        tk.END
    )

    refresh_budget()
    refresh_dashboard()

    messagebox.showinfo(
        "Budget Updated",
        "Monthly budget updated successfully."
    )


tk.Button(
    budget_card,
    text="Save Budget",
    command=update_budget,
    bg=PRIMARY,
    fg=WHITE,
    relief="flat",
    padx=20,
    pady=7,
    cursor="hand2"
).pack(
    anchor="w",
    padx=25,
    pady=(5, 20)
)


budget_status = tk.Frame(
    budget_page,
    bg=WHITE
)

budget_status.pack(
    fill="x",
    padx=30,
    pady=10
)


budget_status_title = tk.Label(
    budget_status,
    text="Budget Status",
    font=("Segoe UI", 13, "bold"),
    bg=WHITE,
    fg=TEXT
)

budget_status_title.pack(
    anchor="w",
    padx=25,
    pady=(20, 10)
)


budget_status_label = tk.Label(
    budget_status,
    text="",
    font=("Segoe UI", 11),
    bg=WHITE,
    fg=SECONDARY_TEXT
)

budget_status_label.pack(
    anchor="w",
    padx=25
)


budget_progress = ttk.Progressbar(
    budget_status,
    orient="horizontal",
    length=500,
    mode="determinate"
)

budget_progress.pack(
    fill="x",
    padx=25,
    pady=15
)


budget_details = tk.Label(
    budget_status,
    text="",
    font=("Segoe UI", 10),
    bg=WHITE,
    fg=SECONDARY_TEXT
)

budget_details.pack(
    anchor="w",
    padx=25,
    pady=(0, 20)
)


def refresh_budget():

    budget = get_budget()
    spent = get_total()

    if budget <= 0:

        budget_status_label.config(
            text="No monthly budget has been set."
        )

        budget_details.config(
            text="Set a budget above to start tracking."
        )

        budget_progress["value"] = 0

        return

    percentage = (
        spent / budget
    ) * 100

    progress_value = min(
        percentage,
        100
    )

    budget_progress["value"] = progress_value

    remaining = budget - spent

    if remaining >= 0:

        budget_status_label.config(
            text=f"You have ₹{remaining:,.2f} remaining."
        )

        budget_details.config(
            text=f"Spent: ₹{spent:,.2f} of ₹{budget:,.2f} "
                 f"({percentage:.1f}%)"
        )

    else:

        budget_status_label.config(
            text=f"Budget exceeded by ₹{abs(remaining):,.2f}."
        )

        budget_details.config(
            text=f"Spent: ₹{spent:,.2f} of ₹{budget:,.2f} "
                 f"({percentage:.1f}%)"
        )


# ============================================================
# ADD EXPENSE PAGE
# ============================================================

add_page = tk.Frame(
    page_container,
    bg=BACKGROUND
)

pages["Add Expense"] = add_page


page_header(
    add_page,
    "Add Expense",
    "Record a new transaction"
)


form = tk.Frame(
    add_page,
    bg=WHITE
)

form.pack(
    padx=100,
    pady=20,
    fill="x"
)


tk.Label(
    form,
    text="Amount",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=TEXT
).grid(
    row=0,
    column=0,
    sticky="w",
    padx=30,
    pady=(30, 8)
)


amount_input = tk.Entry(
    form,
    font=("Segoe UI", 11),
    width=40
)

amount_input.grid(
    row=1,
    column=0,
    padx=30,
    pady=(0, 15)
)


tk.Label(
    form,
    text="Category",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=TEXT
).grid(
    row=2,
    column=0,
    sticky="w",
    padx=30,
    pady=8
)


category_input = ttk.Combobox(
    form,
    values=[
        "Food",
        "Travel",
        "Shopping",
        "Education",
        "Entertainment",
        "Health",
        "Bills",
        "Other"
    ],
    state="readonly",
    width=37
)

category_input.grid(
    row=3,
    column=0,
    padx=30,
    pady=(0, 15)
)


tk.Label(
    form,
    text="Description",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=TEXT
).grid(
    row=4,
    column=0,
    sticky="w",
    padx=30,
    pady=8
)


description_input = tk.Entry(
    form,
    font=("Segoe UI", 11),
    width=40
)

description_input.grid(
    row=5,
    column=0,
    padx=30,
    pady=(0, 20)
)


def save_new_expense():

    amount_text = amount_input.get().strip()
    category = category_input.get().strip()
    description = description_input.get().strip()

    if not amount_text or not category or not description:

        messagebox.showwarning(
            "Missing Information",
            "Please fill all fields."
        )

        return

    try:

        amount = float(amount_text)

        if amount <= 0:
            raise ValueError

    except ValueError:

        messagebox.showerror(
            "Invalid Amount",
            "Please enter a valid positive amount."
        )

        return

    add_expense_db(
        amount,
        category,
        description
    )

    amount_input.delete(
        0,
        tk.END
    )

    category_input.set("")

    description_input.delete(
        0,
        tk.END
    )

    refresh_dashboard()
    refresh_expenses()
    refresh_analytics()
    refresh_budget()

    messagebox.showinfo(
        "Success",
        "Expense added successfully!"
    )

    show_page("Expenses")


tk.Button(
    form,
    text="+  Save Expense",
    command=save_new_expense,
    bg=PRIMARY,
    fg=WHITE,
    activebackground=PRIMARY_DARK,
    activeforeground=WHITE,
    relief="flat",
    font=("Segoe UI", 11, "bold"),
    padx=25,
    pady=9,
    cursor="hand2"
).grid(
    row=6,
    column=0,
    sticky="w",
    padx=30,
    pady=(0, 30)
)


# ============================================================
# INITIAL LOAD
# ============================================================

refresh_dashboard()
refresh_expenses()
refresh_analytics()
refresh_budget()

show_page("Dashboard")


# ============================================================
# START APPLICATION
# ============================================================

root.mainloop()