#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Programa que traduce las etiquetas en ingles. Toma como entrada el archivo de etiquetas. Devuelve dos archivos. Uno con las etiquetas limpias y otro con las etiquetas eliminadas.
archivo = open('etiquetas.txt','r')
archivoSalida = open ('etiquetas2.txt','w')
archivoe = open('errorRepetidas.txt','a')
archivo2 = open('traduccion.txt','r')

dic = {}
for a in archivo2:
  ing = a.split(',')[0]
  esp = a.split(',')[1][:-1]
  dic[ing] = esp

imagenAnt=''
etiquetas=[]
for a in archivo:
  imagen = a.split(';')[0]
  etiqueta = a.split(';')[1][:-1]
  if imagenAnt==imagen: #Procesa todas las etiquetas para cada imagen.
       if etiqueta in dic.keys():
          etiqueta = dic[etiqueta] #Realiza la traduccion.
       if not etiqueta in etiquetas: #Si la etiqueta no se repite lo almacena en archivo de etiquetas limpias. Si  no, lo almacena en el archivo de error de etiquetas.
          etiquetas.append(etiqueta)
          archivoSalida.write(imagen+';'+etiqueta+'\n')
       else: 
          print etiqueta
          archivoe.write(imagen+';'+etiqueta+'\n')
  else: 
     etiquetas=[]
     if etiqueta in dic.keys():
         etiqueta = dic[etiqueta] #Realiza la traduccion
     etiquetas.append(etiqueta)
     archivoSalida.write(imagen+';'+etiqueta+'\n')
     imagenAnt=imagen

archivo.close()
archivoSalida.close()
archivo2.close()




   
