from enum import Enum


class TokenType(Enum):

    INTEGER = 'integer'
    MUL = 'mul'
    DIV = 'div'
    PLUS = 'plus'
    MINUS = 'minus'
    EOF = 'eof'

class Token:

    def __init__(
            self,
            typ: TokenType,
            val: int | str | None
    ):
        self.__typ = typ
        self.__val = val

    @property
    def typ(self) -> TokenType:
        return self.__typ

    @property
    def val(self) -> int | str | None:
        return self.__val

class Lexer:

    def __init__(
            self,
            text: str
    ):
        self.__text = text
        self.__pos = 0
        self.__cur_char = None if len(self.__text) == 0 else self.__text[self.__pos]

    def error(self):
        raise Exception('解析错误')

    def advance(self):
        self.__pos += 1
        if self.__pos >= len(self.__text):
            self.__cur_char = None
        else:
            self.__cur_char = self.__text[self.__pos]

    def skip_whitespace(self):
        while self.__cur_char and self.__cur_char.isspace():
            self.advance()

    def integer(self) -> int | None:
        result: str = ''
        while self.__cur_char and self.__cur_char.isdigit():
            result = f'{result}{self.__cur_char}'
            self.advance()
        return None if len(result) == 0 else int(result)

    def get_next_token(self) -> Token:
        if self.__cur_char is None:
            return Token(TokenType.EOF, None)

        self.skip_whitespace()

        if self.__cur_char.isdigit():
            return Token(TokenType.INTEGER, self.integer())

        if self.__cur_char == '+':
            self.advance()
            return Token(TokenType.PLUS, '+')
        if self.__cur_char == '-':
            self.advance()
            return Token(TokenType.MINUS, '-')
        if self.__cur_char == '*':
            self.advance()
            return Token(TokenType.MUL, '*')
        if self.__cur_char == '/':
            self.advance()
            return Token(TokenType.DIV, '/')

        self.error()

class Interpreter:

    def __init__(
            self,
            lexer: Lexer
    ):
        self.__lexer = lexer
        self.__cur_token: Token | None = self.__lexer.get_next_token()

    def eat(self, typ: TokenType):
        if self.__cur_token.typ == typ:
            self.__cur_token = self.__lexer.get_next_token()
        else:
            self.__lexer.error()

    def factor(self) -> int:
        token: Token = self.__cur_token
        self.eat(TokenType.INTEGER)
        return token.val

    def expr(self) -> int:
        result: int = self.factor()

        while self.__cur_token.typ in (
            TokenType.MUL,
            TokenType.DIV,
            TokenType.PLUS,
            TokenType.MINUS,
        ):
            if self.__cur_token.typ == TokenType.MUL:
                self.eat(TokenType.MUL)
                result *= self.factor()
            elif self.__cur_token.typ == TokenType.DIV:
                self.eat(TokenType.DIV)
                result //= self.factor()
            elif self.__cur_token.typ == TokenType.PLUS:
                self.eat(TokenType.PLUS)
                result += self.factor()
            elif self.__cur_token.typ == TokenType.MINUS:
                self.eat(TokenType.MINUS)
                result -= self.factor()

        return result

def main():
    while True:
        try:
            # To run under Python3 replace 'raw_input' call
            # with 'input'
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()