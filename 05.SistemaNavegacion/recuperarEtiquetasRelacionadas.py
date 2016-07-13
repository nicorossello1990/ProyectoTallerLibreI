#!/usr/bin/env python
# -*- coding: utf-8 -*-


#Programa que devuelve las etiquetas relacionadas a una o varias etiquetas de consulta textual pasada por argumentos. Devuelve una lista con las etiquetas mas relacionadas.

import sys
import unicodedata

#Funcion que carga el Indice etiqueta-etiquetaRelacionadas.
def cargarRelacionadas():
  hashRelacionadas = {}
  archivo = open('postingEtiquetasRelacionadas.txt','r')
  for linea in archivo:
    etiqueta = linea.split('>')[0]
    listaRelacionadas = linea.split('>')[1][:-1]
    hashRelacionadas[etiqueta] = listaRelacionadas
  archivo.close()
  return hashRelacionadas

hashRelacionadas = cargarRelacionadas()


etiquetas = sys.argv #Consulta textual tomada de los argumentos del programa.
et_consulta=[]
for etiqueta in etiquetas[1:]:
   if etiqueta !='': 
      etiqueta= ''.join((c for c in unicodedata.normalize('NFD', etiqueta.decode('utf-8')) if unicodedata.category(c) != 'Mn')) #Elimina las tildes de la etiqueta.
      etiqueta = etiqueta.lower() #Transforma la etiqueta a minusculas.
      et_consulta.append(etiqueta)


ranking = {}
for etiqueta in et_consulta: #Por cada etiquetas de consulta calcula el puntaje de relacion de etiquetas 
   if etiqueta in hashRelacionadas.keys():
        relacionadas = hashRelacionadas[etiqueta].split(';')
        for r in relacionadas:
            etRelacionada = r.split(',')[0]
            peso = r.split(',')[1]
            if etRelacionada in ranking.keys(): #Si la etiqueta se repite suma los pesos
                ranking[etRelacionada] = ranking[etRelacionada] + peso
            else:
                ranking[etRelacionada] = peso

#Ordena el Ranking de Etiquetas Relacionadas de mayor a menor por el peso de relacion de etiqueta.
ranking = ranking.items()
ranking.sort(lambda x,y:cmp(y[1], x[1]))

for r in ranking[:-1]:
    print r[0] + " "
print ranking[-1][0]
