from checker import Checker
from scanner import Scanner
from parser import Parser
import json

fileDir = './example_files/testprogram.txt'


if __name__ == "__main__":
    scanner = Scanner(fileDir)
    parser = Parser(scanner)
    checker = Checker()

    program = parser.parse_program()
    checker.check(program)

    # print(json.dumps(program, default=lambda x: x.__dict__, indent=2))
