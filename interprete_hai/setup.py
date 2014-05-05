from cx_Freeze import setup, Executable
from platform import system

build_exe_options = {        
        "includes":[
            'ply',
            'ply.lex',
            'ply.yacc',
            'pickle',
            'cparse',
            'clex',
            'utils',
            'maquina',
            'nodos',
            'logconfig',
            'settings',
            're',
            'glob',
            'sys',
            'pprint',
            'argparse',
            ],
        'include_files':[
            '../LICENSE'
            ],
        }


if system() == "Windows":
    build_exe_options["includes"].append("pyreadline")
    build_exe_options["include_msvcr"] = True
        
setup(  name = "Interprete Hai",
        version = "1.0",
        description = "Interprete del lenguaje de Programación Hai",
        author = "Asdrúbal Iván Suárez Rivera",
        author_email = "asdrubal.ivan.suarez.rivera@gmail.com",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py",
            shortcutName="Interprete Hai",
            shortcutDir="DesktopFolder",)])
