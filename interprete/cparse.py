import sys
import clex
import ply.yacc as yacc
import re
import operator

from utils import get_decl_total, delete_brackets

from nodos import (BinOpNodo, LlamadaFuncNodo, AsigNodo, RetornoNodo,
        VoidNodo, DeclaracionNodo, LeerNodo, EscribirNodo,
        BloqueSiNodo, BloqueRmNodo, BloqueHmNodo, BloqueRpNodo,
        NegacionNodo, SubprogramaNodo, ProgramaNodo, AlgoritmoNodo,
        AlgoritmoSubNodo, LiteralNodo)

DEBUG_PARSER = True

tokens = clex.tokens

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

def p_raiz(t):
    ''' raiz : programa
    '''
    t[0] = [t[1]]

def p_raiz_subprogramas(t):
    ''' raiz : programa subprogramas '''
    t[0] = [t[1]] + t[2]

def p_raiz_empty(t):
    ''' raiz : empty '''
    t[0] = []

def p_programa(t):
    ''' programa : PROGRAMA COLON ID progvariables algoritmo FINPROGRAMA '''
    t[0] = ProgramaNodo([t[4],t[5]],t[3])


def p_progvariables(t):
    ''' progvariables : VARIABLES COLON declvariables
    '''
    t[0] = t[3]

def p_progvariables_empty(t):
    ''' progvariables : empty '''
    pass

def p_subprogramas(t):
    ''' subprogramas : subprograma subprogramas
    '''
    t[0] = [t[1]] + t[2]

def p_subprogramas_empty(t):
    ''' subprogramas : empty '''
    t[0] = []

def p_subprograma(t):
    ''' subprograma : SUBPROGRAMA COLON tiporetorno ID LPAREN argssubp RPAREN progvariables algoritmosub FINSUBPROGRAMA '''
    t[0] = SubprogramaNodo([t[3],t[6],t[8],t[9]],t[4])

def p_tiporetorno(t):
    ''' tiporetorno : tipo optbrackets
    '''
    t[0] = DeclaracionNodo([t[1],t[2]])


def p_tiporetorno_empty(t):
    ''' tiporetorno : empty '''
    t[0] = VoidNodo()

def p_tipo(t):
    ''' tipo : ENTERO 
             | REAL
             | CARACTER
    '''
    t[0] = t[1]

def p_declvariables(t):
    ''' declvariables : listadecl declvariables
    '''
    t[0] = t[1]
    if t[2]:
        t[0].extend(t[2])

def p_declvariables_empty(t):
    ''' declvariables : empty '''
    pass

#TODO Anotar en las declaraciones el limite de caracteres de cada variable
def p_listadecl(t):
    ''' listadecl : tipo listaids SEMI '''
    if t[2]:
        t[0] = [DeclaracionNodo(get_decl_total(t[1],x),delete_brackets(x),en_declvariables=True) for x in t[2]]
        print("T es : {}".format(t[0]))

def p_listaids(t):
    ''' listaids : iddecl COMMA listaids
    '''
    t[0] = [t[1]]
    if t[3] is not None:
        if isinstance(t[3],list):
            t[0].extend(t[3])
        else:
            #STRING
            t[0].append(t[3])

def p_listaids_id(t):
    ''' listaids : iddecl '''
    t[0] = t[1]

def p_iddecl(t):
    ''' iddecl : ID bracketsdecl
    '''
    temp = t[1]
    if t[2] is not None:
        temp += t[2]
    t[0] = temp



# IDs que se usaran dentro de los algoritmos
# Estos incluyen ejemplo[1][a] Entre otros
# Seran strings
def p_idvariable(t):
    ''' idvariable : ID bracketsvar
    '''
    temp = t[1]
    if t[2] is not None:
        temp += t[2]
    t[0] = temp

def p_bracketsvar(t):
    ''' bracketsvar : LBRACKET ICONST RBRACKET bracketsvar
                    | LBRACKET ID RBRACKET bracketsvar
                    | empty
    '''
    if len(t) == 5:
        t[0] = t[1] + str(t[2]) + t[3]
        if t[4] is not None:
            t[0] += t[4]


def p_bracketsdecl(t):
    ''' bracketsdecl : LBRACKET ICONST RBRACKET bracketsdecl
                     | empty
    '''
    if len(t) == 5:
        t[0] = t[1] + str(t[2]) + t[3]
        if t[4] is not None:
            t[0] += t[4]
def p_algoritmo(t):
    ''' algoritmo : ALGORITMO COLON listasentencias FINALGORITMO
    '''
    t[0] = AlgoritmoNodo([t[3]])

#Algoritmo en Subprograma

def p_algoritmosub(t):
    ''' algoritmosub : ALGORITMO COLON listasentencias retorno FINALGORITMO '''
    t[0] = AlgoritmoSubNodo([t[3],t[4]])

def p_listasentencias(t):
    ''' listasentencias : sentencia SEMI listasentencias
    '''
    t[0] = [t[1]]
    if t[3] is not None:
        t[0] += t[3]

def p_listasentencias_sencomp(t):
    ''' listasentencias : sencomp listasentencias '''
    t[0] = [t[1]]
    if t[2] is not None:
        t[0] += t[2]

def p_listasentencias_empty(t):
    ''' listasentencias : empty '''
    pass

def p_sentencia(t):
    ''' sentencia : asignacion
                  | senleer
                  | senescribir
                  | expresion
    '''
    t[0] = t[1]

def p_senleer(t):
    ''' senleer : LEER iddecl '''
    t[0] = LeerNodo([t[2]],t[1])

def p_senescribir(t):
    ''' senescribir : ESCRIBIR expresion '''
    t[0] = EscribirNodo([t[2]],t[1])

def p_sencomp(t):
    ''' sencomp : bloquesi
                | bloquerp
                | bloquerm
                | bloquehm
    '''
    t[0] = t[1]

def p_bloquesi(t):
    ''' bloquesi : SI expresion ENTONCES listasentencias FINSI
    '''
    t[0] = BloqueSiNodo([t[2],t[4],None])

def p_bloquesi_contrario(t):
    ''' bloquesi : SI expresion ENTONCES listasentencias CONTRARIO listasentencias FINSI
    '''
    t[0] = BloqueSiNodo([t[2],t[4],t[6]])

def p_asignsimple(t):
    ''' asignsimple : idvariable EQUALS expresion
    '''
    t[0] = AsigNodo([t[1],t[3]],t[2])

# Asignacion en Repita para
# NOTE Se usa simple debido a que no
# queremos += -= /= en repitapara
def p_asigrp(t):
    ''' asigrp : asignsimple
               | idvariable
    '''
    t[0] = t[1]

def p_bloquerp(t):
    ''' bloquerp : REPITAPARA asigrp COMMA expresion COMMA expresion COLON listasentencias FINRP
    '''
    t[0] = BloqueRpNodo([t[2],t[4],t[6],t[8]])

def p_bloquerm(t):
    ''' bloquerm : REPITAMIENTRAS expresion COLON listasentencias FINRM
    '''
    t[0] = BloqueRmNodo([t[2],t[4]])

def p_bloquehm(t):
    ''' bloquehm : HAGA COLON listasentencias MIENTRAS LPAREN expresion RPAREN 
    '''
    t[0] = BloqueHmNodo([t[6],t[3]])

def p_expresion(t):
    ''' expresion : NOT expresion
    '''
    t[0] = NegacionNodo([t[2]])

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
    t[0] = LiteralNodo(hoja=t[1])

def p_llamadafunc(t):
    ''' llamadafunc : ID LPAREN arglista RPAREN '''
    t[0] = LlamadaFuncNodo(t[3],t[1])

def p_arglista(t):
    ''' arglista : expresion
    '''
    t[0] = [t[1]]

def p_arglista_listas(t):
    ''' arglista : arglista COMMA expresion '''
    t[0] = [t[1]]
    if t[3] is not None:
        t[0] += t[3]

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
    t[0] = [t[1]]

def p_argssubp(t):
    ''' argssubp : paramsub
    '''
    t[0] = t[1]

def p_argssubp_comma(t):
    ''' argssubp : paramsub COMMA argssubp
    '''
    t[0] = [t[1]]
    if t[3] is not None:
        t[0] += t[3]

def p_argssubp_empty(t):
    ''' argssubp : empty '''
    pass

def p_paramsub(t):
    ''' paramsub : tiporetorno ID '''
    t[1].hoja = t[2] #Añadimos la ID
    t[0] = [t[1]]
    print(t[0])

def p_optbrackets(t):
    ''' optbrackets : LBRACKET RBRACKET optbrackets
    '''
    t[0] = [t[1],t[2]]
    if t[3] is not None:
        t[0] += t[3]

def p_optbrackets_empty(t):
    ''' optbrackets : empty
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

yacc.yacc(check_recursion=1,optimize=1,debug=DEBUG_PARSER)
if __name__=='__main__':
    import sys
    from pprint import pprint
    txt = '\n'.join([t for t in sys.stdin])
    yacc.parse(txt,debug=DEBUG_PARSER)
