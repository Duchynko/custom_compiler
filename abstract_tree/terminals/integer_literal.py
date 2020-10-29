from __future__ import annotations

from .terminal import Terminal
from ..visitor import Visitor


class IntegerLiteral(Terminal):
    def visit(self, visitor: Visitor) -> object:
        return visitor.visit_integer_literal(self)
