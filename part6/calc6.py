from enum import Enum


class TokenType(Enum):
    INTEGER = 'integer'
    LPAREN = '('
    RPAREN = ')'

    MUL = '*'
    DIV = '/'
    REMIND = '%'
    PLUS = '+'
    MINUS = '-'

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
        raise EOFError('解析错误')

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

        if self.__cur_char == TokenType.PLUS.value:
            self.advance()
            return Token(TokenType.PLUS, TokenType.PLUS.value)
        if self.__cur_char == TokenType.MINUS.value:
            self.advance()
            return Token(TokenType.MINUS, TokenType.MINUS.value)
        if self.__cur_char == TokenType.MUL.value:
            self.advance()
            return Token(TokenType.MUL, TokenType.MUL.value)
        if self.__cur_char == TokenType.DIV.value:
            self.advance()
            return Token(TokenType.DIV, TokenType.DIV.value)
        if self.__cur_char == TokenType.REMIND.value:
            self.advance()
            return Token(TokenType.REMIND, TokenType.REMIND.value)
        if self.__cur_char == TokenType.LPAREN.value:
            self.advance()
            return Token(TokenType.LPAREN, TokenType.LPAREN.value)
        if self.__cur_char == TokenType.RPAREN.value:
            self.advance()
            return Token(TokenType.RPAREN, TokenType.RPAREN.value)

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

    def factor(self) -> int | None:
        if self.__cur_token.typ == TokenType.INTEGER:
            token = self.__cur_token
            self.eat(TokenType.INTEGER)
            return token.val
        elif self.__cur_token.typ == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            result = self.expr()
            self.eat(TokenType.RPAREN)
            return result

    def term(self) -> int | None:
        result: int = self.factor()

        while self.__cur_token.typ in (
                TokenType.MUL,
                TokenType.DIV,
                TokenType.REMIND,
        ):
            if self.__cur_token.typ == TokenType.MUL:
                self.eat(TokenType.MUL)
                result *= self.factor()
            elif self.__cur_token.typ == TokenType.DIV:
                self.eat(TokenType.DIV)
                result //= self.factor()
            elif self.__cur_token.typ == TokenType.REMIND:
                self.eat(TokenType.REMIND)
                result %= self.factor()

        return result

    def expr(self) -> int:
        result: int = self.term()

        while self.__cur_token.typ in (
                TokenType.PLUS,
                TokenType.MINUS,
        ):
            if self.__cur_token.typ == TokenType.PLUS:
                self.eat(TokenType.PLUS)
                result += self.term()
            elif self.__cur_token.typ == TokenType.MINUS:
                self.eat(TokenType.MINUS)
                result -= self.term()

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