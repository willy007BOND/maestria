# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 00:06:11 2022

@author: Jesus
"""

resultados = {}

cadenaRecibida = input("Ingrese la cadena recibida: ")
print(cadenaRecibida)

lista = cadenaRecibida.split("-")
print(lista)

nivelLiquido = int(lista[0])
resultadoEtiqueta = bool(int(lista[1]))
cantidadManchas = int(lista[2])
numeroRastreo = lista[3]

# print(nivelLiquido, resultadoEtiqueta, cantidadManchas, numeroRastreo)

resultadoNivel = (nivelLiquido >= 580) and (nivelLiquido <= 600)
resultadoManchas = (cantidadManchas >= 0) and (cantidadManchas <= 2)
resultadoGeneral = resultadoNivel and resultadoManchas and resultadoEtiqueta

resultados[numeroRastreo] = resultadoGeneral
print(resultados)
