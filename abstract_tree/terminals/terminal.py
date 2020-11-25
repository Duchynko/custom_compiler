from __future__ import annotations

from abc import abstractmethod, ABCMeta

from ..abstract_syntax_tree import AbstractSyntaxTree
from ..visitor import Visitor


class Terminal(AbstractSyntaxTree, metaclass=ABCMeta):
    def __init__(self, spelling: str):
        self.spelling = spelling

    @abstractmethod
    def visit(self, visitor: Visitor, *args) -> object:
        pass
