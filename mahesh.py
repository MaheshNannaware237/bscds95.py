import hashlib  # To generate unique hashes
import time     # To add timestamps
import streamlit as st  # For building web app

# Initialize the blockchain list
blockchain = []

# Function to create a block
def create_block(index, data, previous_hash):
    block = {
        "index": index,
        "data": data,
        "timestamp": time.time(),
        "previous_hash": previous_hash
    }
    return block

# Function to generate a unique hash for each block
def generate_hash(block):
    block_string = f"{block['index']}{block['data']}{block['timestamp']}{block['previous_hash']}"
    return hashlib.sha256(block_string.encode()).hexdigest()

# Function to add a new block (new ticket booking)
def add_ticket_booking(passenger_name, bus_number, seat_number, fare):
    previous_block = blockchain[-1]  # Get the last block
    new_index = previous_block["index"] + 1  # Next block index
    new_hash = generate_hash(previous_block)  # Hash of the last block

    # Create ticket data
    ticket_data = {
        "passenger_name": passenger_name,
        "bus_number": bus_number,
        "seat_number": seat_number,
        "fare": fare
    }

    # Create a new block with ticket data
    new_block = create_block(new_index, ticket_data, new_hash)
    blockchain.append(new_block)  # Add to the blockchain

# Create Genesis block (only once)
if not blockchain:
    genesis_block = create_block(1, "Genesis Block", "0")
    blockchain.append(genesis_block)

# Streamlit App Interface
st.title("🚌 Bus Ticket Booking on Blockchain")

st.header("Book a New Ticket")

# Form to add new booking
with st.form(key="booking_form"):
    passenger_name = st.text_input("Passenger Name")
    bus_number = st.text_input("Bus Number")
    seat_number = st.text_input("Seat Number")
    fare = st.number_input("Fare", min_value=0.0, format="%.2f")
    
    submit_button = st.form_submit_button(label="Book Ticket")

# Add booking if form is submitted
if submit_button:
    if passenger_name and bus_number and seat_number and fare > 0:
        add_ticket_booking(passenger_name, bus_number, seat_number, fare)
        st.success(f"Ticket booked successfully for {passenger_name}!")
    else:
        st.error("Please fill all fields correctly.")

# Show Blockchain
st.header("📜 Ticket Booking Blockchain")

for block in blockchain:
    st.subheader(f"Block Index: {block['index']}")
    st.json({
        "Ticket Data": block['data'],
        "Timestamp": time.ctime(block['timestamp']),
        "Previous Hash": block['previous_hash']
    })
