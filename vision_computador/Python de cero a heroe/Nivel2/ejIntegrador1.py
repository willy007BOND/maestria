# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 12:45:29 2022

@author: Jesus
"""

medicionTotal = 0.0
totalMediciones = 0
TEMPERATURA_MAXIMA = 100.0

medicion = float(input("Ingresa la medición 1: "))
medicionTotal += medicion
totalMediciones += 1

medicion = float(input("Ingresa la medición 2: "))
medicionTotal += medicion
totalMediciones += 1

medicion = float(input("Ingresa la medición 3: "))
medicionTotal += medicion
totalMediciones += 1

temperaturaPromedio = medicionTotal / totalMediciones

print("La temperatura promedio del motor supera los 100 C?", 
      temperaturaPromedio > TEMPERATURA_MAXIMA)

print("La temperatura promedio del motor casi supera los 100 C",
      temperaturaPromedio == TEMPERATURA_MAXIMA)

print("La temperatura promedio del motor es menor o igual a 80 C",
      temperaturaPromedio <= 80)

print("La temperatura promedio es:", temperaturaPromedio)