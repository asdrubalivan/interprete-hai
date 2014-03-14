#!/usr/local/bin/python
# coding: utf-8
from abc import ABCMeta, abstractmethod, abstractproperty
from maquina import Maquina, Simbolo
from utils import delete_brackets, val_input
import re
from itertools import repeat
import cparse

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
                if hasattr(val,'__iter__'):
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
        self.izquierda.evaluar(maquina)
        r_izq = maquina.pop_resultado()
        self.derecha.evaluar(maquina)
        r_der = maquina.pop_resultado()
        temp = None
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
        maquina.push_resultado(temp)
class LlamadaFuncNodo(Nodo):
    def colocar_tipo(self):
        self.tipo = LLAMADAFUNC
    def evaluar(self,maquina):
        raise NotImplementedError()

class AsigNodo(Nodo):
    def colocar_tipo(self):
        self.tipo = ASIG
    @property
    def idvariable(self):
        return self.hijos[0]
    @property
    def operador(self):
        return self.hoja
    def evaluar(self,maquina):
        maquina.asignar(self.idvariable,maquina.pop_resultado(),self.operador)

class RetornoNodo(Nodo):
    def colocar_tipo(self):
        self.tipo = RETORNO
    def evaluar(self,maquina):
        raise NotImplementedError()

class EscribirNodo(Nodo):
    def colocar_tipo(self):
        self.tipo = ESCRIBIR
    def evaluar(self,maquina):
        #Chequear si es un literal
        if isinstance(self.hijos[0],Nodo):
            self.hijos[0].evaluar(maquina)
            print(maquina.pop_resultado())
        else:
            print(self.hijos[0])

class LeerNodo(Nodo):
    def colocar_tipo(self):
        self.tipo = LEER
    @property
    def variable(self):
        return self.hijos[0]
    def evaluar(self,maquina):
        maquina.asignar(self.variable,val_input())

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
        self.expresion.evaluar(maquina)
        result_expr = bool(maquina.pop_resultado())
        if result_expr:
            for val in self.si_afirmativo:
                val.evaluar(maquina)
        else:
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
            self.expresion.evaluar(maquina)
            result_expr = bool(maquina.pop_resultado())
            if result_expr:
                for val in self.sentencias:
                    val.evaluar(maquina)
            else:
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
            for val in self.sentencias:
                val.evaluar(maquina)
            self.expresion.evaluar(maquina)
            result_expr = bool(maquina.pop_resultado())
            if not result_expr:
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
        self.asignacion.evaluar(maquina)
        while True:
            self.expr_comp.evaluar(maquina)
            # Comparamos que la expresion no sea cierta
            if not bool(maquina.pop_resultado()):
                break
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
        print(temp)
        return Nodo.__str__(self) + temp
    def colocar_tipo(self):
        self.tipo = DECLARACION
    def colocar_tipovar(self):
        if not self.hijos:
            raise NodoError
        if len(self.hijos) > 1:
            temp = ''
            for x in self.hijos[1:]:
                if x is not None:
                    temp += ''.join([y for y in x])
        else:
            temp = None
        self.tipovar = self.hijos[0] # Entero, real, flotante
        if temp:
            self.tipovar += re.sub("[A-Za-z_\d]+","",temp)
    def evaluar(self,maquina):
        maquina.anadir_var(Simbolo(self.hoja,delete_brackets(self.tipovar),self.tam_nodo))
class ProgramaBaseNodo(Nodo):
    def id(self):
        return self.hoja

class ProgramaNodo(ProgramaBaseNodo):
    def colocar_tipo(self):
        self.tipo = PROGRAMA

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
        maquina.push_resultado(self.literal)

class AlgoritmoBaseNodo(Nodo):
    __metaclass__= ABCMeta
    def evaluar(self,maquina):
        pass
    @abstractproperty
    def sentencias(self):
        pass
    def _evaluar(self,maquina):
        for val in self.sentencias:
            val.evaluar(maquina)

class AlgoritmoNodo(AlgoritmoBaseNodo):
    @property
    def sentencias(self):
        return self.hijos[0]
    def evaluar(self,maquina):
        self._evaluar(maquina)
class AlgoritmoSubNodo(AlgoritmoBaseNodo):
    @property
    def sentencias(self):
        return self.hijos[0]
    def colocar_tipo(self):
        self.tipo = ALGORITMOSUB
    def evaluar(self,maquina):
        try:
            self._evaluar(maquina)
        except RetornoSenal:
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
    nodos = cparse.parse_text('\n'.join([t for t in sys.stdin]))
    pprint(nodos)
