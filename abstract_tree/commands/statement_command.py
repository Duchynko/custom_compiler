from ..ast import AST
from .single_command import SingleCommand
from ..statements.single_statement import SingleStatement


class StatementCommand(SingleCommand):
    def __init__(self, statement: SingleStatement):
        self.statement = statement
