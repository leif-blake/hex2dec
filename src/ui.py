"""
Main UI module
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from universal_format import UniversalFormat
import handlers

class Hex2Dec(tk.Tk):
    """
    Main application class for the Hex2Dec converter.
    """
    def __init__(self, version):
        super().__init__()
        self.title(f"Hex2Dec Converter - {version}")
        self.geometry("800x600")
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.create_widgets()

    def create_widgets(self):
        """
        Create and place all widgets in the main window.
        """
        self.create_option_widgets()
        self.create_conversion_widgets()

        # Configure column weights
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(2, weight=1)

        # Configure row weights
        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)

    def create_conversion_widgets(self):
        """
        Create and place conversion buttons for hexadecimal, decimal, and binary.
        """
        # Create a frame for the conversion buttons
        conversion_frame = ttk.Frame(self.main_frame)
        conversion_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Create text boxes and buttons for each conversion type
        hex_label = ttk.Label(conversion_frame, text="Hexadecimal")
        hex_label.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        hex_text = tk.Text(conversion_frame, width=20, height=15)
        hex_text.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        hex_button = ttk.Button(conversion_frame, text="Convert Hex")
        hex_button.grid(row=2, column=0, padx=5, pady=5)

        dec_label = ttk.Label(conversion_frame, text="Decimal")
        dec_label.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
        dec_text = tk.Text(conversion_frame, width=20, height=15)
        dec_text.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        dec_button = ttk.Button(conversion_frame, text="Convert Decimal")
        dec_button.grid(row=2, column=1, padx=5, pady=5)

        bin_label = ttk.Label(conversion_frame, text="Binary")
        bin_label.grid(row=0, column=2, padx=5, pady=5, sticky="nw")
        bin_text = tk.Text(conversion_frame, width=20, height=15)
        bin_text.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
        bin_button = ttk.Button(conversion_frame, text="Convert Binary")
        bin_button.grid(row=2, column=2, padx=5, pady=5)

        # Bind handlers to buttons
        hex_button.config(command=lambda: handlers.hex_to_other(hex_text, dec_text, bin_text, self.number_type_var, self.little_endian_var, self.pad_var, self.show_prefix_var))
        dec_button.config(command=lambda: handlers.dec_to_other(hex_text, dec_text, bin_text, self.number_type_var, self.little_endian_var, self.pad_var, self.show_prefix_var))
        bin_button.config(command=lambda: handlers.bin_to_other(hex_text, dec_text, bin_text, self.number_type_var, self.little_endian_var, self.pad_var, self.show_prefix_var))

        # Bind handlers to text boxes for shift+enter
        hex_text.bind("<Shift-Return>", lambda event: handlers.hex_to_other(hex_text, dec_text, bin_text, self.number_type_var, self.little_endian_var, self.pad_var, self.show_prefix_var))
        dec_text.bind("<Shift-Return>", lambda event: handlers.dec_to_other(hex_text, dec_text, bin_text, self.number_type_var, self.little_endian_var, self.pad_var, self.show_prefix_var))
        bin_text.bind("<Shift-Return>", lambda event: handlers.bin_to_other(hex_text, dec_text, bin_text, self.number_type_var, self.little_endian_var, self.pad_var, self.show_prefix_var))

        # Configure grid weights for resizing
        conversion_frame.grid_columnconfigure(0, weight=1)
        conversion_frame.grid_columnconfigure(1, weight=1)
        conversion_frame.grid_columnconfigure(2, weight=1)

        conversion_frame.grid_rowconfigure(0, weight=0)
        conversion_frame.grid_rowconfigure(1, weight=1)
        conversion_frame.grid_rowconfigure(2, weight=0)

    def create_option_widgets(self):
        """
        Create and place option widgets for padding, number type, and endianness.
        """
        # Create a frame for the options
        options_frame = ttk.Frame(self.main_frame)
        options_frame.grid(row=0, column=0, pady=5, sticky="nw")

        # Check box for padding
        self.pad_var = tk.BooleanVar()
        pad_check = ttk.Checkbutton(options_frame, text="Enable Padding", variable=self.pad_var)
        pad_check.grid(row=0, column=0, padx=5)

        # Check box for showing prefixes
        self.show_prefix_var = tk.BooleanVar()
        show_prefix_check = ttk.Checkbutton(options_frame, text="Show Prefix", variable=self.show_prefix_var)
        show_prefix_check.grid(row=0, column=1, padx=5)

        # Check box for little endianness
        self.little_endian_var = tk.BooleanVar()
        little_endian_check = ttk.Checkbutton(options_frame, text="Little Endian", variable=self.little_endian_var)
        little_endian_check.grid(row=0, column=2, padx=5)

        # Radio group for type of number
        self.number_type_var = tk.StringVar(value="unsigned")

        unsigned_radio = ttk.Radiobutton(options_frame, text="Unsigned", variable=self.number_type_var, value="unsigned")
        unsigned_radio.grid(row=1, column=0, padx=5, sticky="nw")

        signed_radio = ttk.Radiobutton(options_frame, text="Signed", variable=self.number_type_var, value="signed")
        signed_radio.grid(row=1, column=1, padx=5, sticky="nw")

        floating_radio = ttk.Radiobutton(options_frame, text="Floating Point", variable=self.number_type_var, value="floating")
        floating_radio.grid(row=1, column=2, padx=5, sticky="nw")
