import streamlit as st
import pandas as pd
import json
import os

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'password' not in st.session_state:
    st.session_state.password = ''
if 'users' not in st.session_state:
    st.session_state.users = {}
if 'buses' not in st.session_state:
    st.session_state.buses = []
if 'bookings' not in st.session_state:
    st.session_state.bookings = {}

# Load users from file
def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    else:
        return {}

# Save users to file
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)

# Registration
def register():
    st.title("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Register"):
        if password == confirm_password:
            users = load_users()
            if username not in users:
                users[username] = password
                save_users(users)
                st.success("Registration successful!")
            else:
                st.error("Username already exists")
        else:
            st.error("Passwords do not match")

# Login
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        users = load_users()
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")

# Main app
def main():
    # Create sidebar
    option = st.sidebar.selectbox("Choose an option", ["Add Bus", "Delete Bus", "View Bus", "Search Bus", "Edit Bus", "Book a Seat", "Cancel Booking", "View Bookings"])

    # Add Bus
    if option == "Add Bus":
        bus_number = st.text_input('Bus Number')
        route = st.text_input('Route')
        capacity = st.number_input('Capacity', min_value=0, step=1)
        available_seats = st.number_input('Available Seats', min_value=0, step=1)

        if st.button('Add Bus'):
            for bus in st.session_state.buses:
                if bus["bus_number"] == bus_number:
                    st.error("Bus number already exists")
                    break
            else:
                st.session_state.buses.append({
                    'bus_number': bus_number,
                    'route': route,
                    'capacity': capacity,
                    'available_seats': available_seats
                })
                st.write("Bus added successfully!")

    # Delete Bus
    elif option == "Delete Bus":
        st.write("Select a bus to delete:")
        bus_numbers = [bus['bus_number'] for bus in st.session_state.buses]
        bus_to_delete = st.selectbox("Bus Number", bus_numbers, key='delete_bus')
        if st.button('Delete Bus'):
            st.session_state.buses = [bus for bus in st.session_state.buses if bus['bus_number'] != bus_to_delete]

    # View Bus
    elif option == "View Bus":
        st.session_state.buses = sorted(st.session_state.buses, key=lambda x: x["bus_number"])
        df = pd.DataFrame(st.session_state.buses)
        st.write(df)

    # Search Bus
    elif option == "Search Bus":
        text_search = st.text_input("Search buses by route or bus number", value="")

        if text_search:
            search_results = [bus for bus in st.session_state.buses if text_search in bus['route'] or text_search in bus['bus_number']]
            if search_results:
                df = pd.DataFrame(search_results)
                st.write(df)
            else:
                st.write("Bus not found!")

    # Edit Bus
    elif option == "Edit Bus":
        st.write("Select a bus to edit:")
        bus_numbers = [bus['bus_number'] for bus in st.session_state.buses]
        bus_to_edit = st.selectbox("Bus Number", bus_numbers, key='edit_bus')
        bus_index = [i for i, bus in enumerate(st.session_state.buses) if bus['bus_number'] == bus_to_edit][0]

        new_bus_number = st.text_input('New Bus Number', value=st.session_state.buses[bus_index]['bus_number'])
        new_route = st.text_input('New Route', value=st.session_state.buses[bus_index]['route'])
        new_capacity = st.number_input('New Capacity', min_value=0, step=1, value=st.session_state.buses[bus_index]['capacity'])
        new_available_seats = st.number_input('New Available Seats', min_value=0, step=1, value=st.session_state.buses[bus_index]['available_seats'])

        if st.button('Edit Bus'):
            st.session_state.buses[bus_index]['bus_number'] = new_bus_number
            st.session_state.buses[bus_index]['route'] = new_route
            st.session_state.buses[bus_index]['capacity'] = new_capacity
            st.session_state.buses[bus_index]['available_seats'] = new_available_seats

    # Book a Seat
    elif option == "Book a Seat":
        st.write("Select a bus to book a seat:")
        bus_numbers = [bus['bus_number'] for bus in st.session_state.buses]
        bus_to_book = st.selectbox("Bus Number", bus_numbers, key='book_bus')
        bus_index = [i for i, bus in enumerate(st.session_state.buses) if bus['bus_number'] == bus_to_book][0]

        if st.button('Book a Seat'):
            if st.session_state.buses[bus_index]["available_seats"] > 0:
                st.session_state.buses[bus_index]["available_seats"] -= 1
                if bus_to_book not in st.session_state.bookings:
                    st.session_state.bookings[bus_to_book] = 1
                else:
                    st.session_state.bookings[bus_to_book] += 1
                st.write("Seat booked successfully!")
            else:
                st.error("No available seats on this bus")

    # Cancel Booking
    elif option == "Cancel Booking":
        st.write("Select a bus to cancel a booking:")
        bus_numbers = [bus['bus_number'] for bus in st.session_state.buses]
        bus_to_cancel = st.selectbox("Bus Number", bus_numbers, key='cancel_bus')
        bus_index = [i for i, bus in enumerate(st.session_state.buses) if bus['bus_number'] == bus_to_cancel][0]

        if st.button('Cancel Booking'):
            if bus_to_cancel in st.session_state.bookings:
                st.session_state.buses[bus_index]["available_seats"] += 1
                st.session_state.bookings[bus_to_cancel] -= 1
                if st.session_state.bookings[bus_to_cancel] == 0:
                    del st.session_state.bookings[bus_to_cancel]
                st.write("Booking cancelled successfully!")
            else:
                st.error("No bookings on this bus")

    # View Bookings
    elif option == "View Bookings":
        df = pd.DataFrame({'Bus Number': list(st.session_state.bookings.keys()), 'Number of Bookings': list(st.session_state.bookings.values())})
        st.write(df)

        # Add a button to download the bookings as a CSV file
        @st.cache
        def convert_df(df):
            return df.to_csv().encode('utf-8')

        csv = convert_df(df)

        st.download_button(
            label="Download Bookings as CSV",
            data=csv,
            file_name='bookings.csv',
            mime='text/csv'
        )

# Check if user is logged in
if st.session_state.logged_in:
    main()
else:
    login_page = st.selectbox("Choose an option", ["Login", "Register"])
    if login_page == "Login":
        login()
    elif login_page == "Register":
        register()