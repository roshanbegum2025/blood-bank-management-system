import tkinter as tk

def open_dashboard():
    win = tk.Tk()
    win.title("Blood Bank - Dashboard")
    win.geometry("500x500")
    win.configure(bg="#8B0000")
    win.resizable(False, False)

    # Title
    tk.Label(win,
             text="🩸 Blood Bank System",
             font=("Arial", 20, "bold"),
             bg="#8B0000", fg="white").pack(pady=20)

    tk.Label(win,
             text="Welcome, Admin!",
             font=("Arial", 12),
             bg="#8B0000", fg="#ffcccc").pack()

    # ── Button Functions ──────────────────────
    def go_donors():
        import donors
        donors.open_donors()

    def go_inventory():
        import inventory
        inventory.open_inventory()

    def go_recipients():
        import recipients
        recipients.open_recipients()

    def go_donations():
        import donations
        donations.open_donations()

    def go_reports():
        import reports
        reports.open_reports()

    # ── Buttons ───────────────────────────────
    buttons = [
        ("👤  Manage Donors",    go_donors),
        ("🩸  Blood Inventory",  go_inventory),
        ("🏥  Blood Requests",   go_recipients),
        ("📋  Donation Log",     go_donations),
        ("📊  Reports & Search", go_reports),
    ]

    for label, command in buttons:
        tk.Button(win,
                  text=label,
                  font=("Arial", 12, "bold"),
                  bg="white", fg="#8B0000",
                  width=28, height=2,
                  cursor="hand2",
                  command=command).pack(pady=5)

    # Logout
    tk.Button(win,
              text="🚪  Logout",
              font=("Arial", 10),
              bg="#5a0000", fg="white",
              width=15, cursor="hand2",
              command=win.destroy).pack(pady=15)

    win.mainloop()
