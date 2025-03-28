"""
Class file for decimal representation
"""

class Decimal:
    def __init__(self, value, type="signed"):
        # Define underlying value
        # If string, convert to integer or floating point
        if isinstance(value, str):
            self.value = self.from_string(value, type=type)
        else:
            self.value = value

    def to_string(self):
        """
        Convert the value to a decimal string representation.
        :return:
        """
        decimal_string = str(self.value)

        return decimal_string

    def from_string(self, decimal_string, type="signed"):
        """
        Convert a decimal string representation to the underlying value.
        :param decimal_string:
        :param type: Type of number (signed, unsigned, floating)
        :return:
        """

        # Remove any leading or trailing whitespace
        decimal_string = decimal_string.strip()
        # Handle signed and unsigned types
        if type == "unsigned":
            # Convert to unsigned integer
            decimal_string = decimal_string.lstrip('-')
            self.value = int(decimal_string)
        elif type == "signed":
            # Convert to signed integer
            decimal_string = decimal_string.lstrip('-')
            self.value = int(decimal_string)
        elif type == "floating":
            # Convert to floating point number
            self.value = float(decimal_string)

        return self.value