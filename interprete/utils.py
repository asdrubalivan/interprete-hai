import itertools
import re

REGEX_BRACKETS = r"\[(\d+)?\]"

def count_brackets(string):
    return len(re.findall(REGEX_BRACKETS,string))

def repeat_brackets(times):
    var = list(itertools.repeat(["[]"],times))
    if var == []:
        return None
    return var

def get_brackets_decl(string):
    return repeat_brackets(count_brackets(string))

def get_decl_total(t,string):
    brackets = get_brackets_decl(string)
    if brackets is None:
        return [t]
    return [t,string]

def delete_brackets(string):
    return re.sub(REGEX_BRACKETS,'',string)
