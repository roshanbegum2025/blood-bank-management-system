import tkinter as tk
from tkinter import ttk, messagebox
from db_connect import get_connection
from datetime import date, timedelta

def open_donors():
    win = tk.Toplevel()
    win.title("Manage Donors")
    win.geometry("700x600")
    win.configure(bg="#8B0000")

    tk.Label(win, text="👤 Manage Donors",
             font=("Arial", 16, "bold"),
             bg="#8B0000", fg="white").pack(pady=10)

    # ── Input Frame ──────────────────────────
    frame = tk.Frame(win, bg="#8B0000")
    frame.pack(pady=5)

    fields = ["Name", "Age", "Phone", "Email", "Address"]
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
    bg_menu = ttk.Combobox(frame, textvariable=bg_var, width=28,
                            values=['A+','A-','B+','B-','AB+','AB-','O+','O-'])
    bg_menu.grid(row=5, column=1, padx=10, pady=4)

    # Gender
    tk.Label(frame, text="Gender", bg="#8B0000",
             fg="white", font=("Arial", 10)).grid(row=6, column=0,
             padx=10, pady=4, sticky="e")
    gender_var = tk.StringVar()
    gender_menu = ttk.Combobox(frame, textvariable=gender_var, width=28,
                                values=['Male','Female','Other'])
    gender_menu.grid(row=6, column=1, padx=10, pady=4)

    # ── Add Donor Function ───────────────────
    def add_donor():
        name    = entries["Name"].get()
        age     = entries["Age"].get()
        phone   = entries["Phone"].get()
        email   = entries["Email"].get()
        address = entries["Address"].get()
        bg      = bg_var.get()
        gender  = gender_var.get()

        if not name or not age or not phone or not bg or not gender:
            messagebox.showwarning("Missing!", "Please fill all required fields!")
            return

        # Eligibility check — must be 18+ and donate every 90 days
        if int(age) < 18:
            messagebox.showerror("Not Eligible!", "Donor must be at least 18 years old!")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Donors (name, age, phone, email, address,
                                    blood_group, gender, last_donated, is_eligible)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, int(age), phone, email, address,
                  bg, gender, date.today(), True))
            
            # Update inventory
            cursor.execute("""
                INSERT INTO BloodInventory (blood_group, units, expiry_date)
                VALUES (%s, 1, %s)
                ON DUPLICATE KEY UPDATE units = units + 1
            """, (bg, date.today() + timedelta(days=42)))

            # Log the donation
            cursor.execute("""
                INSERT INTO DonationLog (donor_id, blood_group, units, donated_on)
                VALUES (LAST_INSERT_ID(), %s, 1, %s)
            """, (bg, date.today()))

            conn.commit()
            conn.close()
            messagebox.showinfo("Success!", f"Donor {name} added successfully! 🩸")
            load_donors()

            # Clear fields
            for e in entries.values():
                e.delete(0, tk.END)
            bg_var.set("")
            gender_var.set("")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ── Buttons ──────────────────────────────
    btn_frame = tk.Frame(win, bg="#8B0000")
    btn_frame.pack(pady=5)

    tk.Button(btn_frame, text="➕ Add Donor",
              bg="white", fg="#8B0000",
              font=("Arial", 10, "bold"),
              width=15, cursor="hand2",
              command=add_donor).grid(row=0, column=0, padx=10)

    tk.Button(btn_frame, text="🗑️ Delete Donor",
              bg="#5a0000", fg="white",
              font=("Arial", 10, "bold"),
              width=15, cursor="hand2",
              command=lambda: delete_donor()).grid(row=0, column=1, padx=10)

    tk.Button(btn_frame, text="🔄 Refresh",
              bg="#5a0000", fg="white",
              font=("Arial", 10, "bold"),
              width=15, cursor="hand2",
              command=lambda: load_donors()).grid(row=0, column=2, padx=10)

    # ── Donor Table ──────────────────────────
    cols = ("ID", "Name", "Age", "Gender", "Blood Group",
            "Phone", "Last Donated", "Eligible")
    tree = ttk.Treeview(win, columns=cols, show="headings", height=10)

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=85, anchor="center")

    tree.pack(pady=10, padx=10, fill="x")

    # Scrollbar
    scrollbar = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)

    # ── Load Donors From DB ──────────────────
    def load_donors():
        for row in tree.get_children():
            tree.delete(row)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT donor_id, name, age, gender, blood_group,
                       phone, last_donated, is_eligible
                FROM Donors
            """)
            rows = cursor.fetchall()
            conn.close()
            for row in rows:
                eligible = "✅ Yes" if row[7] else "❌ No"
                tree.insert("", tk.END,
                            values=(row[0], row[1], row[2], row[3],
                                    row[4], row[5], row[6], eligible))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ── Delete Donor ─────────────────────────
    def delete_donor():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Select!", "Please select a donor to delete!")
            return
        donor_id = tree.item(selected[0])["values"][0]
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this donor?")
        if confirm:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Donors WHERE donor_id=%s", (donor_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Deleted!", "Donor removed successfully!")
                load_donors()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    load_donors()
