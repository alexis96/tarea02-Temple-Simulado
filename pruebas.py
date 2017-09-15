# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 00:08:30 2017

@author: alexi
"""

import random
import itertools
import math
import time

vertices = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
aristas = [('B', 'G'),
                    ('E', 'F'),
                    ('H', 'E'),
                    ('D', 'B'),
                    ('H', 'G'),
                    ('A', 'E'),
                    ('C', 'F'),
                    ('H', 'B'),
                    ('F', 'A'),
                    ('C', 'B'),
                    ('H', 'F'),
                    ('D','F')]
for v in vertices:
    lista = [arista for arista in aristas if v in arista ]
    print(lista)
    
    for a1,a2 in itertools.combinations(lista,2):
        print(a1," -> ",a2)
        x1 = a1[0] if v in a1[1] else a1[1]
        x2 = a2[0] if v in a2[1] else a2[1]
        print ("fijo->{} x1->{} x2->{}".format(v,x1,x2))
    print('\n')
    
print(math.degrees(math.acos(.868)))