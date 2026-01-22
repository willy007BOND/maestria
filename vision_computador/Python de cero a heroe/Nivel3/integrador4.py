# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 19:35:16 2022

@author: Jesus
"""

listaMaterias = ["Matematicas", "calculo", "espanol", "cNaturales", "Fisica"]

promedios = []
estudiantes = []

while True:
    nombre = input("Ingresa el nombre del estudiante: ")
    if nombre != "salir":
        suma = 0
        for materia in listaMaterias:
            calificacion = float(input("Ingresa la calificacion para " + materia+" :"))
            suma += calificacion
        promedio = suma / len(listaMaterias)
        promedios.append(promedio)
        estudiantes.append(nombre)
    
    else:
        print("\n")
        for index in range(len(estudiantes)):
            print("El estudiante", estudiantes[index], 
                  "obtuvo de calificacion", promedios[index])
        break