"""
Universal base class for number formats
"""

import numpy as np
import struct

# Define the padding values for hexadecimal representation
pad_nibble_values = np.array([2, 4, 8, 16])

# Define the padding values for binary representation
pad_bit_values = np.array([8, 16, 32, 64, 128])

# Allowed bit values for floating point
float_bit_values = np.array([32])

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

        # Convert to underlying value
        if self.value_type == "unsigned":
            # Convert to unsigned integer
            self.value = int(hex_string, 16)
        elif self.value_type == "signed":
            # Convert to signed integer
            self.value = int(hex_string, 16)
            if self.value >= 2 ** (4 * len(hex_string) - 1):
                self.value -= 2 ** (4 * len(hex_string))
        elif self.value_type == "floating":
            if len(hex_string) * 4 not in float_bit_values:
                raise ValueError("Unsupported length for floating point value")
            # Convert to floating point number
            self.value = struct.unpack('!f', bytes.fromhex(hex_string))[0]

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
            if len(bin_string) not in float_bit_values:
                raise ValueError("Unsupported length for floating point value")
            self.value = struct.unpack('!f', int(bin_string, 2).to_bytes(4, byteorder='big'))[0]

        return self.value

    def to_hex_string(self, pad=False, show_0x=False):
        """
        Convert the value to a hexadecimal string representation.
        :param pad:
        :param show_0x:
        :return:
        """
        self._check_value()

        if self.value_type == "unsigned":
            hex_string = hex(self.value)
        elif self.value_type == "signed":
            if self.value >= 0:
                min_bits_signed = np.min(pad_bit_values[pad_bit_values >= np.log2((np.abs(self.value) + 1) * 2)])
                self.min_bits = max(self.min_bits, min_bits_signed) if self.min_bits is not None else min_bits_signed
                hex_string = hex(self.value)
            else:
                min_bits_signed = np.min(pad_bit_values[pad_bit_values >= np.log2(np.abs(self.value) * 2)])
                hex_string = hex(2**min_bits_signed + self.value)
        elif self.value_type == "floating":
            hex_string = hex(struct.unpack('<I', struct.pack('<f', self.value))[0])[2:]

        # Remove '0x' and '-0x' prefixes
        if hex_string.startswith("-0x"):
            hex_string = hex_string[3:]
        elif hex_string.startswith("0x"):
            hex_string = hex_string[2:]

        pad_val = '0' if self.value >= 0 else 'f'

        # Pad to minimum nibbles
        if self.min_bits is not None and self.min_bits > len(hex_string) * 4:
            num_pad = self.min_bits // 4 - len(hex_string)
            hex_string = pad_val * num_pad + hex_string

        # Pad the string if desired
        if pad:
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
        self._check_value()
        decimal_string = str(self.value)

        return decimal_string

    def to_bin_string(self, pad=False, show_0b=False):
        """
        Convert the value to a binary string representation.
        :param show_0b:
        :param pad:
        :return:
        """
        self._check_value()
        if self.value_type == "unsigned":
            bin_string = bin(self.value)
        elif self.value_type == "signed":
            if self.value >= 0:
                min_bits_signed = np.min(pad_bit_values[pad_bit_values >= np.log2((np.abs(self.value) + 1) * 2)])
                self.min_bits = max(self.min_bits, min_bits_signed) if self.min_bits is not None else min_bits_signed
                bin_string = bin(self.value)
            else:
                min_bits_signed = np.min(pad_bit_values[pad_bit_values >= np.log2(np.abs(self.value) * 2)])
                bin_string = bin(2**min_bits_signed + self.value)
        elif self.value_type == "floating":
            bin_string = bin(struct.unpack('!I', struct.pack('!f', self.value))[0])[2:]
            # Pad to nearest value in float_bit_values
            if len(bin_string) < np.max(float_bit_values):
                pad_num = np.min(float_bit_values[float_bit_values >= len(bin_string)]) - len(bin_string)
                bin_string = '0' * pad_num + bin_string

        # Remove '0b' and '-0b' prefixes
        if bin_string.startswith("-0b"):
            bin_string = bin_string[3:]
        elif bin_string.startswith("0b"):
            bin_string = bin_string[2:]

        # Pad to minimum bits
        pad_val = '0' if self.value >= 0 else '1'
        if self.min_bits is not None and self.min_bits > len(bin_string):
            num_pad = self.min_bits - len(bin_string)
            # Pad with zeros or ones based on sign
            bin_string = pad_val * num_pad + bin_string

        # Pad the string if desired
        if pad:
            num_pad = np.min(pad_bit_values[pad_bit_values >= len(bin_string)]) - len(bin_string)
            bin_string = pad_val * num_pad + bin_string

        # Add 0b prefix if desired
        if show_0b:
            bin_string = "0b" + bin_string

        return bin_string

    def _clean_string(self, string):
        """
        Clean the string by removing leading and trailing whitespace
        :param string: Input string
        :return: Cleaned string
        """

        if self.value_type is None:
            raise ValueError("Type must be set before conversion")

        return string.strip()

    def _check_value(self):
        """
        Check if the value is set
        :return:
        """
        if self.value is None:
            raise ValueError("Value must be set before conversion")
        if self.value_type is None:
            raise ValueError("Type must be set before conversion")

        return True
