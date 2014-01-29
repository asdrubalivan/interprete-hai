import sys
import clex
import ply.yacc as yacc

tokens = clex.tokens


# Variable
# TODO cambiar "empty" por "expression". No lo hago por ahora 
# para evitar error
def p_variable(t):
    '''variable : ID
                | ID LBRACKET empty RBRACKET
    '''
    pass

# Identificador de parametros
def p_parameter_identifier(t):
    '''parameter_identifier : ID'''
    pass

# Constante
def p_constant(t):
    '''constant : ICONST
                | FCONST
                | SCONST
    '''
    pass


#Vacio
def p_empty(t):
    '''empty : '''
    pass

#Error
def p_error(t):
    print("Error")

yacc.yacc()
