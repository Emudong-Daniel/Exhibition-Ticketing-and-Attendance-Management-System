# Exhibition Ticket and Attendance Management System

A user-friendly desktop application built with **Python**, **SQLite**, and **Tkinter** to manage event guest registration, session and seat bookings, ticket confirmation, and administrative reporting.

> Developed as part of the **Systems Analysis and Design (1201 FST)** coursework at **Victoria University**.

---

##  Features

- ✅ Guest Registration Form
- ✅ Seat and Session Booking with live seat availability
- ✅ Auto-generated Ticket IDs
- ✅ Ticket Confirmation Screen
- ✅ Admin Login with access controls
- ✅ Admin Dashboard:
  - View Reserved Seats Per Session
  - View Guest Attendance
  - Manage Sessions (Add/Edit)
  - Manage Seats (Add/Edit)

---

##  Technologies Used

- **Python 3.x**
- **Tkinter** (GUI)
- **SQLite** (Database)
- **Standard Library Only** (No external dependencies)

---

## Getting Started

1. **Clone or download** the repository
2. Open the project in **Visual Studio Code** or any Python IDE
3. Run the application:

```bash
python main.py
```

4. To access the Admin Dashboard:

```bash
python ui/admin_login.py
```

Default Admin Credentials:
- Username: `admin`
- Password: `admin123`

---

## Author

**Emudong Daniel William**  
Registration No: `VU-BCS-2311-0464-EVE`  
Victoria University  
17th May 2025

---

## Project Structure

```
ExhibitionTAMIS/
│
├── main.py
├── exhibition.db
├── ui/
│   ├── guest_form.py
│   ├── seat_booking_form.py
│   ├── ticket_confirmation.py
│   ├── admin_login.py
│   ├── admin_dashboard.py
│   ├── session_config.py
│   └── seat_config.py
└── README.md
```
