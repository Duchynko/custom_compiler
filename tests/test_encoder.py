import unittest

from TAM.machine import Machine
from abstract_tree import Operator, Terminal, Identifier, IntegerLiteral, IntLiteralExpression, TypeIndicator, \
    UnaryExpression, BinaryExpression, VarExpression, VarDeclaration, DeclarationList, FuncDeclaration, ArgumentsList, \
    CommandList, BooleanLiteral, BooleanLiteralExpression, CallExpression, VarDeclarationWithAssignment
from address import Address
from encoder import Encoder


class MyTestCase(unittest.TestCase):
    encoder: Encoder

    def setUp(self) -> None:
        self.encoder = Encoder()
        Machine.code = [None for _ in range(Machine.PB)]

    def test_visit_operator_returns_spelling(self):
        operator = Operator('~')

        s = self.encoder.visit_operator(operator)

        self.assertEqual(s, '~')

    def test_visit_identifier_returns_spelling(self):
        identifier = Identifier('varname')

        i = self.encoder.visit_identifier(identifier)

        self.assertEqual(i, 'varname')

    def test_visit_type_indicator_returns_size(self):
        int_t = TypeIndicator('int')
        bool_t = TypeIndicator('bool')

        int_n = self.encoder.visit_type_indicator(int_t)
        bool_n = self.encoder.visit_type_indicator(bool_t)

        self.assertEqual(int_n, 1)
        self.assertEqual(bool_n, 1)

    def test_visit_integer_literal_returns_int_value(self):
        il = IntegerLiteral('10')

        value = self.encoder.visit_integer_literal(il)

        self.assertEqual(value, int(il.spelling))

    def test_visit_boolean_literal_returns_int_value(self):
        b_true = BooleanLiteral('true')
        b_false = BooleanLiteral('false')

        r_true = self.encoder.visit_boolean_literal(b_true)
        r_false = self.encoder.visit_boolean_literal(b_false)

        self.assertEqual(r_true, 0)
        self.assertEqual(r_false, 1)

    def test_visit_int_literal_expression_emits_if_value_needed(self):
        exp = IntLiteralExpression(IntegerLiteral('4'))

        self.encoder.visit_int_literal_expression(exp, True)
        load_instr = Machine.code[0]

        self.assertEqual(Machine.LOADLop, load_instr.op_code)

    def test_visit_int_literal_expression_doesnt_emit_if_value_not_needed(self):
        exp = IntLiteralExpression(IntegerLiteral('4'))

        self.encoder.visit_int_literal_expression(exp, False)
        instruction = Machine.code[0]

        self.assertIsNone(instruction)

    def test_visit_var_expression_returns_address_if_value_needed(self):
        i = Identifier('x')
        ve = VarExpression(i)
        ve.declaration = VarDeclaration(TypeIndicator('int'), i)
        address = Address(level=1, displacement=1)
        ve.declaration.address = address

        returned_address: Address = self.encoder.visit_var_expression(ve, True)

        self.assertEqual(returned_address.level, address.level)
        self.assertEqual(returned_address.displacement, address.displacement)

    def test_visit_var_expression_returns_address_if_value_not_needed(self):
        i = Identifier('x')
        ve = VarExpression(i)
        ve.declaration = VarDeclaration(TypeIndicator('int'), i)
        address = Address(level=1, displacement=1)
        ve.declaration.address = address

        returned_address: Address = self.encoder.visit_var_expression(ve, False)

        self.assertEqual(returned_address.level, address.level)
        self.assertEqual(returned_address.displacement, address.displacement)

    def test_visit_var_expression_emits_if_value_needed(self):
        i = Identifier('x')
        ve = VarExpression(i)
        ve.declaration = VarDeclaration(TypeIndicator('int'), i)
        address = Address(level=1, displacement=1)
        ve.declaration.address = address

        self.encoder.current_level = 1
        self.encoder.visit_var_expression(ve, True)
        load_instr = Machine.code[0]

        self.assertEqual(load_instr.op_code, Machine.LOADop)
        self.assertEqual(load_instr.register_number, Machine.LBr)
        self.assertEqual(load_instr.length, 1)
        self.assertEqual(load_instr.operand, 1)

    def test_visit_var_expression_doesnt_emit_if_value_not_needed(self):
        i = Identifier('x')
        ve = VarExpression(i)
        ve.declaration = VarDeclaration(TypeIndicator('int'), i)
        ve.declaration.address = Address(level=1, displacement=1)

        self.encoder.visit_var_expression(ve, False)

        self.assertIsNone(Machine.code[0])

    def test_visit_unary_expression_emits_if_value_needed_and_neg_operator(self):
        i = IntegerLiteral('10')
        ue = UnaryExpression(Operator('-'), IntLiteralExpression(i))

        self.encoder.visit_unary_expression(ue, True)
        load_instr = Machine.code[1]  # The first instruction is LOADL 10

        self.assertEqual(load_instr.op_code, Machine.CALLop)
        self.assertEqual(load_instr.length, 0)
        self.assertEqual(load_instr.register_number, Machine.PBr)
        self.assertEqual(load_instr.operand, Machine.negDisplacement)

    def test_visit_unary_expression_doesnt_emit_if_not_neg_operator(self):
        i = IntegerLiteral('10')
        ue = UnaryExpression(Operator('+'), IntLiteralExpression(i))

        self.encoder.visit_unary_expression(ue, True)

        self.assertIsNone(Machine.code[1])  # The first instruction is LOADL 10

    def test_visit_unary_expression_doesnt_emit_if_not_value_needed(self):
        i = IntegerLiteral('10')
        ue = UnaryExpression(Operator('-'), IntLiteralExpression(i))

        self.encoder.visit_unary_expression(ue, False)

        self.assertIsNone(Machine.code[1])  # The first instruction is LOADL 10

    def test_binary_expression_emits_store_op_if_assign_operator_and_load_op_if_value_needed(self):
        ve = VarExpression(Identifier('x'))
        ve.declaration = VarDeclaration(TypeIndicator('int'), ve.name)
        ve.declaration.address = Address()
        il = IntegerLiteral('5')
        be = BinaryExpression(
            operator=Operator('~'),
            expression1=ve,
            expression2=IntLiteralExpression(il)
        )

        self.encoder.visit_binary_expression(be, True)
        store_instr = Machine.code[1]  # The first instruction is LOADL 5
        load_instr = Machine.code[2]

        self.assertEqual(store_instr.op_code, Machine.STOREop)
        self.assertEqual(store_instr.register_number, Machine.SBr)
        self.assertEqual(store_instr.length, 1)
        self.assertEqual(store_instr.operand, 0)
        self.assertEqual(load_instr.op_code, Machine.LOADop)
        self.assertEqual(load_instr.register_number, Machine.SBr)
        self.assertEqual(load_instr.length, 1)
        self.assertEqual(load_instr.operand, 0)

    def test_binary_expression_emits_store_op_if_assign_operator_and_omits_load_op_if_not_value_needed(self):
        ve = VarExpression(Identifier('x'))
        ve.declaration = VarDeclaration(TypeIndicator('int'), ve.name)
        ve.declaration.address = Address()
        il = IntegerLiteral('5')
        be = BinaryExpression(
            operator=Operator('~'),
            expression1=ve,
            expression2=IntLiteralExpression(il)
        )

        self.encoder.visit_binary_expression(be, False)
        store_instr = Machine.code[1]  # The first instruction is LOADL 5
        load_instr = Machine.code[2]

        self.assertEqual(store_instr.op_code, Machine.STOREop)
        self.assertIsNone(load_instr)

    def test_binary_expression_emits_call_op_if_arithmetic_operator_and_value_needed(self):
        ve = VarExpression(Identifier('x'))
        ve.declaration = VarDeclaration(TypeIndicator('int'), ve.name)
        ve.declaration.address = Address()
        il = IntegerLiteral('5')
        be = BinaryExpression(
            operator=Operator('+'),
            expression1=ve,
            expression2=IntLiteralExpression(il)
        )

        self.encoder.visit_binary_expression(be, True)
        load_instr = Machine.code[2]  # The first two instructions are LOAD x and LOADL 5

        self.assertEqual(load_instr.op_code, Machine.CALLop)
        self.assertEqual(load_instr.register_number, Machine.PBr)
        self.assertEqual(load_instr.length, 0)
        self.assertEqual(load_instr.operand, Machine.addDisplacement)

    def test_binary_expression_doesnt_emit_if_arithmetic_operator_but_not_value_needed(self):
        ve = VarExpression(Identifier('x'))
        ve.declaration = VarDeclaration(TypeIndicator('int'), ve.name)
        ve.declaration.address = Address()
        il = IntegerLiteral('5')
        be = BinaryExpression(
            operator=Operator('+'),
            expression1=ve,
            expression2=IntLiteralExpression(il)
        )

        self.encoder.visit_binary_expression(be, False)
        load_instr = Machine.code[2]  # The first two instructions are LOAD x and LOADL 5

        self.assertIsNone(load_instr)

    def test_visit_boolean_literal_expression_emits_if_value_needed(self):
        be = BooleanLiteralExpression(BooleanLiteral('true'))

        self.encoder.visit_boolean_literal_expression(be, True)
        load_instr = Machine.code[0]

        self.assertEqual(load_instr.op_code, Machine.LOADLop)
        self.assertEqual(load_instr.register_number, 0)
        self.assertEqual(load_instr.length, 1)
        self.assertEqual(load_instr.operand, 0)  # int(true) = 0

    def test_visit_boolean_literal_expression_doesnt_emit_if_not_value_needed(self):
        be = BooleanLiteralExpression(BooleanLiteral('true'))

        self.encoder.visit_boolean_literal_expression(be, False)

        self.assertIsNone(Machine.code[0])

    def test_visit_call_expression_emits_only_call_op_if_value_is_needed(self):
        al = ArgumentsList()
        i = Identifier('callme')
        fd = FuncDeclaration(i, al, CommandList())
        fd.address = Address()
        ce = CallExpression(i, al)
        ce.declaration = fd

        self.encoder.current_level += 1
        self.encoder.visit_call_expression(ce, True)
        call_instr = Machine.code[0]
        pop_instr = Machine.code[1]

        self.assertIsNone(pop_instr)
        self.assertEqual(call_instr.op_code, Machine.CALLop)
        self.assertEqual(call_instr.register_number, Machine.SBr)
        self.assertEqual(call_instr.length, 0)
        self.assertEqual(call_instr.operand, fd.address.displacement)

    def test_visit_call_expression_emits_call_op_and_pop_op_if_value_is_not_needed(self):
        al = ArgumentsList()
        i = Identifier('callme')
        fd = FuncDeclaration(i, al, CommandList())
        fd.address = Address()
        ce = CallExpression(i, al)
        ce.declaration = fd

        self.encoder.current_level += 1
        self.encoder.visit_call_expression(ce, False)
        call_instr = Machine.code[0]
        pop_instr = Machine.code[1]

        self.assertEqual(call_instr.op_code, Machine.CALLop)
        self.assertEqual(pop_instr.op_code, Machine.POPop)
        self.assertEqual(pop_instr.register_number, 0)
        self.assertEqual(pop_instr.length, 0)
        self.assertEqual(pop_instr.operand, 1)

    def test_visit_var_declaration_returns_address(self):
        a = Address(2, 2)
        vd = VarDeclaration(TypeIndicator('int'), Identifier('number'))

        address: Address = self.encoder.visit_var_declaration(vd, a)

        self.assertEqual(address.level, a.level)
        self.assertEqual(address.displacement, a.displacement + 1)

    def test_visit_var_declaration_emits(self):
        a = Address(2, 2)
        vd = VarDeclaration(TypeIndicator('int'), Identifier('number'))

        self.encoder.visit_var_declaration(vd, a)
        push_op = Machine.code[0]

        self.assertEqual(push_op.op_code, Machine.PUSHop)
        self.assertEqual(push_op.length, 0)
        self.assertEqual(push_op.register_number, Machine.SBr + 2)  # SBr + a.level
        self.assertEqual(push_op.operand, 1)

    def test_visit_var_declaration_with_assignment_returns_address(self):
        a = Address(2, 2)
        vd = VarDeclarationWithAssignment(
            TypeIndicator('int'),
            Identifier('number'),
            Operator('~'),
            IntLiteralExpression(IntegerLiteral('10'))
        )

        address: Address = self.encoder.visit_var_declaration_with_assignment(vd, a)

        self.assertEqual(address.level, a.level)
        self.assertEqual(address.displacement, a.displacement + 1)

    def test_visit_var_declaration_with_assignment_emits(self):
        a = Address(2, 2)
        vd = VarDeclarationWithAssignment(
            TypeIndicator('int'),
            Identifier('number'),
            Operator('~'),
            IntLiteralExpression(IntegerLiteral('10'))
        )

        self.encoder.visit_var_declaration_with_assignment(vd, a)
        store_op = Machine.code[1]  # The first operation is LOADL 10

        self.assertEqual(store_op.op_code, Machine.STOREop)
        self.assertEqual(store_op.length, 1)
        self.assertEqual(store_op.register_number, Machine.SBr + a.level)  # SBr + a.level
        self.assertEqual(store_op.operand, a.displacement)

    def test_visit_func_declaration_emits(self):
        a = Address()
        fd = FuncDeclaration(
            identifier=Identifier('my_func'),
            args=ArgumentsList(),
            commands=CommandList()
        )

        self.encoder.visit_func_declaration(fd, a)
        jump_instr = Machine.code[0]
        return_instr = Machine.code[1]

        self.assertEqual(jump_instr.op_code, Machine.JUMPop)
        self.assertEqual(jump_instr.length, 0)
        self.assertEqual(jump_instr.register_number, Machine.CBr)
        self.assertEqual(jump_instr.operand, 2)
        self.assertEqual(return_instr.op_code, Machine.RETURNop)
        self.assertEqual(return_instr.length, 1)
        self.assertEqual(return_instr.register_number, 0)
        self.assertEqual(return_instr.operand, 0)

    # def test_visit_declaration_list(self):
    #     a = Address()
    #     vd1 = VarDeclaration(TypeIndicator('int'), Identifier('number'))
    #     vd2 = VarDeclaration(TypeIndicator('bool'), Identifier('truth'))
    #     vd3 = VarDeclaration(TypeIndicator('int'), Identifier('new_number'))
    #     dl = DeclarationList()
    #     dl.declarations.extend([vd1, vd2, vd3])
    #
    #     size = self.encoder.visit_declaration_list(dl, a)
    #
    #     self.assertEqual(size, 3)
    #     self.assertEqual(vd1.address.level, 0)
    #     self.assertEqual(vd1.address.displacement, 0)
    #     self.assertEqual(vd2.address.level, 0)
    #     self.assertEqual(vd2.address.displacement, 1)
    #     self.assertEqual(vd3.address.level, 0)
    #     self.assertEqual(vd3.address.displacement, 2)


if __name__ == '__main__':
    unittest.main()
