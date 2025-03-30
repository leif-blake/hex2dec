"""
Functions to handle ui events
"""

from PyQt6.QtWidgets import QMessageBox
from universal_format import UniversalFormat


def hex_to_other(hex_string, pad=False, show_prefix=False, little_endian=False,
                 is_unsigned=True, is_signed=False, is_float=False):
    """Convert hexadecimal to other formats"""

    # Determine number type
    if is_unsigned:
        number_type = "unsigned"
    elif is_signed:
        number_type = "signed"
    elif is_float:
        number_type = "floating"
    else:
        number_type = "unsigned"  # default

    hex_strings = hex_string.strip().splitlines()
    dec_results = []
    bin_results = []

    value = UniversalFormat()
    value.set_type(number_type)
    if little_endian:
        value.set_endianness('little')

    for hex_str in hex_strings:
        try:
            value.from_hex_string(hex_str)
            dec_results.append(value.to_dec_string())
            bin_results.append(value.to_bin_string(pad, show_prefix))
        except ValueError as error:
            QMessageBox.critical(None, "Conversion Error",
                                 f"Invalid Hexadecimal Value: {hex_str}\n{error}")
            return None, None

    return "\n".join(dec_results), "\n".join(bin_results)


def dec_to_other(dec_string, pad=False, show_prefix=False, little_endian=False,
                 is_unsigned=True, is_signed=False, is_float=False):
    """Convert decimal to other formats"""

    # Determine number type
    if is_unsigned:
        number_type = "unsigned"
    elif is_signed:
        number_type = "signed"
    elif is_float:
        number_type = "floating"
    else:
        number_type = "unsigned"  # default

    decimal_strings = dec_string.strip().splitlines()
    hex_results = []
    bin_results = []
    formatted_decs = []

    value = UniversalFormat()
    value.set_type(number_type)
    if little_endian:
        value.set_endianness('little')

    for dec_str in decimal_strings:
        try:
            # Format decimal string based on number type
            if '.' in dec_str and number_type != "floating":
                dec_str = str(int(float(dec_str)))
            if '-' in dec_str and number_type == "unsigned":
                dec_str = str(abs(int(dec_str)))
            formatted_decs.append(dec_str)

            value.from_dec_string(dec_str)
            hex_results.append(value.to_hex_string(pad, show_prefix))
            bin_results.append(value.to_bin_string(pad, show_prefix))
        except ValueError as error:
            QMessageBox.critical(None, "Conversion Error",
                                 f"Invalid Decimal Value: {dec_str}\n{error}")
            return None, None, None

    return "\n".join(hex_results), "\n".join(formatted_decs), "\n".join(bin_results)


def bin_to_other(bin_string, pad=False, show_prefix=False, little_endian=False,
                 is_unsigned=True, is_signed=False, is_float=False):
    """Convert binary to other formats"""

    # Determine number type
    if is_unsigned:
        number_type = "unsigned"
    elif is_signed:
        number_type = "signed"
    elif is_float:
        number_type = "floating"
    else:
        number_type = "unsigned"  # default

    binary_strings = bin_string.strip().splitlines()
    hex_results = []
    dec_results = []

    value = UniversalFormat()
    value.set_type(number_type)
    if little_endian:
        value.set_endianness('little')

    for bin_str in binary_strings:
        try:
            value.from_bin_string(bin_str)
            hex_results.append(value.to_hex_string(pad, show_prefix))
            dec_results.append(value.to_dec_string())
        except ValueError as error:
            QMessageBox.critical(None, "Conversion Error",
                                 f"Invalid Binary Value: {bin_str}\n{error}")
            return None, None

    return "\n".join(hex_results), "\n".join(dec_results)