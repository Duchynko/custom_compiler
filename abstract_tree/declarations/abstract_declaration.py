from __future__ import annotations

from abc import ABCMeta, abstractmethod

from address import Address
from ..visitor import Visitor
from ..abstract_syntax_tree import AbstractSyntaxTree


class AbstractDeclaration(AbstractSyntaxTree, metaclass=ABCMeta):
    def __init__(self):
        self.address: Address = None

    @abstractmethod
    def visit(self, visitor: Visitor, *args) -> object:
        pass

