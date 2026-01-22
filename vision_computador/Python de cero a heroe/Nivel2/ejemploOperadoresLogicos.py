# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 14:48:18 2022

@author: Jesus
"""

# USUARIO_REGISTRADO = "Abraham"
# CONTRASENA_REGISTRADA = "123456789A"

# usuario = input("Ingresa el nombre de usuario: ")
# contrasena = input("Ingresa la contraseña: ")

# evaluacion = (usuario == USUARIO_REGISTRADO) and (contrasena == CONTRASENA_REGISTRADA)
# print("La contraseña y el usuario son correctos?", evaluacion)

minimo = int(input("Ingresa el valor minimo: "))
maximo = int(input("Ingresa el valor maximo: "))
valor = int(input("Ingresa el valor medido: "))

respuesta = (valor >= minimo) and (valor <= maximo)

print("El valor medido se encuentra dentro del rango especificado?", respuesta)