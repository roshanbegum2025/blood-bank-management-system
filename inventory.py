import tkinter as tk
from tkinter import ttk, messagebox
from db_connect import get_connection

def open_inventory():
    win = tk.Toplevel()
    win.title("Blood Inventory")
    win.geometry("600x400")
    win.configure(bg="#8B0000")

    tk.Label(win, text="🩸 Blood Inventory",
             font=("Arial", 16, "bold"),
             bg="#8B0000", fg="white").pack(pady=15)

    # ── Table ────────────────────────────────
    cols = ("Blood Group", "Units Available", "Expiry Date", "Last Updated")
    tree = ttk.Treeview(win, columns=cols, show="headings", height=10)

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor="center")
    tree.pack(pady=10, padx=10, fill="x")

    def load_inventory():
        for row in tree.get_children():
            tree.delete(row)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT blood_group, SUM(units), MAX(expiry_date), MAX(last_updated)
                FROM BloodInventory
                GROUP BY blood_group
            """)
            rows = cursor.fetchall()
            conn.close()
            for row in rows:
                # Flag low stock
                units = row[1]
                tag = "low" if units < 5 else "ok"
                tree.insert("", tk.END, values=row, tags=(tag,))
            tree.tag_configure("low", background="#ffcccc")
            tree.tag_configure("ok",  background="#ccffcc")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Low stock warning
    def check_low_stock():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT blood_group, SUM(units)
                FROM BloodInventory
                GROUP BY blood_group
                HAVING SUM(units) < 5
            """)
            rows = cursor.fetchall()
            conn.close()
            if rows:
                low = ", ".join([f"{r[0]}({r[1]} units)" for r in rows])
                messagebox.showwarning("⚠️ Low Stock Alert!",
                                       f"Low stock for:\n{low}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    btn_frame = tk.Frame(win, bg="#8B0000")
    btn_frame.pack(pady=5)

    tk.Button(btn_frame, text="🔄 Refresh",
              bg="white", fg="#8B0000",
              font=("Arial", 10, "bold"),
              width=15, cursor="hand2",
              command=load_inventory).grid(row=0, column=0, padx=10)

    tk.Button(btn_frame, text="⚠️ Check Low Stock",
              bg="#5a0000", fg="white",
              font=("Arial", 10, "bold"),
              width=18, cursor="hand2",
              command=check_low_stock).grid(row=0, column=1, padx=10)

    load_inventory()
