import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../exhibition.db")

class SeatConfig(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Configure Seats")
        self.geometry("400x300")
        self.configure(bg="#f9f9f9", padx=20, pady=20)

        tk.Label(self, text="Add New Seat", font=("Arial", 14, "bold"), bg="#f9f9f9").grid(row=0, column=0, columnspan=2, pady=10)

        self.build_label_entry("Seat Number", 1)
        self.build_label_entry("Category", 2)
        self.build_label_entry("Price", 3)

        tk.Button(self, text="Save Seat", bg="#1d72b8", fg="white", font=("Arial", 11),
                  command=self.save_seat).grid(row=4, column=0, columnspan=2, pady=20)

    def build_label_entry(self, label, row):
        tk.Label(self, text=label + ":", bg="#f9f9f9", font=("Arial", 10)).grid(row=row, column=0, sticky="e", padx=5, pady=5)
        entry = tk.Entry(self, width=30)
        entry.grid(row=row, column=1, sticky="w", padx=5, pady=5)
        setattr(self, f"{label.lower().split()[0]}_entry", entry)

    def save_seat(self):
        seat_number = self.seat_entry.get()
        category = self.category_entry.get()
        price = self.price_entry.get()

        if not seat_number or not category or not price:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            price = float(price)
        except ValueError:
            messagebox.showerror("Invalid Price", "Please enter a valid number.")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS seats (
            seat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            price REAL,
            seat_number TEXT,
            status TEXT DEFAULT 'Available'
        )
        """)

        cursor.execute("""
        INSERT INTO seats (category, price, seat_number, status)
        VALUES (?, ?, ?, 'Available')
        """, (category, price, seat_number))

        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Seat added successfully!")
        self.destroy()

if __name__ == "__main__":
    app = SeatConfig()
    app.mainloop()
