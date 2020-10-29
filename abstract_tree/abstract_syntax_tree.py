from __future__ import annotations

from abc import ABC, abstractmethod


class AbstractSyntaxTree(ABC):
    @abstractmethod
    def visit(self, visitor) -> object:
        """
        A visitor pattern method.

        :param visitor: instance of a concrete class extending abstract Visitor.
        :return: object
        """
        pass

