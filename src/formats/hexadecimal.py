"""
Class file for hexadecimal representation
"""

import numpy as np

# Define the padding values for hexadecimal representation
pad_nibble_values = np.array([1, 2, 4, 8, 16])

class Hexadecimal:
    def __init__(self, value, type="signed"):
        # Define underlying value
        # If string, convert to integer or floating point
        if isinstance(value, str):
            self.value = self.from_string(value, type=type)
        else:
            self.value = value

    def to_string(self, pad=False, show_0x=False):
        """
        Convert the value to a hexadecimal string representation.
        :param pad:
        :param show_0x:
        :return:
        """
        # Convert to hexadecimal string
        hex_string = hex(self.value)[2:]

        # Pad the string if desired
        if pad:
            hex_string = hex_string.zfill(np.min(pad_nibble_values[pad_nibble_values >= len(hex_string)]))

        # Add 0x prefix if desired
        if show_0x:
            hex_string = "0x" + hex_string

        return hex_string

    def from_string(self, hex_string, type="signed"):
        """
        Convert a hexadecimal string representation to the underlying value.
        :param hex_string:
        :param type: Type of number (signed, unsigned, floating)
        :return:
        """
        # Remove 0x prefix if present
        if hex_string.startswith("0x"):
            hex_string = hex_string[2:]

        # Handle signed and unsigned types
        if type == "unsigned":
            # Convert to unsigned integer
            value = int(hex_string, 16)
        elif type == "signed":
            # Convert to signed integer
            value = int(hex_string, 16)
            if value >= 2**(4 * len(hex_string) - 1):
                value -= 2**(4 * len(hex_string))
        elif type == "floating":
            # Convert to floating point number
            value = float.fromhex(hex(int(hex_string, 16)))

        return value