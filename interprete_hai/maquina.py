from utils import (delete_brackets, count_brackets,
        strip_del_brackets, ids_bracket,
        tiene_brackets, tipo, esta_en_limites,
        is_sequence, is_literal)
import re
from copy import deepcopy as copy
import logging
import logconfig
logger = logging.getLogger(__name__)
ENTERO = "Entero"
REAL = "Real"
CARACTER = "Caracter"

class SimboloError(Exception):
    pass

class DummyError(Exception):
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
        logger.debug("Iniciando {s}".format(s=str(self)))
    def __eq__(self,otro):
        return (self.nombre == otro.nombre) and (self.tam_vec == otro.tam_vec) and \
            (self.valor == otro.valor) and (self.tipo == otro.tipo)
    def __str__(self):
        return "Simbolo '{nombre}', Tipo {tipo}, Tam {tam}, Valor {val}".format(nombre=self.nombre,tipo=self.tipo,tam=self.tam_vec,val=self.valor)
    def esta_en_limites(self,posicion):
        logger.debug("Calculando si simbolo esta en limites")
        if not is_sequence(self.tam_vec):
            logger.debug("No esta en secuencia, retornamos True")
            return True
        ret = esta_en_limites(posicion,self.tam_vec)
        if ret:
            logger.debug("Esta en limites")
        else:
            logger.debug("No esta en limites")
        return ret
    def brackets_necesarias(self):
        logger.debug("Calculando las brackets necesarias")
        if not is_sequence(self.tam_vec):
            logger.debug("No necesitamos ninguna")
            return 0
        ret = len(self.tam_vec)
        logger.debug("{} pares necesarios".format(ret))
        return ret
    def asegurar_brackets(self,nombre_var):
        ret = self.nombre == strip_del_brackets(nombre_var) and self.brackets_necesarias() == count_brackets(nombre_var)
        if ret:
            logger.debug("Brackets aseguradas")
        else:
            logger.debug("Brackets NO aseguradas")
        return ret
    def obt_valor(self,val_corchetes=None):
        if val_corchetes is None:
            if self.valor is not None:
                logger.debug("Retornando Valor {val}".format(val=self.valor))
                return self.valor
            else:
                logger.warning("Valor no definido")
                raise SimboloError("No inicializado {}".format(self.nombre))
        if not self.esta_en_limites(val_corchetes):
            raise SimboloError("Fuera de rango {}".format(val_corchetes))
        #Tiene corchetes
        try:
            logger.debug("Tratando de retornar valor con clave {}".format(val_corchetes))
            return self.valor[val_corchetes]
        except KeyError:
            logger.warning("Valor no definido")
            raise SimboloError("No inicializado {valores}".format(valores=val_corchetes))
    def asignar(self,valor,posicion=None,asignador="="):
        logger.debug("Tratando de asignar a '{nombre}' -> {v} con asignador {a}".format(v=valor,a=asignador,nombre=self.nombre))
        if is_literal(valor):
            if self.tam_vec and not posicion:
                logger.error("Tratando de asignar escalar {e} a vector de tamaño {t}".format(e=valor,t=self.tam_vec))
                raise RuntimeError("Tratando de asignar escalar a vector")
            tipo_sin_br = strip_del_brackets(self.tipo)
            #NOTE: Se coloca Try ya que quiero que en dado caso se dispare la
            #bandera de que tipos no concuerdan, para dar un mensaje al usuario
            if tipo_sin_br == ENTERO:
                try:
                    valor = int(valor)
                except:
                    pass
            elif tipo_sin_br == REAL:
                try:
                    valor = float(valor)
                except:
                    pass
            if tipo(valor) == tipo_sin_br:
                logger.debug("Tipos concuerdan")
                if posicion:
                    if self.esta_en_limites(posicion):
                        logger.debug("Esta en limites con posicion {p}".format(p=posicion))
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
                logger.warning("Error, tipo invalido {t}".format(t=tipo(valor)))
                raise SimboloError("Tipo invalido {t}".format(t=tipo(valor)))
        else:
            if not self.tam_vec:
                raise RuntimeError("Tratando de asignar vector a escalar")
            tipos = set(tipo(v) for v in valor.values())
            if len(tipos) <= 1 and all(self.esta_en_limites(p) for p in valor.keys()):
                logger.debug("Asignando vector {}".format(valor))
                self.valor = copy(valor)
            else:
                logger.error("Tipos invalidos {}".format(tipos))
                raise SimboloError("Tipo invalido, tipos {}".format(tipos))
class MaquinaError(Exception):
    pass

class Maquina(object):
    def __init__(self,tree=list()):
        self.subprogramas = {}
        self.programa = None
        self.scopes = []
        self.tree = tree
        self.ultimo_resultado = None
        self.pila_funciones = []
    def __str__(self):
        return "Maquina: Programa {programa}, Subprogramas {sub}, Scopes {scopes}, Tree {tree}, ultimo resultado {ult}".format(sub=self.subprogramas,
                scopes=self.scopes,tree=self.tree,programa = self.programa,ult=self.ultimo_resultado)
    def __repr__(self):
        return str(self)
    def push_pila_func(self,r):
        self.pila_funciones.append(r)
    def pop_pila_func(self):
        return self.pila_funciones.pop()
    def push_scope(self):
        self.scopes.append({}) #Diccionario es el scope
    def pop_scope(self):
        self.scopes.pop()
    def current_scope(self):
        return self.scopes[-1]
    def anadir_var(self,var):
        if self.esta_definida(var.nombre):
            raise MaquinaError("Variable {var} ya definida".format(var=var))
        self.current_scope()[strip_del_brackets(var.nombre)] = var
    def in_scope(self,var):
        var = delete_brackets(var).strip()
        return var in self.current_scope()
    def in_subprogramas(self,var):
        return var in self.subprogramas
    def get_subprograma(self,key):
        return self.subprogramas[key]
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
    def pop_resultado(self,excepcion=False):
        if self.ultimo_resultado is None and excepcion:
            raise DummyError("Resultado es none")
        ret_val = self.ultimo_resultado
        return ret_val
    #NOTE Metodo muy importante
    def evaluar_raices(self):
        self.meter_programas_subprogramas()
        self.programa.evaluar(self)
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
            if tiene_brackets(nombre): 
                if simb.asegurar_brackets(nombre):
                    ids = ids_bracket(nombre)
                    #Ids ya con variable definida
                    ids_def = self.get_valores_ids(ids) # NOTE: Recursividad indirecta
                    return simb.obt_valor(ids_def)
                else:
                    raise MaquinaError("Las brackets no concuerdan")
            return simb.obt_valor()
        else:
            raise MaquinaError("Nombre no definido {nombre}".format(nombre=delete_brackets(nombre)))
    def asignar(self,nodo,valor,operador="="):
        try:
            nombre = nodo.nombre
        except AttributeError:
            nombre = nodo
        if self.in_scope(nombre):
            simb = self.get_simbolo(nombre)
            if tiene_brackets(nombre): 
                if simb.asegurar_brackets(nombre):
                    ids = ids_bracket(nombre)
                    ids_def = self.get_valores_ids(ids)
                    simb.asignar(valor,ids_def,operador)
                else:
                    raise MaquinaError("Las brackets no concuerdan")
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
