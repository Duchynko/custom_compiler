from scanner import Scanner
from tokens import Kind as K, TYPE_DENOTERS, ASSIGNOPS, ADDOPS, MULOPS
from abstract_tree import *
from exceptions import (UnexpectedTokenException,
                        UnsupportedExpressionTokenException,
                        UnsupportedCommandTokenException,
                        UnsupportedDeclarationTokenException,
                        UnexpectedEndOfProgramException)


class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        self.current_terminal = scanner.scan()

    def parse_program(self) -> Program:
        cmd = self.parse_command_list()

        if self.current_terminal.kind is not K.EOT:
            raise UnexpectedEndOfProgramException(self.current_terminal)
        print(f"Successfully parsed the program.")
        return Program(command=cmd)

    def parse_command_list(self) -> CommandList:
        valid_kinds = [K.IDENTIFIER, K.FUNC, K.IF,
                       K.WHILE, K.RETURN] + TYPE_DENOTERS
        cmd_list = CommandList()
        while self.current_terminal.kind in valid_kinds:
            cmd = self.parse_single_command()
            cmd_list.commands.append(cmd)
        return cmd_list

    def parse_single_command(self) -> AbstractCommand:
        if self.current_terminal.kind is K.FUNC:
            dec = self.parse_declaration_list()
            return DeclarationCommand(declaration=dec)

        elif self.current_terminal.kind in [K.RETURN, K.IF, K.WHILE]:
            st = self.parse_single_statement()
            return StatementCommand(statement=st)

        elif self.current_terminal.kind is K.IDENTIFIER:
            st = self.parse_single_statement()
            self.accept(K.SEMICOLON)
            return StatementCommand(statement=st)

        elif self.current_terminal.kind in TYPE_DENOTERS:
            dec = self.parse_declaration_list()
            self.accept(K.SEMICOLON)
            return DeclarationCommand(declaration=dec)

        else:
            raise UnsupportedCommandTokenException(
                current_token=self.current_terminal,
                current_line=self.scanner.current_line,
                current_column=self.scanner.current_column
            )

    def parse_single_statement(self):
        if self.current_terminal.kind is K.IF:
            self.accept(K.IF)
            self.accept(K.LEFT_PAR)
            exp = self.parse_expression_list_assign_operator()
            self.accept(K.RIGHT_PAR)
            self.accept(K.COLON)
            if_block = self.parse_command_list()
            else_block = None
            if self.current_terminal.kind is K.ELSE:
                self.accept(K.ELSE)
                self.accept(K.COLON)
                else_block = self.parse_command_list()
            self.accept(K.END)
            return IfStatement(
                expr=exp,
                if_com=if_block,
                else_com=else_block
            )

        elif self.current_terminal.kind is K.WHILE:
            self.accept(K.WHILE)
            self.accept(K.LEFT_PAR)
            exp = self.parse_expression_list_assign_operator()
            self.accept(K.RIGHT_PAR)
            self.accept(K.COLON)
            cmd_list = self.parse_command_list()
            self.accept(K.END)
            return WhileStatement(
                expr=exp,
                command=cmd_list
            )

        elif self.current_terminal.kind is K.RETURN:
            self.accept(K.RETURN)
            exp = self.parse_single_expression()
            return ReturnStatement(exp)

        elif self.current_terminal.kind is K.IDENTIFIER:
            exp_list = self.parse_expression_list_assign_operator()
            return ExpressionStatement(expressions=exp_list)

    def parse_declaration_list(self):
        res = DeclarationList()
        while self.current_terminal.kind in [K.FUNC] + TYPE_DENOTERS:
            res.declarations.append(self.parse_single_declaration())
        return res

    def parse_single_declaration(self):
        if self.current_terminal.kind is K.FUNC:
            self.accept(K.FUNC)
            idf = self.parse_identifier()
            self.accept(K.LEFT_PAR)
            args = self.parse_expressions_list()
            self.accept(K.RIGHT_PAR)
            self.accept(K.COLON)
            command_list = self.parse_command_list()
            self.parse_command_list()
            self.accept(K.END)
            return FuncDeclaration(
                identifier=idf,
                args=args,
                commands=command_list
            )

        elif self.current_terminal.kind in [K.STRING_TYPE, K.INTEGER_TYPE, K.BOOLEAN_TYPE]:
            type_i = self.parse_type_indicator()
            idf = self.parse_identifier()
            if self.current_terminal.kind is K.OPERATOR:
                opr = self.parse_operator()
                exp_list = self.parse_expression_list_assign_operator()
                return VarDeclarationWithAssignment(
                    type_indicator=type_i,
                    identifier=idf,
                    operator=opr,
                    expression=exp_list)
            else:
                return VarDeclaration(
                    type_indicator=type_i,
                    identifier=idf)

        else:
            raise UnsupportedDeclarationTokenException(
                current_token=self.current_terminal,
                current_line=self.scanner.current_line,
                current_column=self.scanner.current_column
            )

    def parse_expression_list_assign_operator(self):
        res = self.parse_expression_list_add_operator()
        while self.current_terminal.kind in ASSIGNOPS:
            opr = self.parse_operator()
            tmp = self.parse_expression_list_add_operator()
            res = BinaryExpression(
                operator=opr,
                expression1=res,
                expression2=tmp
            )
        return res

    def parse_expression_list_add_operator(self):
        res = self.parse_expression_list_mul_operator()
        while self.current_terminal.kind in ADDOPS:
            opr = self.parse_operator()
            tmp = self.parse_expression_list_mul_operator()

            res = BinaryExpression(
                operator=opr,
                expression1=res,
                expression2=tmp
            )
        return res

    def parse_expression_list_mul_operator(self):
        res = self.parse_single_expression()
        while self.current_terminal.kind in MULOPS:
            opr = self.parse_operator()
            tmp = self.parse_single_expression()

            res = BinaryExpression(
                operator=opr,
                expression1=res,
                expression2=tmp
            )
        return res

    def parse_single_expression(self):
        if self.current_terminal.kind is K.INTEGER_LITERAL:
            int_literal = self.parse_integer_literal()
            return IntLiteralExpression(literal=int_literal)

        elif self.current_terminal.kind in [K.TRUE, K.FALSE]:
            bool_literal = self.parse_boolean()
            return BooleanLiteralExpression(literal=bool_literal)

        elif self.current_terminal.kind is K.OPERATOR:
            opr = self.parse_operator()
            exp_list = self.parse_single_expression()
            return UnaryExpression(operator=opr, expression=exp_list)

        elif self.current_terminal.kind is K.IDENTIFIER:
            idf = self.parse_identifier()
            # identifier()
            if self.current_terminal.kind is K.LEFT_PAR:
                self.accept(K.LEFT_PAR)
                exp_list = self.parse_expressions_list()
                self.accept(K.RIGHT_PAR)
                return CallExpression(name=idf, args=exp_list)
            # identifier ~ expression
            elif self.current_terminal.kind in ASSIGNOPS:
                var_exp = VarExpression(idf)
                opr = self.parse_operator()
                exp_list = self.parse_expression_list_assign_operator()
                return BinaryExpression(
                    operator=opr,
                    expression1=var_exp,
                    expression2=exp_list
                )
            else:
                return VarExpression(idf)

        else:
            raise UnsupportedExpressionTokenException(
                current_token=self.current_terminal,
                current_line=self.scanner.current_line,
                current_column=self.scanner.current_column
            )

    def parse_expressions_list(self):
        if self.current_terminal.kind in [K.IDENTIFIER, K.INTEGER_LITERAL, K.OPERATOR, K.TRUE, K.FALSE]:
            exp_list = ArgumentsList()
            exp = self.parse_expression_list_assign_operator()
            exp_list.expressions.append(exp)
            while self.current_terminal.kind is K.COMMA:
                self.accept(K.COMMA)
                exp_list.expressions.append(self.parse_expression_list_assign_operator())
            return exp_list

    def parse_type_indicator(self):
        if self.current_terminal.kind in TYPE_DENOTERS:
            type_i = TypeIndicator(spelling=self.current_terminal.spelling)
            self.current_terminal = self.scanner.scan()
            return type_i

    def parse_integer_literal(self) -> IntegerLiteral:
        if self.current_terminal.kind is K.INTEGER_LITERAL:
            int_literal = IntegerLiteral(self.current_terminal.spelling)
            self.current_terminal = self.scanner.scan()
            return int_literal

    def parse_identifier(self) -> Identifier:
        if self.current_terminal.kind is K.IDENTIFIER:
            idf = Identifier(self.current_terminal.spelling)
            self.current_terminal = self.scanner.scan()
            return idf

    def parse_boolean(self) -> BooleanLiteral:
        if self.current_terminal.kind in [K.TRUE, K.FALSE]:
            bool_literal = BooleanLiteral(spelling=self.current_terminal.spelling)
            return bool_literal

    def parse_operator(self) -> Operator:
        if self.current_terminal.kind is K.OPERATOR:
            opr = Operator(self.current_terminal.spelling)
            self.current_terminal = self.scanner.scan()
            return opr
        else:
            raise UnexpectedTokenException(
                expected_kind=K.OPERATOR,
                current_token=self.current_terminal,
                current_line=self.scanner.current_line,
                current_column=self.scanner.current_column
            )

    def accept(self, token: K):
        if self.current_terminal.kind is token:
            self.current_terminal = self.scanner.scan()
            return True
        else:
            # return False
            raise UnexpectedTokenException(
                expected_kind=token,
                current_token=self.current_terminal,
                current_line=self.scanner.current_line,
                current_column=self.scanner.current_column
            )
