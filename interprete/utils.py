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

def delete_brackets(string):
    return re.sub(REGEX_BRACKETS,'',string)
