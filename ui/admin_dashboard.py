import tkinter as tk
import sqlite3
import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../exhibition.db")
SESSION_CONFIG_PATH = os.path.join(BASE_DIR, "session_config.py")
SEAT_CONFIG_PATH = os.path.join(BASE_DIR, "seat_config.py")

class AdminDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Admin Dashboard")
        self.geometry("700x600")
        self.configure(bg="#f4f4f4", padx=20, pady=20)

        tk.Label(self, text="📊 Admin Dashboard", font=("Arial", 16, "bold"), bg="#f4f4f4").pack(pady=10)

        btn_style = {"font": ("Arial", 11), "bg": "#1d72b8", "fg": "white", "padx": 10, "pady": 5}

        tk.Button(self, text="View Reserved Seats Per Session", command=self.view_seats, **btn_style).pack(pady=10)
        tk.Button(self, text="View Guest Attendance", command=self.view_attendance, **btn_style).pack(pady=10)
        tk.Button(self, text="Manage Sessions", command=self.open_session_config, **btn_style).pack(pady=10)
        tk.Button(self, text="Manage Seats", command=self.open_seat_config, **btn_style).pack(pady=10)

        self.output = tk.Text(self, height=20, width=85, font=("Courier", 10), bg="white", fg="black")
        self.output.pack(pady=20)

    def view_seats(self):
        self.output.delete("1.0", tk.END)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT s.session_type, s.date, g.name, st.seat_number, r.ticket_id
        FROM reservations r
        JOIN guests g ON r.guest_id = g.guest_id
        JOIN sessions s ON r.session_id = s.session_id
        JOIN seats st ON r.seat_id = st.seat_id
        ORDER BY s.date
        """)
        rows = cursor.fetchall()
        conn.close()

        if rows:
            for row in rows:
                self.output.insert(tk.END, f"Session: {row[0]} on {row[1]}\nGuest: {row[2]} | Seat: {row[3]} | Ticket: {row[4]}\n\n")
        else:
            self.output.insert(tk.END, "No reservations found.")

    def view_attendance(self):
        self.output.delete("1.0", tk.END)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT g.name, COUNT(r.reservation_id) as sessions_attended
        FROM guests g
        LEFT JOIN reservations r ON g.guest_id = r.guest_id
        GROUP BY g.guest_id
        ORDER BY sessions_attended DESC
        """)
        rows = cursor.fetchall()
        conn.close()

        if rows:
            for row in rows:
                self.output.insert(tk.END, f"{row[0]} attended {row[1]} session(s)\n")
        else:
            self.output.insert(tk.END, "No guest data available.")

    def open_session_config(self):
        subprocess.Popen([sys.executable, SESSION_CONFIG_PATH])

    def open_seat_config(self):
        subprocess.Popen([sys.executable, SEAT_CONFIG_PATH])

if __name__ == "__main__":
    app = AdminDashboard()
    app.mainloop()
