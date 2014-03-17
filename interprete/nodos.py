#!/usr/local/bin/python
# coding: utf-8
from abc import ABCMeta, abstractmethod, abstractproperty
from maquina import Maquina, Simbolo
from utils import delete_brackets, val_input, is_sequence, is_num
import re
from itertools import repeat
import logging
import logconfig
logger = logging.getLogger(__name__)

BINOP = "binop"
LLAMADAFUNC = "llamadafunc"
ASIG = "asig"
RETORNO = "retorno"
DECLARACION = "declaracion"
VOID = "void"
ESCRIBIR = "escribir"
LEER = "leer"
BLOQUESI = "bloquesi"
BLOQUERM = "bloquerm"
BLOQUEHM = "bloquehm"
BLOQUERP = "bloquerp"
NEGACION = "negacion"
SUBPROGRAMA = "subprograma"
PROGRAMA = "programa"
ALGORITMO = "algoritmo"
ALGORITMOSUB = "algoritmosub"
LITERAL = "literal"



class NodoError(Exception):
    pass

class BinOpError(NodoError):
    pass

class RetornoSenal(Exception):
    pass

class Nodo(object):
    __metaclass__ = ABCMeta

    def __init__(self,hijos=None,hoja=None):
        if hijos:
            self.hijos = hijos
        else:
            self.hijos = []
        self.hoja = hoja

    def append(self,val):
        self.hijos.append(val)

    def __str__(self):
        return "{clase} -> Hijos: {hijos} Hoja: {hoja}".format(
                clase=self.__class__.__name__,
                hijos=self.hijos,hoja=self.hoja)
    def __repr__(self):
        return str(self)
    def _print_clase_hoja(self):
        return "[{clase}] => Hoja {hoja} ".format(clase=self.__class__.__name__,hoja=self.hoja)
    def dump(self,indent=0,max_level=100,sp_per_level=4):
        spaces = ' ' * (indent * sp_per_level)
        print(spaces + self._print_clase_hoja())
        spaces = ' ' * (indent * (sp_per_level + 1))
        if indent < max_level:
            for val in self.hijos:
                if is_sequence(val):
                    for v in val:
                        if not isinstance(val,str):
                            v.dump(indent+1)
                        else:
                            print(spaces + val)
                else:
                    if not isinstance(val,str):
                        val.dump(indent+1)
                    else:
                        print(spaces + val)
    
    @abstractmethod
    def evaluar(self,maquina):
        pass

class DummyNodo(Nodo):
    def evaluar(self,maquina):
        pass

class BinOpNodo(Nodo):
    def colocar_tipo(self):
        self.tipo = BINOP
    @property
    def izquierda(self):
        return self.hijos[0]
    @property
    def derecha(self):
        return self.hijos[1]
    def evaluar(self,maquina):
        if isinstance(self.izquierda,str):
            logger.debug("Buscamos valor de variable {var}".format(var=self.izquierda))
            r_izq = maquina.obtener_valor_maq(self.izquierda)
            logger.debug("Valor de r_izq es {}".format(r_izq))
            eval_izq = False
        elif is_num(self.izquierda):
            logger.debug("Valor es numero {}".format(self.izquierda))
            eval_izq = False
            r_izq = self.izquierda
        else:
            logger.debug("Valor es de tipo {t}".format(t=type(self.izquierda)))
            izq = self.izquierda
            eval_izq = True
        if eval_izq:
            logger.debug("Evaluando lado izquierdo")
            izq.evaluar(maquina)
            r_izq = maquina.pop_resultado()
            logger.debug("Resultado {r}".format(r=r_izq))
        if isinstance(self.derecha,str):
            logger.debug("Buscamos en derecha la variable {var}".format(var=self.derecha))
            r_der = maquina.obtener_valor_maq(self.izquierda)
            logger.debug("Tenemos como resultado {r}".format(r=r_der))
            eval_der = False
        elif is_num(self.derecha):
            logger.debug("Derecha es numero {d}".format(d=self.derecha))
            eval_der = False
            r_der = self.derecha
        else:
            logger.debug("Valor es de tipo {t}".format(t=type(self.derecha)))
            der = self.derecha
            eval_der = True
        if eval_der:
            logger.debug("Evaluando derecha")
            der.evaluar(maquina)
            r_der = maquina.pop_resultado()
            logger.debug("Valor de r_der es {}".format(r_der))
        temp = None
        logger.debug("Operador es {}".format(self.hoja))
        if self.hoja == '+':
            temp = r_izq + r_der
        elif self.hoja == '-':
            temp = r_izq - r_der
        elif self.hoja == '/':
            temp = r_izq / r_der
        elif self.hoja == '*':
            temp = r_izq * r_der
        elif self.hoja == '%':
            temp = r_izq % r_der
        elif self.hoja == '||':
            temp = r_izq or r_der
        elif self.hoja == '&&':
            temp = r_izq and r_der
        elif self.hoja == '<':
            temp = r_izq < r_der
        elif self.hoja == '<=':
            temp = r_izq <= r_der
        elif self.hoja == '>':
            temp = r_izq > r_der
        elif self.hoja == '>=':
            temp = r_izq >= r_der
        elif self.hoja == '==':
            temp = r_izq == r_der
        elif self.hoja == '!=':
            temp = r_izq != r_der
        else:
            raise BinOpError("Error en operador {}".format(self.hoja))
        logger.debug("Pushing resultado {}".format(temp))
        maquina.push_resultado(temp)
class LlamadaFuncNodo(Nodo):
    def colocar_tipo(self):
        self.tipo = LLAMADAFUNC
    def evaluar(self,maquina):
        logger.debug("Llamando a funcion")#TODO Poner nombre de la funcion
        raise NotImplementedError()

class AsigNodo(Nodo):
    def colocar_tipo(self):
        self.tipo = ASIG
    @property
    def idvariable(self):
        return self.hijos[0]
    @property
    def operador(self):
        if is_sequence(self.hoja):
            return self.hoja[0]
        return self.hoja
    @property
    def expr(self):
        return self.hijos[1]
    def evaluar(self,maquina):
        self.expr.evaluar(maquina)
        res = maquina.pop_resultado()
        logger.debug("Asignando a {var} {op} {result}".format(var=self.idvariable,op=self.hoja,result=res))
        maquina.asignar(self.idvariable,res,self.operador)

class RetornoNodo(Nodo):
    def colocar_tipo(self):
        self.tipo = RETORNO
    def evaluar(self,maquina):
        logger.debug("Nodo retorno")#TODO Poner tipo y nombre del retorno
        raise NotImplementedError()

class EscribirNodo(Nodo):
    def colocar_tipo(self):
        self.tipo = ESCRIBIR
    @property
    def expr(self):
        return self.hijos[0]
    def evaluar(self,maquina):
        #Chequear si es un literal
        if isinstance(self.expr,Nodo):
            logger.debug("Expr es de tipo nodo, evaluando")
            self.expr.evaluar(maquina)
            res = maquina.pop_resultado()
            logger.debug("Resultado es {r}".format(r=res))
            print(res)
        else:
            logger.debug("Expr no es de tipo nodo, es de tipo {t}".format(t=type(self.expr)))
            logger.debug("Imprimiendo {}".format(self.expr))
            print(self.expr)

class LeerNodo(Nodo):
    def colocar_tipo(self):
        self.tipo = LEER
    @property
    def variable(self):
        return self.hijos[0]
    def evaluar(self,maquina):
        logger.debug("Leyendo variable")
        l = val_input()
        logger.debug("Variable es {v}".format(v=l))
        maquina.asignar(self.variable,l)

class BloqueSiNodo(Nodo):
    def colocar_tipo(self):
        self.tipo = BLOQUESI
    @property
    def expresion(self):
        return self.hijos[0]
    @property
    def si_afirmativo(self):
        return self.hijos[1]
    @property
    def si_contrario(self):
        return self.hijos[2]
    def evaluar(self,maquina):
        logger.debug("Evaluando expresion SiNodo")
        self.expresion.evaluar(maquina)
        result_expr = bool(maquina.pop_resultado())
        logger.debug("Expresion es {}".format(result_expr))
        if result_expr:
            logger.debug("Evaluando si afirmativo")
            for val in self.si_afirmativo:
                val.evaluar(maquina)
        else:
            logger.debug("Evaluando contrario")
            for val in self.si_contrario:
                val.evaluar(maquina)
class BloqueRmNodo(Nodo):
    def colocar_tipo(self):
        self.tipo = BLOQUERM
    @property
    def expresion(self):
        return self.hijos[0]
    @property
    def sentencias(self):
        return self.hijos[1]
    def evaluar(self,maquina):
        while True:
            logger.debug("Evaluando expresion en repita mientras")
            self.expresion.evaluar(maquina)
            result_expr = bool(maquina.pop_resultado())
            logger.debug("Resultado de expresion es {r}".format(r=result_expr))
            if result_expr:
                logger.debug("Evaluando sentencias de repita mientras")
                for val in self.sentencias:
                    val.evaluar(maquina)
            else:
                logger.debug("Saliendo")
                break

class BloqueHmNodo(Nodo):
    @property
    def expresion(self):
        return self.hijos[1]
    @property
    def sentencias(self):
        return self.hijos[0]
    def evaluar(self,maquina):
        while True:
            logger.debug("Evaluando sentencias en hacer mientras")
            for val in self.sentencias:
                val.evaluar(maquina)
            self.expresion.evaluar(maquina)
            result_expr = bool(maquina.pop_resultado())
            logger.debug("Evaluando expresion, da como resultado {r}".format(result_expr))
            if not result_expr:
                logger.debug("Saliendo de hacer mientras")
                break

class BloqueRpNodo(Nodo):
    @property
    def asignacion(self):
        return self.hijos[0]
    @property 
    def expr_comp(self):
        return self.hijos[1]
    @property
    def expr_incr(self):
        return self.hijos[2]
    @property
    def sentencias(self):
        return self.hijos[3]
    def evaluar(self,maquina):
        logger.debug("Evaluando expresion asignacion repita para")
        self.asignacion.evaluar(maquina)
        while True:
            logger.debug("Evaluando expresion comparacion repita para")
            self.expr_comp.evaluar(maquina)
            exp = maquina.pop_resultado()
            logger.debug("Expresion comparacion es {}".format(exp))
            # Comparamos que la expresion no sea cierta
            if not bool(exp):
                logger.debug("Saliendo de Repita para")
                break
            logger.debug("Evaluando sentencias")
            for val in self.sentencias:
                val.evaluar(maquina)
class NegacionNodo(Nodo):
    def colocar_tipo(self):
        self.tipo = NEGACION

class VoidNodo(Nodo):
    def colocar_tipo(self):
        self.tipo = VOID

#Hoja = Nombre de variable sin corchetes
class DeclaracionNodo(Nodo):
    def __init__(self,hijos=None,hoja=None,en_declvariables=False,tam_nodo=None):
        Nodo.__init__(self,hijos,hoja)
        self.tam_nodo = tam_nodo
        self.en_declvariables = en_declvariables
        self.colocar_tipovar()

    def __str__(self):
        temp = " tipovar: {} tam_nodo {}".format(self.tipovar,self.tam_nodo)
        return Nodo.__str__(self) + temp
    def colocar_tipo(self):
        self.tipo = DECLARACION
    def colocar_tipovar(self):
        if not self.hijos:
            logger.error("No hay hijos en declaracion")
            raise NodoError
        if len(self.hijos) > 1:
            temp = ''
            for x in self.hijos[1:]:
                if x is not None:
                    temp += ''.join([y for y in x])
            logger.debug("Temp en declaracion es {}".format(temp))
        else:
            logger.debug("No hay brackets en declaracion")
            temp = None
        self.tipovar = self.hijos[0] # Entero, real, flotante
        logger.debug("Tipovar es {}".format(self.tipovar))
        if temp:
            logger.debug("Anadiendo a tipovar valor {}".format(temp))
            self.tipovar += re.sub("[A-Za-z_\d]+","",temp)
            logger.debug("Tipo var es ahora {}".format(self.tipovar))
    def evaluar(self,maquina):
        maquina.anadir_var(Simbolo(self.hoja,delete_brackets(self.tipovar),self.tam_nodo))
class ProgramaBaseNodo(Nodo):
    def id(self):
        return self.hoja

#TODO Colocar progvariables como abstracta (Sera necesario?)
class ProgramaNodo(ProgramaBaseNodo):
    @property
    def progvariables(self):
        return self.hijos[0]
    @property
    def algoritmo(self):
        return self.hijos[1]
    def colocar_tipo(self):
        self.tipo = PROGRAMA
    def evaluar(self,maquina):
        logger.debug("Colocando push_scope en Programanodo")#TODO poner el id
        maquina.push_scope()
        logger.debug("Declarando variables")
        for val in self.progvariables:
            val.evaluar(maquina)
        logger.debug("Evaluando algoritmo")
        self.algoritmo.evaluar(maquina)
        logger.debug("Saliendo de programa nodo")
        maquina.pop_scope()

class SubprogramaNodo(ProgramaBaseNodo):
    def colocar_tipo(self):
        self.tipo = SUBPROGRAMA
class LiteralNodo(Nodo):
    def colocar_tipo(self):
        self.tipo = LITERAL
    @property
    def literal(self):
        return self.hoja
    def evaluar(self,maquina):
        logger.debug("Colocando resultado de literalnodo {}".format(self.literal))
        maquina.push_resultado(self.literal)

class AlgoritmoBaseNodo(Nodo):
    __metaclass__= ABCMeta
    def evaluar(self,maquina):
        pass
    @abstractproperty
    def sentencias(self):
        pass
    def _evaluar(self,maquina):
        logger.debug("Evaluando sentencias en AlgoritmoBaseNodo")
        for val in self.sentencias:
            val.evaluar(maquina)

class AlgoritmoNodo(AlgoritmoBaseNodo):
    @property
    def sentencias(self):
        return self.hijos[0]
    def evaluar(self,maquina):
        logger.debug("Evaluando AlgorimoNodo")
        self._evaluar(maquina)
class AlgoritmoSubNodo(AlgoritmoBaseNodo):
    @property
    def sentencias(self):
        return self.hijos[0]
    def colocar_tipo(self):
        self.tipo = ALGORITMOSUB
    def evaluar(self,maquina):
        try:
            logger.debug("Evaluando AlgoritmoSubNodo")
            self._evaluar(maquina)
        except RetornoSenal:
            logger.debug("Senal de Retorno")
            pass
        

if __name__=='__main__':
    '''tree = [BinOpNodo(
        [BinOpNodo(
            [LiteralNodo(hoja=3),
            LiteralNodo(hoja=3)],'-'),
        LiteralNodo(hoja=5)],'+')]
    maquina = Maquina()
    tree[0].evaluar(maquina)
    tree[0].dump()
    print(maquina)'''
    import sys
    from pprint import pprint
    from cparse import parse_text
    nodos = parse_text('\n'.join([t for t in sys.stdin]))
    pprint(nodos)
