from abc import ABCMeta, abstractmethod
from maquina import Maquina, Simbolo
from utils import delete_brackets
import re

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

class Nodo(object):
    __metaclass__ = ABCMeta

    def __init__(self,hijos=None,hoja=None):
        self.colocar_tipo()
        if hijos:
            self.hijos = hijos
        else:
            self.hijos = []
        self.hoja = hoja

    @abstractmethod
    def colocar_tipo(self):
        pass

    def append(self,val):
        self.hijos.append(val)

    def __str__(self):
        return "{clase} -> Hijos: {hijos} Hoja: {hoja}".format(
                clase=self.__class__.__name__,
                hijos=self.hijos,hoja=self.hoja)
    def __repr__(self):
        return str(self)
    
    def evaluar(self,ref):
        print("Evaluando {string}".format(string=str(self)))

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

class AsigNodo(Nodo):
    def colocar_tipo(self):
        self.tipo = ASIG

class RetornoNodo(Nodo):
    def colocar_tipo(self):
        self.tipo = RETORNO

class EscribirNodo(Nodo):
    def colocar_tipo(self):
        self.tipo = ESCRIBIR

class LeerNodo(Nodo):
    def colocar_tipo(self):
        self.tipo = LEER

class BloqueSiNodo(Nodo):
    def colocar_tipo(self):
        self.tipo = BLOQUESI

class BloqueRmNodo(Nodo):
    def colocar_tipo(self):
        self.tipo = BLOQUERM

class BloqueHmNodo(Nodo):
    def colocar_tipo(self):
        self.tipo = BLOQUEHM

class BloqueRpNodo(Nodo):
    def colocar_tipo(self):
        self.tipo = BLOQUERP

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
        maquina.anadir_var(Simbolo(self.hoja,delete_brackets(self.tipovar),señf.tam_nodo))
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
    pass

class AlgoritmoNodo(AlgoritmoBaseNodo):
    def colocar_tipo(self):
        self.tipo = ALGORITMO

class AlgoritmoSubNodo(AlgoritmoBaseNodo):
    def colocar_tipo(self):
        self.tipo = ALGORITMOSUB

if __name__=='__main__':
    tree = [BinOpNodo(
        [BinOpNodo(
            [LiteralNodo(hoja=3),
            LiteralNodo(hoja=3)],'-'),
        LiteralNodo(hoja=5)],'+')]
    maquina = Maquina()
    tree[0].evaluar(maquina)
    print(maquina)
