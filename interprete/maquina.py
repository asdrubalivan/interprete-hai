from utils import delete_brackets, count_brackets, strip_del_brackets, ids_bracket, tiene_brackets
import re
ENTERO = "Entero"
REAL = "Real"
CARACTER = "Caracter"

class SimboloError(Exception):
    pass

class Simbolo(object):
    #Ejemplo Simbolo("nombre","Entero",(3,3))
    #Si vec es [][] ("nombre","Entero",(None,None))
    #Si es unidimensional tam_vec = None
    def __init__(self,nombre,tipo,tam_vec=None):
        self.nombre = strip_del_brackets(nombre)
        self.tam_vec = tam_vec
        self.valor = None #TODO Inicializar vectores en caso de no existir
        self.tipo = tipo
    def __eq__(self,otro):
        return (self.nombre == otro.nombre) and (self.tam_vec == otro.tam_vec) and \
            (self.valor == otro.valor) and (self.tipo == otro.tipo)
    def asegurar_brackets(self,nombre_var):
        return self.nombre == strip_del_brackets(nombre_var) and count_brackets(self.nombre) == count_brackets(nombre_var)
    def obt_valor(self,val_corchetes=None):
        if val_corchetes is None:
            return self.valor
        #Tiene corchetes
        try:
            return self.valor[val_corchetes]
        except KeyError:
            raise SimboloError("Fuera de rango {valores}".format(valores=val_corchetes))
class MaquinaError(Exception):
    pass

class Maquina(object):
    def __init__(self,tree=list()):
        self.subprogramas = {}
        self.programa = None
        self.scopes = []
        self.tree = tree
        self.ultimo_resultado = None
    def __str__(self):
        return "Maquina: Programa {programa}, Subprogramas {sub}, Scopes {scopes}, Tree {tree}, ultimo resultado {ult}".format(sub=self.subprogramas,
                scopes=self.scopes,tree=self.tree,programa = self.programa,ult=self.ultimo_resultado)
    def __repr__(self):
        return str(self)
    def push_scope(self):
        self.scopes.append({}) #Diccionario es el scope
    def pop_scope(self):
        self.scopes.pop()
    def current_scope(self):
        return self.scopes[-1]
    def anadir_var(self,var):
        if self.esta_definida(var):
            raise MaquinaError("Variable {var} ya definida".format(var=var))
        self.current_scope()[strip_del_brackets(var.nombre)] = var
    def in_scope(self,var):
        var = delete_brackets(var).strip()
        return var in self.current_scope()
    def in_subprogramas(self,var):
        return var in self.subprogramas
    def esta_definida(self,var):
        return self.in_scope(var) or self.in_subprogramas(var)
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
    def push_resultado(self,r):
        self.ultimo_resultado = r
    def pop_resultado(self):
        ret_val = self.ultimo_resultado
        return ret_val
    #NOTE Metodo muy importante
    def evaluar_raices(self):
        self.meter_programas_subprogramas()
        self.programa.evaluar()
    def obtener_valor_maq(self,nombre):
        #Es un entero?
        if re.compile("\d+").match(nombre):
            return nombre
        if self.in_scope(nombre):
            simb = self.current_scope()[delete_brackets(nombre).strip()]
            if tiene_brackets(nombre) and simb.asegurar_brackets(nombre):
                ids = ids_bracket(nombre)
                #Ids ya con variable definida
                ids_def = tuple([self.obtener_valor_maq(x) for x in ids])
                return simb.obt_valor(ids_def)
            return simb.obt_valor()
        else:
            raise MaquinaError("Nombre no definido {nombre}".format(nombre=delete_brackets(nombre)))

if __name__=='__main__':
    from pprint import pprint
    m = Maquina()
    m.push_scope()
    m.current_scope()["a"] = Simbolo("a","Entero")
    m.current_scope()["a"].valor = 1
    m.current_scope()["Probando"] = Simbolo("Probando","Entero",(2,))
    m.current_scope()["Probando"].valor = {(1,3):3}
    pprint(m)
    print("Valor de Probando {}".format(m.obtener_valor_maq(" Probando[a][3]")))
