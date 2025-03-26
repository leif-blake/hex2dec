"""
Python GUI for the project
"""
import tkinter as tk
from tkinter import messagebox

import tkinter as tk
from tkinter import messagebox
import numpy as np
import struct

pad_bit_values = np.array([8, 16, 32, 64, 128])
pad_nibble_values = np.array([1, 2, 4, 8, 16])

def hex_to_other():
    try:
        hex_values = hex_text.get("1.0", tk.END).strip().splitlines()
        decimal_text.delete("1.0", tk.END)
        binary_text.delete("1.0", tk.END)
        for hex_value in hex_values:
            try:
                # Conversion
                if number_type_var.get() == "unsigned":
                    decimal_value = int(hex_value, 16)
                    binary_value = bin(decimal_value)[2:]
                elif number_type_var.get() == "signed":
                    decimal_value = int(hex_value, 16)
                    if decimal_value >= 2**(4 * len(hex_value) - 1):
                        decimal_value -= 2**(4 * len(hex_value))
                    binary_value = bin(decimal_value)[2:]
                    if decimal_value < 0:
                        binary_value = binary_value[1:]
                elif number_type_var.get() == "floating":
                    # Convert to float
                    decimal_value = struct.unpack('!f', bytes.fromhex(hex_value))[0]
                    # Convert to binary string
                    binary_value = bin(struct.unpack('!I', struct.pack('!f', decimal_value))[0])[2:]

                # Padding
                if pad_var.get():
                    binary_value = binary_value.zfill(np.min(pad_bit_values[pad_bit_values >= len(binary_value)]))

                # Add to textboxes
                decimal_text.insert(tk.END, str(decimal_value) + "\n")
                binary_text.insert(tk.END, binary_value + "\n")
            except ValueError:
                messagebox.showerror("Conversion Error", f"Invalid Hexadecimal Value: {hex_value}")
    except ValueError:
        messagebox.showerror("Conversion Error", "Invalid Hexadecimal Value")

def decimal_to_other():
    try:
        decimal_values = decimal_text.get("1.0", tk.END).strip().splitlines()
        hex_text.delete("1.0", tk.END)
        binary_text.delete("1.0", tk.END)
        for decimal_value in decimal_values:
            try:
                # Conversion
                if number_type_var.get() == "unsigned":
                    decimal_value = int(decimal_value)
                    hex_value = hex(decimal_value)[2:].upper()
                    binary_value = bin(decimal_value)[2:]
                elif number_type_var.get() == "signed":
                    decimal_value = int(decimal_value)
                    hex_value = hex(decimal_value)[2:].upper()
                    binary_value = bin(decimal_value)[2:]
                    if decimal_value < 0:
                        binary_value = binary_value[1:]
                elif number_type_var.get() == "floating":
                    decimal_value = float(decimal_value)
                    hex_value = hex(struct.unpack('<I', struct.pack('<f', decimal_value))[0])[2:].upper()
                    binary_value = bin(struct.unpack('<I', struct.pack('<f', decimal_value))[0])[2:]

                # Padding
                if pad_var.get():
                    hex_value = hex_value.zfill(np.min(pad_nibble_values[pad_nibble_values >= len(hex_value)]))
                if pad_var.get():
                    binary_value = binary_value.zfill(np.min(pad_bit_values[pad_bit_values >= len(binary_value)]))

                # Add to textboxes
                hex_text.insert(tk.END, hex_value + "\n")
                binary_text.insert(tk.END, binary_value + "\n")
            except ValueError:
                messagebox.showerror("Conversion Error", f"Invalid Decimal Value: {decimal_value}")
    except ValueError:
        messagebox.showerror("Conversion Error", "Invalid Decimal Value")

def binary_to_other():
    try:
        binary_values = binary_text.get("1.0", tk.END).strip().splitlines()
        decimal_text.delete("1.0", tk.END)
        hex_text.delete("1.0", tk.END)
        for binary_value in binary_values:
            try:
                # Conversion
                if number_type_var.get() == "unsigned":
                    decimal_value = int(binary_value, 2)
                    hex_value = hex(decimal_value)[2:].upper()
                elif number_type_var.get() == "signed":
                    decimal_value = int(binary_value, 2)
                    if binary_value[0] == "1":
                        decimal_value -= 2 ** len(binary_value)
                    hex_value = hex(decimal_value)[2:].upper()
                elif number_type_var.get() == "floating":
                    # Convert to hex string
                    hex_value = hex(int(binary_value, 2))[2:].upper()
                    # Padding
                    if pad_var.get():
                        hex_value = hex_value.zfill(np.min(pad_nibble_values[pad_nibble_values >= len(hex_value)]))
                    # Convert to float
                    decimal_value = struct.unpack('!f', bytes.fromhex(hex_value))[0]

                # Padding
                if pad_var.get():
                    hex_value = hex_value.zfill(np.min(pad_nibble_values[pad_nibble_values >= len(hex_value)]))

                # Add to text boxes
                decimal_text.insert(tk.END, str(decimal_value) + "\n")
                hex_text.insert(tk.END, hex_value + "\n")
            except ValueError:
                messagebox.showerror("Conversion Error", f"Invalid Binary Value: {binary_value}")
    except ValueError:
        messagebox.showerror("Conversion Error", "Invalid Binary Value")

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

frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)

root.mainloop()