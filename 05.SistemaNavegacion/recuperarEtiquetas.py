#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Programa que devuelve las etiquetas de una imagen dada por su ID.

import math
import sys


imagen = sys.argv[1]
archivo = open('postingImagenes.txt','r')
for linea in archivo:
     imagenArchivo = linea.split('>')[0]
     if imagen == imagenArchivo:
          datosImagen = linea.split('>')[1][:-1]
          datosEtiquetas = datosImagen.split(';')
          for etiqueta in datosEtiquetas[:-1]:
              print etiqueta.split(',')[0] + " "
          print datosEtiquetas[-1].split(',')[0]  
          break
