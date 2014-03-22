from cx_Freeze import setup, Executable

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
        ]}

setup(  name = "Interprete Hai",
        version = "0.1",
        description = "Interprete Hai",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py")])
