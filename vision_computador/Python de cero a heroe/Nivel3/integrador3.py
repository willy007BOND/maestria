# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 15:57:18 2022

@author: Jesus
"""

CANTIDAD_BOLSAS = 50
rastreabilidad = {}

while True:
    serial = input("Escanea el codigo serial: ")
    if serial == "salir":
        break
    
    bolsas = int(input("Ingresa la cantidad de bolsas en esta tarima: "))
    if bolsas < CANTIDAD_BOLSAS:
        resultado = "NO OK"
        print("No cumple con las especificaciones")
        
    else:
        resultado = "OK"
        print("Cumple con las especificaciones")
        
    rastreabilidad2 = {"cantidad":bolsas, "resultado":resultado}
    rastreabilidad[serial] = rastreabilidad2
    print(rastreabilidad)
    
print(rastreabilidad, "\n")

cuenta = 0
longitud = len(rastreabilidad)
claves = rastreabilidad.keys()
claves = list(claves)
valores = rastreabilidad.values()
valores = list(valores)

while cuenta < longitud:
    serial = claves[cuenta]
    valor = valores[cuenta]
    print(serial, valor)
    cuenta +=1
