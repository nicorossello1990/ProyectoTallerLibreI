#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Programa que descarga 500 imagenes de Flickr, 100 imagenes por cada capital (50). Se descargan las Imagenes en el directorio "Fotos". Se almacenan los nombres de las imagenes en el archivo "capitales.txt" y las etiquetas en el archivo "etiquetas_or.txt"

import flickr_api
from flickr_api.api import flickr
import os
import unicodedata

#Funcion que saca las tildes de las palabras.
def limpiar(s):
     s= ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
     return s



CANTUSUARIOS = 5 #Limite maximo de Fotos por usuario. 
FOTOSRECUPERAR = 500 #Limite de Imagenes a Recuperar.
capitales = ["Tirana Albania", "Berlín Alemania", "Andorra la Vieja Andorra", "Ereván Armenia", "Viena Austria", "Bakú Azerbaiyán", "Bruselas Bélgica", "Minsk Bielorrusia", "Sarajevo Bosnia y Herzegovina", "Sofía Bulgaria", "Nicosia Chipre", "Ciudad del Vaticano", "Zagreb Croacia", "Copenhague Dinamarca", "Bratislava Eslovaquia", "Liubliana Eslovenia", "Madrid España", "Tallin Estonia", "Helsinki Finlandia", "París Francia", "Tiflis Georgia", "Atenas Grecia", "Budapest Hungría", "Dublín Irlanda", "Reikiavik Islandia", "Roma Italia", "Astaná Kazajistán", "Riga Letonia", "Vaduz Liechtenstein", "Vilna Lituania", "Luxemburgo Luxemburgo", "La Valeta Malta", "Chisinau Moldavia", "Mónaco Mónaco", "Podgorica Montenegro", "Oslo Noruega", "Ámsterdam", "Varsovia Polonia", "Lisboa Portugal", "Londres Reino Unido", "Praga República Checa", "Skopie Macedonia", "Bucarest Rumania", "Moscú Rusia", "San Marino San Marino", "Belgrado Serbia", "Estocolmo Suecia", "Berna Suiza", "Ankara Turquía", "Kiev Ucrania"]
totalFotos = len(capitales)*FOTOSRECUPERAR


#Conctar a la API de Flickr por codigo.
a = flickr_api.auth.AuthHandler.load('codigo')
flickr_api.set_auth_handler(a)


fotosDescargadas=0
archivoCapitales = open ('capitales.txt','w') #Archivo que contiene los nombres de imagenes.
archivoEtiquetas = open ('etiquetas_or.txt','w') #Archivo de etiquetas.


for capital in capitales:
    capital2 = limpiar(capital.decode('utf-8'))
    consulta = flickr_api.Photo.search(text=capital2,sort='relevance',media='photos', per_page=FOTOSRECUPERAR, page=1) #Realiza la consulta a la API de FLickr.
    if not os.path.exists('Fotos/'+capital2):
       os.mkdir('Fotos/'+capital2)
    ranking=1
    intentos = 0
    user={}
    for c in consulta:
         intentos = intentos +1
         foto = flickr_api.Photo(id = c.id)
         print "Descargando foto "+str(ranking)+" de la capital: "+foto.title.encode('utf-8') +". Progreso: "+str(fotosDescargadas) +"/"+str(totalFotos) +". Intentos: "+str(intentos)       
         IDuser = foto.getInfo()['owner'].id #Obtiene el nombre del usuario de la imagen.
         if IDuser in user.keys():
             user[IDuser] = user[IDuser]+1
         else:
             user[IDuser] = 1
         etiquetas = foto.getTags() #Obtiene las etiquetas de la imagen.
         if len(etiquetas)>0 and user[IDuser] <=CANTUSUARIOS: #Si la imagen tiene mas de una etiqueta y si no supera el limite de usuario la descarga.
          try:
            for e in etiquetas:  
               archivoEtiquetas.write(str(c.id)+";"+e.text.encode('utf-8')+"\n") #Almacena las etiquetas de la imagen en el archivo de etiquetas.
            archivoCapitales.write(str(c.id)+";"+c.title.encode('utf-8')+';'+IDuser.encode('utf-8')+"\n") #Almacena el nombre de la imagen y el usuario en el archivo de capitales.
            if not os.path.exists("Fotos/"+capital2+"/"+c.id.encode('utf-8')):
              try:
                foto.save("Fotos/"+capital2+"/"+c.id.encode('utf-8'),size_label = 'Medium 640') #Almacena la imagen en tamaño 640. Si no existe en ese tamaño almacena en tamaño original.
              except:
                foto.save("Fotos/"+capital2+"/"+c.id.encode('utf-8'))   
            ranking=ranking+1
            fotosDescargadas= fotosDescargadas+1
            if ranking > 100:
                fotosDescargadas = (capitales.index(capital) + 1) * FOTOSRECUPERAR +1
                break
          except:
             print "Error"
 
  
archivoCapitales.close()
archivoEtiquetas.close()




