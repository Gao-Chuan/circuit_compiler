import ply.yacc as yacc
from lex import MyLexer
from copy import deepcopy

tokens = MyLexer.tokens

circuit = []

if_expr = []
if_expr_hight = 0

intLength = 8

wire_num = 0
gate_num = 0
temp_name = 0

A_input_len = 0
B_input_len = 0
output_len = 0

precedence = (
    # Nonassociative operators
    ('left', 'ASSIGN'),
    ('nonassoc', 'LESS', 'GREATER', 'EQUAL', 'G_EQUAL', 'L_EQUAL'),
    ('left', 'XOR'),
    ('left', 'AND'),
    ('left', 'INV'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),            # Unary minus operator
)


variable = {
    'name': None,
    'type': None,
    'value': None,
    'wire_start': None
}

variable_table = {}


def _init_variable(name, value, type_):
    global wire_num
    global variable_table

    tmp = deepcopy(variable)
    tmp['name'] = name
    tmp['type'] = type_
    tmp['value'] = value
    tmp['wire_start'] = wire_num
    wire_num += intLength
    variable_table[tmp['name']] = tmp

    if value:
        _set_variable(name, value)

    return name


def _init_tmp_variable(value, type_):
    global wire_num
    global variable_table
    global temp_name

    tmp = deepcopy(variable)
    tmp['name'] = str(temp_name)
    temp_name += 1
    tmp['type'] = type_
    tmp['value'] = value
    tmp['wire_start'] = wire_num
    wire_num += intLength
    variable_table[tmp['name']] = tmp

    if value:
        _set_variable(tmp['name'], value)

    return tmp['name']


def _init_tmp_line():
    global wire_num
    wire_num += 1
    return wire_num - 1


zero = _init_tmp_line()
one = _init_tmp_line()
circuit.append('1 1 ' + str(one) + ' ' + str(one) + ' INV')
gate_num += 1
whoKnows = _init_tmp_line()


def _set_variable(name, value):
    global circuit
    global variable_table
    global gate_num

    for i in range(intLength):
        circuit_line = '2 1 '
        circuit_line += str(variable_table[name]['wire_start'] + i) + ' '
        circuit_line += str(variable_table[name]['wire_start'] + i) + ' '
        circuit_line += 'XOR'
        circuit.append(circuit_line)
        gate_num += 1

    for i in range(intLength):
        if value & (1 << i):
            circuit_line = '1 1 '
            circuit_line += str(variable_table[name]['wire_start'] + i) + ' '
            circuit_line += str(variable_table[name]['wire_start'] + i) + ' '
            circuit_line += 'INV'
            circuit.append(circuit_line)
            gate_num += 1


def _full_adder(A, B, Ci_1, Si, Ci):
    global circuit
    global gate_num

    # 3 INV line
    _A, _B, _Ci_1 = _init_tmp_line(), _init_tmp_line(), _init_tmp_line()
    circuit.append('1 1 ' + str(A) + ' ' + str(_A) + ' INV')
    circuit.append('1 1 ' + str(B) + ' ' + str(_B) + ' INV')
    circuit.append('1 1 ' + str(Ci_1) + ' ' + str(_Ci_1) + ' INV')

    gate_num += 3

    # 1st 3 input AND gate
    tmp_1 = _init_tmp_line()
    circuit.append("2 1 " + str(A) + ' ' + str(B) + ' ' + str(tmp_1) + ' AND')
    and_1 = _init_tmp_line()
    circuit.append("2 1 " + str(tmp_1) + ' ' +
                   str(Ci_1) + ' ' + str(and_1) + ' AND')

    # 2nd 3 input AND gate
    tmp_1 = _init_tmp_line()
    circuit.append("2 1 " + str(A) + ' ' + str(B) + ' ' + str(tmp_1) + ' AND')
    and_2 = _init_tmp_line()
    circuit.append("2 1 " + str(tmp_1) + ' ' +
                   str(_Ci_1) + ' ' + str(and_2) + ' AND')

    # 3rd 3 input AND gate
    tmp_1 = _init_tmp_line()
    circuit.append("2 1 " + str(A) + ' ' + str(_B) + ' ' + str(tmp_1) + ' AND')
    and_3 = _init_tmp_line()
    circuit.append("2 1 " + str(tmp_1) + ' ' +
                   str(Ci_1) + ' ' + str(and_3) + ' AND')

    # 4th 3 input AND gate
    tmp_1 = _init_tmp_line()
    circuit.append("2 1 " + str(_A) + ' ' + str(B) + ' ' + str(tmp_1) + ' AND')
    and_4 = _init_tmp_line()
    circuit.append("2 1 " + str(tmp_1) + ' ' +
                   str(Ci_1) + ' ' + str(and_4) + ' AND')

    # 5th 3 input AND gate
    tmp_1 = _init_tmp_line()
    circuit.append("2 1 " + str(A) + ' ' + str(B) + ' ' + str(tmp_1) + ' AND')
    and_5 = _init_tmp_line()
    circuit.append("2 1 " + str(tmp_1) + ' ' +
                   str(Ci_1) + ' ' + str(and_5) + ' AND')

    # 6th 3 input AND gate
    tmp_1 = _init_tmp_line()
    circuit.append("2 1 " + str(A) + ' ' + str(_B) + ' ' + str(tmp_1) + ' AND')
    and_6 = _init_tmp_line()
    circuit.append("2 1 " + str(tmp_1) + ' ' +
                   str(_Ci_1) + ' ' + str(and_6) + ' AND')

    # 7th 3 input AND gate
    tmp_1 = _init_tmp_line()
    circuit.append("2 1 " + str(_A) + ' ' + str(B) + ' ' + str(tmp_1) + ' AND')
    and_7 = _init_tmp_line()
    circuit.append("2 1 " + str(tmp_1) + ' ' +
                   str(_Ci_1) + ' ' + str(and_7) + ' AND')

    # 8th 3 input AND gate
    tmp_1 = _init_tmp_line()
    circuit.append("2 1 " + str(_A) + ' ' +
                   str(_B) + ' ' + str(tmp_1) + ' AND')
    and_8 = _init_tmp_line()
    circuit.append("2 1 " + str(tmp_1) + ' ' +
                   str(Ci_1) + ' ' + str(and_8) + ' AND')

    gate_num += 16

    # Ci output with 4 input or gate
    # or_1
    tmp_1 = _init_tmp_line()
    circuit.append('2 1 ' + str(and_1) + ' ' +
                   str(and_2) + ' ' + str(tmp_1) + ' XOR')
    tmp_2 = _init_tmp_line()
    circuit.append('2 1 ' + str(and_1) + ' ' +
                   str(and_2) + ' ' + str(tmp_2) + ' AND')
    or_1 = _init_tmp_line()
    circuit.append('2 1 ' + str(tmp_1) + ' ' +
                   str(tmp_2) + ' ' + str(or_1) + ' XOR')
    # or_2
    tmp_1 = _init_tmp_line()
    circuit.append('2 1 ' + str(and_3) + ' ' +
                   str(and_4) + ' ' + str(tmp_1) + ' XOR')
    tmp_2 = _init_tmp_line()
    circuit.append('2 1 ' + str(and_3) + ' ' +
                   str(and_4) + ' ' + str(tmp_2) + ' AND')
    or_2 = _init_tmp_line()
    circuit.append('2 1 ' + str(tmp_1) + ' ' +
                   str(tmp_2) + ' ' + str(or_2) + ' XOR')
    # Ci
    tmp_1 = _init_tmp_line()
    circuit.append('2 1 ' + str(or_1) + ' ' +
                   str(or_2) + ' ' + str(tmp_1) + ' XOR')
    tmp_2 = _init_tmp_line()
    circuit.append('2 1 ' + str(or_1) + ' ' +
                   str(or_2) + ' ' + str(tmp_2) + ' AND')
    or_1 = _init_tmp_line()
    circuit.append('2 1 ' + str(tmp_1) + ' ' +
                   str(tmp_2) + ' ' + str(Ci) + ' XOR')

    gate_num += 9

    # Si output with 4 input or gate
    # or_1
    tmp_1 = _init_tmp_line()
    circuit.append('2 1 ' + str(and_5) + ' ' +
                   str(and_6) + ' ' + str(tmp_1) + ' XOR')
    tmp_2 = _init_tmp_line()
    circuit.append('2 1 ' + str(and_5) + ' ' +
                   str(and_6) + ' ' + str(tmp_2) + ' AND')
    or_1 = _init_tmp_line()
    circuit.append('2 1 ' + str(tmp_1) + ' ' +
                   str(tmp_2) + ' ' + str(or_1) + ' XOR')
    # or_2
    tmp_1 = _init_tmp_line()
    circuit.append('2 1 ' + str(and_7) + ' ' +
                   str(and_8) + ' ' + str(tmp_1) + ' XOR')
    tmp_2 = _init_tmp_line()
    circuit.append('2 1 ' + str(and_7) + ' ' +
                   str(and_8) + ' ' + str(tmp_2) + ' AND')
    or_2 = _init_tmp_line()
    circuit.append('2 1 ' + str(tmp_1) + ' ' +
                   str(tmp_2) + ' ' + str(or_2) + ' XOR')
    # Ci
    tmp_1 = _init_tmp_line()
    circuit.append('2 1 ' + str(or_1) + ' ' +
                   str(or_2) + ' ' + str(tmp_1) + ' XOR')
    tmp_2 = _init_tmp_line()
    circuit.append('2 1 ' + str(or_1) + ' ' +
                   str(or_2) + ' ' + str(tmp_2) + ' AND')
    or_1 = _init_tmp_line()
    circuit.append('2 1 ' + str(tmp_1) + ' ' +
                   str(tmp_2) + ' ' + str(Si) + ' XOR')

    gate_num += 9


def adder_4(A, B, Ci_1, Si, Ci):
    # 1st full adder
    tmp_ci_1 = _init_tmp_line()
    _full_adder(A, B, Ci_1, Si, tmp_ci_1)
    A, B, Si = A + 1, B + 1, Si + 1
    # 2nd full adder
    tmp_ci_2 = _init_tmp_line()
    _full_adder(A, B, tmp_ci_1, Si, tmp_ci_2)
    A, B, Si = A + 1, B + 1, Si + 1
    # 3rd full adder
    tmp_ci_3 = _init_tmp_line()
    _full_adder(A, B, tmp_ci_2, Si, tmp_ci_3)
    A, B, Si = A + 1, B + 1, Si + 1
    # 4th full adder
    _full_adder(A, B, tmp_ci_3, Si, Ci)


def adder_8(A, B, Ci_1, Si, Ci):
    # 1st adder_4
    tmp_ci = _init_tmp_line()
    adder_4(A, B, Ci_1, Si, tmp_ci)
    A, B, Si = A + 4, B + 4, Si + 4
    # 2nd adder_4
    adder_4(A, B, tmp_ci, Si, Ci)


def p_sentence(p):
    '''sentence : statement SEMIC sentence
                | empty'''
    pass


def p_statement(p):
    '''statement    : statement_b
                    | statement_op'''
    pass


def p_statement_b(p):
    '''statement_b  : IF iexpression THEN iblock END
                    | IF iexpression THEN iblock ELSE eblock END'''
    global if_expr_hight
    global if_expr
    if len(p) == 6:
        if_expr_hight -= 1
        if_expr.pop()
    elif len(p) == 8:
        if_expr_hight -= 1
        if_expr.pop()


def p_statement_op(p):
    '''statement_op : word'''
    pass


def p_iexpression(p):
    '''iexpression : expression'''
    global if_expr
    global if_expr_hight

    if type(p[1]) == type(1):
        tmp = _init_tmp_variable(p[1], 'int')
        if_expr.append(tmp)
    else:
        if_expr.append(p[1])
    if_expr_hight += 1


def p_iblock(p):
    '''iblock : istat SEMIC iblock
              | empty'''
    pass


def p_istat(p):
    '''istat : statement_b
             | iword'''
    pass


def _pick_1of2(x, y, k, q):
    ''''8 bits Y-shaped selector.
    k == 1: q = x
    k == 0: q = y'''
    global circuit


def p_iword(p):
    '''iword : ID ASSIGN expression
            | INT ID'''
    print('iword')
    global if_expr
    if len(p) == 3:
        _init_variable(p[2], 0, p[1])
    else:
        if type(p[3]) == str:
            variable_table[p[1]]['value'] = variable_table[p[3]]['value']
            # use 2 INV gate to translate value from 1 int to another
            for i in range(intLength):
                circuit_line = '1 1 '
                circuit_line += str(variable_table[p[3]]
                                    ['wire_start'] + i) + ' '
                circuit_line += str(variable_table[p[1]]
                                    ['wire_start'] + i) + ' '
                circuit_line += 'INV'
                circuit.append(circuit_line)

                circuit_line = '1 1 '
                circuit_line += str(variable_table[p[1]]
                                    ['wire_start'] + i) + ' '
                circuit_line += str(variable_table[p[1]]
                                    ['wire_start'] + i) + ' '
                circuit_line += 'INV'
                circuit.append(circuit_line)

                gate_num += 2

        else:
            variable_table[p[1]]['value'] = p[3]
            _set_variable(p[1], variable_table[p[1]]['value'])


def p_eblock(p):
    '''eblock : estat SEMIC eblock
              | empty'''
    print('eblock')


def p_estat(p):
    '''estat : statement_b
             | eword'''
    print('estat')


def p_eword(p):
    '''eword : ID ASSIGN expression
            | INT ID'''
    print('eword')


def p_word(p):
    '''word : ID ASSIGN expression
            | INT ID'''

    global variable_table
    global circuit
    global gate_num

    if p[2] == '=':
        if type(p[3]) == str:
            variable_table[p[1]]['value'] = variable_table[p[3]]['value']
            # use 2 INV gate to translate value from 1 int to another
            for i in range(intLength):
                circuit_line = '1 1 '
                circuit_line += str(variable_table[p[3]]
                                    ['wire_start'] + i) + ' '
                circuit_line += str(variable_table[p[1]]
                                    ['wire_start'] + i) + ' '
                circuit_line += 'INV'
                circuit.append(circuit_line)

                circuit_line = '1 1 '
                circuit_line += str(variable_table[p[1]]
                                    ['wire_start'] + i) + ' '
                circuit_line += str(variable_table[p[1]]
                                    ['wire_start'] + i) + ' '
                circuit_line += 'INV'
                circuit.append(circuit_line)

                gate_num += 2

        else:
            variable_table[p[1]]['value'] = p[3]
            _set_variable(p[1], variable_table[p[1]]['value'])

    if p[1] == 'int':
        _init_variable(p[2], 0, p[1])


def p_expression(p):
    '''expression : expression PLUS term
                  | expression MINUS term
                  | expression AND term
                  | expression XOR term
                  | INV term
                  | term'''

    global variable_table
    global gate_num
    global circuit

    if len(p) == 2:
        p[0] = p[1]

    elif len(p) == 3:
        if type(p[2]) == type(3):
            p[0] = ~p[2]
        else:
            p[0] = _init_tmp_variable(0, 'int')
            variable_table[p[0]]['value'] = ~variable_table[p[2]]['value']

            for i in range(intLength):
                circuit_line = '1 1 '
                circuit_line += str(variable_table[p[0]]
                                    ['wire_start'] + i) + ' '
                circuit_line += str(variable_table[p[2]]
                                    ['wire_start'] + i) + ' '
                circuit_line += 'INV'

                circuit.append(circuit_line)
                gate_num += 1

    elif p[2] == '+':
        if type(p[1]) == type(1) and type(p[3]) == type(1):
            p[0] = p[1] + p[3]

        elif type(p[1]) == type(1) and type(p[3]) != type(1):
            p[1] = _init_tmp_variable(p[1], 'int')

            p[0] = _init_tmp_variable(0, 'int')
            variable_table[p[0]]['value'] = variable_table[p[1]
                                                           ]['value'] + variable_table[p[3]]['value']
            adder_8(variable_table[p[1]]['wire_start'], variable_table[p[3]]['wire_start'],
                    zero, variable_table[p[0]]['wire_start'], whoKnows)

        elif type(p[1]) != type(1) and type(p[3]) == type(1):
            p[3] = _init_tmp_variable(p[3], 'int')

            p[0] = _init_tmp_variable(0, 'int')
            variable_table[p[0]]['value'] = variable_table[p[1]
                                                           ]['value'] + variable_table[p[3]]['value']
            adder_8(variable_table[p[1]]['wire_start'], variable_table[p[3]]['wire_start'],
                    zero, variable_table[p[0]]['wire_start'], whoKnows)

        else:
            p[0] = _init_tmp_variable(0, 'int')
            variable_table[p[0]]['value'] = variable_table[p[1]
                                                           ]['value'] + variable_table[p[3]]['value']
            adder_8(variable_table[p[1]]['wire_start'], variable_table[p[3]]['wire_start'],
                    zero, variable_table[p[0]]['wire_start'], whoKnows)

    elif p[2] == '-':
        if type(p[1]) == type(1) and type(p[3]) == type(1):
            p[0] = p[1] - p[3]

        elif type(p[1]) == type(1) and type(p[3]) != type(1):
            p[1] = _init_tmp_variable(p[1], 'int')

            p[0] = _init_tmp_variable(0, 'int')
            variable_table[p[0]]['value'] = variable_table[p[1]
                                                           ]['value'] - variable_table[p[3]]['value']
            B = variable_table[p[3]]['wire_start']
            for i in range(intLength):
                circuit.append('2 1 ' + str(B + i) + ' ' +
                               str(one) + ' ' + str(B + i) + ' XOR')

            adder_8(p[1]['wire_start'], p[3]['wire_start'],
                    one, p[0]['wire_start'], whoKnows)

        elif type(p[1]) != type(1) and type(p[3]) == type(1):
            p[3] = _init_tmp_variable(p[3], 'int')

            p[0] = _init_tmp_variable(0, 'int')
            variable_table[p[0]]['value'] = variable_table[p[1]
                                                           ]['value'] - variable_table[p[3]]['value']
            B = variable_table[p[3]]['wire_start']
            for i in range(intLength):
                circuit.append('2 1 ' + str(B + i) + ' ' +
                               str(one) + ' ' + str(B + i) + ' XOR')

            adder_8(p[1]['wire_start'], p[3]['wire_start'],
                    one, p[0]['wire_start'], whoKnows)

        else:
            p[0] = _init_tmp_variable(0, 'int')
            variable_table[p[0]]['value'] = variable_table[p[1]
                                                           ]['value'] - variable_table[p[3]]['value']
            B = variable_table[p[3]]['wire_start']
            for i in range(intLength):
                circuit.append('2 1 ' + str(B + i) + ' ' +
                               str(one) + ' ' + str(B + i) + ' XOR')

            A = variable_table[p[1]]['wire_start']
            B = variable_table[p[3]]['wire_start']
            Si = variable_table[p[0]]['wire_start']
            adder_8(A, B, one, Si, whoKnows)

    elif p[2] == '^':
        p[0] = _init_tmp_variable(0, 'int')
        variable_table[p[0]]['value'] = variable_table[p[1]
                                                       ]['value'] ^ variable_table[p[3]]['value']

        for i in range(intLength):
            circuit_line = '2 1 '
            circuit_line += str(variable_table[p[1]]['wire_start'] + i) + ' '
            circuit_line += str(variable_table[p[3]]['wire_start'] + i) + ' '
            circuit_line += str(variable_table[p[0]]['wire_start'] + i) + ' '
            circuit_line += 'XOR'
            circuit.append(circuit_line)
            gate_num += 1

    elif p[2] == '&':
        p[0] = _init_tmp_variable(0, 'int')
        variable_table[p[0]]['value'] = variable_table[p[1]
                                                       ]['value'] & variable_table[p[3]]['value']

        for i in range(intLength):
            circuit_line = '2 1 '
            circuit_line += str(variable_table[p[1]]['wire_start'] + i) + ' '
            circuit_line += str(variable_table[p[3]]['wire_start'] + i) + ' '
            circuit_line += str(variable_table[p[0]]['wire_start'] + i) + ' '
            circuit_line += 'AND'
            circuit.append(circuit_line)
            gate_num += 1


def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor
            | factor'''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]


def p_factor(p):
    '''factor : NUMBER
              | LPAREN expression RPAREN 
              | ID'''
    if len(p) == 2:
        p[0] = p[1]
    elif p[1] == '(':
        p[0] = p[2]


def p_empty(p):
    'empty :'
    pass

# Error rule for syntax errors


def p_error(p):
    print("Syntax error in input!")


# Build the parser
parser = yacc.yacc()

data = '''
int a;
int b;
a = 3;
b = 7;
if 1+2+3+4+5+6
then 
    if 1+2+3+4
    then 
        a = 1;
    else
        b = 2;
    end;
    a = 4;
else 
    b = 1;
    a = 2;
end;
'''

parser.parse(data)
for k in variable_table:
    print(variable_table[k])
for e in circuit:
    print(e)
print(gate_num, end=', ')
print(wire_num)
