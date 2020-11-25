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

    def __patch(self, adr: int, displacement: int):
        Machine.code[adr].operand = displacement

    def __display_register(self, current_level: int, entity_level: int):
        if entity_level == 0:
            return Machine.SBr
        elif current_level - entity_level <= 6:
            return Machine.LBr + current_level - entity_level
        else:
            raise Exception("Can't access the register")

    def save_target_program(self, file_name: str):
        try:
            with open(f"{file_name}", mode='wb') as f:
                print(f"Length of instructions: {self.next_address}")
                for i in range(self.next_address):
                    print(f"[{i}]: Op_code {Machine.code[i].op_code}")
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
            command.visit(self, *args)
        return

    def visit_declaration_command(self, dc: DeclarationCommand, *args) -> object:
        print(f"Number of declarations: {len(dc.declaration_list.declarations)}")
        return dc.declaration_list.visit(self, *args)

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
        fd.address = Address(self.current_level, self.next_address)
        self.current_level += 1
        address = Address.from_address(args[0])  # Inner frame
        # Jump over the Command part so that it's not executed during the
        # function declaration. register_r is initially set to CBr (0), but
        # will be patched later, when we know the size of the function.
        jump_instr = self.next_address
        self.__emit(
            operation=Machine.JUMPop,
            length=0,
            register_n=Machine.CBr,
            displacement=0
        )
        fd.commands.visit(self, Address.from_address(address, Machine.link_data_size))
        self.__emit(
            operation=Machine.RETURNop,
            length=1,  # TODO: Refactor to set length dynamically
            register_n=0,
            displacement=len(fd.args.expressions)  # TODO: How to do this properly?
        )
        # This is the end of the function, and the jump instruction can be patched
        self.__patch(jump_instr, self.next_address)
        # self.__emit(
        #     operation=Machine.JUMPop,
        #     length=0,
        #     register_n=0,  # TODO: Add static and dynamic link
        #     displacement=0  # TODO: Add static and dynamic link
        # )
        self.current_level -= 1
        return args[0]  # Return back the address

    def visit_var_declaration(self, vd: VarDeclaration, *args) -> object:
        address = args[0]
        vd.address = address
        register = self.__display_register(self.current_level, address.level)
        size: int = vd.type_indicator.visit(self)
        self.__emit(
            operation=Machine.PUSHop,
            length=0,
            register_n=register,
            displacement=size
        )
        return Address.from_address(address=address, increment=1)

    def visit_var_declaration_with_assignment(self, vd: VarDeclarationWithAssignment, *args) -> object:
        address = args[0]  # An address for the new variable
        print(f"Received address: {address}")
        vd.address = address
        register = self.__display_register(self.current_level, address.level)
        size: int = vd.type_indicator.visit(self)
        # Evaluate expression and LOAD it's value on to the stack. Because the value will be
        # stored right away, it's not necessary to call PUSH.
        vd.expression.visit(self, True)
        # Pop the value from the stack top and store it into the register
        self.__emit(
            operation=Machine.STOREop,
            length=size,
            register_n=register,
            displacement=address.displacement
        )
        new_address = Address.from_address(address=address, increment=1)
        print(f"Returning from function: {new_address}")
        return new_address

    def visit_expression_statement(self, es: ExpressionStatement, *args) -> object:
        es.expressions.visit(self, *args)
        return

    def visit_if_statement(self, ifs: IfStatement, *args) -> object:
        # Evaluate an expression and push the result to the stack top
        ifs.expr.visit(self, True)
        # Emit JUMPIF instruction that will jump to the else-part of
        # the block. (This value will be patched once we generate
        # code for the if-part of the block)
        jump1_addr = self.next_address
        self.__emit(Machine.JUMPIFop, 0, Machine.CBr, 0)
        # Generate instructions for the if-part of the block
        ifs.if_com.visit(self, None)
        # Emit JUMP instruction that will jump to the end of the
        # if-else block
        jump2_addr = self.next_address
        self.__emit(Machine.JUMPop, 0, Machine.CBr, 0)
        # Patch the JUMPIF operation, pointing to the address where
        # the else-part of the block begins
        self.__patch(jump1_addr, self.next_address)
        # Generate instructions for the else-part of the block
        ifs.else_com.visit(self, None)
        self.__patch(jump2_addr, self.next_address)
        # Patch the JUMP instruction, pointing to the address after
        # the if-else block.
        return

    def visit_while_statement(self, ws: WhileStatement, *args) -> object:
        start_address = self.next_address
        # Evaluate an expression pushing the result on the top of the stack
        ws.expr.visit(self, True)
        # Jump at the end of the while block if the above expression
        # evaluates to false
        jump_address = self.next_address
        self.__emit(
            operation=Machine.JUMPIFop,
            length=0,
            register_n=Machine.CBr,
            displacement=0
        )
        ws.command.visit(self, None)
        # Jump back to the beginning of the while block and evaluate
        # the expression
        self.__emit(
            operation=Machine.JUMPop,
            length=0,
            register_n=Machine.CBr,
            displacement=start_address
        )
        self.__patch(jump_address, self.next_address)
        return

    def visit_expression_list(self, el: ExpressionList, *args) -> object:
        for expression in el.expressions:
            expression.visit(self, *args)
        return

    def visit_binary_expression(self, be: BinaryExpression, *args) -> object:
        value_needed = args[0]
        operator: str = be.operator.visit(self, None)

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
        value_needed = args[0]
        # Load all parameters on the top of the stack
        ce.args.visit(self, True)
        address = ce.declaration.address
        register = self.__display_register(self.current_level, address.level)
        self.__emit(
            operation=Machine.CALLop,
            length=0,
            register_n=register,
            displacement=address.displacement + 1  # Skip the JUMPop and execute Command part
        )
        # If the return value is not needed, remove it from the stack top
        if not value_needed:
            self.__emit(
                operation=Machine.POPop,
                length=0,
                register_n=0,
                displacement=1  # TODO: Make this dynamic
            )
        return

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
        return

    def visit_int_literal_expression(self, ie: IntLiteralExpression, *args) -> object:
        value_needed: bool = args[0]
        value: int = ie.literal.visit(self, None)
        if value_needed:
            self.__emit(Machine.LOADLop, 1, 0, value)
        return

    def visit_boolean_literal_expression(self, be: BooleanLiteralExpression, *args) -> object:
        value_needed: bool = args[0]
        value: int = be.literal.visit(self, None)
        if value_needed:
            self.__emit(
                operation=Machine.LOADLop,
                length=1,
                register_n=0,
                displacement=value
            )
        return

    def visit_var_expression(self, ve: VarExpression, *args) -> object:
        value_needed: bool = args[0]
        address = ve.declaration.address
        register = self.__display_register(self.current_level, address.level)
        size: int = ve.declaration.type_indicator.visit(self, None)  # TODO: Size probably in the Address object
        if value_needed:
            self.__emit(
                operation=Machine.LOADop,
                length=size,
                register_n=register,
                displacement=address.displacement
            )
        return address

    def visit_arguments_list(self, al: ArgumentsList, *args) -> object:
        for expr in al.expressions:
            expr.visit(self, True)
        return

    def visit_identifier(self, i: Identifier, *args) -> object:
        return i.spelling

    def visit_integer_literal(self, il: IntegerLiteral, *args) -> object:
        return int(il.spelling)

    def visit_boolean_literal(self, bl: BooleanLiteral, *args) -> object:
        return {
            'true': 1,
            'false': 0
        }.get(bl.spelling)

    def visit_operator(self, o: Operator, *args) -> object:
        return o.spelling

    def visit_type_indicator(self, ti: TypeIndicator, *args) -> object:
        return {
            'int': 1,
            'bool': 1
        }.get(ti.spelling, None)
