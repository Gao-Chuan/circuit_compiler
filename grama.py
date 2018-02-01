'''
sentence    :    statement SEMIC sentence
            |    empty
statement   : statement_b
            | statement_op

statement_b :    IF iexpression THEN iblock END
            |    IF iexpression THEN iblock ELSE eblock END

statement_op:   word   

iblock      :    istat SEMIC iblock
            |    empty
istat       :    statement_b
            |    iword
iword       :    ID ASSIGN expression
            |    INT ID

eblock      :    estat SEMIC eblock
            |    empty
estat       :    statement_b
            |    eword
eword       :    ID ASSIGN expression
            |    INT ID
iexpression :    expression 

word        :    ID ASSIGN expression
            |    INT ID
expression  :    expression PLUS term
            |    expression MINUS term
            |    expression AND term
            |    expression XOR term
            |    INV term
            |    term
term        :    term TIMES factor
            |   term DIVIDE factor
            |   factor
factor      :   NUMBER
            |   LPAREN expression RPAREN 
            |   ID

- 1.

Can not declare variables with same name in the hole code.
for a error example:
    if a-3
    then
        int b;
        b = 1;
    else
        int b;  <---------- gramma DO NOT support this kind of behavior.
        b = 2;
'''
