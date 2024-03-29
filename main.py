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

def disconnect_drone():
    global vehicle
    # Disconnecting logic here
    if vehicle:
        print("Disconnecting from drone...")
        vehicle.close()
        # Update disconnection status or handle additional cleanup
        vehicle = None
    else:
        print("No drone connected.")

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
    root.after(100, update_flight_data)#reduced delay from 1000 to 100



# Function to change flight modes
def set_flight_mode(new_mode):
    if vehicle:
        vehicle.mode = VehicleMode(new_mode)

# Function to arm the vehicle
def arm_vehicle():
    if vehicle:
        print("Arming motors")
        vehicle.mode = VehicleMode("GUIDED")
        vehicle.armed = True
        while not vehicle.armed:
            print("Waiting for arming...")
            time.sleep(1)

# Function to disarm the vehicle
def disarm_vehicle():
    if vehicle:
        print("Disarming motors")
        vehicle.armed = False
        while vehicle.armed:
            print("Waiting for disarming...")
            time.sleep(1)

# Function to take off
def takeoff(aTargetAltitude):
    if vehicle and vehicle.armed:
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

# Disconnect button
disconnect_button = ttk.Button(navbar_frame, text="Disconnect", bootstyle=DANGER, command=disconnect_drone)
disconnect_button.pack(side=tk.RIGHT)

# Status frame
status_frame = ttk.Frame(root, padding=20)
status_frame.pack(fill=tk.BOTH, expand=True)


# First row frame for battery, altitude, speed, flight mode
first_row_frame = ttk.Frame(root, padding=10)
first_row_frame.pack(fill=tk.X)

battery_level = ttk.Label(first_row_frame, text="Battery: N/A", font=("Helvetica", 20))
battery_level.pack(side=tk.LEFT, expand=True, padx=5, pady=5)

altitude = ttk.Label(first_row_frame, text="Altitude: N/A", font=("Helvetica", 20))
altitude.pack(side=tk.LEFT, expand=True, padx=5, pady=5)

speed = ttk.Label(first_row_frame, text="Speed: N/A", font=("Helvetica", 20))
speed.pack(side=tk.LEFT, expand=True, padx=5, pady=5)

flight_mode = ttk.Label(first_row_frame, text="Flight Mode: N/A", font=("Helvetica", 20))
flight_mode.pack(side=tk.LEFT, expand=True, padx=5, pady=5)

# Second row frame for sat count, latitude, longitude
second_row_frame = ttk.Frame(root, padding=10)
second_row_frame.pack(fill=tk.X)

sat_count = ttk.Label(second_row_frame, text="Satellites: N/A", font=("Helvetica", 20))
sat_count.pack(side=tk.LEFT, expand=True, padx=5, pady=10)

latitude = ttk.Label(second_row_frame, text="Latitude: N/A", font=("Helvetica", 20))
latitude.pack(side=tk.LEFT, expand=True, padx=5, pady=10)

longitude = ttk.Label(second_row_frame, text="Longitude: N/A", font=("Helvetica", 20))
longitude.pack(side=tk.LEFT, expand=True, padx=5, pady=10)


# Function to create a flight mode button
def create_flight_mode_button(text, mode, style):
    return ttk.Button(root, text=text, bootstyle=style, command=lambda: set_flight_mode(mode))

# Creating buttons for each flight mode
buttons_frame = ttk.Frame(root)
buttons_frame.pack(fill=tk.X, pady=10)

loiter_button = create_flight_mode_button("Loiter", "LOITER", INFO)
loiter_button.pack(in_=buttons_frame, side=tk.LEFT, expand=True, padx=2)

althold_button = create_flight_mode_button("Alt Hold", "ALT_HOLD", INFO)
althold_button.pack(in_=buttons_frame, side=tk.LEFT, expand=True, padx=2)

stabilize_button = create_flight_mode_button("Stabilize", "STABILIZE", INFO)
stabilize_button.pack(in_=buttons_frame, side=tk.LEFT, expand=True, padx=2)

land_button = create_flight_mode_button("Land", "LAND", INFO)
land_button.pack(in_=buttons_frame, side=tk.LEFT, expand=True, padx=2)

rtl_button = create_flight_mode_button("RTL", "RTL", INFO)
rtl_button.pack(in_=buttons_frame, side=tk.LEFT, expand=True, padx=2)

guided_button = create_flight_mode_button("Guided", "GUIDED", INFO)
guided_button.pack(in_=buttons_frame, side=tk.LEFT, expand=True, padx=2)

auto_button = create_flight_mode_button("Auto", "AUTO", INFO)
auto_button.pack(in_=buttons_frame, side=tk.LEFT, expand=True, padx=2)


# Control buttons frame
control_buttons_frame = ttk.Frame(root, padding=30)
control_buttons_frame.pack(fill=tk.X)

# Arm button
arm_button = ttk.Button(control_buttons_frame, text="Arm", bootstyle=DANGER, command=arm_vehicle)
arm_button.pack(side=tk.LEFT, expand=True, padx=5)

# Disarm button
disarm_button = ttk.Button(control_buttons_frame, text="Disarm", bootstyle=DANGER, command=disarm_vehicle)
disarm_button.pack(side=tk.LEFT, expand=True, padx=5)

# Take Off button
takeoff_button = ttk.Button(control_buttons_frame, text="Take Off", bootstyle=DANGER, command=lambda: takeoff(10))
takeoff_button.pack(side=tk.LEFT, expand=True, padx=5)


# Start the Tkinter loop
root.mainloop()
