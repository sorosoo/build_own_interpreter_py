import abc
from enum import Enum
from typing import Callable


class EToken(Enum):
    INTEGER = 'integer'

    PLUS = '+'
    MINUS = '-'
    MUL = '*'
    DIV = '/'

    LPAREN = '('
    RPAREN = ')'

    EOF = 'eof'


class Token:

    def __init__(
            self,
            typ: EToken,
            val: int | str | None
    ):
        self.__typ = typ
        self.__val = val

    @property
    def typ(self) -> EToken: return self.__typ

    @property
    def val(self) -> int | str | None: return self.__val

    def __repr__(self) -> str: return f'{self.typ}: {self.val}'


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

    def integer(self) -> int:
        result: str = ''
        while self.__cur_char and self.__cur_char.isdigit():
            result = f'{result}{self.__cur_char}'
            self.advance()
        return None if len(result) == 0 else int(result)

    def get_next_token(self) -> Token:
        if self.__cur_char is None:
            return Token(EToken.EOF, None)

        self.skip_whitespace()

        if self.__cur_char.isdigit():
            return Token(EToken.INTEGER, self.integer())

        if self.__cur_char == EToken.PLUS.value:
            self.advance()
            return Token(EToken.PLUS, EToken.PLUS.value)
        if self.__cur_char == EToken.MINUS.value:
            self.advance()
            return Token(EToken.MINUS, EToken.MINUS.value)
        if self.__cur_char == EToken.MUL.value:
            self.advance()
            return Token(EToken.MUL, EToken.MUL.value)
        if self.__cur_char == EToken.DIV.value:
            self.advance()
            return Token(EToken.DIV, EToken.DIV.value)
        if self.__cur_char == EToken.LPAREN.value:
            self.advance()
            return Token(EToken.LPAREN, EToken.LPAREN.value)
        if self.__cur_char == EToken.RPAREN.value:
            self.advance()
            return Token(EToken.RPAREN, EToken.RPAREN.value)


class AstNode(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def name(cls) -> str: raise NotImplemented


class BinOp(AstNode):

    __name: str = 'bin_op'

    @classmethod
    def name(cls) -> str: return cls.__name

    def __init__(
            self,
            left: AstNode,
            op: Token,
            right: AstNode
    ):
        self.__left = left
        self.__op = op
        self.__right = right

    @property
    def left(self) -> AstNode: return self.__left

    @property
    def op(self) -> Token: return self.__op

    @property
    def right(self) -> AstNode: return self.__right


class Integer(AstNode):

    __name: str = 'integer'

    @classmethod
    def name(cls) -> str: return cls.__name

    def __init__(
            self,
            value: Token
    ):
        self.__value = value

    @property
    def value(self) -> Token: return self.__value


class Parser:

    def __init__(
            self,
            lexer: Lexer
    ):
        self.__lexer = lexer
        self.__cur_token = self.__lexer.get_next_token()

    def eat(self, e: EToken):
        if self.__cur_token.typ == e:
            self.__cur_token = self.__lexer.get_next_token()
        else:
            self.__lexer.error()

    def factor(self) -> AstNode:
        if self.__cur_token.typ == EToken.INTEGER:
            node: AstNode = Integer(self.__cur_token)
            self.eat(self.__cur_token.typ)
            return node
        if self.__cur_token.typ == EToken.LPAREN:
            self.eat(self.__cur_token.typ)
            node: AstNode = self.expr()
            self.eat(EToken.RPAREN)
            return node

    def term(self) -> AstNode:
        node: AstNode = self.factor()
        while self.__cur_token.typ in (
            EToken.MUL,
            EToken.DIV,
        ):
            if self.__cur_token.typ == EToken.MUL:
                op: Token = Token(EToken.MUL, EToken.MUL.value)
                self.eat(op.typ)
                node = BinOp(node, op, self.factor())
            elif self.__cur_token.typ == EToken.DIV:
                op: Token = Token(EToken.DIV, EToken.DIV.value)
                self.eat(op.typ)
                node = BinOp(node, op, self.factor())
        return node

    def expr(self) -> AstNode:
        node: AstNode = self.term()
        while self.__cur_token.typ in (
            EToken.PLUS,
            EToken.MINUS,
        ):
            if self.__cur_token.typ == EToken.PLUS:
                op: Token = Token(EToken.PLUS, EToken.PLUS.value)
                self.eat(op.typ)
                node = BinOp(node, op, self.term())
            elif self.__cur_token.typ == EToken.MINUS:
                op: Token = Token(EToken.MINUS, EToken.MINUS.value)
                self.eat(op.typ)
                node = BinOp(node, op, self.term())
        return node

    def parse(self) -> AstNode:
        return self.expr()

class NodeVisitor(abc.ABC):

    def visit(self, node: AstNode) -> int:
        method_name: str = f'visit_{node.name()}'
        method: Callable[[AstNode], int] = getattr(self, method_name, None)
        if method:
            return method(node)
        raise RuntimeError

class Interpreter(NodeVisitor):

    def __init__(
            self,
            parser: Parser
    ):
        self.__parser = parser

    def visit_integer(self, node: Integer) -> int:
        # print(node.value)
        print(node.value.val, end='')
        return node.value.val

    def visit_bin_op(self, node: BinOp) -> int:
        if node.op.typ == EToken.PLUS:
            print(f'({node.op.val}', end='')
            left = self.visit(node.left)
            right = self.visit(node.right)
            print(')', end='')
            # print(node.op)
            return left + right
        if node.op.typ == EToken.MINUS:
            print(f'({node.op.val}', end='')
            left = self.visit(node.left)
            right = self.visit(node.right)
            print(')', end='')
            # print(node.op)
            return left - right
        if node.op.typ == EToken.MUL:
            print(f'({node.op.val}', end='')
            left = self.visit(node.left)
            right = self.visit(node.right)
            print(')', end='')
            # print(node.op)
            return left * right
        if node.op.typ == EToken.DIV:
            print(f'({node.op.val}', end='')
            left = self.visit(node.left)
            right = self.visit(node.right)
            print(')', end='')
            # print(node.op)
            return left // right

    def interpret(self):
        ast: AstNode = self.__parser.parse()
        return self.visit(ast)

def main():
    while True:
        try:
            try:
                text = input('spi> ')
            except NameError:  # Python3
                text = input('spi> ')
        except EOFError:
            break
        if not text:
            continue

        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(f'\n{result}')


if __name__ == '__main__':
    main()