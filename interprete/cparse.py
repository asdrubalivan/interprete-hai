import sys
import clex
import ply.yacc as yacc
import re

tokens = clex.tokens




#Vacio
def p_empty(t):
    '''empty : '''
    pass

#Error
def p_error(t):
    print("Error")

yacc.yacc()
