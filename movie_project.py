from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from datetime import datetime

client = MongoClient("mongodb+srv://sabari:seetharamanpoongodi@cluster0.4higtot.mongodb.net/?appName=Cluster0")
db = client["movie_ticket_booking"]
movies = db["movies"]
bookings = db["bookings"]

# Prevent duplicate Movie ID and Booking ID
movies.create_index("movie_id", unique=True)
bookings.create_index("booking_id", unique=True)


# Movie details

def add_movie():
    print("\n        ADD MOVIE         ")
    movie_id = input("Enter Movie ID: ")
    movie_name = input("Enter Movie Name: ")
    language = input("Enter Language: ")
    genre = input("Enter Genre: ")
    duration = input("Enter Duration: ")
    release_date = input("Enter Release Date: ")

    movie = {
        "movie_id": movie_id,
        "movie_name": movie_name,
        "language": language,
        "genre": genre,
        "duration": duration,
        "release_date": release_date
    }
    try:
        movies.insert_one(movie)
        print("Movie added successfully.")
    except DuplicateKeyError:
        print("Error: Movie ID already exists.")


def view_movies():
    print("\n          ALL MOVIES        ")
    movie_list = movies.find()
    found = False
    for movie in movie_list:
        found = True
        print("\nMovie ID     :", movie["movie_id"])
        print("Movie Name   :", movie["movie_name"])
        print("Language     :", movie["language"])
        print("Genre        :", movie["genre"])
        print("Duration     :", movie["duration"])
        print("Release Date :", movie["release_date"])
    if not found:
        print("No movies found.")


def search_movie():
    print("\n            SEARCH MOVIE         ")
    choice = input("Search by (1-ID / 2-Name): ")
    if choice == "1":
        movie_id = input("Enter Movie ID: ")
        movie = movies.find_one({"movie_id": movie_id})
    elif choice == "2":
        movie_name = input("Enter Movie Name: ")
        movie = movies.find_one({"movie_name": movie_name})
    else:
        print("Invalid choice.")
        return
    if movie:
        print("\nMovie Found!")
        print("Movie ID     :", movie["movie_id"])
        print("Movie Name   :", movie["movie_name"])
        print("Language     :", movie["language"])
        print("Genre        :", movie["genre"])
        print("Duration     :", movie["duration"])
        print("Release Date :", movie["release_date"])
    else:
        print("Movie not found.")


def update_movie():
    print("\n            UPDATE MOVIE         ")
    movie_id = input("Enter Movie ID to update: ")
    movie = movies.find_one({"movie_id": movie_id})
    if not movie:
        print("Movie not found.")
        return
    print("\nLeave blank if you don't want to change a field.")
    movie_name = input("New Movie Name: ")
    language = input("New Language: ")
    genre = input("New Genre: ")
    duration = input("New Duration: ")
    release_date = input("New Release Date: ")

    update_data = {}
    if movie_name != "":
        update_data["movie_name"] = movie_name
    if language != "":
        update_data["language"] = language
    if genre != "":
        update_data["genre"] = genre
    if duration != "":
        update_data["duration"] = duration
    if release_date != "":
        update_data["release_date"] = release_date
    if len(update_data) == 0:
        print("No changes made.")
        return
    movies.update_one({"movie_id": movie_id},{"$set": update_data})
    print("Movie updated successfully.")


def delete_movie():
    print("\n            DELETE MOVIE            ")
    movie_id = input("Enter Movie ID to delete: ")
    result = movies.delete_one({"movie_id": movie_id})
    if result.deleted_count > 0:
        print("Movie deleted successfully.")
    else:
        print("Movie not found.")


# Booking system

def add_booking():
    print("\n            CREATE BOOKING           ")
    booking_id = input("Enter Booking ID: ")
    customer_name = input("Enter Customer Name: ")
    phone = input("Enter Customer Phone Number: ")
    movie_id = input("Enter Movie ID: ")

    # Check whether movie exists
    movie = movies.find_one({"movie_id": movie_id})

    if not movie:
        print("Movie not found. Booking cannot be created.")
        return

    movie_name = movie["movie_name"]
    show_date = input("Enter Show Date: ")
    show_time = input("Enter Show Time: ")
    try:
        tickets = int(input("Enter Number of Tickets: "))
        if tickets <= 0:
            print("Number of tickets must be greater than zero.")
            return
    except ValueError:
        print("Please enter a valid number of tickets.")
        return

    ticket_price = 200
    total_amount = tickets * ticket_price
    booking = {
        "booking_id": booking_id,
        "customer_name": customer_name,
        "phone": phone,
        "movie_id": movie_id,
        "movie_name": movie_name,
        "show_date": show_date,
        "show_time": show_time,
        "number_of_tickets": tickets,
        "ticket_price": ticket_price,
        "total_amount": total_amount,
        "created_at": datetime.now()
    }
    try:
        bookings.insert_one(booking)
        print("\nBooking created successfully.")
        print("Movie Name    :", movie_name)
        print("Ticket Price  : ₹", ticket_price)
        print("Tickets       :", tickets)
        print("Total Amount  : ₹", total_amount)
    except DuplicateKeyError:
        print("Error: Booking ID already exists.")


def view_bookings():
    print("\n            ALL BOOKINGS         ")
    booking_list = bookings.find()
    found = False
    for booking in booking_list:
        found = True

        print("\nBooking ID        :", booking["booking_id"])
        print("Customer Name     :", booking["customer_name"])
        print("Phone             :", booking["phone"])
        print("Movie ID          :", booking["movie_id"])
        print("Movie Name        :", booking["movie_name"])
        print("Show Date         :", booking["show_date"])
        print("Show Time         :", booking["show_time"])
        print("Number of Tickets :", booking["number_of_tickets"])
        print("Total Amount      : ₹", booking["total_amount"])
    if not found:
        print("No bookings found.")


def search_booking():
    print("\n            SEARCH BOOKING           ")
    booking_id = input("Enter Booking ID: ")
    booking = bookings.find_one({"booking_id": booking_id})
    if booking:
        print("\nBooking Found!")
        print("Booking ID        :", booking["booking_id"])
        print("Customer Name     :", booking["customer_name"])
        print("Phone             :", booking["phone"])
        print("Movie ID          :", booking["movie_id"])
        print("Movie Name        :", booking["movie_name"])
        print("Show Date         :", booking["show_date"])
        print("Show Time         :", booking["show_time"])
        print("Number of Tickets :", booking["number_of_tickets"])
        print("Total Amount      : ₹", booking["total_amount"])
    else:
        print("Booking not found.")


def update_booking():
    print("\n            UPDATE BOOKING           ")
    booking_id = input("Enter Booking ID to update: ")
    booking = bookings.find_one({"booking_id": booking_id})
    if not booking:
        print("Booking not found.")
        return
    print("\nLeave blank if you don't want to change a field.")
    customer_name = input("New Customer Name: ")
    phone = input("New Phone Number: ")
    show_date = input("New Show Date: ")
    show_time = input("New Show Time: ")
    ticket_input = input("New Number of Tickets: ")
    
    update_data = {}

    if customer_name != "":
        update_data["customer_name"] = customer_name
    if phone != "":
        update_data["phone"] = phone
    if show_date != "":
        update_data["show_date"] = show_date
    if show_time != "":
        update_data["show_time"] = show_time

    # Update ticket count and calculate amount
    if ticket_input != "":
        try:
            tickets = int(ticket_input)
            if tickets <= 0:
                print("Number of tickets must be greater than zero.")
                return
            ticket_price = 200
            total_amount = tickets * ticket_price
            update_data["number_of_tickets"] = tickets
            update_data["total_amount"] = total_amount
        except ValueError:
            print("Please enter a valid number.")
            return
    if len(update_data) == 0:
        print("No changes made.")
        return
    bookings.update_one({"booking_id": booking_id},{"$set": update_data})
    print("Booking updated successfully.")


def delete_booking():
    print("\n            CANCEL BOOKING           ")
    booking_id = input("Enter Booking ID to cancel: ")
    result = bookings.delete_one({"booking_id": booking_id})
    if result.deleted_count > 0:
        print("Booking cancelled successfully.")
    else:
        print("Booking not found.")


# Movies lists

def movie_menu():
    while True:
        print("\n            MOVIE MANAGEMENT            ")
        print("1. Add Movie")
        print("2. View All Movies")
        print("3. Search Movie")
        print("4. Update Movie")
        print("5. Delete Movie")
        print("6. Back")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_movie()
        elif choice == "2":
            view_movies()
        elif choice == "3":
            search_movie()
        elif choice == "4":
            update_movie()
        elif choice == "5":
            delete_movie()
        elif choice == "6":
            break
        else:
            print("Invalid choice.")


# Booking lists

def booking_menu():

    while True:

        print("\n            BOOKING MANAGEMENT          ")
        print("1. Create Booking")
        print("2. View All Bookings")
        print("3. Search Booking")
        print("4. Update Booking")
        print("5. Cancel Booking")
        print("6. Back")
        choice = input("Enter your choice: ")
        if choice == "1":
            add_booking()
        elif choice == "2":
            view_bookings()
        elif choice == "3":
            search_booking()
        elif choice == "4":
            update_booking()
        elif choice == "5":
            delete_booking()
        elif choice == "6":
            break
        else:
            print("Invalid choice.")


# MAIN PROGRAM

while True:

    print("\n")
    print("           MOVIE TICKET BOOKING SYSTEM      ")
    print("1. Movie Management")
    print("2. Ticket Booking Management")
    print("3. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        movie_menu()
    elif choice == "2":
        booking_menu()
    elif choice == "3":
        print("Thank you for using Movie Ticket Booking System.")
        break
    else:
        print("Invalid choice.")