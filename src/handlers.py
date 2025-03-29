"""
Functions to handle ui events
"""

import tkinter as tk
from tkinter import messagebox

from universal_format import UniversalFormat

def hex_to_other(hex_text, dec_text, bin_text, number_type_var, little_endian_var, pad_var, show_prefix_var):
    hex_strings = hex_text.get("1.0", tk.END).strip().splitlines()
    formatted_hex_strings = []
    dec_text.delete("1.0", tk.END)
    bin_text.delete("1.0", tk.END)
    value = UniversalFormat()
    value.set_type(number_type_var.get())
    if little_endian_var.get():
        value.set_endianness('little')
    for hex_string in hex_strings:
        try:
            # Parse value
            value.from_hex_string(hex_string)

            # Convert and add to textboxes
            dec_text.insert(tk.END, value.to_dec_string() + "\n")
            bin_text.insert(tk.END, value.to_bin_string(pad_var.get(), show_prefix_var.get()) + "\n")
        except ValueError as error:
            messagebox.showerror("Conversion Error", f"Invalid Hexadecimal Value: {hex_string}\n"
                                                     f"{error}")
    remove_trailing_newlines(hex_text, dec_text, bin_text)


def dec_to_other(hex_text, dec_text, bin_text, number_type_var, little_endian_var, pad_var, show_prefix_var):
    decimal_strings = dec_text.get("1.0", tk.END).strip().splitlines()
    formatted_decimal_strings = []
    hex_text.delete("1.0", tk.END)
    bin_text.delete("1.0", tk.END)
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
            bin_text.insert(tk.END, value.to_bin_string(pad_var.get(), show_prefix_var.get()) + "\n")
        except ValueError as error:
            messagebox.showerror("Conversion Error", f"Invalid Decimal Value: {decimal_string}\n"
                                                     f"{error}")
    # Replace decimal strings in the text box with formatted decimal strings
    dec_text.delete("1.0", tk.END)
    dec_text.insert(tk.END, "\n".join(formatted_decimal_strings) + "\n")
    remove_trailing_newlines(hex_text, dec_text, bin_text)


def bin_to_other(hex_text, dec_text, bin_text, number_type_var, little_endian_var, pad_var, show_prefix_var):
    binary_strings = bin_text.get("1.0", tk.END).strip().splitlines()
    hex_text.delete("1.0", tk.END)
    dec_text.delete("1.0", tk.END)
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
            dec_text.insert(tk.END, value.to_dec_string() + "\n")
        except ValueError as error:
            messagebox.showerror("Conversion Error", f"Invalid Binary Value: {binary_string}\n"
                                                     f"{error}")
    remove_trailing_newlines(hex_text, dec_text, bin_text)


def remove_trailing_newlines(hex_text, dec_text, bin_text):
    """
    Remove trailing newlines from the text boxes
    """
    hex_string = hex_text.get("1.0", tk.END).strip()
    decimal_string = dec_text.get("1.0", tk.END).strip()
    binary_string = bin_text.get("1.0", tk.END).strip()

    # Remove trailing newlines
    hex_text.delete("1.0", tk.END)
    dec_text.delete("1.0", tk.END)
    bin_text.delete("1.0", tk.END)

    # Insert the cleaned strings back into the text boxes
    hex_text.insert(tk.END, hex_string)
    dec_text.insert(tk.END, decimal_string)
    bin_text.insert(tk.END, binary_string)