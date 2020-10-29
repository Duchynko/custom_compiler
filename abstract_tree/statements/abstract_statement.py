from __future__ import annotations

from abc import ABCMeta, abstractmethod

from ..abstract_syntax_tree import AbstractSyntaxTree
from ..visitor import Visitor


class AbstractStatement(AbstractSyntaxTree, metaclass=ABCMeta):
    @abstractmethod
    def visit(self, visitor: Visitor) -> object:
        pass
