from TAM.instruction import Instruction
from TAM.machine import Machine
from abstract_tree import Visitor, TypeIndicator, Operator, BooleanLiteral, IntegerLiteral, Identifier, ArgumentsList, \
    VarExpression, BooleanLiteralExpression, IntLiteralExpression, UnaryExpression, CallExpression, ReturnStatement, \
    BinaryExpression, ExpressionList, WhileStatement, IfStatement, ExpressionStatement, VarDeclarationWithAssignment, \
    VarDeclaration, FuncDeclaration, DeclarationList, StatementCommand, DeclarationCommand, CommandList, Program
from address import Address


class Encoder(Visitor):
    def __init__(self):
        self.next_address = Machine.CB
        self.current_level = 0

    def __emit(self, operation: int, length: int,
               register_n: int, displacement: int):
        if length > 255:
            raise Exception('Operand too long')

        instruction = Instruction()
        instruction.op_code = operation
        instruction.length = length
        instruction.register_number = register_n
        instruction.operand = displacement  # TODO: Why do we call this operand and displacement?

        if self.next_address >= Machine.PB:
            raise Exception('Program too large')
        else:
            Machine.code[self.next_address] = instruction
            self.next_address += 1

    def __patch(self, adr: int, length: int):
        Machine.code[adr].length = length

    def __display_register(self, current_level: int, entity_level: int):
        if entity_level == 0:
            return Machine.SBr
        elif current_level - entity_level <= 6:
            return Machine.LBr + current_level - entity_level
        else:
            raise Exception("Can't access the register")

    def save_target_program(self, file_name: str):
        try:
            with open(f"{file_name}", mode='x') as f:
                for i in range(self.next_address):
                    Machine.code[i].write(f)
        except(Exception) as e:
            raise e

    def encode(self, p: Program):
        p.visit(self)

    def visit_program(self, p: Program, *args) -> object:
        self.current_level = 0
        p.command_list.visit(self, Address())
        self.__emit(Machine.HALTop, 0, 0, 0)
        return

    def visit_command_list(self, c: CommandList, *args) -> object:
        for command in c.commands:
            command.visit(self)
        return

    def visit_declaration_command(self, dc: DeclarationCommand, *args) -> object:
        return dc.declaration.visit(self, *args)

    def visit_statement_command(self, sc: StatementCommand, *args) -> object:
        return sc.statement.visit(self, *args)

    def visit_declaration_list(self, d: DeclarationList, *args) -> object:
        address: Address = args[0]
        start_displacement = address.displacement
        for declaration in d.declarations:
            address = declaration.visit(self, address)

        size = address.displacement - start_displacement
        return size

    def visit_func_declaration(self, fd: FuncDeclaration, *args) -> object:
        pass

    def visit_var_declaration(self, vd: VarDeclaration, *args) -> object:
        address = args[0]
        vd.address = address
        size: int = vd.type_indicator.visit(self)
        register = self.__display_register(self.current_level, address.level)
        self.__emit(
            operation=Machine.PUSHop,
            length=size,
            register_n=register,
            displacement=address.displacement
        )
        return Address.from_address(address, 1)

    def visit_var_declaration_with_assignment(self, vd: VarDeclarationWithAssignment, *args) -> object:
        address = args[0]
        vd.address = address
        vd.expression.visit(self, True)
        size: int = vd.type_indicator.visit(self)
        register = self.__display_register(self.current_level, address.displacement)
        self.__emit(
            operation=Machine.STOREop,
            length=size,
            register_n=register,
            displacement=address.displacement
        )

    def visit_expression_statement(self, es: ExpressionStatement, *args) -> object:
        pass

    def visit_if_statement(self, ifs: IfStatement, *args) -> object:
        pass

    def visit_while_statement(self, ws: WhileStatement, *args) -> object:
        pass

    def visit_expression_list(self, el: ExpressionList, *args) -> object:
        pass

    def visit_binary_expression(self, be: BinaryExpression, *args) -> object:
        value_needed = args[0]
        operator: str = be.operator.visit(self)

        if operator == '~':
            address: Address = be.expression1.visit(self, False)
            be.expression2.visit(self, True)

            register = self.__display_register(self.current_level, address.level)
            self.__emit(
                operation=Machine.STOREop,
                length=1,
                register_n=register,
                displacement=address.displacement
            )
            if value_needed:
                self.__emit(Machine.LOADop, 1, register, address.displacement)
        else:
            be.expression1.visit(self, *args)
            be.expression2.visit(self, *args)
            if value_needed:
                procedure = {
                    '+': Machine.addDisplacement,
                    '-': Machine.negDisplacement,
                    '/': Machine.divDisplacement,
                    '*': Machine.multDisplacement,
                    '%': Machine.modDisplacement
                }.get(operator)
                self.__emit(
                    operation=Machine.CALLop,
                    length=0,
                    register_n=Machine.PBr,
                    displacement=procedure
                )

    def visit_return_statement(self, rs: ReturnStatement, *args) -> object:
        pass

    def visit_call_expression(self, ce: CallExpression, *args) -> object:
        ce.args.visit(self)
        address = ce.declaration.address
        self.__emit(
            operation=Machine.CALLop,
            length=0,
            register_n=address.register,
            displacement=address.displacement
        )

    def visit_unary_expression(self, be: UnaryExpression, *args) -> object:
        value_needed: bool = args[0]
        operator = be.operator.visit(self)
        be.expression.visit(self, value_needed)

        if operator == '-' and value_needed:
            self.__emit(
                operation=Machine.CALLop,
                length=0,
                register_n=Machine.PBr,
                displacement=Machine.negDisplacement
            )
        return None

    def visit_int_literal_expression(self, ie: IntLiteralExpression, *args) -> object:
        value_needed: bool = args[0]
        value: int = ie.literal.visit(self)
        if value_needed:
            self.__emit(Machine.LOADLop, 1, 0, value)
        return

    def visit_boolean_literal_expression(self, be: BooleanLiteralExpression, *args) -> object:
        value_needed: bool = args[0]
        value: bool = be.literal.visit(self)
        if value_needed:
            self.__emit(Machine.LOADLop, 1, 0, value)
        return

    def visit_var_expression(self, ve: VarExpression, *args) -> object:
        value_needed: bool = args[0]
        address = ve.declaration.address
        register = address.level
        if value_needed:
            self.__emit(
                operation=Machine.LOADop,
                length=1,  # TODO: Change this
                register_n=register,
                displacement=address.displacement
            )
        return address

    def visit_arguments_list(self, al: ArgumentsList, *args) -> object:
        for argument in al.expressions:
            argument.visit(self, True)
        return

    def visit_identifier(self, i: Identifier, *args) -> object:
        return i.spelling

    def visit_integer_literal(self, il: IntegerLiteral, *args) -> object:
        return int(il.spelling)

    def visit_boolean_literal(self, bl: BooleanLiteral, *args) -> object:
        return bl.spelling

    def visit_operator(self, o: Operator, *args) -> object:
        return o.spelling

    def visit_type_indicator(self, ti: TypeIndicator, *args) -> object:
        return {
            'int': 1,
            'bool': 1
        }.get(ti.spelling, None)
