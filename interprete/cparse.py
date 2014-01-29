import sys
import clex
import ply.yacc as yacc

tokens = clex.tokens

def p_constant(t):
    '''constant: 
    '''


#Vacio
def p_empty(t):
    'empty: '
    pass

#Error
def p_error(t):
    print("Error")

