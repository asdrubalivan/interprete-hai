# ----------------------------------------------------------------------
# clex.py
#
# Lexer code
# Part of the code based on 
# http://www.juanjoconti.com.ar/files/python/ply-examples/ansic/clex.py.html
# ----------------------------------------------------------------------
import ply.lex as lex
reserved = ('Programa',
        'Variables',
        'Entero',
        'Real',
        'Caracter',
        'Algoritmo',
        'Escribir',
        'Leer',
        'Finprograma',
        'Subprograma',
        'Finsubprograma',
        'Retorne',
        'Repitamientras',
        'Finrm',
        'Hagamientras',
        'Finhm',
        'Si',
        'Entonces',
        'Contrario',
        'Finsi',
        )

t_ignore = '\t\x0c'

tokens = reserved + (
            'ID',
            'TYPEID',
            'ICONST',
            'FCONST',
            'SCONST',
            'CCONST',
            )

def t_ID(t):
    r'[A-Z][A-Z0-9]*'
    if t.value in reserved:
        t.type = t.value
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    return t

def t_error(t):
    print("Caracter ilegal en {}".format(t.value[0]))
    t.lexer.skip(1)

def t_comment(t):
    r'//(.)*\n*'
    t.lexer.lineno += t.value.count("\n")

# Delimeters
t_LPAREN           = r'\('
t_RPAREN           = r'\)'
t_LBRACKET         = r'\['
t_RBRACKET         = r'\]'
t_LBRACE           = r'\{'
t_RBRACE           = r'\}'
t_COMMA            = r','
t_PERIOD           = r'\.'
t_SEMI             = r';'
t_COLON            = r':'

lexer = lex.lex(optimize=1)
if __name__=="__main__":
    lex.runmain(lexer)
