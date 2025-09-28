from typing import Literal

# Token类型
# INTEGER: 代表整数token
# PLUS: 代表加号(+)
# EOF: 代表表达式结尾
INTEGER, PLUS, EOF = 'INTEGER', 'PLUS', 'EOF'

class Token:

    def __init__(
            self,
            token_type: str,
            val: int | str | None
    ):
        self.__token_type = token_type
        self.__val = val

    @property
    def token_type(self) -> str:
        return self.__token_type

    @property
    def val(self) -> int | str | None:
        return self.__val

    def __repr__(self) -> str:
        return f'Token({self.token_type}, {self.val})'

class Interpreter:

    def __init__(
            self,
            text: str
    ):
        self.__text = text
        self.__pos = 0
        self.__cur_token: Token | None = None

    def error(self):
        raise Exception('解析错误')

    def get_next_token(self) -> Token:

        if self.__pos >= len(self.__text):
            return Token(EOF, None)

        cur_char = self.__text[self.__pos]

        if cur_char.isdigit():
            self.__pos += 1
            return Token(INTEGER, int(cur_char))
        if cur_char == '+':
            self.__pos += 1
            return Token(PLUS, cur_char)

        self.error()

    def eat(self, token_type: str):
        if token_type == self.__cur_token.token_type:
            self.__cur_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        self.__cur_token = self.get_next_token()

        left: Token = self.__cur_token
        self.eat(INTEGER)

        op: Token = self.__cur_token
        self.eat(PLUS)

        right: Token = self.__cur_token
        self.eat(INTEGER)

        return eval(''.join([str(left.val), op.val, str(right.val)]))

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