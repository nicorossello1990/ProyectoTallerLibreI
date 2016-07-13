#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Programa que elimina las etiquetas mas frecuentes y menos frecuentes. Toma como entrada el archivo de etiquetas y elimina las etiquetas de frecuencia 1 y las palabras vacias. Devuelve dos archivos: El archivo de etiquetas limpias y el archivo con las etiquetas eliminadas.


#Funcion que retorna una lista con las palabras vacias.
def cargarPalabrasVacias():
   archivoEntrada = open('stopwords.txt','r')
   vacias =[]
   for linea in archivoEntrada: 
        palabra = linea[:-1]
        vacias.append(palabra)
   archivoEntrada.close()
   return vacias


#Funcion que retorna un diccionario de etiquetas con sus frecuencias.
def cargarFrecuencias():
  archivoEntrada = open('etiquetas.txt','r')
  etiquetas={} 
  for linea in archivoEntrada: 
    etiqueta = linea.split(';')[1][:-1]
    if etiqueta in etiquetas.keys():
       etiquetas[etiqueta] = etiquetas[etiqueta] + 1
    else:    
       etiquetas[etiqueta] = 1
  archivoEntrada.close()
  return etiquetas

frecuencias = cargarFrecuencias()
palabrasVacias = cargarPalabrasVacias()

archivoEntrada = open('etiquetas.txt','r')
archivoSalida = open('etiquetas2.txt','w')
archivoError = open('errorFrecuencias.txt','w')
i=0
for linea in archivoEntrada:
  i=i+1
  print str(i)
  imagen = linea.split(';')[0]
  etiqueta = linea.split(';')[1][:-1]
  if frecuencias[etiqueta] > 1 and not etiqueta in palabrasVacias: #Si la frecuencia de la etiqueta es mayor a 1 y bo es una palabra vacia lo almacena en el archivo de etiquetas limpias, si no lo almacena en el archivo de errores de etiquetas.
       archivoSalida.write(str(imagen)+';'+etiqueta+'\n')
  else:
       archivoError.write(str(imagen)+';'+etiqueta+'\n')
      
archivoEntrada.close()
archivoSalida.close()
archivoError.close()
