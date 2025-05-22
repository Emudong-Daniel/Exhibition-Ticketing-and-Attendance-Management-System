import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../exhibition.db")

class SessionConfig(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Configure Sessions")
        self.geometry("400x300")
        self.configure(bg="#f8f8f8", padx=20, pady=20)

        tk.Label(self, text="Add New Session", font=("Arial", 14, "bold"), bg="#f8f8f8").grid(row=0, column=0, columnspan=2, pady=10)

        self.build_label_entry("Session Type", 1)
        self.build_label_entry("Time Slot (e.g. Morning)", 2)
        self.build_label_entry("Date (YYYY-MM-DD)", 3)

        tk.Button(self, text="Save Session", bg="#1d72b8", fg="white", font=("Arial", 11),
                  command=self.save_session).grid(row=4, column=0, columnspan=2, pady=20)

    def build_label_entry(self, label, row):
        tk.Label(self, text=label + ":", bg="#f8f8f8", font=("Arial", 10)).grid(row=row, column=0, sticky="e", padx=5, pady=5)
        entry = tk.Entry(self, width=30)
        entry.grid(row=row, column=1, sticky="w", padx=5, pady=5)
        setattr(self, f"{label.lower().split()[0]}_entry", entry)

    def save_session(self):
        session_type = self.session_entry.get()
        time_slot = self.time_entry.get()
        date_text = self.date_entry.get()

        try:
            date = datetime.datetime.strptime(date_text, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Invalid Date", "Please use YYYY-MM-DD format.")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER DEFAULT 1,
            session_type TEXT,
            time_slot TEXT,
            date DATE
        )
        """)

        cursor.execute("""
        INSERT INTO sessions (session_type, time_slot, date)
        VALUES (?, ?, ?)
        """, (session_type, time_slot, date))

        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Session added successfully!")
        self.destroy()

if __name__ == "__main__":
    app = SessionConfig()
    app.mainloop()
