import tkinter as tk
from dronekit import connect, VehicleMode
import threading
import time
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Function to connect to the drone
def connect_drone():
    global vehicle
    connection_string = "/dev/tty.usbserial-0001"
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
        sat_count.config(text=f"Satellites: {vehicle.gps_0.satellites_visible}")
        latitude.config(text=f"Latitude: {vehicle.location.global_frame.lat}")
        longitude.config(text=f"Longitude: {vehicle.location.global_frame.lon}")
    root.after(1000, update_flight_data)

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

# Status frame for displaying flight data
status_frame = ttk.Frame(root, padding=20)
status_frame.pack(fill=tk.BOTH, expand=True)

# Data labels
battery_level = ttk.Label(status_frame, text="Battery: N/A", font=("Helvetica", 12), padding=10)
battery_level.pack()

altitude = ttk.Label(status_frame, text="Altitude: N/A", font=("Helvetica", 12), padding=10)
altitude.pack()

speed = ttk.Label(status_frame, text="Speed: N/A", font=("Helvetica", 12), padding=10)
speed.pack()

flight_mode = ttk.Label(status_frame, text="Flight Mode: N/A", font=("Helvetica", 12), padding=10)
flight_mode.pack()

sat_count = ttk.Label(status_frame, text="Satellites: N/A", font=("Helvetica", 12), padding=10)
sat_count.pack()

latitude = ttk.Label(status_frame, text="Latitude: N/A", font=("Helvetica", 12), padding=10)
latitude.pack()

longitude = ttk.Label(status_frame, text="Longitude: N/A", font=("Helvetica", 12), padding=10)
longitude.pack()

# Flight mode buttons frame
buttons_frame = ttk.Frame(root)
buttons_frame.pack(fill=tk.X, pady=10)

# Flight mode buttons
loiter_button = ttk.Button(buttons_frame, text="Loiter", bootstyle=WARNING, command=lambda: set_flight_mode("LOITER"))
loiter_button.pack(side=tk.LEFT, expand=True, padx=2)

# Add other flight mode buttons here following the same pattern as loiter_button

# Control buttons not directly related to flight mode setting
mode_button = ttk.Button(root, text="Set Flight Mode", bootstyle=WARNING)
mode_button.pack(pady=5)

arm_takeoff_button = ttk.Button(root, text="Arm & Take Off", bootstyle=DANGER, command=lambda: arm_and_takeoff(10))
arm_takeoff_button.pack(pady=5)

# Start the Tkinter loop
root.mainloop()
