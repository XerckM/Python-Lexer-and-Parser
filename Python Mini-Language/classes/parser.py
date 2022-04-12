from classes.lexer import Lexer
from classes.error import InvalidSyntaxError


######################
# PARSER
######################


class Parser:
    def __init__(self, text):
        self.tok_pos = None
        self.tok_line = None
        self.tok_val_len = None
        self.lex = Lexer(text)
        self.token = None

    def parse(self):
        return self.program()

    def program(self):
        self.token = self.lex.next()
        match self.token.kind():
            case 'COMMENT':
                return self.program()
            case 'program':
                return self.identifier()
            case 'end':
                return True
            case _:
                return InvalidSyntaxError(self.token.position())

    def identifier(self):
        self.token = self.lex.next()
        if self.token.kind() == 'ID':
            self.tok_pos = self.token.position_
            self.tok_line = self.token.line
            self.tok_val_len = len(self.token.value_)
            return self.close_tok()
        else:
            return InvalidSyntaxError(self.token.position())

    def close_tok(self):
        self.token = self.lex.next()
        match self.token.kind():
            case ':':
                return self.body()
            case ';':
                return self.body()
            case _:
                return InvalidSyntaxError(f'(Line: {self.tok_line}, {self.tok_val_len + self.tok_pos})')

    def body(self):
        # return 'Program Body here!'
        self.token = self.lex.next()
        match self.token.kind():
            case ('int' | 'bool'):
                return self.declarations()
            case 'ID':
                return self.assign_stmt()
            case 'print':
                return self.print_stmt()
            case _:
                return InvalidSyntaxError(self.token.position())

    def print_stmt(self):
        self.token = self.lex.next()
        match self.token.kind():
            case
            case _:
                return InvalidSyntaxError(self.token.position())

    def declarations(self):
        return 'Declarations!'

    def declaration(self):
        pass
