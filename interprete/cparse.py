import sys
import clex
import ply.yacc as yacc
import re
import operator
import logging
import logconfig
logger = logging.getLogger(__name__)


from utils import get_decl_total, delete_brackets, numeros_bracket, is_sequence

from nodos import (BinOpNodo, LlamadaFuncNodo, AsigNodo, RetornoNodo,
        VoidNodo, DeclaracionNodo, LeerNodo, EscribirNodo,
        BloqueSiNodo, BloqueRmNodo, BloqueHmNodo, BloqueRpNodo,
        NegacionNodo, SubprogramaNodo, ProgramaNodo, AlgoritmoNodo,
        AlgoritmoSubNodo, LiteralNodo, DummyNodo, VariableNodo)

DEBUG_PARSER = True

tokens = clex.tokens

precedence = (
    ('left', 'OR', 'AND', 'NOT','LT','GT','LE','GE','EQ','NE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE','MOD'),
    #('left', 'OR', 'AND', 'NOT','LT','GT','LE','GE','EQ','NE'),
)


def p_raiz(t):
    ''' raiz : programa
    '''
    t[0] = [t[1]]
    logger.debug("Parseando Raiz {}".format(t[0]))

def p_raiz_subprogramas(t):
    ''' raiz : programa subprogramas '''
    t[0] = [t[1]] + t[2]
    logger.debug("Parseando programas con subprogramas".format(t[0]))

def p_raiz_empty(t):
    ''' raiz : empty '''
    t[0] = []
    logger.debug("Raiz vacia")

def p_programa(t):
    ''' programa : PROGRAMA COLON ID progvariables algoritmo FINPROGRAMA '''
    t[0] = ProgramaNodo([t[4],t[5]],t[3])
    logger.debug("Colocando programa nodo con ID {i}, variables {v}, y algoritmo {a}".format(i=t[4],v=t[5],a=t[3]))


def p_progvariables(t):
    ''' progvariables : VARIABLES COLON declvariables
    '''
    t[0] = t[3]
    logger.debug("Colocando progvariables {}".format(t[0]))

def p_progvariables_empty(t):
    ''' progvariables : empty '''
    logger.debug("Progvariables vacia")

def p_subprogramas(t):
    ''' subprogramas : subprograma subprogramas
    '''
    t[0] = [t[1]] + t[2]
    logger.debug("Colocando subprograma {s} en subprogramas (Len:{l})".format(s=t[2],l=len(t[0])))

def p_subprogramas_empty(t):
    ''' subprogramas : empty '''
    t[0] = []
    logger.debug("Subprogramas vacio")

def p_subprograma(t):
    ''' subprograma : SUBPROGRAMA COLON tiporetorno ID LPAREN argssubp RPAREN progvariables algoritmosub FINSUBPROGRAMA '''
    t[0] = SubprogramaNodo([t[3],t[6],t[8],t[9]],t[4])
    logger.debug("Subprograma nodo: {}".format(t[0]))

def p_tiporetorno(t):
    ''' tiporetorno : tipo optbrackets
    '''
    t[0] = DeclaracionNodo([t[1],t[2]])
    logger.debug("DeclaracionNodo (tiporetorno) {}".format(t[0]))

def p_tiporetorno_empty(t):
    ''' tiporetorno : empty '''
    t[0] = VoidNodo()
    logger.debug("Colocando VoidNodo")

def p_tipo(t):
    ''' tipo : ENTERO 
             | REAL
             | CARACTER
    '''
    t[0] = t[1]
    logger.debug("Colocando tipo {}".format(t[0]))

def p_declvariables(t):
    ''' declvariables : listadecl declvariables
    '''
    t[0] = t[1]
    logger.debug("Usando regla declvariables")
    logger.debug("t[0] es {}".format(t[0]))
    if t[2]:
        t[0].extend(t[2])
        logger.debug("Luego de extender t[0] es {}".format(t[0]))
    

def p_declvariables_empty(t):
    ''' declvariables : empty '''
    logger.debug("declvariables vacio")

#TODO Anotar en las declaraciones el limite de caracteres de cada variable
def p_listadecl(t):
    ''' listadecl : tipo listaids SEMI '''
    if t[2]:
        #FIXME Aqui hay un problema NUMERO --> N U M E R O
        #En caso de que sea lista hacer algo, y en caso de que no hacer otro
        logger.debug("listadecl : tipo listaids SEMI Tipo de t[2] es {t}".format(t=type(t[2])))
        if is_sequence(t[2]):
            l = []
            for x in t[2]:
                logger.debug("x en t[2] es de tipo {t} y tiene valor {v}".format(t=type(x),v=x))
                var = DeclaracionNodo(get_decl_total(t[1],x),delete_brackets(x),en_declvariables=True,tam_nodo=numeros_bracket(x))
                l.append(var)
                logger.debug("Listadecl es : {}".format(t[0]))
            t[0] = l
        else:
            t[0] = [DeclaracionNodo(get_decl_total(t[1],t[2]),delete_brackets(t[2]),en_declvariables=True,tam_nodo=numeros_bracket(t[2]))]
    else:
        logger.warning("listadecl: listaids vacia")

def p_listaids(t):
    ''' listaids : iddecl COMMA listaids
    '''
    logger.debug("listaids: iddecl COMMA listaids, donde listaids ANTES de ser puesto como lista es {}".format(t[0]))
    t[0] = [t[1]]
    logger.debug("Transformamos t en lista {}".format(t[0]))
    if t[3] is not None:
        if isinstance(t[3],list):
            t[0].extend(t[3])
            logger.debug("t[3] = {t3} Es instance de list por tanto t[0] es {t0}".format(t0=t[0],t3=t[3]))
        else:
            #STRING
            t[0].append(t[3])
            logger.debug("t[3] = {t3} NO es instance de list por tanto t[0] es {t0}".format(t0=t[0],t3=t[0]))

def p_listaids_id(t):
    ''' listaids : iddecl '''
    t[0] = t[1]
    logger.debug("Listaids : iddecl {}".format(t[0]))

def p_iddecl(t):
    ''' iddecl : ID bracketsdecl
    '''
    temp = t[1]
    if t[2] is not None:
        temp += t[2]
    t[0] = temp
    logger.debug("iddecl : ID bracketsdecl t[0] = {t0}".format(t0=t[0]))



# IDs que se usaran dentro de los algoritmos
# Estos incluyen ejemplo[1][a] Entre otros
# Seran strings
def p_idvariable(t):
    ''' idvariable : ID bracketsvar
    '''
    temp = t[1]
    if t[2] is not None:
        temp += t[2]
    t[0] = VariableNodo([temp])  
    logger.debug("idvariable : ID bracketsvar t[0] = {t0}".format(t0=t[0]))

def p_bracketsvar(t):
    ''' bracketsvar : LBRACKET ICONST RBRACKET bracketsvar
                    | LBRACKET ID RBRACKET bracketsvar
                    | empty
    '''
    if len(t) == 5:
        t[0] = t[1] + str(t[2]) + t[3]
        if t[4] is not None:
            t[0] += t[4]
        logger.debug("bracketsvar = {t0}".format(t0=t[0]))
    else:
        logger.debug("bracketsvar vacio")


def p_bracketsdecl(t):
    ''' bracketsdecl : LBRACKET ICONST RBRACKET bracketsdecl
                     | empty
    '''
    if len(t) == 5:
        t[0] = t[1] + str(t[2]) + t[3]
        if t[4] is not None:
            t[0] += t[4]
        logger.debug("bracketsdecl = {t0}".format(t0=t[0]))
def p_algoritmo(t):
    ''' algoritmo : ALGORITMO COLON listasentencias FINALGORITMO
    '''
    t[0] = AlgoritmoNodo([t[3]])
    logger.debug("Colocando algoritmo nodo {t0}".format(t0=t[0]))

#Algoritmo en Subprograma

def p_algoritmosub(t):
    ''' algoritmosub : ALGORITMO COLON listasentencias FINALGORITMO '''
    t[0] = AlgoritmoSubNodo([t[3],t[4]])
    logger.debug("Algoritmo en subprograma {t0}".format(t0=t[0]))

def p_listasentencias(t):
    ''' listasentencias : sentencia SEMI listasentencias
    '''
    t[0] = [t[1]]
    if t[3] is not None:
        t[0] += t[3]
    logger.debug("Lista de sentencias {t0}".format(t0=t[0]))

def p_listasentencias_sencomp(t):
    ''' listasentencias : sencomp listasentencias '''
    t[0] = [t[1]]
    if t[2] is not None:
        t[0] += t[2]
    logger.debug("Lista de sentencias {t0}".format(t0=t[0]))

def p_listasentencias_empty(t):
    ''' listasentencias : empty '''
    logger.debug("Lista de sentencias empty {t0}".format(t0=t[0]))

def p_sentencia(t):
    ''' sentencia : asignacion
                  | senleer
                  | senescribir
    '''
    t[0] = t[1]
    logger.debug("Sentencia (asignacion, senleer, senescribir): {t0}".format(t0=t[0]))

def p_sentencia_expr(t):
    ''' sentencia : expresion '''
    t[0] = DummyNodo()
    logger.debug("Sentencia dummy")

def p_senleer(t):
    ''' senleer : LEER idvariable '''
    t[0] = LeerNodo([t[2]],t[1])
    logger.debug("Sentencia leer, con variable {t0}".format(t0=t[0]))

def p_senescribir(t):
    ''' senescribir : ESCRIBIR expresion '''
    t[0] = EscribirNodo([t[2]],t[1])
    logger.debug("Sentencia escribir, con variable {t0}".format(t0=t[0]))

def p_sencomp(t):
    ''' sencomp : bloquesi
                | bloquerp
                | bloquerm
                | bloquehm
    '''
    t[0] = t[1]
    logger.debug("Sentencia compleja, con variable {t0}".format(t0=t[0]))

def p_bloquesi(t):
    ''' bloquesi : SI expresion ENTONCES listasentencias FINSI
    '''
    t[0] = BloqueSiNodo([t[2],t[4],[]])
    logger.debug("Bloque Si, con variable {t0}".format(t0=t[0]))

def p_bloquesi_contrario(t):
    ''' bloquesi : SI expresion ENTONCES listasentencias CONTRARIO listasentencias FINSI
    '''
    t[0] = BloqueSiNodo([t[2],t[4],t[6]])
    logger.debug("Sentencia leer, con variable {t0}".format(t0=t[0]))

def p_asignsimple(t):
    ''' asignsimple : idvariable EQUALS expresion
    '''
    t[0] = AsigNodo([t[1],t[3]],t[2])
    logger.debug("Asignacion simple, con variable {t0}".format(t0=t[0]))

# Asignacion en Repita para
# NOTE Se usa simple debido a que no
# queremos += -= /= en repitapara
def p_asigrp(t):
    ''' asigrp : asignsimple
               | idvariable
    '''
    t[0] = t[1]
    logger.debug("Asignacion, con variable {t0}".format(t0=t[0]))

def p_bloquerp(t):
    ''' bloquerp : REPITAPARA asigrp COMMA expresion COMMA asignacion COLON listasentencias FINRP
    '''
    t[0] = BloqueRpNodo([t[2],t[4],t[6],t[8]])
    logger.debug("Bloque Repita para, con variable {t0}".format(t0=t[0]))

def p_bloquerm(t):
    ''' bloquerm : REPITAMIENTRAS expresion COLON listasentencias FINRM
    '''
    t[0] = BloqueRmNodo([t[2],t[4]])
    logger.debug("Bloque repita mientras, con variable {t0}".format(t0=t[0]))

def p_bloquehm(t):
    ''' bloquehm : HAGA COLON listasentencias MIENTRAS LPAREN expresion RPAREN 
    '''
    t[0] = BloqueHmNodo([t[6],t[3]])
    logger.debug("Bloque haga mientras, con variable {t0}".format(t0=t[0]))

def p_expresion(t):
    ''' expresion : NOT expresion
    '''
    t[0] = NegacionNodo([t[2]])
    logger.debug("Expresion negacion, con variable {t0}".format(t0=t[0]))

def p_expression_paren(t):
    ''' expresion : LPAREN expresion RPAREN
    '''
    t[0] = t[2]
    logger.debug("Expresion parentesis con variable {t0}".format(t0=t[0]))

def p_expression_unvalor(t):
    ''' expresion : literal
                  | idvariable
                  | llamadafunc
                  | operacionbin
    '''
    t[0] = t[1]
    logger.debug("Expresion con variable {t0}".format(t0=t[0]))

def p_literal(t):
    ''' literal : ICONST
                | FCONST
                | SCONST
    '''
    t[0] = LiteralNodo(hoja=t[1])
    logger.debug("Literal con variable {t0}".format(t0=t[0]))

def p_llamadafunc(t):
    ''' llamadafunc : ID LPAREN arglista RPAREN '''
    t[0] = LlamadaFuncNodo(t[3],t[1])
    logger.debug("Llama de funcion con variable {t0}".format(t0=t[0]))

def p_arglista(t):
    ''' arglista : expresion
    '''
    t[0] = [t[1]]
    logger.debug("Lista de argumenos variable {t0}".format(t0=t[0]))

def p_arglista_listas(t):
    ''' arglista : arglista COMMA expresion '''
    t[0] = [t[1]]
    if t[3] is not None:
        t[0] += t[3]
        logger.debug("Colocando nueva expresion en arglista {t3}".format(t3=t[3]))
    logger.debug("Lista de argumentos con variable {t0}".format(t0=t[0]))

def p_arglista_empty(t):
    ''' arglista : empty '''
    logger.debug("arglista : empty")


#NOTE Toca ponerlo asi para que las precedencias se cumplan
def p_operacionbin(t):
    ''' operacionbin : expresion PLUS expresion
                     | expresion MINUS expresion
                     | expresion TIMES expresion
                     | expresion DIVIDE expresion
                     | expresion OR expresion
                     | expresion AND expresion
                     | expresion LT expresion
                     | expresion GT expresion
                     | expresion GE expresion
                     | expresion EQ expresion
                     | expresion NE expresion
                     | expresion MOD expresion
    '''
    t[0] = BinOpNodo([t[1],t[3]],t[2])
    logger.debug("Operacion binaria {izq} {op} {der}".format(izq=t[1],der=t[3],op=t[2]))

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
    ''' asignacion : idvariable asignador expresion '''
    t[0] = AsigNodo([t[1],t[3]],t[2])
    logger.debug("Asignacion con variable {t0}".format(t0=t[0]))

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
    logger.debug("Argssub : paramsub con variable {t0}".format(t0=t[0]))

def p_argssubp_comma(t):
    ''' argssubp : paramsub COMMA argssubp
    '''
    t[0] = [t[1]]
    if t[3] is not None:
        t[0] += t[3]
        logger.debug("Colocando argsub {}".format(t[3]))
    logger.debug("Expresion argsub : paramsub COMMA argssubp con variable {t0}".format(t0=t[0]))

def p_argssubp_empty(t):
    ''' argssubp : empty '''
    logger.debug("Argssubp vacio")

def p_paramsub(t):
    ''' paramsub : tiporetorno ID '''
    t[1].hoja = t[2] #Anadimos la ID
    t[0] = [t[1]]
    logger.debug("paramsub : tiporetorno con variable {t0}".format(t0=t[0]))

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
    logger.debug("Retorno nodo con variable {t0}".format(t0=t[0]))

#TODO Quitar esto
def p_retorno_empty(t):
    ''' retorno : empty '''
    t[0] = RetornoNodo()
    logger.debug("Retorno nodo vacio con variable")

#Vacio
def p_empty(t):
    '''empty : '''
    pass

#Error
def p_error(t):
    print("Error")

yacc.yacc(check_recursion=1,optimize=1,debug=DEBUG_PARSER)


def parse_text(txt):
    return yacc.parse(txt,debug=DEBUG_PARSER)

if __name__=='__main__':
    import sys
    from pprint import pprint
    txt = '\n'.join([t for t in sys.stdin])
    x=yacc.parse(txt,debug=DEBUG_PARSER)
