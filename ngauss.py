# -*- coding: utf-8 -*-

#!/usr/bin/env python3.7
# usage: python3 <script.py> --name "aint this some shit"

import argparse
import random
import re

parser = argparse.ArgumentParser()
parser.add_argument('--name', action='store')
args = parser.parse_args()

CHARDICT = {
    'a': ['a', 'A', 'α', 'Λ', '4', '/-\\', '/_\\', '@', '/\\', 'Д'],
    'b': ['b', 'B', 'β', 'Β', 'ε', '8', '|3', '13', '|}', '|:', '|8', '6', '|B', '|8', 'lo', '|o', 'j3', 'Ъ', 'ъ'],
    'c': ['c', 'C', 'ς', 'ϲ', 'Ϲ', '<', '{', '[', '(', '©', '¢'],
    'd': ['d', 'D', 'δ', '|)', '|}', '|]', '|>'],
    'e': ['e', 'E', '£', '₤', '€'],
    'f': ['f', 'F', '|=', 'ph', '|#', '|"'],
    'g': ['g', 'G', '[', '-', '[+', '6', 'C-',],
    'h': ['h', 'H', '|-|', '[-]', '{-}', '}-{', '}{', '|=|', '[=]', '{=}', '/-/', '(-)', ')-(', ':-:', 'I+I'],
    'i': ['i', 'I', '1', '|', '!', 'l'],
    'j': ['j', 'j', '_|', '_/', '_7', '_)', '_]', '_}'],
    'k': ['k', 'K', 'К', 'к', 'Κ', 'κ'],
    'l': ['l', 'L', 'Ι', 'ι', 'І', 'і', 'Г', 'г', 'i', 'I'],
    'm': ['m', 'M', '44', '|\/|', '^^', '/\/\\', '/X\\', '[]\/][', '[]V[]', '][\\//][', '(V)', '//.,.\\', 'N\\'],
    'n': ['n', 'N'],
    'o': ['o', 'O', '0', '()', '[]', '{}', '<>', 'Ø', 'oh', 'Θ', 'θ', 'δ', 'Ο', 'ο', 'Φ', 'φ'],
    'p': ['p', 'P', 'Ρ', 'ρ', 'Р', 'р'],
    'q': ['q', 'Q'],
    'r': ['r', 'R'],
    's': ['s', 'S'],
    't': ['t', 'T'],
    'u': ['u', 'U'],
    'v': ['v', 'V'],
    'w': ['w', 'W'],
    'x': ['x', 'X', 'χ', 'Χ', 'Ж', 'ж'],
    'y': ['y', 'Y'],
    'z': ['z', 'Z'],
    '.': [' ']
}

if not args.name:
    print('Please supply a name to ngauss with --name <string>')
else:
    name = args.name.lower()
    name = re.sub(r"[0-9]", "", name)
    name = re.sub(r"[~`!@#$%^&*()_+-={}\[\]\|\'\;\/\,\<\>\?\:\"]", "", name)
    name = name.replace(" ", ".")
    name_out = list()
    for ch in name:
        name_out.append(CHARDICT[ch][random.randint(0, len(CHARDICT[ch]) - 1)])
    print(''.join(name_out))
