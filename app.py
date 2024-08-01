import streamlit as st
import pandas as pd

# Initialize session state
if 'buses' not in st.session_state:
    st.session_state.buses = []

# Create sidebar
option = st.sidebar.selectbox("Choose an option", ["Add Bus", "Delete Bus", "View Bus", "Search Bus"])

# Add Bus
if option == "Add Bus":
    bus_number = st.text_input('Bus Number')
    route = st.text_input('Route')
    capacity = st.number_input('Capacity', min_value=0, step=1)
    available_seats = st.number_input('Available Seats', min_value=0, step=1)

    if st.button('Add Bus'):
        st.session_state.buses.append({
            'bus_number': bus_number,
            'route': route,
            'capacity': capacity,
            'available_seats': available_seats
        })

# Delete Bus
elif option == "Delete Bus":
    st.write("Select a bus to delete:")
    bus_numbers = [bus['bus_number'] for bus in st.session_state.buses]
    bus_to_delete = st.selectbox("Bus Number", bus_numbers)
    if st.button('Delete Bus'):
        st.session_state.buses = [bus for bus in st.session_state.buses if bus['bus_number'] != bus_to_delete]

# View Bus
elif option == "View Bus":
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