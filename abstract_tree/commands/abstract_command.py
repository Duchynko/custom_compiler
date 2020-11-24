from __future__ import annotations

from abc import ABCMeta, abstractmethod

from ..abstract_syntax_tree import AbstractSyntaxTree
from ..visitor import Visitor


class AbstractCommand(AbstractSyntaxTree, metaclass=ABCMeta):
    @abstractmethod
    def visit(self, visitor: Visitor, *args) -> object:
        pass
