from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple


MAX_VARIABLES = 5


@dataclass(frozen=True)
class Token:
    token_type: str
    value: str
    position: int


class Node:
    def evaluate(self, values: Dict[str, int]) -> int:
        raise NotImplementedError

    def collect_variables(self) -> set[str]:
        raise NotImplementedError


@dataclass(frozen=True)
class ConstantNode(Node):
    value: int

    def evaluate(self, values: Dict[str, int]) -> int:
        _ = values
        return int(bool(self.value))

    def collect_variables(self) -> set[str]:
        return set()


@dataclass(frozen=True)
class VariableNode(Node):
    name: str

    def evaluate(self, values: Dict[str, int]) -> int:
        if self.name not in values:
            raise ValueError(f"Для переменной '{self.name}' не задано значение.")
        return int(bool(values[self.name]))

    def collect_variables(self) -> set[str]:
        return {self.name}


@dataclass(frozen=True)
class UnaryNode(Node):
    operator: str
    operand: Node

    def evaluate(self, values: Dict[str, int]) -> int:
        operand_value = self.operand.evaluate(values)

        if self.operator == "!":
            return 1 - operand_value

        raise ValueError(f"Неизвестный унарный оператор: {self.operator}")

    def collect_variables(self) -> set[str]:
        return self.operand.collect_variables()


@dataclass(frozen=True)
class BinaryNode(Node):
    operator: str
    left: Node
    right: Node

    def evaluate(self, values: Dict[str, int]) -> int:
        left_value = self.left.evaluate(values)
        right_value = self.right.evaluate(values)

        if self.operator == "&":
            return left_value & right_value
        if self.operator == "|":
            return left_value | right_value
        if self.operator == "->":
            return int((not left_value) or right_value)
        if self.operator == "~":
            return int(left_value == right_value)

        raise ValueError(f"Неизвестный бинарный оператор: {self.operator}")

    def collect_variables(self) -> set[str]:
        return self.left.collect_variables() | self.right.collect_variables()


@dataclass(frozen=True)
class ParsedExpression:
    source: str
    root: Node
    variables: Tuple[str, ...]


class ExpressionParser:
    SYMBOL_REPLACEMENTS = {
        "¬": "!",
        "∧": "&",
        "∨": "|",
        "→": "->",
        "⇒": "->",
        "↔": "~",
        "≡": "~",
    }

    def parse(self, source: str) -> ParsedExpression:
        normalized_source = self._normalize(source)
        self._validate_source(normalized_source)

        tokens = self._tokenize(normalized_source)
        parser = _Parser(tokens)
        root = parser.parse()

        variables = tuple(sorted(root.collect_variables()))
        if len(variables) > MAX_VARIABLES:
            raise ValueError(
                f"Поддерживается не более {MAX_VARIABLES} переменных."
            )

        return ParsedExpression(
            source=normalized_source,
            root=root,
            variables=variables,
        )

    def _validate_source(self, source: str) -> None:
        if not source or not source.strip():
            raise ValueError("Формула не должна быть пустой.")

    def _normalize(self, source: str) -> str:
        result = source
        for old_symbol, new_symbol in self.SYMBOL_REPLACEMENTS.items():
            result = result.replace(old_symbol, new_symbol)
        return result

    def _tokenize(self, source: str) -> List[Token]:
        tokens: List[Token] = []
        index = 0

        while index < len(source):
            current = source[index]

            if current.isspace():
                index += 1
                continue

            if source.startswith("->", index):
                tokens.append(Token("IMP", "->", index))
                index += 2
                continue

            if current == "!":
                tokens.append(Token("NOT", current, index))
                index += 1
                continue

            if current == "&":
                tokens.append(Token("AND", current, index))
                index += 1
                continue

            if current == "|":
                tokens.append(Token("OR", current, index))
                index += 1
                continue

            if current == "~":
                tokens.append(Token("EQ", current, index))
                index += 1
                continue

            if current == "(":
                tokens.append(Token("LPAREN", current, index))
                index += 1
                continue

            if current == ")":
                tokens.append(Token("RPAREN", current, index))
                index += 1
                continue

            if current in {"0", "1"}:
                tokens.append(Token("CONST", current, index))
                index += 1
                continue

            if current.isalpha() or current == "_":
                start = index
                index += 1
                while index < len(source):
                    next_symbol = source[index]
                    if next_symbol.isalnum() or next_symbol == "_":
                        index += 1
                    else:
                        break
                variable_name = source[start:index]
                tokens.append(Token("VAR", variable_name, start))
                continue

            raise ValueError(f"Недопустимый символ '{current}' в позиции {index}.")

        tokens.append(Token("END", "", len(source)))
        return tokens


class _Parser:
    def __init__(self, tokens: Sequence[Token]) -> None:
        self._tokens = list(tokens)
        self._position = 0

    @property
    def current(self) -> Token:
        return self._tokens[self._position]

    def parse(self) -> Node:
        result = self._parse_equivalence()
        self._consume("END")
        return result

    def _parse_equivalence(self) -> Node:
        node = self._parse_implication()
        while self._match("EQ"):
            node = BinaryNode("~", node, self._parse_implication())
        return node

    def _parse_implication(self) -> Node:
        node = self._parse_or()
        if self._match("IMP"):
            return BinaryNode("->", node, self._parse_implication())
        return node

    def _parse_or(self) -> Node:
        node = self._parse_and()
        while self._match("OR"):
            node = BinaryNode("|", node, self._parse_and())
        return node

    def _parse_and(self) -> Node:
        node = self._parse_unary()
        while self._match("AND"):
            node = BinaryNode("&", node, self._parse_unary())
        return node

    def _parse_unary(self) -> Node:
        if self._match("NOT"):
            return UnaryNode("!", self._parse_unary())
        return self._parse_primary()

    def _parse_primary(self) -> Node:
        token = self.current

        if self._match("VAR"):
            return VariableNode(token.value)

        if self._match("CONST"):
            return ConstantNode(int(token.value))

        if self._match("LPAREN"):
            inner = self._parse_equivalence()
            self._consume("RPAREN")
            return inner

        raise ValueError(
            f"Ожидалась переменная, константа или '(' в позиции {token.position}."
        )

    def _match(self, token_type: str) -> bool:
        if self.current.token_type == token_type:
            self._position += 1
            return True
        return False

    def _consume(self, token_type: str) -> Token:
        token = self.current
        if token.token_type != token_type:
            raise ValueError(
                f"Ожидался токен {token_type} в позиции {token.position}, "
                f"но получен {token.token_type}."
            )
        self._position += 1
        return token