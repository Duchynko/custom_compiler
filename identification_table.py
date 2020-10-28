from typing import Optional, List

from abstract_tree import AbstractDeclaration


class IdEntry:
    def __init__(self, level: int, identifier: str, attr: AbstractDeclaration):
        self.level = level
        self.identifier = identifier
        self.attr = attr

    def __str__(self):
        return f"[{self.level}]: {self.identifier}"


class IdentificationTable:
    def __init__(self):
        self.table: List[IdEntry] = []
        self.level = 0

    def _find(self, identifier: str) -> Optional[IdEntry]:
        for i in reversed(range(len(self.table)-1)):
            if self.table[i].identifier is identifier:
                return self.table[i]
        return None

    def insert(self, identifier: str, attr: AbstractDeclaration):
        entry = self._find(identifier)

        if entry and entry.level == self.level:
            raise Exception(f"{entry.identifier} was identified twice")
        else:
            self.table.append(
                IdEntry(level=self.level, identifier=identifier, attr=attr)
            )

    def get(self, identifier: str) -> Optional[AbstractDeclaration]:
        entry = self._find(identifier)

        if entry:
            return entry.attr
        else:
            return None

    def openScope(self) -> None:
        self.level += 1

    def closeScope(self) -> None:
        pos = len(self.table) - 1
        while pos >= 0 and self.table[pos].level == self.level:
            self.table.pop(pos)
            pos -= 1
        self.level -= 1
