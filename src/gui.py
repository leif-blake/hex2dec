"""
Python GUI for the project
"""

import tkinter as tk
from tkinter import messagebox

from src.universal_format import UniversalFormat

def hex_to_other():
    try:
        hex_strings = hex_text.get("1.0", tk.END).strip().splitlines()
        decimal_text.delete("1.0", tk.END)
        binary_text.delete("1.0", tk.END)
        value = UniversalFormat()
        value.set_type(number_type_var.get())
        for hex_string in hex_strings:
            try:
                # Parse value
                value.from_hex_string(hex_string)

                # Convert and add to textboxes
                decimal_text.insert(tk.END, value.to_dec_string() + "\n")
                binary_text.insert(tk.END, value.to_bin_string(pad_var.get()) + "\n")
            except ValueError:
                messagebox.showerror("Conversion Error", f"Invalid Hexadecimal Value: {hex_string}")
    except ValueError:
        messagebox.showerror("Conversion Error", "Invalid Hexadecimal Value")

def decimal_to_other():
    decimal_strings = decimal_text.get("1.0", tk.END).strip().splitlines()
    hex_text.delete("1.0", tk.END)
    binary_text.delete("1.0", tk.END)
    value = UniversalFormat()
    value.set_type(number_type_var.get())
    for decimal_string in decimal_strings:
        try:
            # Parse value
            value.from_dec_string(decimal_string)

            # Convert and add to textboxes
            hex_text.insert(tk.END, value.to_hex_string(pad_var.get()) + "\n")
            binary_text.insert(tk.END, value.to_bin_string(pad_var.get()) + "\n")
        except ValueError:
            messagebox.showerror("Conversion Error", f"Invalid Decimal Value: {decimal_string}")

def binary_to_other():
    binary_strings = binary_text.get("1.0", tk.END).strip().splitlines()
    hex_text.delete("1.0", tk.END)
    decimal_text.delete("1.0", tk.END)
    value = UniversalFormat()
    value.set_type(number_type_var.get())
    for binary_string in binary_strings:
        try:
            # Parse value
            value.from_bin_string(binary_string)

            # Convert and add to textboxes
            hex_text.insert(tk.END, value.to_hex_string(pad_var.get()) + "\n")
            decimal_text.insert(tk.END, value.to_dec_string() + "\n")
        except ValueError:
            messagebox.showerror("Conversion Error", f"Invalid Binary Value: {binary_string}")

root = tk.Tk()
root.title("Number Base Converter")

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Check Box for Padding
pad_var = tk.BooleanVar()
pad_check = tk.Checkbutton(frame, text="Enable Padding", variable=pad_var)
pad_check.grid(row=0, column=0, pady=5, sticky="nw")

# Radio Group for type of number
number_type_var = tk.StringVar(value="unsigned")

unsigned_radio = tk.Radiobutton(frame, text="Unsigned", variable=number_type_var, value="unsigned")
unsigned_radio.grid(row=1, column=0, pady=5, sticky="nw")

signed_radio = tk.Radiobutton(frame, text="Signed", variable=number_type_var, value="signed")
signed_radio.grid(row=1, column=1, pady=5, sticky="nw")

floating_radio = tk.Radiobutton(frame, text="Floating Point", variable=number_type_var, value="floating")
floating_radio.grid(row=1, column=2, pady=5, sticky="nw")

hex_text = tk.Text(frame, width=20, height=15)
hex_text.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
hex_button = tk.Button(frame, text="Convert Hex", command=hex_to_other)
hex_button.grid(row=3, column=0, padx=5, pady=5)

decimal_text = tk.Text(frame, width=20, height=15)
decimal_text.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
decimal_button = tk.Button(frame, text="Convert Decimal", command=decimal_to_other)
decimal_button.grid(row=3, column=1, padx=5, pady=5)

binary_text = tk.Text(frame, width=20, height=15)
binary_text.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")
binary_button = tk.Button(frame, text="Convert Binary", command=binary_to_other)
binary_button.grid(row=3, column=2, padx=5, pady=5)

# Configure column weights
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)

# Configure row weights
frame.grid_rowconfigure(0, weight=0)
frame.grid_rowconfigure(1, weight=0)
frame.grid_rowconfigure(2, weight=1)
frame.grid_rowconfigure(3, weight=0)

root.mainloop()