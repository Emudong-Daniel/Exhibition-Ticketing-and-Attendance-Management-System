import tkinter as tk
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../exhibition.db")

class TicketConfirmation(tk.Toplevel):
    def __init__(self, reservation_id):
        super().__init__()
        self.title("Ticket Confirmation")
        self.geometry("450x300")
        self.configure(bg="#f4f4f4", padx=20, pady=20)
        self.reservation_id = reservation_id

        tk.Label(self, text="🎟️ Ticket Confirmation", font=("Arial", 16, "bold"), bg="#f4f4f4").pack(pady=10)

        self.output = tk.Text(self, height=10, width=50, bg="white", fg="black", font=("Courier", 10))
        self.output.pack(pady=10)

        self.load_ticket_info()

    def load_ticket_info(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT g.name, s.session_type, s.date, st.seat_number, r.ticket_id
        FROM reservations r
        JOIN guests g ON r.guest_id = g.guest_id
        JOIN sessions s ON r.session_id = s.session_id
        JOIN seats st ON r.seat_id = st.seat_id
        WHERE r.reservation_id = ?
        """, (self.reservation_id,))
        record = cursor.fetchone()
        conn.close()

        if record:
            guest_name, session_type, date, seat_number, ticket_id = record
            output = (
                f"Name:       {guest_name}\n"
                f"Session:    {session_type}\n"
                f"Date:       {date}\n"
                f"Seat No.:   {seat_number}\n"
                f"Ticket ID:  {ticket_id}"
            )
            self.output.insert(tk.END, output)
        else:
            self.output.insert(tk.END, "Ticket not found.")

if __name__ == "__main__":
    win = TicketConfirmation(reservation_id=1)
    win.mainloop()
