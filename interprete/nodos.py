from abc import ABCMeta, abstractmethod
BINOP = "binop"
LLAMADAFUNC = "llamadafunc"
ASIG = "asig"
RETORNO = "retorno"

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
