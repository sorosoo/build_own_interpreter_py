INTEGER, PLUS, MINUS, MULTIPLE, DIVISION, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MULTIPLE', 'DIVISION',  'EOF'


class Token:

    def __init__(
            self,
            typ: str,
            value: int | str | None
    ):
        self.__typ = typ
        self.__value = value

    @property
    def typ(self) -> str:
        return self.__typ

    @property
    def value(self) -> int | str | None:
        return self.__value

    def __repr__(self):
        return f'Token({self.typ}, {self.value})'


class Interpreter:

    def __init__(
            self,
            text: str
    ):
        self.__text = text
        self.__pos = 0
        self.__cur_char: str | None = self.__text[self.__pos]
        self.__cur_token: Token | None = None

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

    def integer(self) -> str:
        result: str = ''
        while self.__cur_char and self.__cur_char.isdigit():
            result = f'{result}{self.__cur_char}'
            self.advance()
        return result

    def get_next_token(self) -> Token:

        if self.__cur_char is None:
            return Token(EOF, None)

        self.skip_whitespace()

        if self.__cur_char.isdigit():
            return Token(INTEGER, self.integer())

        if self.__cur_char == '+':
            self.advance()
            return Token(PLUS, '+')

        if self.__cur_char == '-':
            self.advance()
            return Token(MINUS, '-')

        if self.__cur_char == '*':
            self.advance()
            return Token(MULTIPLE, '*')

        if self.__cur_char == '/':
            self.advance()
            return Token(DIVISION, '/')

        self.error()

    def eat(self, typ: str):
        if self.__cur_token.typ == typ:
            self.__cur_token = self.get_next_token()
        else:
            self.error()

    def expr(self) -> int:
        self.__cur_token = self.get_next_token()

        left: Token | None = None
        while self.__cur_token.typ != EOF:
            if left is None:
                left: Token = self.__cur_token
                self.eat(INTEGER)

            op: Token = self.__cur_token
            if op.typ == PLUS:
                self.eat(PLUS)
            elif op.typ == MINUS:
                self.eat(MINUS)
            elif op.typ == MULTIPLE:
                self.eat(MULTIPLE)
            else:
                self.eat(DIVISION)

            right: Token = self.__cur_token
            self.eat(INTEGER)

            left = Token(INTEGER, eval(''.join([str(left.value), op.value, str(right.value)])))

        return left.value


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
