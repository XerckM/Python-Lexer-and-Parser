from classes.lexer import Lexer

######################
# PARSER
######################


class Parser:
    def __init__(self, text):
        self.lex = Lexer(text)
        self.token = self.lex.next()
        self.ast = dict()

    def parse(self):
        return self.program

    def match(self, value):
        if self.token.kind() == value:
            self.token = self.lex.next()
        else:
            raise Exception(f'At {self.token.position()} I see "{self.token.kind()}" but expected "{value}"')

    def program(self):
        self.match('program')
        self.match('ID')
        self.match(':')
        self.body()
        self.match('end')
        return True

    def body(self):
        if self.token.kind() in ('bool', 'int'):
            self.declarations()
        self.statements()

    def declarations(self):
        self.declaration()
        while self.token.kind() in ('bool', 'int'):
            self.declaration()

    def declaration(self):
        assert self.token.kind() in ('bool', 'int'), \
            f'ERROR! at {self.token.position()}. ' \
            f'Expected "bool" or "int" instead' \
            f'found {self.token.kind()}'
        self.token = self.lex.next()
        self.match('ID')
        self.match(';')

    def statements(self):
        self.statement()
        while self.token.kind() == ';':
            self.token = self.lex.next()
            self.statement()

    def statement(self):
        if self.token.kind() == 'ID':
            self.assignment_statement()
        elif self.token.kind() == 'if':
            self.conditional_statement()
        elif self.token.kind() == 'while':
            self.iterative_statement()
        elif self.token.kind() == 'print':
            self.print_statement()
        else:
            self.expected(('if', 'ID', 'while', 'print'))

    def expected(self, type_list):
        if self.token.kind() not in type_list:
            raise Exception(
                f'ERROR! at {self.token.position()}. Expected to see {type_list}, but see {self.token.kind()}')

    def assignment_statement(self):
        assert self.token.kind() == 'ID', f'Expected "ID" instead found {self.token.kind()}'
        self.match('ID')
        self.match(':=')
        self.expr()

    def conditional_statement(self):
        self.match('if')
        self.expr()
        self.match('then')
        self.body()
        if self.token.kind() == 'else':
            self.token = self.lex.next()
            self.body()
        self.match('fi')

    def expr(self):
        self.simple_expr()
        if self.token.kind() in ('<', '>', '<=', '>=', '!=', '='):
            self.token = self.lex.next()
            self.simple_expr()

    def simple_expr(self):
        self.term()
        while self.token.kind() in ('+', '-', 'or'):
            self.token = self.lex.next()
            self.term()

    # Needs fixing
    def term(self):
        self.factor()
        while self.token.kind() in ('*', '/', 'and'):
            self.token = self.lex.next()
            self.factor()

    def factor(self):
        if self.token.kind() in ('-', 'not'):
            self.token = self.lex.next()
        if self.token.kind() in ('true', 'false', 'NUM'):
            self.literal()
        elif self.token.kind() == 'ID':
            self.token = self.lex.next()
        elif self.token.kind() == '(':
            self.token = self.lex.next()
            self.expr()
            self.match(')')
        else:
            self.expected(['true', 'false', 'NUM', 'ID', ')'])

    def literal(self):
        assert self.token.kind() in ('true', 'false', 'NUM'), \
            f'ERROR! at {self.token.position()}.' \
            f'Expected "true" or "false" or "NUM" instead' \
            f'found {self.token.kind()}'
        if self.token.kind() == 'NUM':
            self.token = self.lex.next()
        else:
            self.boolean_literal()

    def boolean_literal(self):
        if self.token.kind() in ('true ', 'false'):
            self.token = self.lex.next()
        else:
            raise Exception(f'ERROR! at {self.token.position()}. At position Expected "true" or "false" or "NUM" '
                            f'instead found {self.token.kind()}')

    def iterative_statement(self):
        self.match('while')
        self.expr()
        self.match('do')
        self.body()

    def print_statement(self):
        if self.token.kind() == 'print':
            self.token = self.lex.next()
            self.expr()
