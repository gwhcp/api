import math


class ConvertBytes:
    def __init__(self, data):
        """
        Convert Bytes

        :param int data: Data to convert
        """

        self.data = data

        if data is None:
            raise ValueError('Missing data parameter.')

        if type(self.data) is not int:
            raise TypeError('Data should be an INT')

    def to_kb(self):
        return math.ceil(self.data * 1024)

    def to_mb(self):
        return math.ceil(self.data / 1024)
