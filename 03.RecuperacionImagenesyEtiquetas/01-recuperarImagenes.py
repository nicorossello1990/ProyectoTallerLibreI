#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Programa que recupera las imagenes relevantes a una o varias etiquetas de consulta textual pasada por argumentos. Devuelve un archivo de Ranking con los ID de las imagenes relevantes de la consulta dada.

import math
import sys
import unicodedata


#Funcion que carga el Indice etiqueta-etiquetaRelacionadas.
def cargarRelacionados():
   archivo = open ('postingEtiquetasRelacionadas.txt','r')
   hashRelacionados= {}
   for linea in archivo:
      etiqueta1=linea.split('>')[0]
      hashRelacionados[etiqueta1] = {}
      listaRelacionados = linea[:-1].split('>')[1].split(';')
      for datosRelacionados in listaRelacionados:
          etiqueta2 = datosRelacionados.split(',')[0]
          peso = float(datosRelacionados.split(',')[1])
          hashRelacionados[etiqueta1][etiqueta2] = peso
   archivo.close()
   return hashRelacionados

#Funcion que carga el Indice etiqueta-imagenes.
def cargarImagenes():
   archivo = open ('postingImagenes.txt','r')
   hashImagenes= {}
   for linea in archivo:     
      imagen=linea.split('>')[0]
      etiquetas = linea.split('>')[1][:-1].split(';')
      hashImagenes[imagen] = etiquetas
   archivo.close()
   return hashImagenes

#Funcion que carga el Indice imagen-etiquetas.
def cargarEtiquetas():
   archivo = open ('postingEtiquetas.txt','r')
   hashEtiquetas = {}
   for linea in archivo: 
      etiqueta = linea.split('>')[0]
      imagenes = linea.split('>')[1][:-1].split(';')
      hashEtiquetas[etiqueta] = imagenes
   return hashEtiquetas


salida = open ('rankingImagenes.txt','w') #Archivo de salida. Ranking de imagenes
hashEtiquetas = cargarEtiquetas()
hashImagenes = cargarImagenes()
hashRelacionados = cargarRelacionados()
imagenes = len(hashImagenes)

etiquetas = sys.argv #Consulta textual tomada de los argumentos del programa.
et_consulta=[]
consulta= ''
for etiqueta in etiquetas[1:]:
   if etiqueta !='': 
      etiqueta= ''.join((c for c in unicodedata.normalize('NFD', etiqueta.decode('utf-8')) if unicodedata.category(c) != 'Mn')) #Elimina las tildes de la etiqueta.
      etiqueta = etiqueta.lower() #Transforma la etiqueta a minusculas.
      et_consulta.append(etiqueta)
      consulta = consulta + ' ' + etiqueta


ranking={}
for eq in et_consulta: #Por cada etiquetas de consulta calcula el puntaje por el enfoque propuesto
   if eq in hashEtiquetas.keys():    
       for imagen in hashEtiquetas[eq]:
           puntaje = 0
           lon = 1.00/float(math.sqrt(len(hashImagenes[imagen]))) #Longitud de etiquetas
           for lista in hashImagenes[imagen]:
               etiqueta = lista.split(',')[0]
               rel = float(lista.split(',')[1]) #Relevancia de etiquetas
               dis = 1.00 + math.log10(imagenes/(1.00 + len(hashEtiquetas[etiqueta]))) #Discriminacion de etiqueta
               if etiqueta ==eq:   
                   asoc = 1 #Coincidencia de etiqueta consulta-etiqueta
               else:             
                  asoc = hashRelacionados[etiqueta][eq] #Coincidencia de etiqueta consulta-etiqueta
               puntaje = puntaje + (rel*dis*lon*asoc) #Sumatoria de las 4 formulas.
           if imagen in ranking.keys():
              ranking[imagen] = ranking[imagen] + puntaje
           else:
              ranking[imagen] = puntaje

#Ordena el Ranking de imagenes de mayor a menor por el puntaje de coincidencia. 
ranking = ranking.items()
ranking.sort(lambda x,y:cmp(y[1], x[1]))
i = 0
salida.write("Consulta: "+ consulta + " \n")
salida.write("Ranking     Imagen      Puntuacion \n")
for r in ranking[:-1]:
     i=i+1
     salida.write(str(i)+ "\t"+r[0]+"\t"+str(r[1])+"\n")
salida.write(str(i)+ "\t"+ranking[-1][0]+"\t"+str(ranking[-1][1])+"\n")
salida.close()



