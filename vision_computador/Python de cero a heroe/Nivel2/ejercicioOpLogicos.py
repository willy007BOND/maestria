# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 16:05:02 2022

@author: Jesus
"""

VALOR_MINIMO = 590
VALOR_MAXIMO = 600
MAXIMO_MANCHAS = 2

nLiquido = int(input("Ingresa el nivel de liquido: "))
manchas = int(input("Ingresa el numero de manchas encontradas en el plastico "))
etiqueta = int(input("La etiqueta está bien colocada? "))
etiqueta = bool(etiqueta)

evLiquido = (nLiquido >= VALOR_MINIMO) and (nLiquido <= VALOR_MAXIMO)
evManchas = manchas <= MAXIMO_MANCHAS

evTotal = (evLiquido and evManchas and etiqueta)

print("El proceso terminó OK?", evTotal)