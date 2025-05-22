import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ADMIN_DASHBOARD_PATH = os.path.join(BASE_DIR, "admin_dashboard.py")

class AdminLogin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Admin Login")
        self.geometry("350x250")
        self.configure(bg="#f0f0f0", padx=20, pady=20)

        tk.Label(self, text="🔐 Admin Access", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

        self.create_labeled_entry("Username", 0)
        self.create_labeled_entry("Password", 1, show="*")

        tk.Button(self, text="Login", bg="#1d72b8", fg="white", font=("Arial", 11),
                  command=self.authenticate).pack(pady=20, ipadx=10)

    def create_labeled_entry(self, label_text, row, show=None):
        tk.Label(self, text=label_text + ":", bg="#f0f0f0", font=("Arial", 11)).pack(anchor="w")
        entry = tk.Entry(self, show=show, width=30)
        entry.pack(pady=5)
        setattr(self, f"{label_text.lower()}_entry", entry)

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "admin123":
            self.destroy()
            subprocess.Popen([sys.executable, ADMIN_DASHBOARD_PATH])
        else:
            messagebox.showerror("Access Denied", "Invalid credentials.")

if __name__ == "__main__":
    app = AdminLogin()
    app.mainloop()
