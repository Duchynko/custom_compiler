from __future__ import annotations

from abc import ABCMeta, abstractmethod

from ..visitor import Visitor
from ..abstract_syntax_tree import AbstractSyntaxTree


class AbstractDeclaration(AbstractSyntaxTree, metaclass=ABCMeta):
    @abstractmethod
    def visit(self, visitor: Visitor) -> object:
        pass

