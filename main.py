from scanner import SourceFile, Scanner
from tokens import Token, TokenType
from parser import Parser

fileDir = './example_files/testprogram.txt'

if __name__ == "__main__":
    scanner = Scanner(fileDir)
    parser = Parser(scanner)

    parser.parse_program()
