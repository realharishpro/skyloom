# Flight Booking System

The Flight Booking System is a web application that allows users to search for flights, book tickets, and manage their bookings. It provides a user-friendly interface for users to browse available flights, select their preferred flights, and make secure online bookings. The system also includes an admin dashboard for managing flights, user accounts, and bookings.

## Features

- User Registration and Authentication: Users can create accounts, log in, and manage their bookings.
- Flight Search and Booking: Users can search for flights based on various criteria such as destination, date, and number of passengers. They can select flights, view flight details, and book tickets.
- Booking Management: Users can view their bookings, check booking details, and manage their reservations.
- Admin Dashboard: Admin users have access to a dashboard where they can manage flights, user accounts, and bookings. They can add new flights, edit existing flights, and remove flights if needed.
- Passenger Details: Users can enter passenger details during the booking process, including name, age, and gender.
- PNR Generation: Each booking is assigned a unique PNR (Passenger Name Record) number for identification and reference.

## Technologies Used

- Python
- Flask (Web Framework)
- SQLAlchemy (ORM)
- HTML/CSS
- Bootstrap (Front-end Framework)
- PostgreSQL (Database)
- JavaScript (Optional, for additional functionality)

## Installation and Usage

1. Clone the repository: `git clone https://github.com/skyloom/skyloom.git`
2. Create and activate a virtual environment:
   - On Windows:
     ```
     python -m venv venv
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```
3. Install dependencies: `pip install -r requirements.txt`
4. Set up the database: Create a PostgreSQL database and update the database URI in the configuration file.
5. Run the application: `python app.py`
6. Access the application in a web browser at `http://localhost:8000`

## Demo Account

To explore the features of the Flight Booking System, you can use the following demo account:
http://103.14.123.98:8000/
### User
- Username: user1
- Password: user1@123
### Admin
- Username: admin
- Password: adminpassword

## Contributing

Contributions are welcome! If you would like to contribute to this project, please fork the repository and create a new branch for your feature or bug fix. Submit a pull request with your changes, and they will be reviewed and merged.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
