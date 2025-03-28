"""
Class file for binary representation
"""

import numpy as np

# Define the padding values for binary representation
pad_bit_values = np.array([8, 16, 32, 64, 128])

class Binary:
    def __init__(self, value, type="signed"):
        # Define underlying value
        # If string, convert to integer or floating point
        if isinstance(value, str):
            self.value = self.from_string(value, type=type)
        else:
            self.value = value

    def to_string(self, pad=False, show_0b=False):
        """
        Convert the value to a binary string representation.
        :param show_0b:
        :param pad:
        :return:
        """
        binary_string = bin(self.value)[2:]

        # Pad the string if desired
        if pad:
            binary_string = binary_string.zfill(np.min(pad_bit_values[pad_bit_values >= len(binary_string)]))

        # Add 0b prefix if desired
        if show_0b:
            binary_string = "0b" + binary_string

        return binary_string

    def from_string(self, binary_string, type="signed"):
        """
        Convert a binary string representation to the underlying value.
        :param binary_string:
        :param type: Type of number (signed, unsigned, floating)
        :return:
        """
        # Remove 0b prefix if present
        if binary_string.startswith("0b"):
            binary_string = binary_string[2:]

        # Handle signed and unsigned types
        if type == "unsigned":
            # Convert to unsigned integer
            self.value = int(binary_string, 2)
        elif type == "signed":
            # Convert to signed integer
            self.value = int(binary_string, 2)
            if self.value >= 2**(len(binary_string) - 1):
                self.value -= 2**len(binary_string)
        elif type == "floating":
            # Convert to floating point number
            self.value = float.fromhex(hex(int(binary_string, 2)))

        return self.value

