"""
Universal base class for number formats
"""

import numpy as np

# Define the padding values for hexadecimal representation
pad_nibble_values = np.array([1, 2, 4, 8, 16])

# Define the padding values for binary representation
pad_bit_values = np.array([8, 16, 32, 64, 128])

class UniversalFormat:
    """
    Universal base class for number formats
    """

    def __init__(self):
        """
        Initialize the UniversalFormat object
        """
        self.value = None
        self.value_type = None
        self.min_bits = None

    def set_type(self, type):
        """
        Set the type of the number
        :param type: Type of number (signed, unsigned, floating)
        """
        self.value_type = type

    def from_hex_string(self, hex_string):
        """
        Convert a hexadecimal string representation to the underlying value.
        :param hex_string: Hexadecimal string
        :return: Converted value
        """

        hex_string = self._clean_string(hex_string)

        # Remove 0x prefix if present
        if hex_string.startswith("0x"):
            hex_string = hex_string[2:]

        self.min_bits = len(hex_string) * 4

        # Handle signed and unsigned types
        if self.value_type == "unsigned":
            # Convert to unsigned integer
            self.value = int(hex_string, 16)
        elif self.value_type == "signed":
            # Convert to signed integer
            self.value = int(hex_string, 16)
            if self.value >= 2 ** (4 * len(hex_string) - 1):
                self.value -= 2 ** (4 * len(hex_string))
        elif self.value_type == "floating":
            # Convert to floating point number
            self.value = float.fromhex(hex(int(hex_string, 16)))

        return self.value

    def from_dec_string(self, dec_string):
        """
        Convert a decimal string representation to the underlying value.
        :param dec_string:
        :return:
        """

        dec_string = self._clean_string(dec_string)

        # Handle signed and unsigned types
        if self.value_type == "unsigned":
            # Convert to unsigned integer
            dec_string = dec_string.lstrip('-')
            self.value = int(dec_string)
        elif self.value_type == "signed":
            # Convert to signed integer
            dec_string = dec_string.lstrip('-')
            self.value = int(dec_string)
        elif self.value_type == "floating":
            # Convert to floating point number
            self.value = float(dec_string)

        return self.value

    def from_bin_string(self, bin_string):
        """
        Convert a binary string representation to the underlying value.
        :param bin_string:
        :return:
        """

        bin_string = self._clean_string(bin_string)

        # Remove 0b prefix if present
        if bin_string.startswith("0b"):
            bin_string = bin_string[2:]

        self.min_bits = len(bin_string)

        # Handle signed and unsigned types
        if self.value_type == "unsigned":
            # Convert to unsigned integer
            self.value = int(bin_string, 2)
        elif self.value_type == "signed":
            # Convert to signed integer
            self.value = int(bin_string, 2)
            if self.value >= 2 ** (len(bin_string) - 1):
                self.value -= 2 ** len(bin_string)
        elif self.value_type == "floating":
            # Convert to floating point number
            self.value = float.fromhex(hex(int(bin_string, 2)))

        return self.value

    def _clean_string(self, string):
        """
        Clean the string by removing leading and trailing whitespace
        :param string: Input string
        :return: Cleaned string
        """

        if self.value_type is None:
            raise ValueError("Type must be set before conversion")

        return string.strip()

    def to_hex_string(self, pad=False, show_0x=False):
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
            pad_val = '0' if self.value >= 0 else 'F'
            num_pad = np.min(pad_nibble_values[pad_nibble_values >= len(hex_string)]) - len(hex_string)
            hex_string = pad_val * num_pad + hex_string

        # Add 0x prefix if desired
        if show_0x:
            hex_string = "0x" + hex_string

        return hex_string

    def to_dec_string(self):
        """
                Convert the value to a decimal string representation.
                :return:
                """
        decimal_string = str(self.value)

        return decimal_string

    def to_bin_string(self, pad=False, show_0b=False):
        """
        Convert the value to a binary string representation.
        :param show_0b:
        :param pad:
        :return:
        """
        binary_string = bin(self.value)

        # Remove '0b' and '-0b' prefixes
        if binary_string.startswith("-0b"):
            binary_string = binary_string[3:]
        elif binary_string.startswith("0b"):
            binary_string = binary_string[2:]

        # Pad to minimum bits
        pad_val = '0' if self.value >= 0 else '1'
        if self.min_bits is not None and self.min_bits > len(binary_string):
            num_pad = self.min_bits - len(binary_string)
            # Pad with zeros or ones based on sign
            binary_string = pad_val * num_pad + binary_string

        # Pad the string if desired
        if pad:
            num_pad = np.min(pad_bit_values[pad_bit_values >= len(binary_string)]) - len(binary_string)
            binary_string = pad_val * num_pad + binary_string

        # Add 0b prefix if desired
        if show_0b:
            binary_string = "0b" + binary_string

        return binary_string
