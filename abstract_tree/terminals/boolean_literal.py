from abstract_tree.visitor import Visitor
from .terminal import Terminal


class BooleanLiteral(Terminal):
    def __init__(self, spelling: str):
        super().__init__(spelling)

    def visit(self, v: Visitor) -> object:
        return v.visit_boolean_literal(self)
