from abc import ABCMeta, abstractmethod

from abstract_tree.visitor import Visitor
from ..ast import AST


class AbstractStatement(AST, metaclass=ABCMeta):
    @abstractmethod
    def visit(self, v: Visitor) -> object:
        pass
