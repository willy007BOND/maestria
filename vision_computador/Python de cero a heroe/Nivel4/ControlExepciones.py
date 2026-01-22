# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 01:38:25 2022

@author: Jesus
"""

# try:
#     #codigo a ejecutarse y que puede provocar un error
# except tipoError:
#     #bloque de codigo a ejecutar en caso de presentarse un error en try

# lista = [1,2,3,4,5,6]
# lista[20]

# lista = [1,2,3,4,5,6]
# for i in range(20):
#     try:
#         print(lista[i])
#     except IndexError:
#         print("El index está fuera del rango de la lista")
#         break

# print("funciona")

# sensor = 0
# try:
#     senal = 5/sensor
#     print(senal)
# except ZeroDivisionError:
#     print("No se puede dividir entre cero")

sensor = 0
try:
    senal = 5/sensor
    
except ZeroDivisionError:
    print("No se puede dividir entre cero")
    
else:
    print(senal)
    
finally:
    print("se acabó")
    
