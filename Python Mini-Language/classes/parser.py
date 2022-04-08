from classes.lexer import Lexer
from classes.error import IllegalSyntaxError

######################
# PARSER
######################


class Parser:
    def __init__(self, text):
        self.lex = Lexer(text)
        self.token = self.lex.next()

    def parse_program(self):
        pass

    def is_identifier(self):
        ok = False
        try:
            if self.token.kind() == 'ID':
                ok = True
        except AttributeError:
            pass
        return ok
