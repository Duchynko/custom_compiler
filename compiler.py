from checker import Checker
from scanner import Scanner
from parser import Parser
from encoder import Encoder

fileDir = './example_files/prog1.txt'


if __name__ == "__main__":
    scanner = Scanner(fileDir)
    parser = Parser(scanner)
    checker = Checker()
    encoder = Encoder()

    program = parser.parse_program()
    checker.check(program)
    encoder.encode(program)
    encoder.save_target_program('examples_files/prog1.tam')

    # print(json.dumps(program, default=lambda x: x.__dict__, indent=2))
