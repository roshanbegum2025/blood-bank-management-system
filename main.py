import tkinter as tk
from tkinter import messagebox
from db_connect import get_connection

def login():
    username = entry_user.get()
    password = entry_pass.get()

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Admin WHERE username=%s AND password=%s",
                       (username, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            messagebox.showinfo("Success", "Welcome to Blood Bank System!")
            root.destroy()
            import dashboard
            dashboard.open_dashboard()
        else:
            messagebox.showerror("Error", "Wrong username or password!")

    except Exception as e:
        messagebox.showerror("Connection Error", str(e))

# ── Window Setup ──────────────────────────
root = tk.Tk()
root.title("Blood Bank Management System")
root.geometry("450x350")
root.configure(bg="#8B0000")
root.resizable(False, False)

# ── Title ─────────────────────────────────
tk.Label(root,
         text="🩸 Blood Bank System",
         font=("Arial", 20, "bold"),
         bg="#8B0000", fg="white").pack(pady=30)

# ── Username ──────────────────────────────
tk.Label(root, text="Username",
         font=("Arial", 11),
         bg="#8B0000", fg="white").pack()
entry_user = tk.Entry(root, width=30, font=("Arial", 11))
entry_user.pack(pady=5)

# ── Password ──────────────────────────────
tk.Label(root, text="Password",
         font=("Arial", 11),
         bg="#8B0000", fg="white").pack()
entry_pass = tk.Entry(root, show="*", width=30, font=("Arial", 11))
entry_pass.pack(pady=5)

# ── Login Button ──────────────────────────
tk.Button(root,
          text="Login",
          font=("Arial", 12, "bold"),
          bg="white", fg="#8B0000",
          width=15, cursor="hand2",
          command=login).pack(pady=25)

# ── Footer ────────────────────────────────
tk.Label(root,
         text="Default: admin / admin123",
         font=("Arial", 8),
         bg="#8B0000", fg="#ffcccc").pack()

root.mainloop()
