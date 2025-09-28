from enum import Enum


class TokenType(Enum):
    INTEGER = 'integer'
    PLUS = 'plus'
    MINUS = 'minus'
    MULTIPLY = 'multiply'
    DIVIDE = 'divide'
    EOF = 'eof'


class Token:

    def __init__(
            self,
            token_type: TokenType = TokenType.EOF,
            value: int | str | None = None
    ):
        self.__token_type = token_type
        self.__value = value

    @property
    def token_type(self) -> TokenType: return self.__token_type

    @property
    def value(self) -> int | str | None: return self.__value


class Interpreter:

    def __init__(
            self,
            text: str
    ):

        self.__text = text
        self.__pos = 0
        self.__cur_char = self.__text[self.__pos]
        self.__cur_token: Token | None = None

    def error(self):
        raise Exception('解析失败')

    def advance(self):
        self.__pos += 1
        if self.__pos >= len(self.__text):
            self.__cur_char = None
        else:
            self.__cur_char = self.__text[self.__pos]

    def skip_whitespace(self):
        while self.__cur_char and self.__cur_char.isspace():
            self.advance()

    def integer(self) -> int:
        result: str = ''
        while self.__cur_char and self.__cur_char.isdigit():
            result = f'{result}{self.__cur_char}'
            self.advance()
        return None if len(result) == 0 else int(result)

    def get_next_token(self) -> Token:

        if self.__cur_char is None:
            return Token(TokenType.EOF, None)

        self.skip_whitespace()

        if self.__cur_char:
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
                return Token(TokenType.MULTIPLY, '*')

            if self.__cur_char == '/':
                self.advance()
                return Token(TokenType.DIVIDE, '/')

        self.error()

    def eat(self, token_type: TokenType):
        if token_type == self.__cur_token.token_type:
            self.__cur_token = self.get_next_token()
        else:
            self.error()

    def term(self) -> Token:
        token = self.__cur_token
        self.eat(TokenType.INTEGER)
        return token

    def expr(self) -> int:

        self.__cur_token = self.get_next_token()

        result: int = self.term().value
        while self.__cur_token.token_type in (
                TokenType.PLUS,
                TokenType.MINUS,
                TokenType.MULTIPLY,
                TokenType.DIVIDE,
        ):
            if self.__cur_token.token_type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
                term: Token = self.term()
                result += term.value
            elif self.__cur_token.token_type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
                term: Token = self.term()
                result -= term.value
            elif self.__cur_token.token_type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
                term: Token = self.term()
                result *= term.value
            else:
                self.eat(TokenType.DIVIDE)
                term: Token = self.term()
                result //= term.value

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
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()