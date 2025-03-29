"""
Entry point for the number converter application
"""

from ui import Hex2Dec

if __name__ == "__main__":
    # Define the version of the application
    version = "0.0.1"
    # Create an instance of the Hex2Dec application
    app = Hex2Dec(version)
    # Start the main loop of the application
    app.mainloop()