from abc import abstractmethod, ABCMeta

from abstract_tree.visitor import Visitor
from ..ast import AST


class Terminal(AST, metaclass=ABCMeta):
    def __init__(self, spelling: str):
        self.spelling = spelling

    @abstractmethod
    def visit(self, v: Visitor) -> object:
        pass
