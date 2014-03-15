from utils import (delete_brackets, count_brackets,
        strip_del_brackets, ids_bracket,
        tiene_brackets, tipo, esta_en_limites,
        is_sequence)
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
        if not self.tam_vec:
            self.valor = None #TODO Inicializar vectores en caso de no existir
        else:
            self.valor = {}
        self.tipo = tipo
    def __eq__(self,otro):
        return (self.nombre == otro.nombre) and (self.tam_vec == otro.tam_vec) and \
            (self.valor == otro.valor) and (self.tipo == otro.tipo)
    def esta_en_limites(self,posicion):
        if not is_sequence(self.tam_vec):
            return True
        return esta_en_limites(posicion,self.tam_vec)
    def brackets_necesarias(self):
        if not is_sequence(self.tam_vec):
            return 0
        return len(self.tam_vec)
    def asegurar_brackets(self,nombre_var):
        return self.nombre == strip_del_brackets(nombre_var) and self.brackets_necesarias() == count_brackets(nombre_var)
    def obt_valor(self,val_corchetes=None):
        if val_corchetes is None:
            if self.valor is not None:
                return self.valor
            else:
                raise SimboloError("No inicializado {}".format(self.nombre))
        if not self.esta_en_limites(val_corchetes):
            raise SimboloError("Fuera de rango {}".format(val_corchetes))
        #Tiene corchetes
        try:
            return self.valor[val_corchetes]
        except KeyError:
            raise SimboloError("No inicializado {valores}".format(valores=val_corchetes))
    def asignar(self,valor,posicion=None,asignador="="):
        if tipo(valor) == strip_del_brackets(self.tipo):
            if posicion:
                if self.esta_en_limites(posicion):
                    if asignador == "=":
                        self.valor[posicion] = valor
                    elif asignador == "+=":
                        self.valor[posicion] += valor
                    elif asignador == "-=":
                        self.valor[posicion] -= valor
                    else:
                        raise SimboloError("Asignacion invalida '{}'".format(asignador))
                else:
                    raise SimboloError("Asignacion fuera de rango Posicion: {p}".format(p=posicion))
            else:
                if asignador == "=":
                    self.valor = valor
                elif asignador == "+=":
                    self.valor += valor
                elif asignador == "-=":
                    self.valor -= valor
                else:
                    raise SimboloError("Asignacion invalida '{}'".format(asignador))
        else:
            raise SimboloError("Tipo invalido {t}".format(t=tipo(valor)))
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
    def get_simbolo(self,nombre):
        return self.current_scope()[strip_del_brackets(nombre)]
    def get_valores_ids(self,ids):
        return tuple([self.obtener_valor_maq(x) for x in ids]) 
    def obtener_valor_maq(self,nombre):
        #Es un entero?
        if re.compile("\d+").match(nombre):
            return int(nombre)
        if self.in_scope(nombre):
            simb = self.get_simbolo(nombre)
            if tiene_brackets(nombre) and simb.asegurar_brackets(nombre):
                ids = ids_bracket(nombre)
                #Ids ya con variable definida
                ids_def = self.get_valores_ids(ids) # NOTE: Recursividad indirecta
                return simb.obt_valor(ids_def)
            return simb.obt_valor()
        else:
            raise MaquinaError("Nombre no definido {nombre}".format(nombre=delete_brackets(nombre)))
    def asignar(self,nombre,valor,operador="="):
        if self.in_scope(nombre):
            simb = self.get_simbolo(nombre)
            if tiene_brackets(nombre) and simb.asegurar_brackets(nombre):
                ids = ids_bracket(nombre)
                ids_def = self.get_valores_ids(ids)
                simb.asignar(valor,ids_def,operador)
            else:
                simb.asignar(valor,asignador=operador)
        else:
            raise MaquinaError("Nombre no definido {nombre}".format(nombre=nombre))
if __name__=='__main__':
    from pprint import pprint
    m = Maquina()
    m.push_scope()
    m.current_scope()["a"] = Simbolo("a","Entero")
    m.current_scope()["a"].valor = 1
    m.current_scope()["Probando"] = Simbolo("Probando","Entero",(2,8))
    m.current_scope()["Probando"].valor = {(1,3):3,(1,9):7}
    m.current_scope()["Probando"].asignar(2,posicion=(1,1))
    pprint(m)
    print("Valor de Probando {}".format(m.obtener_valor_maq(" Probando[a][3]")))
    print("Valor 1:1 es {}".format(m.obtener_valor_maq("Probando[a][9]")))
