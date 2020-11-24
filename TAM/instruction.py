import io


class Instruction:
    """
    Represents an TAM instruction

    Attributes:
        op_code (int): One of operation codes defined in machine.py
        register_number (int): Number of a register ranging from 0 to 15
        length (int): A length of an instruction ranging from 0 to 255 {8 bits unsigned}
        operand (int): An operand size ranging from -32767 to +32767 {16 bits signed}
    """
    def __init__(self):
        self.op_code = 0
        self.register_number = 0
        self.length = 0
        self.operand = 0

    def write(self, output: io.TextIOBase) -> None:
        output.write(str(self.op_code))
        output.write(str(self.register_number))
        output.write(str(self.length))
        output.write(str(self.operand))

    def read(self, data_input: io.TextIOBase) -> 'Instruction':
        inst = Instruction()
        inst.op_code = str(data_input.read())
        inst.register_number = str(data_input.read())
        inst.length = str(data_input.read())
        inst.operand = str(data_input.read())
        return inst

    def __uint_to_bytes(self, x: int) -> bytes:
        """
        Converts an unsigned integer to bytes array

        Args:
            x: an unsigned integer to convert

        Returns: bytes array
        """
        return x.to_bytes((x.bit_length() + 7) // 8, 'big')

    def __bytes_to_uint(self, b: bytes) -> int:
        """
        Converts bytes array to an unsigned integer

        Args:
            b: a bytes array to convert

        Returns: an unsigned integer
        """
        return int.from_bytes(b, 'big')

    def __int_to_bytes(self, x: int) -> bytes:
        """
        Converts a signed integer to bytes array

        Args:
            x: a signed integer to convert

        Returns: a bytes array
        """
        return x.to_bytes((x.bit_length() + 7) // 8, 'big')

    def __bytes_to_int(self, b: bytes) -> int:
        """
        Converts bytes array to a signed integer

        Args:
            b: a bytes array to convert

        Returns: a signed integer
        """
        return int.from_bytes(b, 'big')
