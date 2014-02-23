from abc import ABCMeta, abstractmethod
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

    def __str__(self):
        return "{clase} -> Hijos: {hijos}. Hoja: {hoja}".format(
                clase=self.__class__.__name__,
                hijos=self.hijos,hoja=self.hoja)

class BinOpNodo(Nodo):
    def colocar_tipo(self):
        self.tipo = "binop"

if __name__=="__main__":
    print(BinOpNodo([],"+"))
