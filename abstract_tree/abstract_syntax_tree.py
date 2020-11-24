from __future__ import annotations

from abc import ABC, abstractmethod


class AbstractSyntaxTree(ABC):
    @abstractmethod
    def visit(self, visitor, *args) -> object:
        """
        A visitor pattern method.

        Arguments:
            visitor: An instance of a concrete class extending abstract Visitor.
            *args: Additional arguments

        Returns:

        """
        pass

