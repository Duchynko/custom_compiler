from abc import ABC, abstractmethod
from .visitor import Visitor


class AST(ABC):
    @abstractmethod
    def visit(self, v: Visitor) -> object:
        pass

