from abstract_tree.visitor import Visitor
from .terminal import Terminal


class Operator(Terminal):
    def __init__(self, spelling: str):
        super().__init__(spelling)

    def visit(self, v: Visitor) -> object:
        return v.visit_operator(self)
