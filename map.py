import webbrowser

def open_in_macos_maps(lat, lon):
    # macOS Maps URL scheme
    url = f"http://maps.apple.com/?q={lat},{lon}"
    webbrowser.open(url)

# Example usage
open_in_macos_maps(37.7749, -122.4194)
