# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 11:02:37 2022

@author: Jesus
"""

from deepface import DeepFace
import cv2
import pyttsx3

def reconocimiento(frame):
    try:
        recognition = DeepFace.find(frame, db_path="db", model_name="VGG-Face",
                                    silent=True)
        recognition2 = recognition["identity"][0]
        nombre = recognition2.split("\\")[1].split("/")[0]
        return nombre
    
    except ValueError:
        return "Rostro no detectado"
    except KeyError:
        return "Rostro no detectado"
    
def saludar(mensaje):
    if mensaje != "Rostro no detectado":
        engine.say("hola" + mensaje)
        engine.runAndWait()


vid = cv2.VideoCapture(0)
engine = pyttsx3.init()
engine.setProperty('rate', 125)
mensajeAnterior = ""
cv2.namedWindow("Proyecto", cv2.WINDOW_NORMAL)
while True:
    ret, frame = vid.read()
    if not ret:
        break
    
    mensaje = reconocimiento(frame)
    if mensaje != mensajeAnterior:
        saludar(mensaje)
    
    cv2.putText(frame, mensaje, (0,115), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    cv2.imshow("Proyecto", frame)
    if cv2.waitKey(1) == ord('q'):
        break
    mensajeAnterior = mensaje
    

vid.release()
cv2.destroyAllWindows()