from utils import delete_brackets

class MaquinaError(Exception):
    pass

class Maquina(object):
    def __init__(self,tree=list()):
        self.subprogramas = {}
        self.programa = None
        self.scopes = []
        self.tree = tree
    def __str__(self):
        return "Maquina: Subprogramas {sub}, Scopes {scopes}, Tree {tree}".format(sub=self.subprogramas,
                scopes=self.scopes,tree=self.tree)
    def __repr__(self):
        return str(self)
    def push_scope(self):
        self.scopes.append({}) #Diccionario es el scope
    def pop_scope(self):
        self.scopes.pop()
    def current_scope(self):
        return self.scopes[-1]
    def in_scope(self,var):
        var = delete_brackets(var)
        return var in self.current_scope()
    def in_subprogramas(self,var):
        return var in self.subprogramas
    def meter_programas_subprogramas(self):
        if self.tree:
            self.programa = self.tree[0]
            for val in self.tree[1:]:
                string = val.id()
                if string != self.programa.id() and not self.in_subprogramas(string):
                    self.subprogramas[string] = val
                else:
                    raise MaquinaError("Error en subprograma {string}".format(string=string))
        else:
            raise MaquinaError("Self.tree vacio <-- {tree} -->".format(tree=self.tree))
    #NOTE Metodo muy importante
    def evaluar_raices(self):
        self.meter_programas_subprogramas()
        self.programa.evaluar()

if __name__=='__main__':
    from pprint import pprint
    m = Maquina()
    m.push_scope()
    m.current_scope()["Probando"] = 3
    pprint(m)
