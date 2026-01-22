# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 22:02:09 2022

@author: Jesus
"""

coordenada1 = (1,5)
coordenada2 = (6,8)

tupla = (1,5,6,8,1,2,3,4,6,8,7,6,4,2,3,6)
print(tupla.count(4))

print(len(tupla))

print(2 in tupla)

print(tupla.index(7))

print(tupla[10])

# tupla[1] = 6
lista = list(tupla)
lista[1] = 6
tupla = tuple(lista)
print(tupla)


