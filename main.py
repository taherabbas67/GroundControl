import tkinter as tk
from dronekit import connect, VehicleMode
import threading
import time  # Import 'time' for sleep in arm_and_takeoff
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Function to connect to the drone
def connect_drone():
    global vehicle
    connection_string = "/dev/tty.usbserial-0001"  # Example connection string, replace with your actual USB connection info
    print("Connecting to drone on: %s" % connection_string)
    vehicle = connect(connection_string, baud=57600)
    update_flight_data()

# Function to update flight data on the interface
def update_flight_data():
    if vehicle:
        battery_level.config(text=f"Battery: {vehicle.battery}")
        altitude.config(text=f"Altitude: {vehicle.location.global_relative_frame.alt}")
        speed.config(text=f"Speed: {vehicle.groundspeed}")
        flight_mode.config(text=f"Flight Mode: {vehicle.mode.name}")
    root.after(1000, update_flight_data)  # Update the labels every second

# Function to change flight modes
def set_flight_mode(new_mode):
    if vehicle:
        vehicle.mode = VehicleMode(new_mode)

# Function to arm and take off
def arm_and_takeoff(aTargetAltitude):
    if vehicle:
        while not vehicle.is_armable:
            print(" Waiting for vehicle to initialise...")
            time.sleep(1)

        print("Arming motors")
        vehicle.mode = VehicleMode("GUIDED")
        vehicle.armed = True

        while not vehicle.armed:
            print(" Waiting for arming...")
            time.sleep(1)

        print("Taking off!")
        vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

# Creating the main window
root = ttk.Window(title="Ground Control", size=(800, 600), themename="darkly")

# Navbar frame
navbar_frame = ttk.Frame(root, bootstyle="dark", padding=10)
navbar_frame.pack(fill=tk.X)

# Navbar title
navbar_title = ttk.Label(navbar_frame, text="Ground Control", bootstyle="inverse", font=("Helvetica", 18, "bold"))
navbar_title.pack(side=tk.LEFT, padx=10)

# Connect button
connect_button = ttk.Button(navbar_frame, text="Connect", bootstyle=SUCCESS, command=lambda: threading.Thread(target=connect_drone).start())
connect_button.pack(side=tk.RIGHT, padx=10)

# Status frame
status_frame = ttk.Frame(root, padding=20)
status_frame.pack(fill=tk.BOTH, expand=True)

# Labels for displaying flight data with larger font and padding for better visibility
battery_level = ttk.Label(status_frame, text="Battery: N/A", font=("Helvetica", 12), padding=10)
battery_level.pack()

altitude = ttk.Label(status_frame, text="Altitude: N/A", font=("Helvetica", 12), padding=10)
altitude.pack()

speed = ttk.Label(status_frame, text="Speed: N/A", font=("Helvetica", 12), padding=10)
speed.pack()

flight_mode = ttk.Label(status_frame, text="Flight Mode: N/A", font=("Helvetica", 12), padding=10)
flight_mode.pack()

# Control buttons
mode_button = ttk.Button(root, text="Set Flight Mode", bootstyle=WARNING, command=lambda: set_flight_mode("GUIDED"))
mode_button.pack(pady=5)

arm_takeoff_button = ttk.Button(root, text="Arm & Take Off", bootstyle=DANGER, command=lambda: arm_and_takeoff(10))
arm_takeoff_button.pack(pady=5)

# Start the Tkinter loop
root.mainloop()
