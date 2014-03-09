#!/usr/local/bin/python
# coding: utf-8
import itertools
import re
from collections import namedtuple

#TODO Cambiar esta regex para colocar tambier palabras, sin embargo hay que ver si sera necesario
REGEX_BRACKETS = r"\[(\d+|[A-Za-z_]+)?\]"
REGEX_BRACKETS_ID = r'\[(?P<ids>(\d+|[A-Za-z_]+))\]'
REGEX_CAPTURE = r'(\[(?P<num>\d+)\])'

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

def strip_del_brackets(string):
    return delete_brackets(string).strip()

def numeros_bracket(string):
    return [match.group("num") for match in re.finditer(REGEX_CAPTURE,string)]

def ids_bracket(string):
    return [match.group("ids") for match in re.finditer(REGEX_BRACKETS_ID,string)]

def tiene_brackets(string):
    return bool(re.compile(REGEX_BRACKETS_ID).match(string))
