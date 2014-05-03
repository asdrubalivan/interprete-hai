# ----------------------------------------------------------------------
# clex.py
#
# Lexer code
# Part of the code based on 
# http://www.juanjoconti.com.ar/files/python/ply-examples/ansic/clex.py.html
# ----------------------------------------------------------------------
import ply.lex as lex

states = (
        ('slashcomment','exclusive'),
)
reserved = ('PROGRAMA',
        'VARIABLES',
        'ENTERO',
        'REAL',
        'CARACTER',
        'ALGORITMO',
        'FINALGORITMO',
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
        'HAGA',
        'MIENTRAS',
        'FINHM',
        'SI',
        'ENTONCES',
        'CONTRARIO',
        'FINSI',
        'FINLINEA',
        'FINDELINEA',
        'CLASE',
        'EXTIENDE',
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
            'SEMI',
            'COLON',
            'PERIOD',
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

def t_error(t):
    print("Caracter ilegal en {}".format(t.value[0]))
    t.lexer.skip(1)

def t_comment(t):
    r'//(.)*\n*'
    t.lexer.lineno += t.value.count("\n")

def t_slashcomment(t):
    r'/\*'
    t.lexer.begin("slashcomment")

def t_slashcomment_end(t):
    r'\*/'
    t.lexer.lineno += t.value.count("\n")
    t.lexer.begin("INITIAL")

def t_slashcomment_error(t):
    t.lexer.skip(1)


# Delimeters
t_LPAREN           = r'\('
t_RPAREN           = r'\)'
t_LBRACKET         = r'\['
t_RBRACKET         = r'\]'
t_LBRACE           = r'\{'
t_RBRACE           = r'\}'
t_COMMA            = r','
t_SEMI             = r';'
t_COLON            = r':'
t_PERIOD           = r'\.'

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


#Float

#NOTE: FCONST va antes que ICONST debido a que
#FCONST tiene mayor precedencia

def t_FCONST(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Integer

def t_ICONST(t):
    r'\d+'
    t.value = int(t.value)
    return t


STRING_ESCAPE_CARAC = {
    r'\\':"\\",
    r'\t':'\t',
    r'\n':'\n',
    r'\'':'\'',
    r'\"':'\"',
}

# String
def t_SCONST(t):
    r'(\"([^\\\n]|(\\.))*?\")'
    temp = t.value[1:-1]
    for unescaped, character in STRING_ESCAPE_CARAC.items():
        temp = temp.replace(unescaped,character)
    t.value = temp
    return t

# Equals
t_EQUALS = r'='
t_PLUSEQUALS = r'\+='
t_LESSEQUALS = r'\-='

lexer = lex.lex(optimize=1)
if __name__=="__main__":
    lex.runmain(lexer)
