import sys
import clex
import ply.yacc as yacc
import re

tokens = clex.tokens

NODE_TYPES = {
    'REAL':'real',
    'ENTERO':'entero',
}

precedence = (
    ('left', 'PLUS','MINUS'),
    ('left', 'TIMES','DIVIDE'),
    ('left', 'POWER'),
    ('right','UMINUS')
)

class Node:
	def __init__(self, name, children = None, leaf = None):
		self.name = name
		if children == None:
			children = []
		self.children = children
		self.leaf = leaf
	
	def __str__(self):
		return "<%s>" % self.name

	def __repr__(self):
		return "<%s>" % self.name

	def append(self, node):
		self.children.append(node)

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
              | ICONST PERIOD ICONST
    '''
    if len(t) == 4:
        valor = float(p[1] + "." + p[3])
        p[0] = Node(NODE_TYPES['REAL'],None,valor)
        p[0].typ = ("float",None)
    else:
        valor = int(p[1])
        p[0] = Node(NODE_TYPES['Entero'],None,valor)
        p[0].typ = ("int",None)

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
            t[0] = -t[2] #Operador Unario TODO poner nodo
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
