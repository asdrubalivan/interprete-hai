from cparse import parse_text
import maquina
import nodos
import sys
from argparse import ArgumentParser

def crear_parser():
    parser = ArgumentParser(description="Procesa archivos")
    parser.add_argument('archivo',help="Path del archivo",type=str)
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
    m = maquina.Maquina(nodos_desde_arch(args.archivo))
    m.evaluar_raices()

if __name__=='__main__':
    main()
