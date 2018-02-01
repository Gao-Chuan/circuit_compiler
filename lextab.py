# lextab.py. This file automatically created by PLY (version 3.10). Don't edit!
_tabversion   = '3.10'
_lextokens    = set(('LPAREN', 'PLUS', 'NUMBER', 'DIVIDE', 'MINUS', 'RPAREN', 'TIMES'))
_lexreflags   = 64
_lexliterals  = ''
_lexstateinfo = {'INITIAL': 'inclusive'}
_lexstatere   = {'INITIAL': [('(?P<t_NUMBER>\\d+)|(?P<t_newline>\\n+)|(?P<t_PLUS>\\+)|(?P<t_TIMES>\\*)|(?P<t_LPAREN>\\()|(?P<t_RPAREN>\\))|(?P<t_MINUS>-)|(?P<t_DIVIDE>/)', [None, ('t_NUMBER', 'NUMBER'), ('t_newline', 'newline'), (None, 'PLUS'), (None, 'TIMES'), (None, 'LPAREN'), (None, 'RPAREN'), (None, 'MINUS'), (None, 'DIVIDE')])]}
_lexstateignore = {'INITIAL': ' \t'}
_lexstateerrorf = {'INITIAL': 't_error'}
_lexstateeoff = {}
