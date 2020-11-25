from __future__ import annotations

from .terminal import Terminal
from ..visitor import Visitor


class BooleanLiteral(Terminal):
    def visit(self, visitor: Visitor, *args) -> object:
        return visitor.visit_boolean_literal(self, *args)
