#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Programa que retiene las etiquetas que esten escritas en ingles y español, ademas de los nombres de capitales y paises. Toma como entrada el archivo de etiquetas. Devuelve dos archivos. Uno con las etiquetas limpias y otro con las etiquetas eliminadas.

archivoEntrada = open('etiquetas.txt','r')
archivoSalida = open ('etiquetas2.txt','w')
archivoFalta = open ('ErrorIdiomas.txt','w')
archivoEsp = open('esp.txt','r')
archivoIng = open('en.txt','r')
archivoCiu = open('ciudades.txt','r')

dic = []
l=0
for a in archivoEsp: #Agrega al diccionario Palabras en Español
  l=l+1
  print str(l)
  dic.append(a[:-1])

l=0
for a in archivoIng: #Agrega al diccionario Palabras en Ingles
  l=l+1
  print str(l) 
  dic.append(a[:-1])

l=0
for a in archivoCiu: #Agrega al diccionario los nombres de Capitales con sus Paises
  l=l+1
  print str(l)
  dic.append(a[:-1])

l=0
for a in archivoEntrada:
  l=l+1
  print str(l)
  imagen = a.split(';')[0]
  etiqueta = a.split(';')[1][:-1]
  if etiqueta in dic: #Si la etiqueta es un nombre en español, ingles o nombre de ciudad lo almacena en archivo de etiquetas limpias si no lo almacena en archivo de errores.
     archivoSalida.write(imagen+';'+etiqueta+'\n')
  else:
     archivoFalta.write(imagen+';'+etiqueta+'\n')

archivoEntrada.close()
archivoSalida.close()
archivoFalta.close()
archivoEsp.close()
archivoIng.close()
archivoCiu.close()
