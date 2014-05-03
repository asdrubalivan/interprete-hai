from cparse import parse_text
import maquina
import nodos
import sys
from argparse import ArgumentParser
from cmd import Cmd
from settings import VERSION
from os import path, chdir, listdir
from glob import glob
import re

def crear_parser():
    parser = ArgumentParser(description="Procesa archivos")
    parser.add_argument('archivo',help="Path del archivo",type=str,nargs='?')
    return parser

def leer_archivo(path):
    with open(path,'r') as arch:
        ret_val = arch.read()
    return ret_val

def nodos_desde_arch(path):
    arch = leer_archivo(path)
    return parse_text(arch)

def main():
    parser = crear_parser()
    args = parser.parse_args()
    if args.archivo:
        evaluar(args.archivo)
    else:
        ComandosInterprete().cmdloop()

def evaluar(archivo):
    m = maquina.Maquina(nodos_desde_arch(archivo))
    m.evaluar_raices()

class ComandosInterprete(Cmd):
    prompt = "HAI> "
    intro = ''' 
    *******************************************
    Compilador del Lenguaje de Programación HAI
    Versión: {version}
    
    COMANDOS:

    hai [archivo]: para leer un archivo
    salir: para salir
    *******************************************
    '''.format(version=VERSION)
    currdir = None
    def do_hai(self,archivo):
        if not archivo:
            print("No se incluyo archivo, el mismo es obligatorio")
        else:
            try:
                evaluar(archivo)
            except Exception as e:
                print("Error: {e}".format(e=e))
    def help_hai(self):
        print('\n'.join(("Lee y ejecuta un archivo","Se ejecuta de la forma","hai [archivo]")))
    def do_salir(self,linea):
        sys.exit(0)
    def do_cd(self,dir_):
        if not dir_:
            self.currdir = path.realpath("")
            return
        if path.isdir(dir_):
            temp = path.realpath(dir_)
            chdir(temp)
            self.currdir = temp
            print("Directorio actual cambiado a {dir_}".format(dir_=temp))
        else:
            print("\"{dir_}\" no es un directorio".format(dir_=dir_))
    def complete_cd(self, text, line, begidx, endidx):
        ret_val = [x for x in listdir() if path.isdir(x) and text in x]
        if not re.match('^\w+$',text) or not ret_val:
            ret_val +=[".."]
        return sorted(ret_val)
    def do_archivos(self,linea):
        if self.currdir:
            dir_ = self.currdir
        else:
            dir_ = ''
        print('\n'.join(sorted(glob("*.hai"))))
    def complete_hai(self, text, line, begidx, endidx):
        return [x for x in sorted(glob("*.hai")) if text in x]
if __name__=='__main__':
    main()
