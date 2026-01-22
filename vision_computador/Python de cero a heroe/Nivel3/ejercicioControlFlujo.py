# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 14:24:32 2022

@author: Jesus
"""

NUMERO_CONTROL = "55x"
BARRENOS_REQUERIDOS = 7
COLOR_REQUERIDO = (253,80,97)
PORCENTAJE = 3
rastreabilidad = {}

numeroSerie = input("Escanea el numero de serie: ")
if len(numeroSerie) == 10:
    numeroControl = numeroSerie[:3]
    if numeroControl == NUMERO_CONTROL:
        serie = numeroSerie[3:]
        print("Iniciando prueba")
        print("Contandoo barrenos")
        barrenos = int(input("Numero de barrenos en la pieza?: "))
        print("Sistema de vision analizando el color de la pieza")
        color = input("Color de la pieza: ") #255-255-255
        listaColor = color.split("-")
        listaColor[0] = int(listaColor[0])
        listaColor[1] = int(listaColor[1])
        listaColor[2] = int(listaColor[2])
        
        tc = tuple(listaColor)
        print("\nEvaluando barrenos")
        
        if barrenos == BARRENOS_REQUERIDOS:
            respuestaBarrenos = 1
        else:
            respuestaBarrenos = 0
        listaResultados = []
        listaResultados.append(respuestaBarrenos)
        
        print("Evaluando color\n")
        porcentaje = PORCENTAJE/100
        porcentaje1 = COLOR_REQUERIDO[0] * porcentaje
        porcentaje2 = COLOR_REQUERIDO[1] * porcentaje
        porcentaje3 = COLOR_REQUERIDO[2] * porcentaje
        #(R,G,B)
        minCanalR = COLOR_REQUERIDO[0] - porcentaje1
        maxCanalR = COLOR_REQUERIDO[0] + porcentaje1
        minCanalG = COLOR_REQUERIDO[1] - porcentaje2
        maxCanalG = COLOR_REQUERIDO[1] + porcentaje2
        minCanalB = COLOR_REQUERIDO[2] - porcentaje3
        maxCanalB = COLOR_REQUERIDO[2] + porcentaje3
        
        if ((tc[0] >= minCanalR and tc[0] <= maxCanalR) and
            (tc[1] >= minCanalG and tc[1] <= maxCanalG) and
            (tc[2] >= minCanalB and tc[2] <= maxCanalB)):
            
            respuestaColor = 1
        else:
            respuestaColor = 0
        
        listaResultados.append(respuestaColor)
        rastreabilidad[serie] = listaResultados
        print(rastreabilidad)
        
        if (respuestaBarrenos == 1 and respuestaColor == 1):
            print("El resultado es OK")
        else:
            print("El resultado es NO OK")
    else:
        print("El numero de control no es correcto")

else:
    print("El numero no es de 10 digitos")