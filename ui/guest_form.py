import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
import subprocess
import sys

# Automatically get absolute path to the database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../exhibition.db")
SEAT_FORM_PATH = os.path.join(BASE_DIR, "seat_booking_form.py")

class GuestForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Guest Registration")
        self.geometry("450x400")
        self.configure(bg="#f4f4f4", padx=20, pady=20)

        tk.Label(self, text="Guest Registration Form", font=("Helvetica", 16, "bold"), bg="#f4f4f4").grid(row=0, column=0, columnspan=2, pady=10)

        self.build_form_row("Name", 1)
        self.build_form_row("Email", 2)
        self.build_form_row("Phone", 3)
        self.build_form_row("Title", 4)
        self.build_form_row("Affiliation", 5)

        submit_btn = tk.Button(self, text="Submit", font=("Helvetica", 12, "bold"), bg="#1d72b8", fg="white", command=self.save_guest)
        submit_btn.grid(row=6, column=0, columnspan=2, pady=20, ipadx=10)

    def build_form_row(self, label, row):
        tk.Label(self, text=label + ":", bg="#f4f4f4", font=("Helvetica", 10)).grid(row=row, column=0, sticky="e", pady=5, padx=5)
        entry = tk.Entry(self, width=30)
        entry.grid(row=row, column=1, sticky="w", pady=5, padx=5)
        setattr(self, f"{label.lower()}_entry", entry)

    def save_guest(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        title = self.title_entry.get()
        affiliation = self.affiliation_entry.get()

        if not all([name, email, phone]):
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS guests (
            guest_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            title TEXT,
            affiliation TEXT
        )
        """)

        cursor.execute("INSERT INTO guests (name, email, phone, title, affiliation) VALUES (?, ?, ?, ?, ?)",
                       (name, email, phone, title, affiliation))
        guest_id = cursor.lastrowid
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Guest registered successfully!")

        # Open Seat Booking Form
        try:
            subprocess.Popen([sys.executable, SEAT_FORM_PATH, str(guest_id)])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open seat booking form: {e}")
        self.destroy()

if __name__ == "__main__":
    app = GuestForm()
    app.mainloop()
