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
    """

    def __init__(self, lexer):
        self.lex = lexer
        self.token = self.lex.next()  # initializing first token

    def match(self, value):
        """
        Takes a value and matches it to the type of the current token.
        If it is true it will get the next token and store it in a variable,
        otherwise it will raise an error with the position and type of token that
        should have been expected.
        """
        scaffold = {}
        if self.token.kind() == value:
            scaffold['type'] = self.token.type_
            scaffold['position'] = self.token.position_
            scaffold['value'] = self.token.value_
            self.token = self.lex.next()
            return scaffold
        else:
            raise Exception(f'<At {self.token.position()} I see "{self.token.kind()}" but expected "{value}">')

    def program(self):
        """
        Program  =  "program"  Identifier  ":"  Body  "end"
        Identifier  =  Letter { Letter | Digit | "_" } <--handled by lexer
        """
        ast = []
        try:
            ast.append(self.match('program'))
            ast.append(self.match('ID'))
            ast.append(self.match(':'))
            ast.append(self.body())
            ast.append(self.match('end'))
            return f'\n{ast}\n\n{True}'
        except BaseException as err:
            print(f'\n{err}')
            return f'\n{False}'

    def body(self):
        """
        Body  =  [ Declarations ]  Statements
        """
        values = []
        if self.token.kind() in ('bool', 'int'):
            values.append({
                'type': "Body",
                'value': self.declarations()
            })
        values.append({
            'type': "Body",
            'value': self.statements()
        })

        return values

    def declarations(self):
        """
        Declarations  =  Declaration { Declaration }
        """
        values = []
        values.append(self.declaration())
        while self.token.kind() in ('bool', 'int'):
            values.append(self.declaration())

        return values

    def declaration(self):
        """
        Declaration  =  ( "bool" | "int" )  Identifier ";"
        """
        values = []
        assert self.token.kind() in ('bool', 'int'), \
            f'<ERROR! at {self.token.position()}. ' \
            f'Expected "bool" or "int" instead' \
            f'found {self.token.kind()}>'
        scaffold = {
            "type": self.token.type_,
            "position": self.token.position_,
            "value": self.token.value_
        }
        values.append(scaffold)
        self.token = self.lex.next()
        values.append(self.match('ID'))
        values.append(self.match(';'))

        return values

    def statements(self):
        """
        Statements  =  Statement { ";" Statement }
        """
        values = []
        values.append(self.statement())
        while self.token.kind() == ';':
            self.token = self.lex.next()
            values.append(self.statement())

        return values

    def statement(self):
        """
        Statement  =  AssignmentStatement
                   |  ConditionalStatement
                   |  IterativeStatement
                   |  PrintStatement
        """
        scaffold = {}
        if self.token.kind() == 'ID':
            scaffold = {
                'type': 'Assignment Statement',
                'value': self.assignment_statement(),
            }
        elif self.token.kind() == 'if':
            scaffold = {
                'type': 'Conditional Statement',
                'value': self.conditional_statement(),
            }
        elif self.token.kind() == 'while':
            scaffold = {
                'type': 'Iterative Statement',
                'value': self.iterative_statement(),
            }
        elif self.token.kind() == 'print':
            scaffold = {
                'type': 'Print Statement',
                'value': self.print_statement(),
            }
        else:
            self.expected(('if', 'ID', 'while', 'print'))  # Error is raised here
        return scaffold

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
        values = []
        assert self.token.kind() == 'ID', f'<Expected "ID" instead found {self.token.kind()}>'
        values.append(self.match('ID'))
        values.append(self.match(':='))
        values.append(self.expr())
        return values

    def conditional_statement(self):
        """
        ConditionalStatement  =  "if"  Expression  "then"  Body  [ "else" Body ]  "fi"
        """
        values = [self.match('if'), self.expr(), self.match('then'), self.body()]
        if self.token.kind() == 'else':
            values.append({
                'type': self.token.type_,
                'position': self.token.position_,
                'value': self.token.value_
            })
            self.token = self.lex.next()
            values.append(self.body())
        self.match('fi')

    def expr(self):
        """
        Expression  =  SimpleExpression [ RelationalOperator SimpleExpression ]
        RelationalOperator  =  "<" | "=<" | "=" | "!=" | ">=" | ">"
        """
        # value = self.simple_expr()
        value = {
            'type': "Expression",
            'value': self.simple_expr()
        }
        if self.token.kind() in ('<', '>', '<=', '>=', '!=', '='):
            self.token = self.lex.next()
            # value = self.simple_expr()
            value = {
                'type': "Expression",
                'value': self.simple_expr()
            }
        return value

    def simple_expr(self):
        """
        SimpleExpression  =  Term { AdditiveOperator Term }
        AdditiveOperator  =  "+" | "-" | "or"
        """
        value = self.term()
        while self.token.kind() in ('+', '-', 'or'):
            self.token = self.lex.next()
            value = self.term()
        return value

    def term(self):
        """
        Term  =  Factor { MultiplicativeOperator Factor }
        MultiplicativeOperator  =  "*" | "/" | "and"
        """
        value = self.factor()
        while self.token.kind() in ('*', '/', 'and'):
            self.token = self.lex.next()
            value = self.factor()
        return value

    def factor(self):
        """
        Factor  =  [ UnaryOperator ] ( Literal  |  Identifier  | "(" Expression ")" )
        UnaryOperator  =  "-" | "not"
        """
        values = []
        if self.token.kind() in ('-', 'not'):
            values.append({
                "type": self.token.type_,
                "position": self.token.position_,
                "value": self.token.value_
            })
            self.token = self.lex.next()
        if self.token.kind() in ('true', 'false', 'NUM'):
            values = self.literal()
        elif self.token.kind() == 'ID':
            values.append({
                "type": self.token.type_,
                "position": self.token.position_,
                "value": self.token.value_
            })
            self.token = self.lex.next()
        elif self.token.kind() == '(':
            values.append({
                "type": self.token.type_,
                "position": self.token.position_,
                "value": self.token.value_
            })
            self.token = self.lex.next()
            values.append(self.expr())
            values.append(self.match(')'))
        else:
            self.expected(['true', 'false', 'NUM', 'ID', '('])
        return values

    def literal(self):
        """
        Literal  =  BooleanLiteral  |  IntegerLiteral
        IntegerLiteral  =  Digit { Digit } <-- handled by lexer
        """
        values = []
        assert self.token.kind() in ('true', 'false', 'NUM'), \
            f'<ERROR! at {self.token.position()}.' \
            f'Expected "true" or "false" or "NUM" instead' \
            f'found {self.token.kind()}>'
        if self.token.kind() == 'NUM':
            values.append({
                "type": self.token.type_,
                "position": self.token.position_,
                "value": self.token.value_
            })
            prev_token = self.token
            next_token = self.lex.next()
            if next_token.kind() in (";", '<', '>', '<=', '>=', '!=', '=',
                                     '+', '-', 'or', '*', '/', 'and', ')',
                                     'do', 'od', 'fi', 'then'):
                self.token = next_token
            else:
                raise Exception(f'<ERROR! at (Line: {prev_token.line}, Pos: {prev_token.position_ + 1}). '
                                f'Expected ";" but none found.>')
        else:
            self.boolean_literal()
        return values

    def boolean_literal(self):
        """
        BooleanLiteral  =  "false"  |  "true"
        """
        values = []
        if self.token.kind() in ('true ', 'false'):
            values.append({
                "type": self.token.type_,
                "position": self.token.position_,
                "value": self.token.value_
            })
            self.token = self.lex.next()
        else:
            raise Exception(f'<ERROR! at {self.token.position()}. Expected "true" or "false" or "NUM" '
                            f'instead found {self.token.kind()}>')
        return values

    def iterative_statement(self):
        """
        IterativeStatement  =  "while"  Expression  "do"  Body  "od"
        """
        values = []
        values.append(self.match('while'))
        values.append(self.expr())
        values.append(self.match('do'))
        values.append(self.body())
        prev_token = self.token
        values.append(self.match('od'))
        next_token = self.token
        if next_token.kind() == ';':
            values.append({
                "type": self.token.type_,
                "position": self.token.position_,
                "value": self.token.value_
            })
            self.token = next_token
        else:
            raise Exception(f'<ERROR! at (Line: {prev_token.line}, Pos: {prev_token.position_ + 2}). '
                            f'Expected ";" but none found.>')
        return values

    def print_statement(self):
        """
        PrintStatement  =  "print"  Expression
        """
        values = []
        if self.token.kind() == 'print':
            values.append({
                "type": self.token.type_,
                "position": self.token.position_,
                "value": self.token.value_
            })
            self.token = self.lex.next()
            self.expr()
        return values
