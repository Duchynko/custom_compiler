import unittest

from TAM.machine import Machine
from abstract_tree import Operator, Terminal, Identifier, IntegerLiteral, IntLiteralExpression, TypeIndicator, \
    UnaryExpression, BinaryExpression, VarExpression, VarDeclaration, DeclarationList, FuncDeclaration, ArgumentsList, \
    CommandList
from address import Address
from encoder import Encoder


class MyTestCase(unittest.TestCase):
    encoder: Encoder

    def setUp(self) -> None:
        self.encoder = Encoder()

    def test_visit_operator(self):
        operator = Operator('~')

        s = self.encoder.visit_operator(operator)

        self.assertEqual(s, '~')

    def test_visit_identifier(self):
        identifier = Identifier('varname')

        i = self.encoder.visit_identifier(identifier)

        self.assertEqual(i, 'varname')

    def test_visit_type_indicator(self):
        t = TypeIndicator('int')

        n = self.encoder.visit_type_indicator(t)

        self.assertEqual(n, 1)

    def test_visit_int_literal_expression(self):
        i = IntegerLiteral('4')
        exp = IntLiteralExpression(i)

        self.encoder.visit_int_literal_expression(exp, True)
        instruction = Machine.code[self.encoder.next_address]

        self.assertEqual(instruction.op_code, Machine.LOADLop)

    def test_visit_var_expression(self):
        pass

    def test_visit_unary_expression(self):
        i = IntegerLiteral('10')
        ie = IntLiteralExpression(i)
        o = Operator('-')
        ue = UnaryExpression(o, ie)

        self.encoder.visit_unary_expression(ue, True)
        literal_inst = Machine.code[0]
        call_inst = Machine.code[1]

        self.assertEqual(literal_inst.op_code, Machine.LOADLop)
        self.assertEqual(call_inst.op_code, Machine.CALLop)

    def test_binary_expression_with_minus_operator(self):
        i1 = IntegerLiteral('10')
        ie1 = IntLiteralExpression(i1)
        i2 = IntegerLiteral('5')
        ie2 = IntLiteralExpression(i2)
        o = Operator('-')
        be = BinaryExpression(
            operator=o,
            expression1=ie1,
            expression2=ie2
        )

        self.encoder.visit_binary_expression(be, True)
        instr1 = Machine.code[0]
        instr2 = Machine.code[1]
        instr3 = Machine.code[2]

        self.assertEqual(instr1.op_code, Machine.LOADLop)
        self.assertEqual(instr2.op_code, Machine.LOADLop)
        self.assertEqual(instr3.op_code, Machine.CALLop)
        self.assertEqual(instr3.operand, Machine.negDisplacement)

    def test_binary_expression_with_assignment_operator(self):
        varname = Identifier('varname')
        ve = VarExpression(varname)
        ve.declaration = VarDeclaration(TypeIndicator('int'), varname)
        ve.declaration.address = Address()
        i2 = IntegerLiteral('5')
        ie = IntLiteralExpression(i2)
        o = Operator('~')
        be = BinaryExpression(
            operator=o,
            expression1=ve,
            expression2=ie
        )

        self.encoder.visit_binary_expression(be, True)
        instr1 = Machine.code[0]
        instr2 = Machine.code[1]
        instr3 = Machine.code[2]

        self.assertEqual(instr1.op_code, Machine.LOADLop)
        self.assertEqual(instr2.op_code, Machine.STOREop)
        self.assertEqual(instr2.register_number, Machine.SBr)
        self.assertEqual(instr3.op_code, Machine.LOADop)
        self.assertEqual(instr3.register_number, Machine.SBr)

    def test_visit_var_declaration(self):
        a = Address(2, 0)
        vd = VarDeclaration(TypeIndicator('int'), Identifier('number'))

        address: Address = self.encoder.visit_var_declaration(vd, a)

        self.assertEqual(address.level, a.level)
        self.assertEqual(address.displacement, a.displacement + 1)

    def test_visit_func_declaration(self):
        a = Address()
        fd = FuncDeclaration(
            identifier=Identifier('my_func'),
            args=ArgumentsList(),
            commands=CommandList()
        )

        self.encoder.current_level = 1
        self.encoder.visit_func_declaration(fd, a)

        self.assertEqual(fd.address.level, 1)
        self.assertEqual(fd.address.displacement, 0)

    def test_visit_declaration_list(self):
        a = Address()
        vd1 = VarDeclaration(TypeIndicator('int'), Identifier('number'))
        vd2 = VarDeclaration(TypeIndicator('bool'), Identifier('truth'))
        vd3 = VarDeclaration(TypeIndicator('int'), Identifier('new_number'))
        dl = DeclarationList()
        dl.declarations.extend([vd1, vd2, vd3])

        size = self.encoder.visit_declaration_list(dl, a)

        self.assertEqual(size, 3)
        self.assertEqual()


if __name__ == '__main__':
    unittest.main()
