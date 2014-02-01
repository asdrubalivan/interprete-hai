# ----------------------------------------------------------------------
# clex.py
#
# Lexer code
# Part of the code based on 
# http://www.juanjoconti.com.ar/files/python/ply-examples/ansic/clex.py.html
# ----------------------------------------------------------------------
import ply.lex as lex
reserved = ('PROGRAMA',
        'VARIABLES',
        'ENTERO',
        'REAL',
        'CARACTER',
        'ALGORITMO',
        'ESCRIBIR',
        'LEER',
        'FINPROGRAMA',
        'SUBPROGRAMA',
        'FINSUBPROGRAMA',
        'RETORNE',
        'REPITAMIENTRAS',
        'FINRM',
        'REPITAPARA',
        'FINRP',
        'HAGAMIENTRAS',
        'FINHM',
        'SI',
        'ENTONCES',
        'CONTRARIO',
        'FINSI',
        )

t_ignore = ' \t\x0c'

tokens = reserved + (
            # Literales (Constante entero, floatante, string, ID, char)
            'ID',
            'TYPEID',
            'ICONST',
            'FCONST',
            'SCONST',
            'CCONST',
            # Operadores (+,-,*,/,%,||,&&,!,<,<=,>,>=,==,!=)
            'PLUS',
            'MINUS',
            'TIMES',
            'DIVIDE',
            'MOD',
            'OR',
            'AND',
            'NOT',
            'LT',
            'LE',
            'GT',
            'GE',
            'EQ',
            'NE',
            # Delimitadores
            'LPAREN',
            'RPAREN',
            'LBRACKET',
            'RBRACKET',
            'LBRACE',
            'RBRACE',
            'COMMA',
            'PERIOD',
            'SEMI',
            'COLON',
            #Increment / Decrement
            'PLUSPLUS',
            'MINUSMINUS',
            #Igual
            'EQUALS',
            'PLUSEQUALS',
            'LESSEQUALS',
            )


reserved_map = { }
for r in reserved:
    reserved_map[r.capitalize()] = r

def t_ID(t):
    r'[A-Za-z_][\w_]*'
    t.type = reserved_map.get(t.value,"ID")
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    return t

def t_error(t):
    print("Caracter ilegal en {}".format(t.value[0]))
    t.lexer.skip(1)

def t_comment(t):
    r'//(.)*\n*'
    t.lexer.lineno += t.value.count("\n")

# Delimeters
t_LPAREN           = r'\('
t_RPAREN           = r'\)'
t_LBRACKET         = r'\['
t_RBRACKET         = r'\]'
t_LBRACE           = r'\{'
t_RBRACE           = r'\}'
t_COMMA            = r','
t_PERIOD           = r'\.'
t_SEMI             = r';'
t_COLON            = r':'

# Operadores

t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_OR = r'\|\|'
t_AND = r'\&\&'
t_NOT = '!'
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='

# Increment/Decrement
t_PLUSPLUS = r'\+\+'
t_MINUSMINUS = r'\-\-'


# Integer
t_ICONST = r'\d+'

# Floating
t_FCONST = r'(\+|\-)?\d+\.\d+'

# String
t_SCONST = r'(\"([^\\\n]|(\\.))*?\")|(“([^\\\n]|(\\.))*?”)'

# Character
t_CCONST = r'\'([^\\\n]|(\\.)){0,4}?\''

# Equals
t_EQUALS = r'='
t_PLUSEQUAL = r'\+='
t_LESSEQUAL = r'\-='

lexer = lex.lex(optimize=1)
if __name__=="__main__":
    lex.runmain(lexer)
