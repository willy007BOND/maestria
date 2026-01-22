# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 16:31:08 2022

@author: Jesus
"""

# NOMBRE = "Abraham"
# EDAD = "27"
# ESTADO = "Tamaulipas"

# print(NOMBRE, EDAD, ESTADO)

# cResultante = NOMBRE+EDAD+ESTADO
# print(cResultante)

# cResultante = "Hola mi nombre es "+NOMBRE+", tengo "+EDAD+" años y nací en el estado de "+ESTADO
# print(cResultante)

# cResultante = NOMBRE + 27

# cResultante = NOMBRE * 50

# print(cResultante)

# print(len(cResultante))

# cadena = "el caballo corre por el campo"
# index = cadena.find("caballo")
# print(index)
# index = cadena.find("el")
# print(index)

# index = cadena.rfind("el")
# print(index)

# print(cadena[index:])

# index = cadena.find("carro")
# print(index)

# cadena = input("Ingresa una cadena sin espacios en blanco: ")
# eBlanco = cadena.rfind(" ")
# print("Se encontró un espacio en blanco?", eBlanco != -1)


# cadena = "ESTO ES UNA CADENA DE TEXTO"
# cadena = cadena.lower()
# print(cadena)

# cEelectronico = input("Ingresa tu correo electrónico: ")
# cProcesado = cEelectronico.lower()
# print(cProcesado)

# correo = "jesuS.6584ä@yupmail.com"
# print(correo.islower())

# curp = input("Ingresa tu curp ")
# print("Este es el CURP sin procesar", curp)
# curpProcesada = curp.upper()
# print("Esta es la CURP procesada", curpProcesada)

# curp = "ASA1548S13W21WE87R"
# print(curp.isupper())

# nombre = input("Ingresa tu nombre: ")
# print("Nombre sin procesar:", nombre)
# nombre = nombre.capitalize()
# print("Nombre procesado", nombre)

# nombre = input("Ingresa tu nombre completo: ")
# print("Nombre sin procesar:", nombre)
# nombre = nombre.title()
# print("Nombre procesado", nombre)

# cadena = "el caballo corre por el campo"
# cadenaNueva = cadena.replace("caballo", "perro")
# print(cadena)
# print(cadenaNueva)
# cadenaNueva2 = cadenaNueva.replace("e", "a")
# print(cadenaNueva)
# print(cadenaNueva2)

# cadena = "carro carro carro carro carro carro carro carro"
# cadenaNueva = cadena.replace("carro", "moto", 1)
# print(cadenaNueva)

# ½

# alfabetica = "abcde"
# print(alfabetica.isalpha())
# numerica = "½"
# print(numerica.isnumeric())
# numerica = "½"
# print(numerica.isdigit())

# alfanumerica = "123456"

# print("Es una cadena alfanumerica?", alfanumerica.isalnum())

# nombre = input("Ingresa tu primer nombre: ")
# year = input("ingresa tu año de nacimiento en numero: ")
# folio = input("Ingresa el folio de registro: ")
# evTotal = (nombre.isalpha() and year.isdigit() and folio.isalnum())

# print("Los datos introducidos son correctos?", evTotal)

# cadena = input("ingresa un texto")
# print(cadena)

# print(cadena.strip())

# nombre = input("Ingresa tu primer nombre: ")
# year = input("ingresa tu año de nacimiento en numero: ")
# folio = input("Ingresa el folio de registro: ")

# nombre = nombre.strip()
# year = year.strip()
# folio = folio.strip()

# evTotal = (nombre.isalpha() and year.isdigit() and folio.isalnum())

# print("Los datos introducidos son correctos?", evTotal)

# cadena = "0,1024,568,456,125"
# print(cadena)
# cadenaX = cadena.split(",")
# print(cadenaX[2])

# SEPARADOR = "-"

# dia = input("ingresa tu dia de nacimiento: ")
# mes = input("ingresa tu mes de nacimiento: ")
# year = input("Ingresa tu año de nacimiento: ")

# fecha = dia+SEPARADOR+mes+SEPARADOR+year
# print(fecha)

# fechaSeparada = fecha.split(SEPARADOR)
# print(fechaSeparada)

# cadena = "esto es una cadena de texto 123"
# cadenaRecortada = cadena[10]

# print(cadenaRecortada)

SEPARADOR = "-"

dia = input("ingresa tu dia de nacimiento: ")
mes = input("ingresa tu mes de nacimiento: ")
year = input("Ingresa tu año de nacimiento: ")

fecha = dia+SEPARADOR+mes+SEPARADOR+year
print(fecha)

fechaSeparada = fecha.split(SEPARADOR)
print(fechaSeparada)

diaX = fechaSeparada[0]
mesX = fechaSeparada[1]
yearX = fechaSeparada[2]

print(diaX)
print(mesX)
print(yearX)