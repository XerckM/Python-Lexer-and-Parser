# Change this if classes are in different directory
from classes.token import Token
from classes.error import IllegalCharacterError

##########################
# CONSTANTS
##########################

keywords = ['program', 'int', 'print', 'if',
            'then', 'else', 'while', 'do',
            'od', 'fi', 'bool', 'end', 'true',
            'false', 'or', 'and', 'not']
single_char_special = [';', '(', ')', '{', '}', '+', '-', '*', '=']


###########################
# LEXER CLASS
###########################

"""
This class represents a Lexer object.

Most functions in this class is mainly used for the next() function

Following the requirements, libraries like 're' are not allowed.

The actual purpose of this class is to return tokens from the input file.
"""


class Lexer:
    def __init__(self, text):
        self.text = text
        self.idx = -1
        self.line = 1
        self.pos = 0
        self.token = None

    @staticmethod
    def is_alphabet(char):
        """
        This function returns a boolean value if the character
        is a letter
        """
        return ('A' <= char <= 'Z') or ('a' <= char <= 'z')

    def begin_scan(self):
        """
        This function scans the next character by skipping
        all space, tabs, and newline characters
        """
        self.idx += 1

        while self.idx < len(self.text) and self.text[self.idx].isspace() or \
                self.text[self.idx] == '\t' or self.text[self.idx] == '\n':
            if self.text[self.idx] == '\n':
                self.line += 1
                self.pos = 0
            else:
                self.pos += 1
            self.idx += 1

        self.pos += 1
        return '\0' if self.idx == len(self.text) else self.text[self.idx]

    def next_char(self):
        """
        This function simply returns the next character in
        the text whatever character it is
        """
        self.idx += 1
        self. pos += 1
        return '\0' if self.idx == len(self.text) else self.text[self.idx]

    def next(self):
        """
        This function is used to find the next lexeme in the
        text.

        (next() is called to find next lexeme as per requirements)

        It returns a class of Token with its attributes.

        Error is handled by the Error class if there
        are any characters detected which are not allowed
        or encoded in this function. It stops looking for tokens
        once an invalid character is found.
        """

        try:
            peek = self.begin_scan()

            # Checks for characters that start with a letter and has
            # a digit or underscore '_' and concatenates it in a variable
            # if word is not in keywords it is returned as an Identifier else
            # it returns as a token with a type of itself
            if self.is_alphabet(peek):
                word = ''
                while self.is_alphabet(peek) or peek == '_' or peek.isdigit():
                    word += peek
                    peek = self.next_char()
                self.idx -= 1
                self.pos -= 1
                if word not in keywords:
                    self.token = Token('ID', self.line, self.pos - len(word), word)

                else:
                    self.token = Token(word, self.line, self.pos - len(word), word)

            # Checks for characters that start with a number
            elif peek.isdigit():
                num = 0
                digits = 0
                while peek.isdigit():
                    num = 10 * num + int(peek, 10)
                    peek = self.next_char()
                    digits += 1
                self.idx -= 1
                self.pos -= 1
                self.token = Token('NUM', self.line, self.pos - digits, num)

            # OTHER ALLOWED CHARACTERS
            elif peek in single_char_special:
                self.token = Token(peek, self.line, self.pos - 1, peek)

            # ASSIGN CHARACTER OR COLON
            elif peek == ':':
                peek = self.next_char()
                if peek == '=':
                    self.token = Token(':=', self.line, self.pos - 2, ':=')
                else:
                    self.idx -= 1
                    self.pos -= 1
                    self.token = Token(':', self.line, self.pos - 1, ':')

            # GREATER THAN OR EQUAL TO or GREATER THAN CHARACTER
            elif peek == '>':
                peek = self.next_char()
                if peek == '=':
                    self.token = Token('>=', self.line, self.pos - 2, '>=')
                else:
                    self.idx -= 1
                    self.pos -= 1
                    self.token = Token('>', self.line, self.pos - 1, '>')

            # LESS THAN OR EQUAL TO or LESS THAN CHARACTER
            elif peek == '<':
                peek = self.next_char()
                if peek == '=':
                    self.token = Token('<=', self.line, self.pos - 2, '<=')
                else:
                    self.idx -= 1
                    self.pos -= 1
                    self.token = Token('<', self.line, self.pos - 1, '<')

            # NOT EQUAL TO
            # Error found if character is '!' as it is not an accepted character
            elif peek == '!':
                peek = self.next_char()
                if peek == '=':
                    self.token = Token('!=', self.line, self.pos - 2, '!=')
                else:
                    self.idx -= 1
                    self.pos -= 1
                    self.token = Token('end-of-text', self.line, self.pos - 1, 'end-of-text')
                    print(f'\nError at <(Line: {self.line}, Pos: {self.pos - 1}),',
                          IllegalCharacterError("'!'>"))

            # COMMENT HANDLING SECTION
            # This section handles ignoring the rest of the characters found after '//'
            # If the character is just '/' return it as a token with a kind of itself
            elif peek == '/':
                peek = self.next_char()
                str_len = 0
                if peek == '/':
                    while peek != '\n':
                        str_len += 1
                        peek = self.next_char()
                    self.idx -= 1
                    self.pos -= 1
                    self.token = Token('//', self.line, self.pos - str_len - 1, '//')
                else:
                    self.idx -= 1
                    self.pos -= 1
                    self.token = Token('/', self.line, self.pos - 1, '/')

            # Catches illegal characters not handled in the whole function
            # Prints an error along with its line number and position as well
            # as the value of the character
            else:
                self.token = Token('end-of-text', self.line, self.pos - 1, 'end-of-text')
                print(f'\nError at <(Line: {self.line}, Pos: {self.pos - 1}),',
                      IllegalCharacterError("'" + peek + "'>"))

        # Handles IndexError from begin_scan() function
        # (Not an issue in returning tokens but may need fixing in the future)
        except IndexError:
            self.token = Token('end-of-text', self.line, self.pos - 1, 'end-of-text')

        return self.token
