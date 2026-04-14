import os
import pandas as pd
import matplotlib.pyplot as plt
from booking import get_all_bookings

def export_bookings_to_csv():
    bookings = get_all_bookings()

    data = []
    for booking in bookings:
        data.append({
            "Booking ID": booking[0],
            "User ID": booking[1],
            "Session ID": booking[2],
            "Seat Number": booking[3],
            "Booking Date": booking[4],
            "Total Price": booking[5]
        })

    df = pd.DataFrame(data)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "bookings_report.csv")

    df.to_csv(file_path, index=False)
    return file_path

def show_booking_chart():
    bookings = get_all_bookings()

    if not bookings:
        return False

    seat_counts = {}

    for booking in bookings:
        seat = booking[3]
        seat_counts[seat] = seat_counts.get(seat, 0) + 1

    x = list(seat_counts.keys())
    y = list(seat_counts.values())

    plt.figure(figsize=(8, 5))
    plt.bar(x, y)
    plt.title("Booking Count by Seat")
    plt.xlabel("Seat Number")
    plt.ylabel("Number of Bookings")
    plt.tight_layout()
    plt.show()

    return True