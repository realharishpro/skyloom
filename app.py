from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import random
import string
import datetime
def generate_pnr_number():
    # Generate a random string of alphanumeric characters
    characters = string.ascii_uppercase + string.digits
    pnr_number = ''.join(random.choices(characters, k=8))
    
    return pnr_number

app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.static_folder = 'assets'
# PostgreSQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dbuser:dbpass@localhost/dbname'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, default=0.00)  # New field for user's balance

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email



# Flight model
class Flight(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    from_location = db.Column(db.String(100), nullable=False)
    to_location = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(100), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    seats = db.Column(db.Integer, nullable=False)

    def __init__(self, name, from_location, to_location, duration, datetime, cost, seats):
        self.name = name
        self.from_location = from_location
        self.to_location = to_location
        self.duration = duration
        self.datetime = datetime
        self.cost = cost
        self.seats = seats

# Booking model
class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    pnr_number = db.Column(db.String(50), nullable=False, unique=True)

    user = db.relationship('User', backref='bookings')
    flight = db.relationship('Flight', backref='bookings')

# Passenger model
class Passenger(db.Model):
    __tablename__ = 'passengers'
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)

    booking = db.relationship('Booking', backref='passengers')

    def __init__(self, booking_id, name, age, gender):
        self.booking_id = booking_id
        self.name = name
        self.age = age
        self.gender = gender

@app.route('/book_ticket', methods=['POST'])
def book_ticket():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)

        # Retrieve flight information from the form
        flight_id = int(request.form['flight_id'])
        ticket_count = int(request.form['ticket_count'])
        flight = Flight.query.get(flight_id)

        # Retrieve passenger details from the form
        passenger_name = request.form['passenger_name']
        passenger_age = int(request.form['passenger_age'])
        passenger_gender = request.form['passenger_gender']

        # Retrieve ticket count from the session
        ticket_count = session.get('ticket_count')

        if user and flight and ticket_count is not None:
            total_cost = flight.cost * ticket_count
            if user.balance >= total_cost:
                # Deduct the total cost from the user's balance
                user.balance -= total_cost

                # Generate a unique PNR number
                pnr_number = generate_pnr_number()

                # Create a new booking record
                booking = Booking(user_id=user.id, flight_id=flight.id, amount_paid=total_cost, pnr_number=pnr_number)
                db.session.add(booking)
                db.session.commit()

                # Create a new passenger record
                passenger = Passenger(booking_id=booking.id, name=passenger_name, age=passenger_age, gender=passenger_gender)
                db.session.add(passenger)
                db.session.commit()
                content = 'Tickets booked successfully! PNR Number: {}'.format(pnr_number)

                return render_template('blank.html', content=content)
            else:
                content =  'Insufficient balance.'
                return render_template('blank.html', content=content)
        else:
            content = 'Invalid user, flight, or ticket count.'
            return render_template('blank.html', content=content)
    else:
        return redirect('/signin')

@app.route('/passenger_details', methods=['GET', 'POST'])
def passenger_details():
    if 'user_id' in session:
        if request.method == 'POST':
            # Retrieve flight and user information from the session
            flight_id = session.get('flight_id')
            ticket_count = session.get('ticket_count')
            print("TI: ",ticket_count)
            user_id = session.get('user_id')

            # Retrieve passenger details from the form
            passenger_name = request.form['passenger_name']
            passenger_age = int(request.form['passenger_age'])
            passenger_gender = request.form['passenger_gender']

            # Retrieve flight and user objects from the database
            flight = Flight.query.get(flight_id)
            user = User.query.get(user_id)

            if flight and user:
                # Calculate the total cost based on the number of passengers
                ticket_count = int(ticket_count)
                total_cost = flight.cost * ticket_count

                # Check if the user has sufficient balance for the booking
                if user.balance >= total_cost:
                    # Deduct the total cost from the user's balance
                    user.balance -= total_cost

                    # Generate a unique PNR number
                    pnr_number = generate_pnr_number()

                    # Create a new booking record
                    booking = Booking(
                        user_id=user.id,
                        flight_id=flight.id,
                        amount_paid=total_cost,
                        pnr_number=pnr_number
                    )
                    db.session.add(booking)
                    db.session.commit()

                    # Create a new passenger record
                    passenger = Passenger(
                        booking_id=booking.id,  # Assign the booking_id value
                        name=passenger_name,
                        age=passenger_age,
                        gender=passenger_gender
                    )
                    db.session.add(passenger)
                    db.session.commit()

                    content = 'Tickets booked successfully! PNR Number: {}'.format(pnr_number)
                    return render_template('blank.html', content=content)
                else:
                    content = 'Insufficient balance.'
                    return render_template('blank.html', content=content)
            else:
                content = 'Invalid flight or user.'
                return render_template('blank.html', content=content)
        else:
            # Retrieve flight information from the query parameters
            flight_id = request.args.get('flight_id')
            ticket_count = request.args.get('ticket_count')

            if flight_id is not None:
                # Store flight ID in the sessionticket_count
                session['flight_id'] = int(flight_id)
                session['ticket_count'] = int(ticket_count)

                return render_template('passenger_details.html', flight_id=int(flight_id),ticket_count=int(ticket_count))
            else:
                return redirect('/dashboard')
    else:
        return redirect('/signin')



# Create database tables
with app.app_context():
    db.create_all()

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Routes for signup, signin, and admin login
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if the username already exists
        if User.query.filter_by(username=username).first():
            content =  'Username already exists. Please choose a different username.'
            return render_template('blank.html', content=content)

        # Create a new user instance and add it to the database
        new_user = User(username=username, password=password, email=email)

        db.session.add(new_user)
        db.session.commit()

        return redirect('/dashboard')

    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists in the database
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['username'] = username
            session['user_id'] = user.id
            return redirect('/dashboard')
        else:
            content = 'Invalid username or password.'
            return render_template('blank.html', content=content)

    return render_template('signin.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username != 'admin' or password != 'adminpassword':
            content = 'Invalid admin credentials.'
            return render_template('blank.html', content=content)

        session['admin'] = True
        return redirect('/admin/dashboard')

    return render_template('admin_login.html')

# Protected dashboard routes for regular users and admin
@app.route('/dashboard', methods=['GET', 'POST'])
def user_dashboard():
    locations = Flight.query.with_entities(Flight.from_location).distinct().all()
    from_locations = [location[0] for location in locations]
    print(from_locations)
    locations = ['Chennai', 'Mumbai', 'Bangalore', 'Delhi', 'Kolkata', 'Pune', 'Jaipur', 'Cochin', 'Madurai']
    random.shuffle(locations)
    locations2 = ['Mumbai', 'Bangalore', 'Chennai', 'Delhi', 'Kolkata', 'Pune', 'Jaipur', 'Cochin', 'Madurai']
    random.shuffle(locations2)
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        bookings = Booking.query.filter_by(user_id=user_id).all()
        flights = Flight.query.all()
        try:
            if request.method == 'POST':
                amount = float(request.form['amount'])
                user.balance += amount
                db.session.commit()
        except:
            pass
        try:
            if request.method == 'POST':
                # Retrieve form inputs
                from_location = request.form['from_location']
                to_location = request.form['to_location']
                num_passengers = int(request.form['num_passengers'])
                dates = request.form['date']
                date_object = datetime.datetime.strptime(dates, "%m/%d/%Y")
                formatted_date = date_object.strftime("%Y-%m-%d")
                print(formatted_date)
                # Perform flight filtering based on inputs
                flights = Flight.query.filter(
                    Flight.from_location == from_location,
                    Flight.to_location == to_location,
                    Flight.seats >= num_passengers
                ).all()
        except:
            pass
        print(flights)
        return render_template('dashboard.html', user=user, flights=flights, bookings=bookings, locations=locations, locations2=locations2)
    else:
        return redirect('/signin')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect('/admin')

    users = User.query.all()
    flights = Flight.query.all()
    bookings = Booking.query.all()
    total_booking_fund = db.session.query(db.func.sum(Booking.amount_paid)).scalar()

    return render_template('admin_dashboard.html', users=users, flights=flights, total_funds=total_booking_fund,bookings=bookings)

@app.route('/admin/add-flight', methods=['GET', 'POST'])
def add_flight():
    if 'admin' not in session:
        return redirect('/admin')

    if request.method == 'POST':
        # Retrieve form inputs
        name = request.form['name']
        from_location = request.form['from_location']
        to_location = request.form['to_location']
        duration = request.form['duration']
        datetime = request.form['datetime']
        cost = float(request.form['cost'])
        seats = int(request.form['seats'])

        # Create a new Flight instance
        new_flight = Flight(name=name, from_location=from_location, to_location=to_location,
                            duration=duration, datetime=datetime, cost=cost, seats=seats)

        # Add the new flight to the database
        db.session.add(new_flight)
        db.session.commit()

        return redirect('/admin/dashboard')

    return render_template('add_flight.html')

@app.route('/admin/edit-flight/<int:flight_id>', methods=['GET', 'POST'])
def edit_flight(flight_id):
    if 'admin' not in session:
        return redirect('/admin')

    flight = Flight.query.get(flight_id)
    if not flight:
        content = 'Flight not found.'
        return render_template('blank.html', content=content)

    if request.method == 'POST':
        # Retrieve form inputs
        flight.name = request.form['name']
        flight.from_location = request.form['from_location']
        flight.to_location = request.form['to_location']
        flight.duration = request.form['duration']
        flight.datetime = request.form['datetime']
        flight.cost = float(request.form['cost'])
        flight.seats = int(request.form['seats'])

        # Update the flight in the database
        db.session.commit()

        return redirect('/admin/dashboard')

    return render_template('edit_flight.html', flight=flight)

@app.route('/admin/remove-flight/<int:flight_id>')
def remove_flight(flight_id):
    if 'admin' not in session:
        return redirect('/admin')

    flight = Flight.query.get(flight_id)
    if not flight:
        content = 'Flight not found.'
        return render_template('blank.html', content=content)

    # Remove the flight from the database
    db.session.delete(flight)
    db.session.commit()

    return redirect('/admin/dashboard')

@app.template_filter('float_to_str')
def float_to_str(value):
    str_value = str(value)  # Convert float to string
    sliced_str = str_value+"0"  # Perform string slicing as needed
    return sliced_str

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/signin')


if __name__ == '__main__':
    app.run(debug=True, port=8000)
