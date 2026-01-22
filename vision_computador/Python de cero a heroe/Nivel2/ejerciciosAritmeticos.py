# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 17:19:10 2022

@author: Jesus
"""

# a = int(input("Ingresa el valor de a"))
# b = int(input("Ingresa el valor de b"))

# print("El resultado de la suma de a y b es:", a+b)
# print("El resultado de la resta de a y b es", a-b)
# print("El resultado de la división de a y b es", a/b)
# print("El resultado de la división entera de a y b es", a//b)

# print("El resultado de la multiplicación de a y b es", a*b)
# print("El resultado de elevar a a la b potencia es ", a**b)
# print("El residuo de la división de a entre b es ", a%b)

# base = float(input("Ingresa la base del triangulo: "))
# altura = float(input("Ingresa la altura del triangulo: "))

# area = (base * altura) / 2
# print(area)

# x^3+15y^2 -(15/2)(14xy)

x = float(input("Ingresa el valor de x: "))
y = float(input("Ingresa el valor de y"))

resultado = (x**3) + (15*(y**2)) - (15/2)*(14*x*y)
print(resultado)