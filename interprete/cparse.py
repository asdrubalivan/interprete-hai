import sys
import clex
import ply.yacc as yacc
import re

tokens = clex.tokens


# Variable
# TODO cambiar "empty" por "expression". No lo hago por ahora 
# para evitar error
def p_variable(t):
    '''variable : ID
                | ID LBRACKET empty RBRACKET
    '''
    pass

def p_sign(t):
    '''sign : PLUS 
            | MINUS
    '''
    pass

def p_multiplication_operator(t):
    '''multiplication_operator : TIMES 
                              | AND 
                              | DIVIDE '''
    pass

def p_add_operator(t):
    '''add_operator : PLUS
                   | MINUS
                   | OR
    '''
    pass

def p_relational_operator(t):
    '''relational_operator : LT
                          | GT
                          | LE
                          | GE
                          | EQ
                          | NE
    '''
    pass

def p_term(t):
    '''term : factor
            | multiplication_operator factor
    '''
    pass


def p_factor(t):
    '''factor : number
              | string
              | variable
              | function_designator
              | LPAREN expression RPAREN
    '''
    pass

def p_simple_expression(t):
    '''simple_expression : sign term
                         | sign term add_operator term
    '''
    pass

def p_number(t):
    '''number : ICONST
             | FCONST
    '''
    if re.compile(clex.t_ICONST).match(t[1]):
        t[0] = int(t[1])
    elif re.compile(clex.t_FCONST).match(t[1]):
        t[0] = float(t[1])
    else:
        raise TypeError("Error parseando numero, lista {}".format(t))

# Identificador de parametros
def p_parameter_identifier(t):
    '''parameter_identifier : ID'''
    pass

# Constante
def p_constant(t):
    '''constant : sign number
                | number
                | string
    '''
    if len(t) < 3:
        t[0] = t[1]
    else:
        #Caso sign number
        if t[1] == "-":
            t[0] = -t[2]
        elif t[1] == "+":
            t[0] = t[2]
        else:
            raise TypeError("Error en signo {}".format(t[1]))

def p_string(t):
    '''string : SCONST'''
    t[0] = t[1]


#Vacio
def p_empty(t):
    '''empty : '''
    pass

#Error
def p_error(t):
    print("Error")

yacc.yacc()
