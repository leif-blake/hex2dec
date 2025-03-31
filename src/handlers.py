"""
Functions to handle ui events
"""

from PyQt6.QtWidgets import QMessageBox
from number_list import NumberList


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

    # Create a NumberList object to handle the conversion
    number_list = NumberList()

    try:
        if little_endian:
            number_list.parse_numbers(hex_string, "hex", number_type, endianness='little')
        else:
            number_list.parse_numbers(hex_string, "hex", number_type, endianness='big')

        hex_result = number_list.to_hex_string(pad=pad, show_0x=show_prefix)
        dec_result = number_list.to_dec_string()
        bin_result = number_list.to_bin_string(pad=pad, show_0b=show_prefix)
    except ValueError as error:
        QMessageBox.critical(None, "Conversion Error",
                             f"Invalid Hexadecimal Value\n{error}")
        return None, None, None

    return hex_result, dec_result, bin_result


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

    # Create a NumberList object to handle the conversion
    number_list = NumberList()

    try:
        if little_endian:
            number_list.parse_numbers(dec_string, "dec", number_type, endianness='little')
        else:
            number_list.parse_numbers(dec_string, "dec", number_type, endianness='big')

        hex_result = number_list.to_hex_string(pad=pad, show_0x=show_prefix)
        dec_result = number_list.to_dec_string()
        bin_result = number_list.to_bin_string(pad=pad, show_0b=show_prefix)
    except ValueError as error:
        QMessageBox.critical(None, "Conversion Error",
                             f"Invalid Decimal Value\n{error}")
        return None, None, None

    return hex_result, dec_result, bin_result


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

    # Create a NumberList object to handle the conversion
    number_list = NumberList()

    try:
        if little_endian:
            number_list.parse_numbers(bin_string, "bin", number_type, endianness='little')
        else:
            number_list.parse_numbers(bin_string, "bin", number_type, endianness='big')

        hex_result = number_list.to_hex_string(pad=pad, show_0x=show_prefix)
        dec_result = number_list.to_dec_string()
        bin_result = number_list.to_bin_string(pad=pad, show_0b=show_prefix)
    except ValueError as error:
        QMessageBox.critical(None, "Conversion Error",
                             f"Invalid Binary Value\n{error}")
        return None, None, None

    return hex_result, dec_result, bin_result