import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from auth import login_user, register_user
from movie import get_movies, add_movie
from booking import add_booking, get_user_bookings, get_all_bookings
from report import export_bookings_to_csv, show_booking_chart

current_user = None

def open_admin_panel(user):
    admin_window = tk.Toplevel(window)
    admin_window.title("Admin Panel")
    admin_window.geometry("500x500")

    tk.Label(admin_window, text=f"Welcome Admin: {user[1]}", font=("Arial", 14)).pack(pady=10)

    tk.Label(admin_window, text="Add Movie", font=("Arial", 12)).pack(pady=10)

    tk.Label(admin_window, text="Title").pack()
    title_entry = tk.Entry(admin_window, width=30)
    title_entry.pack(pady=5)

    tk.Label(admin_window, text="Genre").pack()
    genre_entry = tk.Entry(admin_window, width=30)
    genre_entry.pack(pady=5)

    tk.Label(admin_window, text="Duration").pack()
    duration_entry = tk.Entry(admin_window, width=30)
    duration_entry.pack(pady=5)

    tk.Label(admin_window, text="Age Limit").pack()
    age_limit_entry = tk.Entry(admin_window, width=30)
    age_limit_entry.pack(pady=5)

    def export_csv():
        file_path = export_bookings_to_csv()
        messagebox.showinfo("CSV Export", f"Report saved:\n{file_path}")

    def show_chart():
        success = show_booking_chart()
        if not success:
            messagebox.showerror("Chart", "No bookings available for chart")

    tk.Button(admin_window, text="Export Bookings CSV", command=export_csv).pack(pady=10)
    tk.Button(admin_window, text="Show Booking Chart", command=show_chart).pack(pady=10)

    def save_movie():
        title = title_entry.get()
        genre = genre_entry.get()
        duration = duration_entry.get()
        age_limit = age_limit_entry.get()

        if title == "" or genre == "" or duration == "" or age_limit == "":
            messagebox.showerror("Error", "Please fill all fields")
            return

        add_movie(title, genre, int(duration), age_limit)
        messagebox.showinfo("Success", "Movie added successfully!")

    tk.Button(admin_window, text="Add Movie", command=save_movie).pack(pady=10)

    def show_all_bookings():
        bookings_window = tk.Toplevel(admin_window)
        bookings_window.title("All Bookings")
        bookings_window.geometry("500x400")

        tk.Label(bookings_window, text="All Bookings", font=("Arial", 14)).pack(pady=10)

        bookings = get_all_bookings()

        if not bookings:
            tk.Label(bookings_window, text="No bookings yet").pack()
            return

        for booking in bookings:
            booking_text = f"User ID: {booking[1]} | Seat: {booking[3]} | Date: {booking[4]} | Price: {booking[5]} TL"
            tk.Label(bookings_window, text=booking_text).pack(pady=5)

    tk.Button(admin_window, text="View All Bookings", command=show_all_bookings).pack(pady=20)

def open_seat_screen(movie, session):
    seat_window = tk.Toplevel(window)
    seat_window.title("Seat Selection")
    seat_window.geometry("450x500")

    tk.Label(seat_window, text=f"{movie[1]} - {session}", font=("Arial", 14)).pack(pady=10)

    selected_seats = []

    def select_seat(seat):
        if seat in selected_seats:
            selected_seats.remove(seat)
            messagebox.showinfo("Seat", f"{seat} removed")
        else:
            selected_seats.append(seat)
            messagebox.showinfo("Seat", f"{seat} selected")

    seat_frame = tk.Frame(seat_window)
    seat_frame.pack(pady=20)

    for i in range(3):
        for j in range(4):
            seat_number = f"{chr(65+i)}{j+1}"

            tk.Button(
                seat_frame,
                text=seat_number,
                width=5,
                command=lambda s=seat_number: select_seat(s)
            ).grid(row=i, column=j, padx=5, pady=5)

    def confirm_booking():
        if not selected_seats:
            messagebox.showerror("Error", "Please select at least one seat")
            return

        for seat in selected_seats:
            add_booking(
                current_user[0],
                seat,
                datetime.now().strftime("%Y-%m-%d"),
                180
            )

        messagebox.showinfo("Success", f"Booking confirmed for seats: {', '.join(selected_seats)}")
        seat_window.destroy()

    tk.Button(
        seat_window,
        text="Confirm Booking",
        command=confirm_booking
    ).pack(pady=20)

def open_session_screen(movie):
    session_window = tk.Toplevel(window)
    session_window.title("Sessions")
    session_window.geometry("400x300")

    tk.Label(session_window, text=f"{movie[1]} Sessions", font=("Arial", 14)).pack(pady=10)

    sessions = [
    "10:00 - 2D",
    "13:00 - 3D",
    "16:00 - 2D",
    "20:00 - 3D"
]

    def select_session(session):
        open_seat_screen(movie, session)

    for session in sessions:
        frame = tk.Frame(session_window)
        frame.pack(pady=5)

        tk.Label(frame, text=session, width=10).pack(side="left", padx=10)

        tk.Button(
            frame,
            text="Select",
            command=lambda s=session: select_session(s)
        ).pack(side="right")

def open_bookings_screen():
    bookings_window = tk.Toplevel(window)
    bookings_window.title("My Bookings")
    bookings_window.geometry("500x400")

    tk.Label(bookings_window, text="My Bookings", font=("Arial", 14)).pack(pady=10)

    bookings = get_user_bookings(current_user[0])

    if not bookings:
        tk.Label(bookings_window, text="No bookings yet").pack()
        return

    total = 0
    for booking in bookings:
        total += booking[5]

    tk.Label(
        bookings_window,
        text=f"Total Spent: {total} TL",
        font=("Arial", 12, "bold")
    ).pack(pady=10)

    tk.Label(
        bookings_window,
        text=f"Total Bookings: {len(bookings)}",
        font=("Arial", 12)
    ).pack()

    for booking in bookings:
        booking_text = f"Seat: {booking[3]} | Date: {booking[4]} | Price: {booking[5]} TL"
        tk.Label(bookings_window, text=booking_text).pack(pady=5)

def open_movie_screen(user):
    global current_user
    current_user = user

    movie_window = tk.Toplevel(window)
    movie_window.title("Movies")
    movie_window.geometry("550x450")

    tk.Label(movie_window, text=f"Welcome {user[1]}", font=("Arial", 14)).pack(pady=10)

    tk.Button(
        movie_window,
        text="My Bookings",
        command=open_bookings_screen
    ).pack(pady=10)

    movies = get_movies()

    if not movies:
        tk.Label(movie_window, text="No movies available").pack()
        return

    def select_movie(movie):
        open_session_screen(movie)

    for movie in movies:
        frame = tk.Frame(movie_window)
        frame.pack(pady=5)

        movie_text = f"{movie[1]} - {movie[2]} - {movie[3]} min"
        tk.Label(frame, text=movie_text, width=30, anchor="w").pack(side="left", padx=10)

        tk.Button(
            frame,
            text="Select",
            command=lambda m=movie: select_movie(m)
        ).pack(side="right")

def login():
    email = email_entry.get()
    password = password_entry.get()

    user = login_user(email, password)

    if user:
        if user[4] == "admin":
            open_admin_panel(user)
        else:
            open_movie_screen(user)
    else:
        messagebox.showerror("Error", "Invalid email or password")

def open_register_window():
    register_window = tk.Toplevel(window)
    register_window.title("Register")
    register_window.geometry("400x350")

    tk.Label(register_window, text="Register Screen", font=("Arial", 16)).pack(pady=20)

    tk.Label(register_window, text="Full Name").pack()
    full_name_entry = tk.Entry(register_window, width=30)
    full_name_entry.pack(pady=5)

    tk.Label(register_window, text="Email").pack()
    reg_email_entry = tk.Entry(register_window, width=30)
    reg_email_entry.pack(pady=5)

    tk.Label(register_window, text="Password").pack()
    reg_password_entry = tk.Entry(register_window, width=30, show="*")
    reg_password_entry.pack(pady=5)

    def register():
        full_name = full_name_entry.get()
        email = reg_email_entry.get()
        password = reg_password_entry.get()

        if full_name == "" or email == "" or password == "":
            messagebox.showerror("Error", "Please fill all fields")
            return

        register_user(full_name, email, password)
        messagebox.showinfo("Success", "User registered successfully!")
        register_window.destroy()

    tk.Button(register_window, text="Register", command=register).pack(pady=20)

window = tk.Tk()
window.title("Cinema Ticket Booking System")
window.geometry("400x300")

tk.Label(window, text="Login Screen", font=("Arial", 16)).pack(pady=20)

tk.Label(window, text="Email").pack()
email_entry = tk.Entry(window, width=30)
email_entry.pack(pady=5)

tk.Label(window, text="Password").pack()
password_entry = tk.Entry(window, width=30, show="*")
password_entry.pack(pady=5)

tk.Button(window, text="Login", command=login).pack(pady=10)
tk.Button(window, text="Register", command=open_register_window).pack()

window.mainloop()