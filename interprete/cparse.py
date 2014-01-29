import sys
import clex
import ply.yacc as yacc

tokens = clex.tokens


# Constante
def p_constant(t):
    '''constant: ICONST
                | FCONST
                | SCONST
    '''
    pass


#Vacio
def p_empty(t):
    'empty: '
    pass

#Error
def p_error(t):
    print("Error")

yacc.yacc()
