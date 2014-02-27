import sys
import clex
import ply.yacc as yacc
import re
import operator

from nodos import BinOpNodo, LlamadaFuncNodo, AsigNodo, RetornoNodo

tokens = clex.tokens

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

def p_raiz(t):
    ''' raiz : empty
            | programa
            | programa subprogramas
    '''
    pass

def p_programa(t):
    ''' programa : PROGRAMA COLON ID progvariables algoritmo FINPROGRAMA '''
    pass


def p_progvariables(t):
    ''' progvariables : VARIABLES COLON declvariables
                      | empty
    '''
    pass

def p_subprogramas(t):
    ''' subprogramas : subprograma subprogramas
                     | empty
    '''
    pass

def p_subprograma(t):
    ''' subprograma : SUBPROGRAMA COLON tiporetorno ID LPAREN argssubp RPAREN progvariables algoritmo retorno FINSUBPROGRAMA '''
    pass

def p_tiporetorno(t):
    ''' tiporetorno : tipo optbrackets
                    | empty
    '''
    pass

def p_tipo(t):
    ''' tipo : ENTERO 
             | REAL
             | CARACTER
    '''
    pass

def p_declvariables(t):
    ''' declvariables : listadecl declvariables
                      | empty
    '''
    pass

def p_listadecl(t):
    ''' listadecl : tipo listaids SEMI '''
    pass

def p_listaids(t):
    ''' listaids : iddecl COMMA listaids
                 | iddecl
    '''
    pass

def p_iddecl(t):
    ''' iddecl : ID bracketsdecl
    '''
    pass


# IDs que se usaran dentro de los algoritmos
# Estos incluyen ejemplo[1][a] Entre otros
def p_idvariable(t):
    ''' idvariable : ID bracketsvar
    '''
    pass

def p_bracketsvar(t):
    ''' bracketsvar : LBRACKET ICONST RBRACKET bracketsvar
                    | LBRACKET ID RBRACKET bracketsvar
                    | empty
    '''
    pass

def p_bracketsdecl(t):
    ''' bracketsdecl : LBRACKET ICONST RBRACKET bracketsdecl
                     | empty
    '''
    pass

def p_algoritmo(t):
    ''' algoritmo : ALGORITMO COLON listasentencias FINALGORITMO
    '''
    pass

def p_listasentencias(t):
    ''' listasentencias : sentencia SEMI listasentencias
                        | sencomp listasentencias
                        | empty
    '''
    pass

def p_sentencia(t):
    ''' sentencia : asignacion
                  | senleer
                  | senescribir
                  | expresion
    '''
    pass

def p_senleer(t):
    ''' senleer : LEER iddecl '''
    pass

def p_senescribir(t):
    ''' senescribir : ESCRIBIR expresion '''
    pass

def p_sencomp(t):
    ''' sencomp : bloquesi
                | bloquerp
                | bloquerm
                | bloquehm
    '''
    pass

def p_bloquesi(t):
    ''' bloquesi : SI expresion ENTONCES listasentencias FINSI
                 | SI expresion ENTONCES listasentencias CONTRARIO listasentencias FINSI
    '''
    pass

def p_asignsimple(t):
    ''' asignsimple : idvariable EQUALS expresion
    '''
    pass

# Asignacion en Repita para
# NOTE Se usa simple debido a que no
# queremos += -= /= en repitapara
def p_asigrp(t):
    ''' asigrp : asignsimple
               | idvariable
    '''
    pass

def p_bloquerp(t):
    ''' bloquerp : REPITAPARA asigrp COMMA expresion COMMA expresion COLON listasentencias FINRP
    '''
    pass

def p_bloquerm(t):
    ''' bloquerm : REPITAMIENTRAS expresion COLON listasentencias FINRM
    '''
    pass

def p_bloquehm(t):
    ''' bloquehm : HAGA COLON listasentencias MIENTRAS LPAREN expresion RPAREN 
    '''
    pass

def p_expresion(t):
    ''' expresion : NOT expresion
    '''
    pass

def p_expression_paren(t):
    ''' expresion : LPAREN expresion RPAREN
    '''
    t[0] = t[2]

def p_expression_unvalor(t):
    ''' expresion : literal
                  | idvariable
                  | llamadafunc
                  | operacionbin
    '''
    t[0] = t[1]

def p_literal(t):
    ''' literal : ICONST
                | FCONST
                | SCONST
    '''
    t[0] = t[1]

def p_llamadafunc(t):
    ''' llamadafunc : ID LPAREN arglista RPAREN '''
    t[0] = LlamadaFuncNodo(t[3],t[1])

def p_arglista(t):
    ''' arglista : expresion
    '''
    t[0] = t[1]

def p_arglista_listas(t):
    ''' arglista : arglista COMMA expresion '''
    t[0].append(t[1])

def p_arglista_empty(t):
    ''' arglista : empty '''
    pass

def p_operacionbin(t):
    ''' operacionbin : expresion operador expresion '''
    t[0] = BinOpNodo([t[1],t[3]],t[2])

def p_operador(t):
    ''' operador : PLUS
                 | MINUS
                 | TIMES
                 | DIVIDE
                 | MOD
                 | OR
                 | AND
                 | LT
                 | LE
                 | GT
                 | GE
                 | EQ
                 | NE
    '''
    t[0] = t[1]

def p_asignacion(t):
    ''' asignacion : ID asignador expresion '''
    t[0] = AsigNodo([t[1],t[3]],t[2])

def p_asignador(t):
    ''' asignador : EQUALS
                  | PLUSEQUALS
                  | LESSEQUALS
    '''
    t[0] = t[1]

def p_argssubp(t):
    ''' argssubp : paramsub
                 | paramsub COMMA argssubp
                 | empty
    '''
    pass


def p_paramsub(t):
    ''' paramsub : tiporetorno ID '''
    pass

def p_optbrackets(t):
    ''' optbrackets : LBRACKET RBRACKET optbrackets
                    | empty
    '''
    pass

def p_retorno(t):
    ''' retorno : RETORNE idvariable SEMI
    '''
    t[0] = RetornoNodo([t[2]])

def p_retorno_empty(t):
    ''' retorno : empty '''
    t[0] = RetornoNodo()

#Vacio
def p_empty(t):
    '''empty : '''
    pass

#Error
def p_error(t):
    print("Error")

yacc.yacc(debug=True,check_recursion=1,optimize=1)
if __name__=='__main__':
    import sys
    txt = '\n'.join([t for t in sys.stdin])
    yacc.parse(txt,debug=True)
