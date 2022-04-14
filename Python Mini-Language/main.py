from classes.lexer import Lexer
from classes.parser import Parser
import os
import sys
import time


##########################
# MAIN
##########################

def lexer_test(text):
    """
    Test lexer here
    """
    kind = 'Kind'
    position = 'Position'
    value = 'Value'
    tk = 'TOKENS'

    print(f'\n\n{tk : ^54}\n=======================================================\n' +
          f'{position : ^17}{kind : ^20}{value : ^14}\n' +
          '=======================================================')

    lex = Lexer(text)
    token = lex.next()

    while token.kind() != 'EOF':
        print(f'{token.position() : <24} {token.kind() : <15} {token.value() : <20}')
        print('-------------------------------------------------------')
        token = lex.next()


def parser_test(text):
    """
    Test parser here
    """
    lexer = Lexer(text)
    parser = Parser(lexer)
    print(parser.program())


def main():
    # while True:  # uncomment and wrap all the code segment below for repeated filename input
    # filename = input('\nEnter filename: ')  # uncomment this and replace string below with 'filename' for input

    with open(os.path.join(sys.path[0], 'test cases\\b.txt')) as file:  # change input file here manually
        text = file.read()

    start_time = time.time()

    # lexer_test(text)      # lexer test
    parser_test(text)       # parser test

    print("\n--- Program finished in %.6s seconds ---" % (time.time() - start_time))  # testing code runtime


main()
