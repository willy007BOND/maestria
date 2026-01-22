# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 19:28:15 2022

@author: Jesus
"""

# lista = ["a",1,2,"/", 587, "hola mundo"]
# elemento = lista[1]
# print(elemento)
# print(lista[:])
# print(lista[:3])
# print(lista[2:])
# print(lista[-1])
# print(lista[::-1])

# lista.append(1554)
# print(lista)

# lista.append("cadena de texto")
# print(lista)

# lista.append([5,9,7,8,1,3,["a", "b"]])
# print(lista)

# lista.insert(2, 15)
# print(lista)

# lista.insert(1500, "hola")
# print(lista)

# listaA = [1,2,3,4,5,6]
# listaB = ["hola", "hello", "1234", 5,6,9,8,7]

# listaA.extend(listaB)
# print(listaA)

# listaA = [1,2,3,4,5,6, [9,8,7,6,5,4,3,2,1,0]]
# listaA[3] = "cuatro"
# print(listaA)

# listaA[5] = 500
# print(listaA)

# listaA[6][2] = "hola mundo"

# print(listaA)

# usersAndPass = [["jesus", "123456"], ["abraham", "456789"]]

# usuario = input("Ingresa el nuevo nombre de usuario: ")
# contrasena = input("Ingresa la nueva contraseña: ")

# nuevaLista = [usuario, contrasena]
# usersAndPass.append(nuevaLista)
# print(usersAndPass)
# print(usersAndPass[-1])

# indice = int(input("Ingresa el indice de la lista a modificar: "))
# usuario = input("Ingresa el nuevo nombre de usuario: ")
# contrasena = input("Ingresa la nueva contraseña: ")

# usersAndPass[indice] = [usuario, contrasena]
# print(usersAndPass)
# print(usersAndPass[indice])

# lista = [1,2,3,4,5,6,5,8,9,5, "elemento algo"]

# del lista[4]
# print(lista)

# del lista[9]
# print(lista)

# del lista[:]
# print(lista)

# lista.remove(5)
# print(lista)

# lista.append("algo")
# print(lista)
# lista.remove("algo")
# print(lista)

# eEliminado = lista.pop(10)
# print(eEliminado)
# print(lista)

# print(lista)
# lista.clear()
# print(lista)

# lista = [1,2,3,4,5,6, "hola"]
# # longitud = len(lista)
# # print(longitud)
# x = "hola  " not in lista
# print(x)

# listaInvitados = ["Jesus", "Abraham", "Mario", "Bailey"]
# nombre = input("Ingresa el nombre a verificar ")
# print("Se encuentra en la lista?", nombre in listaInvitados)

# listaInvitados = ["Jesus", "Abraham", "Mario", "Bailey"]
# nombre = input("Ingresa el nombre a verificar ")
# print("Se encuentra en la lista?", nombre not in listaInvitados)

listaInvitados = ["Jesus", "Abraham", "Mario", "Bailey"]
# indice = listaInvitados.index("Bailey2")
# print(indice)

# invitadoACambiar = input("Ingresa el nombre del invitado a cambiar: ")
# invitadoNuevo = input("Ingresa el nombre del nuevo invitado: ")
# indice = listaInvitados.index(invitadoACambiar)
# listaInvitados[indice] = invitadoNuevo
# print("La lista actualizada es la siguiente:", listaInvitados)

# print(listaInvitados.sort())
# c = listaInvitados.sort()
# print(c)

# listaInvitados.sort()
# print(listaInvitados)

# lista = [8,4,5,6,9,8,7,4,1,2,3,2,1,2,1,2,56,6]
# lista.sort()
# print(lista)
lista = [8,4,5,6,9,8,7,4,1,2,3,2,1,2,1,2,56,6]
# listaNueva = sorted(lista)
# print(listaNueva)

# conteo = lista.count(2)
# print("El numero 2 aparece " + str(conteo) + " veces en la lista")

# lista.reverse()
# print(lista)

lista2 = lista.copy()

print(lista2)