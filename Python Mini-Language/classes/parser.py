######################
# PARSER
######################


class Parser:
    """
    This class is an implementation of a top-down, predictive, recursive descent parser.
    It takes tokens returned from the lexer and returns 'True' if the program is accepted
    by the grammar rules else it will return 'False' and stop parsing while returning the
    position and error details.

    Comments are not tokenized in the lexer to simplify the process. That way '//'
    and anything after the symbol is already ignored and will not be parsed.

    (Still needs an AST)
    """

    def __init__(self, lexer):
        self.lex = lexer
        self.token = self.lex.next()    # initializing first token

    def parse(self):
        pass

    def match(self, value):
        """
        Takes a value and matches it to the type of the current token.
        If it is true it will get the next token and store it in a variable,
        otherwise it will raise an error with the position and type of token that
        should have been expected.
        """
        if self.token.kind() == value:
            self.token = self.lex.next()
        else:
            raise Exception(f'<At {self.token.position()} I see "{self.token.kind()}" but expected "{value}">')

    def program(self):
        """
        Program  =  "program"  Identifier  ":"  Body  "end"
        Identifier  =  Letter { Letter | Digit | "_" } <--handled by lexer
        """
        try:
            self.match('program')
            self.match('ID')
            self.match(':')
            self.body()
            self.match('end')
            return f'\n{True}'
        except BaseException as err:
            print(f'\n{err}')
            return f'\n{False}'

    def body(self):
        """
        Body  =  [ Declarations ]  Statements
        """
        if self.token.kind() in ('bool', 'int'):
            self.declarations()
        self.statements()

    def declarations(self):
        """
        Declarations  =  Declaration { Declaration }
        """
        self.declaration()
        while self.token.kind() in ('bool', 'int'):
            self.declaration()

    def declaration(self):
        """
        Declaration  =  ( "bool" | "int" )  Identifier ";"
        """
        assert self.token.kind() in ('bool', 'int'), \
            f'<ERROR! at {self.token.position()}. ' \
            f'Expected "bool" or "int" instead' \
            f'found {self.token.kind()}>'
        self.token = self.lex.next()
        self.match('ID')
        self.match(';')

    def statements(self):
        """
        Statements  =  Statement { ";" Statement }
        """
        self.statement()
        while self.token.kind() == ';':
            self.token = self.lex.next()
            self.statement()

    def statement(self):
        """
        Statement  =  AssignmentStatement
                   |  ConditionalStatement
                   |  IterativeStatement
                   |  PrintStatement
        """
        if self.token.kind() == 'ID':
            self.assignment_statement()
        elif self.token.kind() == 'if':
            self.conditional_statement()
        elif self.token.kind() == 'while':
            self.iterative_statement()
        elif self.token.kind() == 'print':
            self.print_statement()
        else:
            self.expected(('if', 'ID', 'while', 'print'))   # Error is raised here

    def expected(self, type_list):
        """
        This function takes a list if the token type is not in that list
        it will raise an error returning the position and details of the
        error.
        """
        if self.token.kind() not in type_list:
            raise Exception(
                f'<ERROR! at {self.token.position()}. Expected to see {type_list}, but see "{self.token.kind()}">')

    def assignment_statement(self):
        """
        AssignmentStatement  =  Identifier ":=" Expression
        """
        assert self.token.kind() == 'ID', f'<Expected "ID" instead found {self.token.kind()}>'
        self.match('ID')
        self.match(':=')
        self.expr()

    def conditional_statement(self):
        """
        ConditionalStatement  =  "if"  Expression  "then"  Body  [ "else" Body ]  "fi"
        """
        self.match('if')
        self.expr()
        self.match('then')
        self.body()
        if self.token.kind() == 'else':
            self.token = self.lex.next()
            self.body()
        prev_token = self.token
        self.match('fi')
        next_token = self.token
        if next_token.kind() == ';':
            self.token = next_token
        else:
            raise Exception(f'<ERROR! at (Line: {prev_token.line}, Pos: {prev_token.position_ + 2}). '
                            f'Expected ";" but none found.>')

    def expr(self):
        """
        Expression  =  SimpleExpression [ RelationalOperator SimpleExpression ]
        RelationalOperator  =  "<" | "=<" | "=" | "!=" | ">=" | ">"
        """
        self.simple_expr()
        if self.token.kind() in ('<', '>', '<=', '>=', '!=', '='):
            self.token = self.lex.next()
            self.simple_expr()

    def simple_expr(self):
        """
        SimpleExpression  =  Term { AdditiveOperator Term }
        AdditiveOperator  =  "+" | "-" | "or"
        """
        self.term()
        while self.token.kind() in ('+', '-', 'or'):
            self.token = self.lex.next()
            self.term()

    def term(self):
        """
        Term  =  Factor { MultiplicativeOperator Factor }
        MultiplicativeOperator  =  "*" | "/" | "and"
        """
        self.factor()
        while self.token.kind() in ('*', '/', 'and'):
            self.token = self.lex.next()
            self.factor()

    def factor(self):
        """
        Factor  =  [ UnaryOperator ] ( Literal  |  Identifier  | "(" Expression ")" )
        UnaryOperator  =  "-" | "not"
        """
        if self.token.kind() in ('-', 'not'):
            self.token = self.lex.next()
        if self.token.kind() in ('true', 'false', 'NUM'):
            self.literal()
        elif self.token.kind() == 'ID':
            prev_token = self.token
            next_token = self.lex.next()
            if next_token.kind() in (";", '<', '>', '<=', '>=', '!=', '=',
                                     '+', '-', 'or', '*', '/', 'and', ')',
                                     'else', 'do', 'od', 'fi'):
                self.token = next_token
            else:
                raise Exception(f'<ERROR! at (Line: {prev_token.line}, Pos: {prev_token.position_ + 1}). '
                                f'Expected ";" but none found.>')
        elif self.token.kind() == '(':
            self.token = self.lex.next()
            self.expr()
            self.match(')')
        else:
            self.expected(['true', 'false', 'NUM', 'ID', '('])

    def literal(self):
        """
        Literal  =  BooleanLiteral  |  IntegerLiteral
        IntegerLiteral  =  Digit { Digit } <-- handled by lexer
        """
        assert self.token.kind() in ('true', 'false', 'NUM'), \
            f'<ERROR! at {self.token.position()}.' \
            f'Expected "true" or "false" or "NUM" instead' \
            f'found {self.token.kind()}>'
        if self.token.kind() == 'NUM':
            prev_token = self.token
            next_token = self.lex.next()
            if next_token.kind() in (";", '<', '>', '<=', '>=', '!=', '=',
                                     '+', '-', 'or', '*', '/', 'and', ')',
                                     'do', 'od', 'fi'):
                self.token = next_token
            else:
                raise Exception(f'<ERROR! at (Line: {prev_token.line}, Pos: {prev_token.position_ + 1}). '
                                f'Expected ";" but none found.>')
        else:
            self.boolean_literal()

    def boolean_literal(self):
        """
        BooleanLiteral  =  "false"  |  "true"
        """
        if self.token.kind() in ('true ', 'false'):
            self.token = self.lex.next()
        else:
            raise Exception(f'<ERROR! at {self.token.position()}. Expected "true" or "false" or "NUM" '
                            f'instead found {self.token.kind()}>')

    def iterative_statement(self):
        """
        IterativeStatement  =  "while"  Expression  "do"  Body  "od"
        """
        self.match('while')
        self.expr()
        self.match('do')
        self.body()
        prev_token = self.token
        self.match('od')
        next_token = self.token
        if next_token.kind() == ';':
            self.token = next_token
        else:
            raise Exception(f'<ERROR! at (Line: {prev_token.line}, Pos: {prev_token.position_ + 2}). '
                            f'Expected ";" but none found.>')

    def print_statement(self):
        """
        PrintStatement  =  "print"  Expression
        """
        if self.token.kind() == 'print':
            self.token = self.lex.next()
            self.expr()
