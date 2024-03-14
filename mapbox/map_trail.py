import tkinter as tk
from tkinterweb import HtmlFrame  # Import the HtmlFrame widget
import tempfile

def update_map(lat, lon):
    # Mapbox Access Token
    mapbox_access_token = 'pk.eyJ1IjoidGFoZXJhYmJhcyIsImEiOiJjbHN3aTRkY2YweHU4MmlxdG5veXQzYm9oIn0.9FA7D696-r1TmIv_iPYPeA'
    
    # HTML template for the Mapbox map
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset='utf-8' />
        <title>Drone Location</title>
        <meta name='viewport' content='initial-scale=1,maximum-scale=1,user-scalable=no' />
        <script src='https://api.mapbox.com/mapbox-gl-js/v2.3.1/mapbox-gl.js'></script>
        <link href='https://api.mapbox.com/mapbox-gl-js/v2.3.1/mapbox-gl.css' rel='stylesheet' />
        <style>
            body {{ margin:0; padding:0; }}
            #map {{ position:absolute; top:0; bottom:0; width:100%; }}
        </style>
    </head>
    <body>
    <div id='map'></div>
    <script>
        mapboxgl.accessToken = '{mapbox_access_token}';
        var map = new mapboxgl.Map({{
            container: 'map', // container ID
            style: 'mapbox://styles/mapbox/streets-v11', // style URL
            center: [{lon}, {lat}], // starting position [lng, lat]
            zoom: 9 // starting zoom
        }});

        var marker = new mapboxgl.Marker() // Initialize a new marker
            .setLngLat([{lon}, {lat}]) // Marker [lng, lat] coordinates
            .addTo(map); // Add the marker to the map
    </script>
    </body>
    </html>
    """
    
    # Save the HTML content to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
    with open(temp_file.name, 'w') as file:
        file.write(html_template)
    
    # Load the HTML file into the HtmlFrame
    map_frame.load_file(temp_file.name)

# Creating the main window
root = tk.Tk()
root.title("Ground Control")
root.geometry("800x600")

# Navbar frame
navbar_frame = tk.Frame(root, bg="blue", height=50)
navbar_frame.pack(fill=tk.X)

# Map frame using HtmlFrame
map_frame = HtmlFrame(root, horizontal_scrollbar="auto")
map_frame.pack(fill="both", expand=True)

# Flight data frame
flight_data_frame = tk.Frame(root, bg="green", height=100)
flight_data_frame.pack(fill=tk.X)

# Initialize map with a default location (example coordinates)
update_map(37.7749, -122.4194)

root.mainloop()
