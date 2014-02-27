from abc import ABCMeta, abstractmethod
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

class NodoError(Exception):
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


class BinOpNodo(Nodo):
    def colocar_tipo(self):
        self.tipo = BINOP

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
class DeclaracionNodo(Nodo):
    def __init__(self,hijos=None,hoja=None,en_declvariables=False):
        Nodo.__init__(self,hijos,hoja)
        self.en_declvariables = en_declvariables
        self.colocar_tipovar()

    def __str__(self):
        temp = " tipovar: {}".format(self.tipovar)
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

