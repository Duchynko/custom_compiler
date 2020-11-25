from typing import BinaryIO


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

    def write(self, output: BinaryIO) -> None:
        output.write(self.op_code.to_bytes(4, byteorder='big'))
        output.write(self.register_number.to_bytes(4, byteorder='big'))
        output.write(self.length.to_bytes(4, byteorder='big'))
        output.write(self.operand.to_bytes(4, byteorder='big'))

    def read(self, data_input: BinaryIO) -> 'Instruction':
        inst = Instruction()
        inst.op_code = str(data_input.read())
        inst.register_number = str(data_input.read())
        inst.length = str(data_input.read())
        inst.operand = str(data_input.read())
        return inst
