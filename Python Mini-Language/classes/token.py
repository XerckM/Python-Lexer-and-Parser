##########################
# TOKEN CLASS
##########################


"""
This class creates a token with type, line position,
value as attributes.

The methods in this class will return its type, position,
and value respectively.
"""


class Token(object):
    def __init__(self, type_, line, position, value):
        self.type_ = type_
        self.line = line
        self.position_ = position
        self.value_ = value

    def __repr__(self):
        if self.value_:
            return f'{self.position() : <20}{self.kind() : <15}{self.value() : <20}'

    def kind(self):
        """
        This function returns the type of token
        i.e. NUM, ID, KEYWORD, etc.
        """
        return self.type_

    def position(self):
        """
        This function returns the position of the token
        in the text.
        It returns the line number and its position starting
        from index 0 -> n
        """
        return f'(Line: {self.line}, Pos: {self.position_})'

    def value(self):
        """
        This function returns the value of the token, or
        the character that was found
        """
        return self.value_
