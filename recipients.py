import tkinter as tk
from tkinter import ttk, messagebox
from db_connect import get_connection
from datetime import date

def open_recipients():
    win = tk.Toplevel()
    win.title("Blood Requests")
    win.geometry("700x600")
    win.configure(bg="#8B0000")

    tk.Label(win, text="🏥 Blood Requests",
             font=("Arial", 16, "bold"),
             bg="#8B0000", fg="white").pack(pady=10)

    frame = tk.Frame(win, bg="#8B0000")
    frame.pack(pady=5)

    fields = ["Name", "Age", "Phone", "Hospital Name", "Units Needed"]
    entries = {}

    for i, field in enumerate(fields):
        tk.Label(frame, text=field, bg="#8B0000",
                 fg="white", font=("Arial", 10)).grid(row=i, column=0,
                 padx=10, pady=4, sticky="e")
        e = tk.Entry(frame, width=30, font=("Arial", 10))
        e.grid(row=i, column=1, padx=10, pady=4)
        entries[field] = e

    # Blood Group
    tk.Label(frame, text="Blood Group", bg="#8B0000",
             fg="white", font=("Arial", 10)).grid(row=5, column=0,
             padx=10, pady=4, sticky="e")
    bg_var = tk.StringVar()
    ttk.Combobox(frame, textvariable=bg_var, width=28,
                 values=['A+','A-','B+','B-','AB+','AB-','O+','O-']
                 ).grid(row=5, column=1, padx=10, pady=4)

    # Gender
    tk.Label(frame, text="Gender", bg="#8B0000",
             fg="white", font=("Arial", 10)).grid(row=6, column=0,
             padx=10, pady=4, sticky="e")
    gender_var = tk.StringVar()
    ttk.Combobox(frame, textvariable=gender_var, width=28,
                 values=['Male','Female','Other']
                 ).grid(row=6, column=1, padx=10, pady=4)

    def add_request():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Recipients
                (name, age, phone, hospital_name, units_needed,
                 blood_group, gender, request_date, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Pending')
            """, (entries["Name"].get(), entries["Age"].get(),
                  entries["Phone"].get(), entries["Hospital Name"].get(),
                  entries["Units Needed"].get(), bg_var.get(),
                  gender_var.get(), date.today()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success!", "Blood request added! 🏥")
            load_requests()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="➕ Add Request",
              bg="white", fg="#8B0000",
              font=("Arial", 10, "bold"),
              width=15, cursor="hand2",
              command=add_request).pack(pady=5)

    cols = ("ID", "Name", "Blood Group", "Units", "Hospital", "Date", "Status")
    tree = ttk.Treeview(win, columns=cols, show="headings", height=8)
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=90, anchor="center")
    tree.pack(pady=10, padx=10, fill="x")

    def load_requests():
        for row in tree.get_children():
            tree.delete(row)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT recipient_id, name, blood_group, units_needed,
                       hospital_name, request_date, status
                FROM Recipients
            """)
            rows = cursor.fetchall()
            conn.close()
            for row in rows:
                tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    load_requests()
