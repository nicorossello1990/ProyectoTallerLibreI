#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Programa que devuelve el titulo de un ID de imagen dado.

import math
import sys


imagen = sys.argv[1]
archivo = open('capitales.txt','r')
titulo=''
for linea in archivo:
     imagenArchivo = linea.split(';')[0]
     if imagen == imagenArchivo:
          titulo = linea.split(';')[1]
          break
print titulo
