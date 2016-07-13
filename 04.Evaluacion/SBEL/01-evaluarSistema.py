#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Programa para evaluar la Precision y la Exhaustividad del Sistema de Recuperacion basado en etiquetas limpias. Devuelve un archivo con el Resultado de la Evaluacion.

import recuperarImagenes

capital ='budapest hungria' #Consulta de capital
evaluacion = open('Resultados/evaluacionBudapest.txt','w') #Archivo de salida con el resultado de la evaluacion
archivoRelevantes = open('Resultados/relBudapest.txt','r') #Archivo que contiene las imagenes relevantes de la consulta
relevantes=[] #Lista de imagenes relevantes
for r in archivoRelevantes: 
   relevantes.append(r[:-1])

resultados = recuperarImagenes.devolverRanking(capital) #Ranking de imagenes devueltos
totalRelevantes =len(relevantes)
recuperados = 0
relevantesRecuperados = 0

#Evaluacion de Precision y Exhaustividad
evaluacion.write("Consulta: "+capital+"\n")
evaluacion.write("Ranking Precision Exhautividad\n")
for r in resultados:
   recuperados = recuperados +1
   if r in relevantes:
       relevantesRecuperados = relevantesRecuperados+1
   precision = float(relevantesRecuperados) / float(recuperados)
   exhautividad = float(relevantesRecuperados) / float(totalRelevantes)
   evaluacion.write(str(recuperados) +"\t"+str(precision) +"\t\t"+str(exhautividad)+"\n")

evaluacion.close()
archivoRelevantes.close()
