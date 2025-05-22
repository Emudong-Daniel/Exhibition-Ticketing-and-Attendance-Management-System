import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import sys
import os
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../exhibition.db")

class SeatBookingForm(tk.Tk):
    def __init__(self, guest_id):
        super().__init__()
        self.title("Seat & Session Booking")
        self.geometry("500x350")
        self.configure(bg="#f9f9f9", padx=20, pady=20)
        self.guest_id = guest_id

        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

        tk.Label(self, text="Book Session & Seat", font=("Arial", 16, "bold"), bg="#f9f9f9").grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(self, text="Select Session:", bg="#f9f9f9", font=("Arial", 11)).grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.session_box = ttk.Combobox(self, width=30)
        self.session_box.grid(row=1, column=1, sticky="w")

        tk.Label(self, text="Select Seat:", bg="#f9f9f9", font=("Arial", 11)).grid(row=2, column=0, sticky="e", padx=10, pady=10)
        self.seat_box = ttk.Combobox(self, width=30)
        self.seat_box.grid(row=2, column=1, sticky="w")

        tk.Button(self, text="Confirm Booking", font=("Arial", 12), bg="#1d72b8", fg="white",
                  command=self.confirm_booking).grid(row=3, column=0, columnspan=2, pady=30)

        self.load_sessions()
        self.load_seats()

    def load_sessions(self):
        self.cursor.execute("SELECT session_id, session_type || ' (' || date || ')' FROM sessions")
        sessions = self.cursor.fetchall()
        self.session_map = {f"{label}": sid for sid, label in sessions}
        self.session_box['values'] = list(self.session_map.keys())

    def load_seats(self):
        self.cursor.execute("SELECT seat_id, seat_number || ' - ' || category FROM seats WHERE status = 'Available'")
        seats = self.cursor.fetchall()
        self.seat_map = {f"{label}": sid for sid, label in seats}
        self.seat_box['values'] = list(self.seat_map.keys())

    def confirm_booking(self):
        session_label = self.session_box.get()
        seat_label = self.seat_box.get()

        if not session_label or not seat_label:
            messagebox.showerror("Error", "Please select both session and seat.")
            return

        session_id = self.session_map[session_label]
        seat_id = self.seat_map[seat_label]
        ticket_id = "TKT-" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS reservations (
                    reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guest_id INTEGER,
                    session_id INTEGER,
                    seat_id INTEGER,
                    booking_time DATETIME,
                    ticket_id TEXT
                )
            """)

            self.cursor.execute("""
                INSERT INTO reservations (guest_id, session_id, seat_id, booking_time, ticket_id)
                VALUES (?, ?, ?, ?, ?)
            """, (self.guest_id, session_id, seat_id, datetime.datetime.now(), ticket_id))

            self.cursor.execute("UPDATE seats SET status = 'Booked' WHERE seat_id = ?", (seat_id,))
            self.conn.commit()

            messagebox.showinfo("Success", f"Booking confirmed! Your Ticket ID is {ticket_id}")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to book seat: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        guest_id = int(sys.argv[1])
        app = SeatBookingForm(guest_id)
        app.mainloop()
    else:
        print("Guest ID not provided.")
