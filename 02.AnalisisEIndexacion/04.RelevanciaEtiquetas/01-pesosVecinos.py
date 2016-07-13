#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Programa que calcula la relevencia de etiquetas para cada etiqueta. Almacena 3 archivos indices para soportar la recuperacion de imagenes y etiquetas relacionadas: "postingEtiquetas.txt", "postingImagnes.txt" y "postingEtiquetasRelacionadas".

import cv2
import time
import sys

K = 30
Alfa=0.50



#Funcion que devuelve las imagenes de una capital.
def devolverImagenesCapitales(imagen1,capitales):
      for c in capitales:
        if imagen1 in capitales[c]:
           return capitales[c]


#Funcion que devuelve las imagenes similares a una imagen dada.
def extraerVecinos(imagen1,capitales):
  listaImagenes=[]
  try:
     imagenes = devolverImagenesCapitales(imagen1,capitales)
     img1 = cv2.imread( 'Fotos/'+imagen1 );
     v = cv2.calcHist([img1], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256]) #Calculo de histograma de imagen
     v = v.flatten()
     hist1 = v / sum(v)
     dictSumas ={}
     for imagen2 in imagenes:
        if not imagen2==imagen1:
          try:
            img2 = cv2.imread( 'Fotos/'+imagen2);
            v = cv2.calcHist([img2], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256]) #Calculo de histograma de imagen
            v = v.flatten()
            hist2 = v / sum(v)
            d = cv2.compareHist( hist1, hist2, cv2.cv.CV_COMP_INTERSECT) #Calculo de similitud de imagenes
            dictSumas[imagen2] = d             
          except: 
             print "Error"          
     dictSumas = dictSumas.items()
     dictSumas.sort(lambda x,y:cmp(y[1], x[1]))
     i=0
     while i<K: #Devuelve las K imagenes mas similares.
        listaImagenes.append(dictSumas[i][0]) 
        i=i+1 
  except: 
        print "Error"
  return listaImagenes




#Funcion que carga las imagenes de cada capital.
def cargarCapitales():
     archivoCapitales = open('archivoCapitales.txt','r')
     capitales={}
     cant=0
     for a in archivoCapitales:
         cant=cant+1
         capitales[cant] = a[:-1].split(',')
     archivoCapitales.close()
     return capitales
     


#Funcion que calcula el peso de relevancia por el algoritmo de Voto-VecinoVisuales
def calcularPesoVecinos(etiqueta, ImagenesVecinosVisuales,hashImagenes,hashEtiquetas):
   suma = 0  
   for imagen in ImagenesVecinosVisuales:
       if imagen in hashEtiquetas.keys():
         etiquetas = hashEtiquetas[imagen]
         if etiqueta in etiquetas:
            suma = suma + 1
   probabilidadVecinos = float(suma)/float(K)
   probabilidadEtiqueta = float(len(hashImagenes[etiqueta]))/float(D)
   peso = probabilidadVecinos - probabilidadEtiqueta
   if peso <0:
      peso=0
   return peso


#Funcion que carga los datos de las etiquetas para crear las Listas de Posteo.
def cargarDatos():
   etiquetas = {} #Diccionario imagen-Etiquetas
   imagenes ={}  #Diccionario etiqueta-Imagenes
   archivo = open('etiquetas.txt','r')
   for linea in archivo:
     imagen = linea.split(';')[0]
     etiqueta = linea.split(';')[1][:-1]
     if imagen in etiquetas.keys():
        etiquetas[imagen].append(etiqueta)   
     else:
        etiquetas[imagen] = []
        etiquetas[imagen].append(etiqueta)
     if etiqueta in imagenes.keys():
        imagenes[etiqueta].append(imagen)   
     else:
        imagenes[etiqueta] = []
        imagenes[etiqueta].append(imagen)
   return etiquetas, imagenes

#Funcion que calcula la correlacion de las etiquetas de una imagen dada.
def calcularCorrelacion(etiquetai,hashRelacionados,hashEtiquetas,imagen):
    if not etiquetai in hashRelacionados.keys() and len(hashEtiquetas[imagen])>1:
       hashRelacionados[etiquetai] = {}
    for etiquetaj in hashEtiquetas[imagen]:
       if etiquetai!=etiquetaj:            
          if etiquetaj in hashRelacionados[etiquetai].keys():
                hashRelacionados[etiquetai][etiquetaj] = hashRelacionados[etiquetai][etiquetaj] + 1
          else: 
                hashRelacionados[etiquetai][etiquetaj] = 1 
    return  hashRelacionados 

hashEtiquetas,hashImagenes = cargarDatos()
capitales = cargarCapitales()
D = len(hashEtiquetas) #Total de imagenes.
archivoEtiquetas = open ('postingEtiquetas.txt','w')#Indice etiqueta-imagenes.
archivoPesosImagenes = open('postingImagenes.txt','w')#Indice imagen-etiquetas.
archivoRelacionados = open('postingEtiquetasRelacionadas.txt','w')#Indice etiqueta-etiquetaRelacionadas
contador =0
hashRelacionados = {}

#Creacion del Indice imagen-etiquetas
for imagen in hashEtiquetas: 
   contador = contador+1
   ImagenesVecinosVisuales = extraerVecinos(imagen,capitales)
   dicEtiquetas = {} #Diccionario que almacena las etiquetas con sus peso de relevancia de etiqueta de la imagen. 
   for etiqueta in hashEtiquetas[imagen]:
      print "Trabajando en etiqueta: " + etiqueta  +" de la imagen "+str(contador)        
      pesoVecinosCap = calcularPesoVecinos(etiqueta,ImagenesVecinosVisuales,hashImagenes,hashEtiquetas)
      dicEtiquetas[etiqueta] = Alfa + (1-Alfa)*(pesoVecinosCap)
      hashRelacionados = calcularCorrelacion(etiqueta,hashRelacionados,hashEtiquetas,imagen)               
   ranking = dicEtiquetas.items()
   ranking.sort(lambda x,y:cmp(y[1], x[1])) #Ordena la relevancia de mayor a menor
   pesoMaximo = ranking[0][1]
   archivoPesosImagenes.write(imagen+'>')
   for r in ranking[:-1]:
        peso = Alfa + ((1-Alfa)*r[1]/pesoMaximo)
        archivoPesosImagenes.write(r[0]+','+str(peso)+';')
   peso = Alfa + ((1-Alfa)*ranking[-1][1]/pesoMaximo)
   archivoPesosImagenes.write(ranking[-1][0]+','+str(peso)+'\n')
   print "Progreso: "+ str(contador*100.00/D) +"%"


#Creacion del Indice etiqueta-imagenes.
for etiqueta in hashImagenes:
    archivoEtiquetas.write(etiqueta+'>')
    for imagen in hashImagenes[etiqueta][:-1]:
        archivoEtiquetas.write(imagen+';') 
    archivoEtiquetas.write(hashImagenes[etiqueta][-1]+'\n') 

#Creacion del Indice etiqueta-etiquetaRelacionadas
for etiqueta1 in hashRelacionados:
    for etiqueta2 in hashRelacionados[etiqueta1]:
       hashRelacionados[etiqueta1][etiqueta2] = float(hashRelacionados[etiqueta1][etiqueta2]) / float( len(hashImagenes[etiqueta1]) +  len(hashImagenes[etiqueta2]) - hashRelacionados[etiqueta1][etiqueta2] ) 
    hashRelacionados[etiqueta1] = hashRelacionados[etiqueta1].items()
    hashRelacionados[etiqueta1].sort(lambda x,y:cmp(y[1], x[1]))
    archivoRelacionados.write(etiqueta1 + '>')
    for lista in hashRelacionados[etiqueta1][:-1]:
         archivoRelacionados.write(lista[0] +','+str(lista[1])+';')
    archivoRelacionados.write(hashRelacionados[etiqueta1][-1][0] +','+str(hashRelacionados[etiqueta1][-1][1])+'\n')

archivoRelacionados.close()
archivoEtiquetas.close()
archivoPesosImagenes.close()


