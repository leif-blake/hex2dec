"""
Python GUI for the project
"""

import tkinter as tk
from tkinter import messagebox

from universal_format import UniversalFormat

version = "0.0"

def remove_trailing_newlines():
    """
    Remove trailing newlines from the text boxes
    """
    hex_string = hex_text.get("1.0", tk.END).strip()
    decimal_string = decimal_text.get("1.0", tk.END).strip()
    binary_string = binary_text.get("1.0", tk.END).strip()

    # Remove trailing newlines
    hex_text.delete("1.0", tk.END)
    decimal_text.delete("1.0", tk.END)
    binary_text.delete("1.0", tk.END)

    # Insert the cleaned strings back into the text boxes
    hex_text.insert(tk.END, hex_string)
    decimal_text.insert(tk.END, decimal_string)
    binary_text.insert(tk.END, binary_string)

def hex_to_other():
    hex_strings = hex_text.get("1.0", tk.END).strip().splitlines()
    formatted_hex_strings = []
    decimal_text.delete("1.0", tk.END)
    binary_text.delete("1.0", tk.END)
    value = UniversalFormat()
    value.set_type(number_type_var.get())
    if little_endian_var.get():
        value.set_endianness('little')
    for hex_string in hex_strings:
        try:
            # Parse value
            value.from_hex_string(hex_string)

            # Convert and add to textboxes
            decimal_text.insert(tk.END, value.to_dec_string() + "\n")
            binary_text.insert(tk.END, value.to_bin_string(pad_var.get(), show_prefix_var.get()) + "\n")
        except ValueError as error:
            messagebox.showerror("Conversion Error", f"Invalid Hexadecimal Value: {hex_string}\n"
                                                     f"{error}")
    remove_trailing_newlines()

def decimal_to_other():
    decimal_strings = decimal_text.get("1.0", tk.END).strip().splitlines()
    formatted_decimal_strings = []
    hex_text.delete("1.0", tk.END)
    binary_text.delete("1.0", tk.END)
    value = UniversalFormat()
    value.set_type(number_type_var.get())
    if little_endian_var.get():
        value.set_endianness('little')
    for decimal_string in decimal_strings:
        try:
            # If decimal string contains a decimal point, but type is not floating, convert to integer
            if '.' in decimal_string and number_type_var.get() != "floating":
                decimal_string = str(int(float(decimal_string)))
            if '-' in decimal_string and number_type_var.get() == "unsigned":
                decimal_string = str(abs(int(decimal_string)))
            formatted_decimal_strings.append(decimal_string)

            # Parse value
            value.from_dec_string(decimal_string)

            # Convert and add to textboxes
            hex_text.insert(tk.END, value.to_hex_string(pad_var.get(), show_prefix_var.get()) + "\n")
            binary_text.insert(tk.END, value.to_bin_string(pad_var.get(), show_prefix_var.get()) + "\n")
        except ValueError as error:
            messagebox.showerror("Conversion Error", f"Invalid Decimal Value: {decimal_string}\n"
                                                     f"{error}")
    # Replace decimal strings in the text box with formatted decimal strings
    decimal_text.delete("1.0", tk.END)
    decimal_text.insert(tk.END, "\n".join(formatted_decimal_strings) + "\n")
    remove_trailing_newlines()

def binary_to_other():
    binary_strings = binary_text.get("1.0", tk.END).strip().splitlines()
    hex_text.delete("1.0", tk.END)
    decimal_text.delete("1.0", tk.END)
    value = UniversalFormat()
    value.set_type(number_type_var.get())
    if little_endian_var.get():
        value.set_endianness('little')
    for binary_string in binary_strings:
        try:
            # Parse value
            value.from_bin_string(binary_string)

            # Convert and add to textboxes
            hex_text.insert(tk.END, value.to_hex_string(pad_var.get(), show_prefix_var.get()) + "\n")
            decimal_text.insert(tk.END, value.to_dec_string() + "\n")
        except ValueError as error:
            messagebox.showerror("Conversion Error", f"Invalid Binary Value: {binary_string}\n"
                                                     f"{error}")
    remove_trailing_newlines()

root = tk.Tk()
root.title(f"Hex2Dec Converter - {version}")

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# New frame for padding and number type selection
options_frame = tk.Frame(frame)
options_frame.grid(row=0, column=0, pady=5, sticky="nw")

# Check Box for Padding
pad_var = tk.BooleanVar()
pad_check = tk.Checkbutton(options_frame, text="Enable Padding", variable=pad_var)
pad_check.grid(row=0, column=0, pady=5, sticky="nw")

# Check box for showing prefixes
show_prefix_var = tk.BooleanVar()
show_prefix_check = tk.Checkbutton(options_frame, text="Show Prefix", variable=show_prefix_var)
show_prefix_check.grid(row=0, column=1, pady=5, sticky="nw")

# Check box for little endianness
little_endian_var = tk.BooleanVar()
little_endian_check = tk.Checkbutton(options_frame, text="Little Endian", variable=little_endian_var)
little_endian_check.grid(row=0, column=2, pady=5, sticky="nw")

# Radio Group for type of number
number_type_var = tk.StringVar(value="unsigned")

unsigned_radio = tk.Radiobutton(options_frame, text="Unsigned", variable=number_type_var, value="unsigned")
unsigned_radio.grid(row=1, column=0, pady=5, sticky="nw")

signed_radio = tk.Radiobutton(options_frame, text="Signed", variable=number_type_var, value="signed")
signed_radio.grid(row=1, column=1, pady=5, sticky="nw")

floating_radio = tk.Radiobutton(options_frame, text="Floating Point", variable=number_type_var, value="floating")
floating_radio.grid(row=1, column=2, pady=5, sticky="nw")

conversion_frame = tk.Frame(frame)
conversion_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

hex_label = tk.Label(conversion_frame, text="Hexadecimal")
hex_label.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
hex_text = tk.Text(conversion_frame, width=20, height=15)
hex_text.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
hex_button = tk.Button(conversion_frame, text="Convert Hex", command=hex_to_other)
hex_button.grid(row=2, column=0, padx=5, pady=5)

decimal_label = tk.Label(conversion_frame, text="Decimal")
decimal_label.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
decimal_text = tk.Text(conversion_frame, width=20, height=15)
decimal_text.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
decimal_button = tk.Button(conversion_frame, text="Convert Decimal", command=decimal_to_other)
decimal_button.grid(row=2, column=1, padx=5, pady=5)

binary_label = tk.Label(conversion_frame, text="Binary")
binary_label.grid(row=0, column=2, padx=5, pady=5, sticky="nw")
binary_text = tk.Text(conversion_frame, width=20, height=15)
binary_text.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
binary_button = tk.Button(conversion_frame, text="Convert Binary", command=binary_to_other)
binary_button.grid(row=2, column=2, padx=5, pady=5)

# Configure the grid layout
conversion_frame.grid_columnconfigure(0, weight=1)
conversion_frame.grid_columnconfigure(1, weight=1)
conversion_frame.grid_columnconfigure(2, weight=1)

conversion_frame.grid_rowconfigure(0, weight=0)
conversion_frame.grid_rowconfigure(1, weight=1)
conversion_frame.grid_rowconfigure(2, weight=0)

# Configure column weights
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)

# Configure row weights
frame.grid_rowconfigure(0, weight=0)
frame.grid_rowconfigure(1, weight=0)
frame.grid_rowconfigure(2, weight=1)


root.mainloop()