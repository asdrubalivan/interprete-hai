import itertools
import re

#TODO Cambiar esta regex para colocar tambier palabras, sin embargo hay que ver si será necesario
REGEX_BRACKETS = r"\[(\d+)?\]"

def count_brackets(string):
    return len(re.findall(REGEX_BRACKETS,string))

def repeat_brackets(times):
    if times <= 0:
        return None
    i = 0
    var = []
    while i < times:
        i+= 1
        var.extend(('[',']'))
    return var

def get_brackets_decl(string):
    return repeat_brackets(count_brackets(string))

def get_decl_total(t,string):
    brackets = get_brackets_decl(string)
    if not brackets:
        return [t]
    return [t,brackets]

def delete_brackets(string):
    return re.sub(REGEX_BRACKETS,'',string)
