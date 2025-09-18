import tkinter as tk
import sqlite3

from tkinter import ttk
from tkinter import*
from tkinter import filedialog, messagebox
from tkmacosx import Button

class ReportPage:
    def __init__(self, window):
        self.window = window
        self.frame = tk.Frame(window, background="gray74")
        self.frame.pack(side="top", fill="both", expand=True)
        self.current_report = None
        
####################################################################################################################################################################################        
############   LEFT SECTION   ####################################################################################################################################################################################
####################################################################################################################################################################################      

        left_frame = tk.Frame(self.frame, background="gray74", highlightbackground="black", highlightthickness=None)
        left_frame.place(relx=0, rely=0, relwidth=0.3, relheight=1)
        
        inner_left_frame = tk.LabelFrame(left_frame, text="Budgets", font="system 15 bold", foreground="black", background="gray74", borderwidth=1, relief="sunken")
        inner_left_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # TREEVIEW
        
        # Style
        style = ttk.Style()
        
        # Theme 
        style.theme_use("default")
        
        # Config. Colors
        style.configure("Treeview",
            background="LightCyan2",
            foreground="black",
            rowheight=25,
            fieldbackground="white")
        
        # Selected Color
        style.map("Treeview",
            background=[('selected', 'blue2')])
        
        # Scrollbar
        tree_scroll = Scrollbar(inner_left_frame)
        tree_scroll.pack(side="right", fill="y")
        
        # Tree
        tree = ttk.Treeview(inner_left_frame, selectmode="extended",
                            columns=("Year", "Month"), show="headings")
        
        tree.bind("<<TreeviewSelect>>", self.on_budget_select)
        
        # Config Scrollbar
        tree_scroll.config(command=tree.yview)
        
        # Format Columns
        tree.column("Year", anchor="center", width=80)
        tree.column("Month",anchor="center",  width=120)

        # Heading
        tree.heading("Year", text="Year")
        tree.heading("Month", text="Month")
        
        tree.pack(fill="both", expand=True)
        
        # Striped Rows 
        tree.tag_configure("oddrow", background="white")
        tree.tag_configure("evenrow", background="lightsteelblue1")
        
        # Load budgets from database
        conn = sqlite3.connect("moneywand.db")
        c = conn.cursor()
        c.execute("""
            SELECT year, month FROM budgets
            ORDER BY year DESC,
            CASE month
                WHEN 'January' THEN 1
                WHEN 'February' THEN 2
                WHEN 'March' THEN 3
                WHEN 'April' THEN 4
                WHEN 'May' THEN 5
                WHEN 'June' THEN 6
                WHEN 'July' THEN 7
                WHEN 'August' THEN 8
                WHEN 'September' THEN 9
                WHEN 'October' THEN 10
                WHEN 'November' THEN 11
                WHEN 'December' THEN 12
            END DESC
        """)
        rows = c.fetchall()
        conn.close()
        for i, (year, month) in enumerate(rows):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            tree.insert("", "end", values=(year, month), tags=(tag,))
               
        
####################################################################################################################################################################################        
############   RIGHT SECTION   ####################################################################################################################################################################################
####################################################################################################################################################################################      

        right_frame = tk.Frame(self.frame, background="gray74", highlightbackground="black", highlightthickness=None)
        right_frame.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)

        inner_right_frame = tk.LabelFrame(right_frame, text="Report", font="system 15 bold", foreground="black", background="gray74", borderwidth=1, relief="sunken")
        inner_right_frame.pack(padx=10, pady=10, fill="both", expand=True)

        canvas = tk.Canvas(inner_right_frame, background="white", highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=0, pady=0)

        # Add vertical scrollbar to canvas
        scrollbar = tk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Income and Expenses section inside canvas
        self.section1 = tk.LabelFrame(canvas, background="white", highlightcolor="black", highlightthickness=0, foreground="black",
                    font="system 15 bold", borderwidth=0, relief="flat")
        canvas.create_window((0, 0), window=self.section1, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.section1.bind("<Configure>", on_frame_configure)

        # Section 0 - Title
        header_frame = tk.Frame(self.section1, background="white")
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(10, 5), padx=0)
        header_frame.grid_columnconfigure(0, weight=1)
        self.budget_name_label = tk.Label(header_frame, text="Select a budget", font="system 16 bold", background="white", foreground="black")
        self.budget_name_label.grid(row=0, column=0, sticky="w")
        self.export_btn = Button(header_frame, text="Export PDF", bg="royalblue", fg="white",
                                 borderless=1, command=self.export_to_pdf)
        self.export_btn.grid(row=0, column=1, sticky="e", padx=(6, 0))

    def on_budget_select(self, event):
        # Get Budget Date
        selected = event.widget.selection()
        if not selected:
            return
        item = event.widget.item(selected[0])
        values = item["values"]
        year = values[0]
        month = values[1]
        budget_title = f"{month} {year}"
        
        # Collect Categories
        conn = sqlite3.connect("moneywand.db")
        c = conn.cursor()
        c.execute("SELECT id, categories, spending_limits, contributors FROM budgets WHERE year=? AND month=?", (year, month))
        result = c.fetchone()
        if not result:
            conn.close()
            return
        budget_id, categories_json, limits_json, contributors_json = result
        categories = []
        limits = {}
        contributors = []
        try:
            import json
            categories = json.loads(categories_json)
            if limits_json:
                limits = json.loads(limits_json)
            if contributors_json:
                contributors = json.loads(contributors_json)
        except Exception:
            categories = []
            limits = {}
            contributors = []

        if "You" not in contributors:
            contributors = ["You"] + contributors
        else:
            contributors = ["You"] + [n for n in contributors if n != "You"]
        contributors = contributors[:2]
            
        # Get amount spent
        spent_per_cat = {}
        total_spent = 0
        for cat in categories:
            c.execute("SELECT SUM(amount) FROM expenses WHERE budget_id=? AND category=?", (budget_id, cat))
            spent = c.fetchone()[0] or 0
            spent_per_cat[cat] = spent
            total_spent += spent
        conn.close()
        
        for widget in self.section1.winfo_children():
            widget.destroy()

        header_frame = tk.Frame(self.section1, background="white")
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(10, 5), padx=0)
        header_frame.grid_columnconfigure(0, weight=1)
        self.budget_name_label = tk.Label(header_frame, text=budget_title, font="system 16 bold", background="white", foreground="black")
        self.budget_name_label.grid(row=0, column=0, sticky="w")
        self.export_btn = Button(header_frame, text="Export PDF", bg="royalblue", fg="white", borderless=1, command=self.export_to_pdf)
        self.export_btn.grid(row=0, column=1, sticky="e", padx=(6, 0))

        self.info_label = tk.Label(self.section1, text="Income and Expenses", font="system 15 bold", background="white", foreground="blue2", anchor="w", justify="left")
        self.info_label.grid(row=1, column=0, columnspan=4, pady=0, padx=0, sticky="w")

        tk.Label(self.section1, text="Category", font="system 12 bold", background="white", foreground="black").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(self.section1, text="Spent", font="system 12 bold", background="white", foreground="black").grid(row=2, column=1, padx=5, pady=5)

        for i, cat in enumerate(categories, start=3):
            tk.Label(self.section1, text=cat, background="white", foreground="black").grid(row=i, column=0, padx=5, pady=2, sticky="w")
            tk.Label(self.section1, text=f"{spent_per_cat[cat]:.2f}", background="white", foreground="black").grid(row=i, column=1, padx=5, pady=2, sticky="e")

        tk.Label(self.section1, text="Total", font="system 12 bold", background="white", foreground="red4").grid(row=len(categories)+3, column=0, padx=5, pady=8, sticky="w")
        tk.Label(self.section1, text=f"{total_spent:.2f}", font="system 12 bold", background="white", foreground="red4").grid(row=len(categories)+3, column=1, padx=5, pady=8, sticky="e")

        separator1 = ttk.Separator(self.section1, orient=tk.HORIZONTAL)
        separator1.grid(row=len(categories)+4, column=0, columnspan=3, pady=[10, 10], padx=5, sticky="ew")
        
        conn = sqlite3.connect("moneywand.db")
        c = conn.cursor()
        c.execute("SELECT source, amount FROM income WHERE budget_id=?", (budget_id,))
        income_entries = c.fetchall()
        conn.close()

        income_start_row = len(categories) + 4
        tk.Label(self.section1, text="Source", font="system 12 bold", background="white", foreground="black").grid(row=income_start_row, column=0, padx=5, pady=5)
        tk.Label(self.section1, text="Amount", font="system 12 bold", background="white", foreground="black").grid(row=income_start_row, column=1, padx=5, pady=5)

        total_income = 0
        for i, (source, amount) in enumerate(income_entries, start=1):
            tk.Label(self.section1, text=source, background="white", foreground="black").grid(row=income_start_row+i, column=0, padx=5, pady=2, sticky="w")
            tk.Label(self.section1, text=f"{amount:.2f}", background="white", foreground="black").grid(row=income_start_row+i, column=1, padx=5, pady=2, sticky="e")
            total_income += amount

        # Totals and balance 
        tk.Label(self.section1, text="Total Income", font="system 12 bold", background="white", foreground="green4").grid(row=income_start_row+len(income_entries)+1, column=0, padx=5, pady=8, sticky="w")
        tk.Label(self.section1, text=f"{total_income:.2f}", font="system 12 bold", background="white", foreground="green4").grid(row=income_start_row+len(income_entries)+1, column=1, padx=5, pady=8, sticky="e")

        sep2 = ttk.Separator(self.section1, orient=tk.HORIZONTAL)
        sep2.grid(row=income_start_row+len(income_entries)+2, column=0, columnspan=2, pady=[12, 12], padx=5, sticky="ew")

        balance = total_income - total_spent
        balance_color = "green4" if balance >= 0 else "red4"
        tk.Label(self.section1, text="Balance", font="system 12 bold", background="white", foreground=balance_color).grid(row=income_start_row+len(income_entries)+3, column=0, padx=5, pady=8, sticky="w")
        tk.Label(self.section1, text=f"{balance:.2f}", font="system 12 bold", background="white", foreground=balance_color).grid(row=income_start_row+len(income_entries)+3, column=1, padx=5, pady=8, sticky="e")

        sep3 = ttk.Separator(self.section1, orient=tk.HORIZONTAL)
        sep3.grid(row=income_start_row+len(income_entries)+4, column=0, columnspan=4, pady=[15, 15], padx=5, sticky="ew")

        # Budget Details section
        details_row_start = income_start_row + len(income_entries) + 5
        details_frame = tk.LabelFrame(self.section1, text="Budget Details", font="system 14 bold", background="white", foreground="blue2", borderwidth=0, relief="flat")
        details_frame.grid(row=details_row_start, column=0, columnspan=4, sticky="nsew", padx=0, pady=0)

        tk.Label(details_frame, text="Category", font="system 12 bold", background="white", foreground="black").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Label(details_frame, text="Spending Limit", font="system 12 bold", background="white", foreground="black").grid(row=0, column=1, padx=5, pady=5, sticky="e")
        tk.Label(details_frame, text="Amount Spent", font="system 12 bold", background="white", foreground="black").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        tk.Label(details_frame, text="Over / Under", font="system 12 bold", background="white", foreground="black").grid(row=0, column=3, padx=5, pady=5, sticky="e")

        for idx, cat in enumerate(categories, start=1):
            limit_val = limits.get(cat, 0) or 0
            spent_val = spent_per_cat.get(cat, 0) or 0
            spent_color = "green4" if spent_val <= float(limit_val) else "red4"
            diff = spent_val - float(limit_val)
            diff_color = "red4" if diff > 0 else ("green4" if diff < 0 else "black")
            tk.Label(details_frame, text=cat, background="white", foreground="black").grid(row=idx, column=0, padx=5, pady=2, sticky="w")
            tk.Label(details_frame, text=f"{float(limit_val):.2f}", background="white", foreground="black").grid(row=idx, column=1, padx=5, pady=2, sticky="e")
            tk.Label(details_frame, text=f"{spent_val:.2f}", background="white", foreground=spent_color).grid(row=idx, column=2, padx=5, pady=2, sticky="e")
            tk.Label(details_frame, text=f"{diff:.2f}", background="white", foreground=diff_color).grid(row=idx, column=3, padx=5, pady=2, sticky="e")

        sep_after_details = ttk.Separator(self.section1, orient=tk.HORIZONTAL)
        sep_after_details.grid(row=details_row_start+1, column=0, columnspan=4, pady=[15, 15], padx=5, sticky="ew")

        # Contributors section
        contributors_row_start = details_row_start + 2
        contrib_frame = tk.LabelFrame(self.section1, text="Contributors", font="system 14 bold", background="white", foreground="blue2", borderwidth=0, relief="flat")
        contrib_frame.grid(row=contributors_row_start, column=0, columnspan=4, sticky="nsew", padx=0, pady=(0,5))

        conn = sqlite3.connect("moneywand.db")
        c = conn.cursor()
        c.execute("""
            SELECT date, category, amount, comment, contributor
            FROM expenses
            WHERE budget_id=? AND contributor IS NOT NULL AND TRIM(contributor) <> ''
            ORDER BY date ASC
        """, (budget_id,))
        assigned = c.fetchall()
        conn.close()

        contrib_map = {name: [] for name in contributors}
        for d, cat, amt, com, contr in assigned:
            if contr in contrib_map:
                contrib_map[contr].append((d or '', cat or '', com or '', float(amt or 0)))

        totals = {}
        for col_idx, name in enumerate(contributors):
            col = tk.Frame(contrib_frame, background="white")
            col.grid(row=0, column=col_idx, padx=10, pady=5, sticky="nw")
            tk.Label(col, text=name, font="system 12 bold", background="white", foreground="black").grid(row=0, column=0, columnspan=2, sticky="w")

            total = 0.0
            entries = contrib_map.get(name, [])
            for ridx, (d, cat, com, amt) in enumerate(entries, start=1):
                left = cat if not com else f"{cat} - {com}"
                if d:
                    left = f"{d} | {left}"
                tk.Label(col, text=left, background="white", foreground="black").grid(row=ridx, column=0, padx=2, pady=1, sticky="w")
                tk.Label(col, text=f"{amt:.2f}", background="white", foreground="black").grid(row=ridx, column=1, padx=2, pady=1, sticky="e")
                total += amt

            base = len(entries) + 1
            tk.Label(col, text="Total", font="system 11 bold", background="white", foreground="black").grid(row=base, column=0, padx=2, pady=(6,0), sticky="w")
            tk.Label(col, text=f"{total:.2f}", font="system 11 bold", background="white", foreground="black").grid(row=base, column=1, padx=2, pady=(6,0), sticky="e")
            totals[name] = total

        sep_after_contrib = ttk.Separator(self.section1, orient=tk.HORIZONTAL)
        sep_after_contrib.grid(row=contributors_row_start+1, column=0, columnspan=4, pady=[15, 15], padx=5, sticky="ew")

        diff_row = contributors_row_start + 2
        diff_frame = tk.Frame(self.section1, background="white")
        diff_frame.grid(row=diff_row, column=0, columnspan=4, sticky="w", padx=5, pady=(0,10))

        you_total = totals.get("You", 0.0)
        if len(contributors) > 1:
            other = contributors[1]
            diff_val = you_total - totals.get(other, 0.0)
            tk.Label(diff_frame, text=f"You - {other}: {diff_val:.2f}", background="white", foreground="black", font="system 11").pack(anchor="w")
        else:
            tk.Label(diff_frame, text=f"You: {you_total:.2f}", background="white", foreground="black", font="system 11").pack(anchor="w")
            
        sep_after_diff = ttk.Separator(self.section1, orient=tk.HORIZONTAL)
        sep_after_diff.grid(row=diff_row+1, column=0, columnspan=4, pady=[15, 15], padx=5, sticky="ew")

        # Expense Details section
        expense_details_row_start = diff_row + 2
        expense_frame = tk.LabelFrame(self.section1, text="Expense Details", font="system 14 bold", background="white", foreground="blue2", borderwidth=0, relief="flat")
        expense_frame.grid(row=expense_details_row_start, column=0, columnspan=4, sticky="nsew", padx=0, pady=(0,10))

        # Headers
        tk.Label(expense_frame, text="Date", font="system 12 bold", background="white", foreground="black").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Label(expense_frame, text="Category", font="system 12 bold", background="white", foreground="black").grid(row=0, column=1, padx=5, pady=5, sticky="w")
        tk.Label(expense_frame, text="Comment", font="system 12 bold", background="white", foreground="black").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        tk.Label(expense_frame, text="Contributor", font="system 12 bold", background="white", foreground="black").grid(row=0, column=3, padx=5, pady=5, sticky="w")
        tk.Label(expense_frame, text="Amount", font="system 12 bold", background="white", foreground="black").grid(row=0, column=4, padx=5, pady=5, sticky="e")

        # Fetch and list all expenses for this budget, sorted by date
        conn = sqlite3.connect("moneywand.db")
        c = conn.cursor()
        c.execute(
            """
                SELECT date, category, comment, contributor, amount
                FROM expenses
                WHERE budget_id=?
                ORDER BY date ASC
            """,
            (budget_id,)
        )
        expense_rows = c.fetchall()
        conn.close()

        for ridx, (d, cat, com, contr, amt) in enumerate(expense_rows, start=1):
            tk.Label(expense_frame, text=f"{d or ''}", background="white", foreground="black").grid(row=ridx, column=0, padx=5, pady=2, sticky="w")
            tk.Label(expense_frame, text=f"{cat or ''}", background="white", foreground="black").grid(row=ridx, column=1, padx=5, pady=2, sticky="w")
            tk.Label(expense_frame, text=f"{com or ''}", background="white", foreground="black").grid(row=ridx, column=2, padx=5, pady=2, sticky="w")
            tk.Label(expense_frame, text=f"{contr or ''}", background="white", foreground="black").grid(row=ridx, column=3, padx=5, pady=2, sticky="w")
            tk.Label(expense_frame, text=f"{float(amt or 0):.2f}", background="white", foreground="black").grid(row=ridx, column=4, padx=5, pady=2, sticky="e")

        # Store the current report data for export
        self.current_report = {
            "title": budget_title,
            "year": year,
            "month": month,
            "budget_id": budget_id,
            "categories": categories,
            "limits": limits,
            "spent_per_cat": spent_per_cat,
            "total_spent": total_spent,
            "income_entries": income_entries,
            "total_income": total_income,
            "balance": balance,
            "contributors": contributors,
            "contrib_map": contrib_map,
            "contrib_totals": totals,
            "expense_rows": expense_rows,
        }

    def export_to_pdf(self):
        # Ensure a report is selected
        if not getattr(self, "current_report", None):
            messagebox.showinfo("Export PDF", "Please select a budget first.")
            return

        # Lazily import reportlab and handle absence
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        except Exception:
            messagebox.showerror(
                "ReportLab not available",
                "ReportLab is required to export PDFs.\nInstall with:\n\npip install reportlab",
            )
            return

        rpt = self.current_report

        # Ask the user for a save path
        safe_title = str(rpt.get("title", "report")).replace("/", "-").replace("\\", "-")
        initial = f"{safe_title}.pdf"
        file_path = filedialog.asksaveasfilename(
            title="Save Report as PDF",
            defaultextension=".pdf",
            initialfile=initial,
            filetypes=[("PDF files", "*.pdf")]
        )
        if not file_path:
            return

        doc = SimpleDocTemplate(file_path, pagesize=A4, title=rpt.get("title", "Report"))
        styles = getSampleStyleSheet()
        story = []

        # Title
        story.append(Paragraph(rpt.get("title", "Report"), styles["Title"]))
        story.append(Spacer(1, 12))

        # Income and Expenses overview
        story.append(Paragraph("Income and Expenses", styles["Heading2"]))
        story.append(Spacer(1, 6))

        # Spent per category table
        cat_data = [["Category", "Spent"]]
        for cat in rpt.get("categories", []):
            cat_data.append([cat, f"{float(rpt['spent_per_cat'].get(cat, 0) or 0):.2f}"])
        if len(cat_data) > 1:
            t = Table(cat_data, hAlign='LEFT', colWidths=[200, 80])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                ('TEXTCOLOR', (0,0), (-1,0), colors.black),
                ('GRID', (0,0), (-1,-1), 0.25, colors.grey),
                ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
            ]))
            story.append(t)
            story.append(Spacer(1, 6))

        # Total spent
        story.append(Paragraph(f"Total Spent: <b>{float(rpt.get('total_spent', 0)):.2f}</b>", styles["Normal"]))
        story.append(Spacer(1, 6))

        # Income table
        income_data = [["Source", "Amount"]]
        for source, amount in rpt.get("income_entries", []):
            income_data.append([str(source), f"{float(amount or 0):.2f}"])
        if len(income_data) > 1:
            t = Table(income_data, hAlign='LEFT', colWidths=[200, 80])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                ('GRID', (0,0), (-1,-1), 0.25, colors.grey),
                ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
            ]))
            story.append(t)
            story.append(Spacer(1, 6))

        # Totals and balance
        story.append(Paragraph(f"Total Income: <b>{float(rpt.get('total_income', 0)):.2f}</b>", styles["Normal"]))
        bal = float(rpt.get('balance', 0))
        bal_color = 'green' if bal >= 0 else 'red'
        story.append(Paragraph(f"Balance: <font color='{bal_color}'><b>{bal:.2f}</b></font>", styles["Normal"]))
        story.append(Spacer(1, 12))

        # Budget Details
        story.append(Paragraph("Budget Details", styles["Heading2"]))
        details_data = [["Category", "Spending Limit", "Amount Spent", "Over / Under"]]
        for cat in rpt.get("categories", []):
            limit_val = float(rpt.get("limits", {}).get(cat, 0) or 0)
            spent_val = float(rpt.get("spent_per_cat", {}).get(cat, 0) or 0)
            diff = spent_val - limit_val
            details_data.append([
                cat,
                f"{limit_val:.2f}",
                f"{spent_val:.2f}",
                f"{diff:.2f}",
            ])
        if len(details_data) > 1:
            t = Table(details_data, hAlign='LEFT', colWidths=[160, 80, 80, 80])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                ('GRID', (0,0), (-1,-1), 0.25, colors.grey),
                ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
            ]))
            story.append(t)
            story.append(Spacer(1, 12))

        # Contributors
        contribs = rpt.get("contributors", [])
        if contribs:
            story.append(Paragraph("Contributors", styles["Heading2"]))
            for name in contribs:
                story.append(Paragraph(name, styles["Heading3"]))
                entries = rpt.get("contrib_map", {}).get(name, [])
                contrib_data = [["Entry", "Amount"]]
                for d, cat, com, amt in entries:
                    left = cat if not com else f"{cat} - {com}"
                    if d:
                        left = f"{d} | {left}"
                    contrib_data.append([left, f"{float(amt or 0):.2f}"])
                total_val = float(rpt.get("contrib_totals", {}).get(name, 0))
                contrib_data.append(["Total", f"{total_val:.2f}"])
                t = Table(contrib_data, hAlign='LEFT', colWidths=[300, 80])
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                    ('GRID', (0,0), (-1,-1), 0.25, colors.grey),
                    ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
                ]))
                story.append(t)
                story.append(Spacer(1, 6))
            story.append(Spacer(1, 6))

        # Expense Details
        exp_rows = rpt.get("expense_rows", [])
        if exp_rows:
            story.append(Paragraph("Expense Details", styles["Heading2"]))
            exp_data = [["Date", "Category", "Comment", "Contributor", "Amount"]]
            for d, cat, com, contr, amt in exp_rows:
                exp_data.append([
                    str(d or ''), str(cat or ''), str(com or ''), str(contr or ''), f"{float(amt or 0):.2f}"
                ])
            t = Table(exp_data, hAlign='LEFT', colWidths=[70, 100, 190, 90, 70])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                ('GRID', (0,0), (-1,-1), 0.25, colors.grey),
                ('ALIGN', (4,1), (4,-1), 'RIGHT'),
            ]))
            story.append(t)

        try:
            doc.build(story)
        except Exception as e:
            messagebox.showerror("Export PDF", f"Failed to export PDF:\n{e}")
            return

        messagebox.showinfo("Export PDF", "Report exported successfully.")