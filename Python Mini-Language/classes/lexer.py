# Change this if classes are in different directory
from classes.token import Token
from classes.error import IllegalCharacterError

###########################
# LEXER CLASS
###########################

"""
This class represents a Lexer object.

Most functions in this class is mainly used for the next() function

Following the requirements, libraries like 're' are not allowed.

The purpose of this class is to return tokens from the input file.
"""


class Lexer:

    KEYWORDS = frozenset(['program', 'int', 'print', 'if',
                          'then', 'else', 'while', 'do',
                          'od', 'fi', 'bool', 'end', 'true',
                          'false', 'or', 'and', 'not'])

    def __init__(self, text):
        self.text = text
        self.idx = -1
        self.line = 1
        self.pos = 0
        self.token = None

    def next_char(self):
        """
        This function simply returns the next character in
        the text.

        If self.idx is equal to the length of text it returns 'EOF'
        which will be a token as an end of file.
        """
        self.idx += 1
        self.pos += 1
        if self.idx == len(self.text):
            return 'EOF'
        return self.text[self.idx]

    def next(self):
        """
        This function is used to find the next lexeme in the
        text and returns a Token class with its attributes.

        (next() is called to find next lexeme as per requirements)

        Returns an error if there are any characters detected which
        are not allowed or encoded in this function. It stops looking for tokens
        once an invalid character is found.
        """
        peek = self.next_char()
        match peek:
            case peek if peek.isalpha() and peek != 'EOF':
                word = ''
                while peek.isalpha() or peek == '_' or peek.isdigit():
                    word += peek
                    peek = self.next_char()
                    if peek == 'EOF':
                        break
                self.idx -= 1
                self.pos -= 1
                if word not in Lexer.KEYWORDS:
                    self.token = Token('ID', self.line, self.pos - len(word), word)
                else:
                    self.token = Token(word, self.line, self.pos - len(word), word)
            case peek if peek.isdigit():
                num = 0
                digits = 0
                while peek.isdigit():
                    num = 10 * num + int(peek, 10)
                    peek = self.next_char()
                    digits += 1
                self.idx -= 1
                self.pos -= 1
                self.token = Token('NUM', self.line, self.pos - digits, num)
            case '/':
                peek = self.next_char()
                str_len = 0
                if peek == '/':
                    while peek != '\n':
                        str_len += 1
                        peek = self.next_char()
                    self.idx -= 1
                    self.pos -= 1
                    self.next()
                else:
                    self.idx -= 1
                    self.pos -= 1
                    self.token = Token('/', self.line, self.pos - 1, '/')
            case ':':
                peek = self.next_char()
                if peek == '=':
                    self.token = Token(':=', self.line, self.pos - 2, ':=')
                else:
                    self.idx -= 1
                    self.pos -= 1
                    self.token = Token(':', self.line, self.pos - 1, ':')
            case '>':
                peek = self.next_char()
                if peek == '=':
                    self.token = Token('>=', self.line, self.pos - 2, '>=')
                else:
                    self.idx -= 1
                    self.pos -= 1
                    self.token = Token('>', self.line, self.pos - 1, '>')
            case '<':
                peek = self.next_char()
                if peek == '=':
                    self.token = Token('<=', self.line, self.pos - 2, '<=')
                else:
                    self.idx -= 1
                    self.pos -= 1
                    self.token = Token('<', self.line, self.pos - 1, '<')
            case '!':
                peek = self.next_char()
                if peek == '=':
                    self.token = Token('!=', self.line, self.pos - 2, '!=')
                else:
                    print(f'\nError at <(Line: {self.line}, Pos: {self.pos - 2}),',
                          IllegalCharacterError("'!'>"))
                    self.token = Token('EOF', self.line, self.pos - 1, 'EOF')
            case ';':
                self.token = Token(peek, self.line, self.pos - 1, peek)
            case '(':
                self.token = Token(peek, self.line, self.pos - 1, peek)
            case ')':
                self.token = Token(peek, self.line, self.pos - 1, peek)
            case '+':
                self.token = Token(peek, self.line, self.pos - 1, peek)
            case '-':
                self.token = Token(peek, self.line, self.pos - 1, peek)
            case '*':
                self.token = Token(peek, self.line, self.pos - 1, peek)
            case '=':
                self.token = Token(peek, self.line, self.pos - 1, peek)
            case '\n':
                self.line += 1
                self.pos = 0
                return self.next()
            case peek if peek.isspace():
                return self.next()
            case 'EOF':
                self.token = Token('EOF', self.line, self.pos - 1, 'EOF')
            case _:
                print(f'\nError at <(Line: {self.line}, Pos: {self.pos - 1}),',
                      IllegalCharacterError("'" + peek + "'>"))
                self.token = Token('EOF', self.line, self.pos - 1, 'EOF')

        return self.token

    def kind(self):
        return self.token.kind()

    def position(self):
        return self.token.position()

    def value(self):
        return self.token.value()
