import tkinter as tk
from tkinter import ttk, messagebox
from db_connect import get_connection

def open_donations():
    win = tk.Toplevel()
    win.title("Donation Log")
    win.geometry("600x400")
    win.configure(bg="#8B0000")

    tk.Label(win, text="📋 Donation Log",
             font=("Arial", 16, "bold"),
             bg="#8B0000", fg="white").pack(pady=15)

    cols = ("Log ID", "Donor ID", "Blood Group", "Units", "Donated On")
    tree = ttk.Treeview(win, columns=cols, show="headings", height=12)
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=110, anchor="center")
    tree.pack(pady=10, padx=10, fill="x")

    def load_logs():
        for row in tree.get_children():
            tree.delete(row)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT log_id, donor_id, blood_group, units, donated_on
                FROM DonationLog
                ORDER BY donated_on DESC
            """)
            rows = cursor.fetchall()
            conn.close()
            for row in rows:
                tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="🔄 Refresh",
              bg="white", fg="#8B0000",
              font=("Arial", 10, "bold"),
              width=15, cursor="hand2",
              command=load_logs).pack(pady=5)

    load_logs()
