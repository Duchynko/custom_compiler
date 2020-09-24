from scanner import SourceFile, Scanner
from tokens import Token, TokenType

fileDir = './example_files/testprogram.txt'

if __name__ == "__main__":
    scanner = Scanner(fileDir)
    token = scanner.scan()

    while token.tokenType != TokenType.EOT:
        print(f"{token.tokenType}: {token.spelling}")
        token = scanner.scan()
