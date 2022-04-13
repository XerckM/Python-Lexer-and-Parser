from classes.lexer import Lexer

######################
# PARSER
######################


class Parser:
    def __init__(self, text):
        self.lex = Lexer(text)
        self.token = self.lex.next()
        self.op = None

    def parse(self):
        return self.program()

    def match(self, value):
        if self.token.kind() == value:
            self.token = self.lex.next()
        else:
            return f'<At {self.token.position()} I see {self.token.kind()} \
                   but expected {value}>'

    def program(self):
        while self.token.kind() == 'COMMENT':
            self.match('COMMENT')
        self.match('program')
        self.match('ID')
        self.match(':')
        self.body()
        self.match('end')
        print('True')

    def body(self):
        if self.token.kind() == ('bool' or 'int'):
            self.declarations()
        self.statements()

    def declarations(self):
        self.declaration()
        while self.token.kind() == ('bool' or 'int'):
            self.declaration()

    def declaration(self):
        assert self.token.kind() == ('bool' or 'int'), f'Expected \
               "bool" or "int" instead found {self.token.kind()}'
        self.token = self.lex.next()
        self.match('ID')
        self.match(';')

    def statements(self):
        self.statement()
        while self.token.kind() == ';':
            self.token = self.lex.next()
            self.statement()

    def statement(self):
        match self.token.kind():
            case 'ID':
                self.assignment_statement()
            case 'if':
                self.conditional_statement()
            case 'while':
                self.iterative_statement()
            case 'print':
                self.print_statement()
            case _:
                self.expected(['if', 'ID', 'while', 'print'])

    def expected(self, type_list):
        if self.token.kind() not in type_list:
            return f'ERROR! at {self.token.position()}. Expected to see \
                   {type_list}, but see {self.token.kind()}'

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
            self.body()
        self.match('fi')

    def expr(self):
        self.simple_expr()
        if self.token.kind() in ['<', '>', '<=', '>=', '!=', '=']:
            self.token = self.lex.next()
            self.simple_expr()

    def simple_expr(self):
        self.term()
        while self.token.kind() is ('+' or '-' or 'or'):
            self.token = self.lex.next()
            self.term()

    # Needs fixing
    def term(self):
        self.factor()
        while self.token.kind() is ('*' or '/' or 'and'):
            op = self.token.kind()
            self.token = self.lex.next()
            t = self.factor()

    def factor(self):
        match self.token.kind():
            case ('+' | '-'):
                tok = self.token.kind()
                self.token = self.lex.next()
                return tok
            case ('true' | 'false' | 'NUM'):
                tok = self.token.kind()
                self.literal()
                return tok
            case 'ID':
                self.token = self.lex.next()
            case '(':
                tok = self.token.kind()
                self.token = self.lex.next()
                self.expr()
                self.match(')')
            case _:
                self.expected(['true', 'false', 'NUM', 'ID', ')'])

    def literal(self):
        assert self.token.kind() == ('true' or 'false' or 'NUM'), \
            f'Expected "true" or "false" or "NUM" instead found {self.token.kind()}'
        match self.token.kind():
            case ('true' | 'false'):
                self.boolean_literal()
            case 'NUM':
                self.token = self.lex.next()

    def boolean_literal(self):
        assert self.token.kind() == ('true' or 'false'), \
            f'Expected "true" or "false" instead found {self.token.kind()}'
        self.token = self.lex.next()

    def iterative_statement(self):
        self.match('while')
        self.expr()
        self.match('do')
        self.body()

    def print_statement(self):
        assert self.token.kind() == 'print', f'Expected "print" instead found {self.token.kind()}'
        self.token = self.lex.next()
        self.expr()
