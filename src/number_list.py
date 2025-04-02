"""
Class file to store list of numbers and their positions in a text string
"""

from PySide6.QtWidgets import QMessageBox

from universal_format import UniversalFormat

class NumberList:
    """
    Class to store a list of numbers and their positions in a text string
    """
    def __init__(self):
        """
        Initialize the NumberList object
        """
        self.input_string = ""
        self.numbers = []
        self.positions = []
        self.input_number_lengths = []

    def parse_numbers(self, text_string, number_format, value_type, endianness='big'):
        """
        Parse numbers from the text string.
        :param text_string: Text string to parse
        :param number_format: Format of the numbers (hex, dec, bin)
        :param value_type: Type of the numbers (unsigned, signed, floating)
        :param endianness: Endianness of the numbers (big, little)
        :return: List of UniversalFormat objects
        """
        self.input_string = text_string

        numbers = []
        positions = []
        input_number_lengths = []

        delimiters = [' ', ',', '\n', '\r', '\t', ';', ':', '[', ']', '{', '}', '(', ')']
        allowed_hex = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'A', 'B', 'C', 'D', 'E', 'F']
        allowed_bin = ['0', '1']
        allowed_dec = ['-', '.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        allowed_hex_start = ['0x', '0X', '$']
        allowed_bin_start = ['0b', '0B', '%']

        # Set appropriate allowed characters based on number format
        if number_format == "hex":
            allowed_chars = allowed_hex
        elif number_format == "dec":
            allowed_chars = allowed_dec
        elif number_format == "bin":
            allowed_chars = allowed_bin
        else:
            raise ValueError("Invalid number format")

        # Replace delimiters with spaces for easier splitting
        for delimiter in delimiters:
            text_string = text_string.replace(delimiter, ' ')

        # Split the string into words
        word_pos = 0
        words = text_string.split(' ')
        for word in words:
            # Skip empty strings
            if not word:
                word_pos += len(word) + 1  # +1 for delimiter
                continue

            try:
                # Check if the word has a valid prefix
                if number_format == "hex" and any(word.startswith(prefix) for prefix in allowed_hex_start):
                    word_without_prefix = word[2:] if word.startswith(('0x', '0X')) else word[1:] if word.startswith('$') else word
                    if not all(char in allowed_chars for char in word_without_prefix):
                        word_pos += len(word) + 1
                        continue
                elif number_format == "bin" and any(word.startswith(prefix) for prefix in allowed_bin_start):
                    word_without_prefix = word[2:] if word.startswith(('0b', '0B')) else word[1:] if word.startswith('%') else word
                    if not all(char in allowed_chars for char in word_without_prefix):
                        word_pos += len(word) + 1
                        continue
                # If no prefix, check if all characters are allowed
                elif not all(char in allowed_chars for char in word):
                    word_pos += len(word) + 1
                    continue

                # Create a UniversalFormat object
                uf = UniversalFormat()
                uf.set_type(value_type)
                uf.set_endianness(endianness)

                # Parse based on format
                if number_format == "hex":
                    uf.from_hex_string(word)
                elif number_format == "dec":
                    uf.from_dec_string(word)
                elif number_format == "bin":
                    uf.from_bin_string(word)
                else:
                    # Try to autodetect
                    if word.lower().startswith(('0x', '$')):
                        uf.from_hex_string(word)
                    elif word.lower().startswith(('0b', '%')):
                        uf.from_bin_string(word)
                    else:
                        uf.from_dec_string(word)

                numbers.append(uf)
                positions.append(word_pos)
                input_number_lengths.append(len(word))

            except ValueError as error:
                QMessageBox.critical(None, "Conversion Error",
                                     f"Invalid Value: {word}\n{error}")

            # Update position for next word
            word_pos += len(word) + 1  # +1 for space

        self.numbers = numbers
        self.positions = positions
        self.input_number_lengths = input_number_lengths

    def to_hex_string(self, pad=False, show_0x=False):
        """
        Replace all numbers in the input string with their hexadecimal representations.

        :param pad: Whether to pad the hex strings to a power of 2
        :param show_0x: Whether to show the '0x' prefix
        :return: The input string with numbers replaced by hex strings
        """
        if not self.input_string:
            return ""

        if not self.numbers:
            return self.input_string

        # Make a copy of the input string
        result = self.input_string

        # Process numbers in reverse order to avoid position shifts
        for i in range(len(self.numbers) - 1, -1, -1):
            hex_str = self.numbers[i].to_hex_string(pad=pad, show_0x=show_0x)
            pos = self.positions[i]
            length = self.input_number_lengths[i]

            # Replace the original number with the hex string
            result = result[:pos] + hex_str + result[pos + length:]

        return result

    def to_dec_string(self):
        """
        Replace all numbers in the input string with their decimal representations.

        :return: The input string with numbers replaced by decimal strings
        """
        if not self.input_string:
            return ""

        if not self.numbers:
            return self.input_string

        # Make a copy of the input string
        result = self.input_string

        # Process numbers in reverse order to avoid position shifts
        for i in range(len(self.numbers) - 1, -1, -1):
            dec_str = self.numbers[i].to_dec_string()
            pos = self.positions[i]
            length = self.input_number_lengths[i]

            # Replace the original number with the decimal string
            result = result[:pos] + dec_str + result[pos + length:]

        return result

    def to_bin_string(self, pad=False, show_0b=False):
        """
        Replace all numbers in the input string with their binary representations.
        :param pad: Whether to pad the binary strings to a power of 2
        :param show_0b: Whether to show the '0b' prefix
        :return:
        """
        if not self.input_string:
            return ""

        if not self.numbers:
            return self.input_string

        # Make a copy of the input string
        result = self.input_string

        # Process numbers in reverse order to avoid position shifts
        for i in range(len(self.numbers) - 1, -1, -1):
            bin_str = self.numbers[i].to_bin_string(pad=pad, show_0b=show_0b)
            pos = self.positions[i]
            length = self.input_number_lengths[i]

            # Replace the original number with the binary string
            result = result[:pos] + bin_str + result[pos + length:]

        return result