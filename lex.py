import ply.lex as lex
import ply.yacc as yacc


class MyLexer:
    reserved = {
        'if': 'IF',
        'then': 'THEN',
        'else': 'ELSE',
        'end': 'END',
        'int': 'INT'
    }

    # List of token names.   This is always required
    tokens = (
        'INT',

        'IF',
        'THEN',
        'ELSE',
        'END',

        'NUMBER',
        'ID',

        'UMINUS',
        'XOR',
        'AND',
        'INV',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',

        'LPAREN',
        'RPAREN',
        'LS_PAREN',
        'RS_PAREN',
        'LF_PAREN',
        'RF_PAREN',
        'COMMA',
        'SEMIC',

        'EQUAL',
        'GREATER',
        'LESS',
        'G_EQUAL',
        'L_EQUAL',

        'ASSIGN',

        'RETURN',
    )

    # Regular expression rules for simple tokens
    t_XOR = r'\^'
    t_AND = r'\&'
    t_INV = r'\~'
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LS_PAREN = r'\['
    t_RS_PAREN = r'\]'
    t_LF_PAREN = r'\{'
    t_RF_PAREN = r'\}'
    t_COMMA = r','
    t_SEMIC = r';'
    t_EQUAL = r'\=\='
    t_GREATER = r'>'
    t_LESS = r'\<'
    t_G_EQUAL = r'>\='
    t_L_EQUAL = r'\<\='
    t_ASSIGN = r'\='
    t_RETURN = r'RETURN'

    # A regular expression rule with some action code
    # Note addition of self parameter since we're in a class

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'ID')    # Check for reserved words
        return t

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Test it output
    def test(self, data):
        self.lexer.input(data)
        tok = self.lexer.token()
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            # print(tok)


# Build the lexer and try it out
m = MyLexer()
m.build()           # Build the lexer


# s = """
# [int A, int B];
# if (2 + 5 > 3)
# then{
#     A = 3;
# }
# else{
#     B = 5;
# }
# int C;
# C = A + B;

# int t;
# t = A <=B;
# int T;
# A = T>=B;
# int D;
# D = A==B;
# D = A= =B;
# """
# m.test(s)     # Test it
