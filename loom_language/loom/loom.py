import sys
import os

# Add the parent directory containing loom.py to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

def main():
    while True:
        try:
            text = input('loom> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)

if __name__ == '__main__':
    main()
