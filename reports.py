import tkinter as tk
from tkinter import ttk, messagebox
from db_connect import get_connection

def open_reports():
    win = tk.Toplevel()
    win.title("Reports & Search")
    win.geometry("650x500")
    win.configure(bg="#8B0000")

    tk.Label(win, text="📊 Reports & Search",
             font=("Arial", 16, "bold"),
             bg="#8B0000", fg="white").pack(pady=15)

    # Search by blood group
    frame = tk.Frame(win, bg="#8B0000")
    frame.pack(pady=5)

    tk.Label(frame, text="Search Blood Group:",
             bg="#8B0000", fg="white",
             font=("Arial", 11)).grid(row=0, column=0, padx=10)

    bg_var = tk.StringVar()
    ttk.Combobox(frame, textvariable=bg_var, width=15,
                 values=['A+','A-','B+','B-','AB+','AB-','O+','O-']
                 ).grid(row=0, column=1, padx=10)

    def search_donors():
        for row in tree.get_children():
            tree.delete(row)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT donor_id, name, phone, blood_group, is_eligible
                FROM Donors WHERE blood_group = %s
            """, (bg_var.get(),))
            rows = cursor.fetchall()
            conn.close()
            for row in rows:
                eligible = "✅ Yes" if row[4] else "❌ No"
                tree.insert("", tk.END,
                            values=(row[0], row[1], row[2], row[3], eligible))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def expiry_alert():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT blood_group, units, expiry_date
                FROM BloodInventory
                WHERE expiry_date < CURDATE()
            """)
            rows = cursor.fetchall()
            conn.close()
            if rows:
                msg = "\n".join([f"{r[0]} - {r[1]} units (expired {r[2]})"
                                 for r in rows])
                messagebox.showwarning("⚠️ Expired Blood!", msg)
            else:
                messagebox.showinfo("✅ All Good!", "No expired blood units!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(frame, text="🔍 Search",
              bg="white", fg="#8B0000",
              font=("Arial", 10, "bold"),
              width=10, cursor="hand2",
              command=search_donors).grid(row=0, column=2, padx=10)

    tk.Button(frame, text="⚠️ Expiry Alert",
              bg="#5a0000", fg="white",
              font=("Arial", 10, "bold"),
              width=15, cursor="hand2",
              command=expiry_alert).grid(row=0, column=3, padx=10)

    cols = ("ID", "Name", "Phone", "Blood Group", "Eligible")
    tree = ttk.Treeview(win, columns=cols, show="headings", height=12)
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=110, anchor="center")
    tree.pack(pady=15, padx=10, fill="x")
