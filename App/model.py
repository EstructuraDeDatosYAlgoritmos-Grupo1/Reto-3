"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as merge
import datetime
assert cf
import random

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
#------------------------
# Construccion de modelos
#------------------------
def newCatalog():

    catalog = {"reps":None,
                "instrumentalness":None,
                "liveness":None,
                "speechiness":None,
                "danceability":None,
                "valence":None,
                "loudness":None,
                "tempo":None,
                "acousticness":None,
                "energy":None,
                "artists":None,
                "userMap":None,
                "time":None,
                "feeling":None}

    catalog["reps"] = lt.newList(datastructure="ARRAY_LIST")
    catalog["instrumentalness"]= om.newMap(omaptype='RBT', comparefunction=cmpCharacteristics)
    catalog["liveness"] = om.newMap(omaptype='RBT', comparefunction=cmpCharacteristics)
    catalog["speechiness"] = om.newMap(omaptype='RBT', comparefunction=cmpCharacteristics)
    catalog["danceability"] = om.newMap(omaptype='RBT', comparefunction=cmpCharacteristics)
    catalog["valence"] = om.newMap(omaptype='RBT', comparefunction=cmpCharacteristics)
    catalog["loudness"] = om.newMap(omaptype='RBT', comparefunction=cmpCharacteristics)
    catalog["tempo"] = om.newMap(omaptype='RBT', comparefunction=cmpCharacteristics)
    catalog["acousticness"] = om.newMap(omaptype='RBT', comparefunction=cmpCharacteristics)
    catalog["energy"] = om.newMap(omaptype='RBT', comparefunction=cmpCharacteristics)
    catalog['time'] = om.newMap(omaptype='RBT',comparefunction = compareTimes)


    catalog["artists"] = mp.newMap(numelements=40000, prime=20011, maptype="CHAINING", loadfactor = 2.0, comparefunction=cmpArtistId)
    catalog["userMap"] = mp.newMap(numelements=40000, prime=20011, maptype="CHAINING", loadfactor = 2.0, comparefunction=cmpUserId)
    catalog["feelings"] = mp.newMap(numelements=40000, prime=20011, maptype="CHAINING", loadfactor = 2.0)
    catalog["track"] = mp.newMap(numelements=40000, prime=20011, maptype="CHAINING", loadfactor = 2.0)

    return catalog

#------------------------------------------------
# Funciones para agregar informacion al catalogo
#------------------------------------------------

def addTrack(catalog,rep):
    existsEntry = mp.get(catalog["track"], rep["track_id"])
    if existsEntry == None:
        dataentry = lt.newList("SINGLE_LINKED")
        mp.put(catalog["track"],rep["track_id"],dataentry)
    else:
        dataentry = me.getValue(existsEntry)
    lt.addLast(dataentry, rep['hashtag'])

def addRep2(catalog, rep2):
    addToUserMap(catalog,rep2)

def addRep1(catalog,rep):
    existsRep = mp.get(catalog["userMap"], rep["user_id"])
    if existsRep != None:
        repList = me.getValue(existsRep)
        for rep2 in lt.iterator(repList):
            if rep2["track_id"]==rep["track_id"] and rep["created_at"]==rep2["created_at"]:
                rep1 = (rep, rep2["hashtag"])
                lt.addLast(catalog["reps"], rep1)
                break
    else:
        return -1

def addReps(catalog, rep, position):
    ans = addRep1(catalog,rep)
    if ans == -1:
        return None
    else:
        addArtist(catalog, rep, position)
        updateChar(catalog,"instrumentalness",rep, position)
        updateChar(catalog,"liveness",rep, position)
        updateChar(catalog,"speechiness",rep, position)
        updateChar(catalog,"danceability",rep, position)
        updateChar(catalog,"valence",rep, position)
        updateChar(catalog,"loudness",rep, position)
        updateChar(catalog,"tempo",rep, position)
        updateChar(catalog,"acousticness",rep, position)
        updateChar(catalog,"energy",rep, position)
        updateTimes(catalog,"time", rep, position)


def addEntry(dataentry, position):
    lt.addLast(dataentry, position)
    return dataentry

def newDataEntry():
    entry = lt.newList("ARRAY_LIST")
    return entry

def addToUserMap(catalog,rep2):
    existsEntry = mp.get(catalog["userMap"], rep2["user_id"])
    if existsEntry == None:
        dataentry = newDataEntry()
        mp.put(catalog["userMap"],rep2["user_id"],dataentry)
    else:
        dataentry = me.getValue(existsEntry)
    addEntry(dataentry, rep2)

def addArtist(catalog, rep, position):
    existsArtist = mp.get(catalog["artists"], rep["artist_id"])
    if existsArtist == None:
        dataentry = newDataEntry()
        mp.put(catalog["artists"], rep["artist_id"],dataentry)
    else:
        dataentry = me.getValue(existsArtist)
    addEntry(dataentry,position)

def addFeeling(catalog, rep):
    existsEntry = mp.get(catalog["feelings"], rep["hashtag"])
    if existsEntry == None:
        dataentry = lt.newList("SINGLE_LINKED")
        mp.put(catalog["feelings"],rep["hashtag"],dataentry)
    else:
        dataentry = me.getValue(existsEntry)
    lt.addLast(dataentry, rep)


# Funciones para la carga de las caracteristicas

def updateChar(catalog, char, rep, position):
    repChar = float(rep[char])
    entry = om.get(catalog[char],repChar)
    if (entry is None):
        dataentry = newDataEntry()
        om.put(catalog[char], repChar, dataentry)
    else:
        dataentry = me.getValue(entry)
    addEntry(dataentry, position)


def updateTimes(catalog, char,  rep, position):
    repOccuredOn = rep['created_at']
    repDate = datetime.datetime.strptime(repOccuredOn, '%Y-%m-%d %H:%M:%S')
    entry = om.get(catalog['time'],repDate.time())
    if (entry is None):
        dataentry = lt.newList("SINGLE_LINKED")
        om.put(catalog['time'], repDate.time(), dataentry)
    else:
        dataentry = me.getValue(entry)
    lt.addLast(dataentry,position)
    

#---------------------------------
# Funciones para creacion de datos
#----------------------------------

def newCharList():
    charList = mp.newMap(numelements = 18, loadfactor = 0.5, prime = 19, maptype="PROBING")
    mp.put(charList, 1, "instrumentalness")
    mp.put(charList, 2, "liveness")
    mp.put(charList, 3, "speechiness")

    mp.put(charList, 4, "danceability")
    mp.put(charList, 5, "valence")
    mp.put(charList, 6, "loudness")

    mp.put(charList, 7, "tempo")
    mp.put(charList, 8, "acousticness")
    mp.put(charList, 9, "energy")
    return charList

def newGenreList():
    genreList = lt.newList(datastructure="ARRAY_LIST", cmpfunction= cmpTempoRange)
    reggae = (60.0,90.0,"Reggae")
    downTempo = (70.0,100.0,"Down-Tempo")
    chillOut = (90.0,120.0,"Chill-out")

    hipHop = (85.0,115.0,"Hip-hop")
    JazzAndFunk = (120.0,125.0,"Jazz and Funk")
    pop = (100.0,130.0,"Pop")

    RnB = (60.0,80.0,"R&B")
    rock = (110.0,140.0,"Rock")
    metal = (100.0,160.0,"Metal")

    lt.addLast(genreList, reggae )
    lt.addLast(genreList, downTempo)
    lt.addLast(genreList, chillOut)
    lt.addLast(genreList, hipHop)
    lt.addLast(genreList, JazzAndFunk)
    lt.addLast(genreList, pop)
    lt.addLast(genreList, RnB)
    lt.addLast(genreList, rock)
    lt.addLast(genreList, metal)
    return genreList

def newGenreList1():
    genreList = lt.newList(datastructure="ARRAY_LIST")
    reggae = {'mini': 60.0, 'maxi': 90.0, 'name': "Reggae", 'reps': 0, 'avg': lt.newList(datastructure='SINGLE_LINKED')}
    downTempo = {'mini':70.0, 'maxi':100.0,'name':"Down-Tempo",'reps': 0, 'avg': lt.newList(datastructure='SINGLE_LINKED')}
    chillOut = {'mini':90.0, 'maxi':120.0,'name':"Chill-out",'reps': 0, 'avg': lt.newList(datastructure='SINGLE_LINKED')}

    hipHop = {'mini':85.0, 'maxi':115.0,'name':"Hip-hop",'reps': 0, 'avg': lt.newList(datastructure='SINGLE_LINKED')}
    JazzAndFunk = {'mini':120.0, 'maxi':125.0,'name':"Jazz and Funk",'reps': 0, 'avg': lt.newList(datastructure='SINGLE_LINKED')}
    pop = {'mini':100.0, 'maxi':130.0,'name':"Pop",'reps': 0, 'avg': lt.newList(datastructure='SINGLE_LINKED')}

    RnB = {'mini':60.0, 'maxi':80.0,'name':"R&B",'reps': 0, 'avg': lt.newList(datastructure='SINGLE_LINKED')}
    rock = {'mini':110.0, 'maxi':140.0,'name':"Rock",'reps': 0, 'avg': lt.newList(datastructure='SINGLE_LINKED')}
    metal = {'mini':100.0, 'maxi':160.0,'name':"Metal",'reps': 0, 'avg': lt.newList(datastructure='SINGLE_LINKED')}

    lt.addLast(genreList, reggae )
    lt.addLast(genreList, downTempo)
    lt.addLast(genreList, chillOut)
    lt.addLast(genreList, hipHop)
    lt.addLast(genreList, JazzAndFunk)
    lt.addLast(genreList, pop)
    lt.addLast(genreList, RnB)
    lt.addLast(genreList, rock)
    lt.addLast(genreList, metal)
    return genreList

#------------------------
# Funciones de consulta
#------------------------

def repSize(catalog):
    return lt.size(catalog["reps"])

def indexHeight(catalogIndex):
    return om.height(catalogIndex)

def getChar(charList, charPos):
    bestChar = mp.get(charList, charPos)
    return me.getValue(bestChar)

def getGenre(genreList, genrePos):
    tempoRange = lt.getElement(genreList,genrePos)
    return tempoRange


def getPosition(catalog):
    pos = lt.size(catalog["reps"]) + 1
    return pos

def numArtists(catalog):
    artistList = mp.keySet(catalog["artists"])
    return lt.size(artistList)
#--------------------------------------------------------------------------------------------

# Primer Requerimiento

def getCharByRange(catalog, bestChar, minIns, maxIns):
    lst = om.values(catalog[bestChar], minIns, maxIns)
    finalLst = combineLists(lst)
    totreps = lt.size(finalLst)
    return totreps, finalLst

def combineLists(lst):
    finalLst = lt.newList(datastructure="ARRAY_LIST", cmpfunction=cmpPosition)
    for cmpLst in lt.iterator(lst):
        for cmpPos in lt.iterator(cmpLst):
            lt.addLast(finalLst, cmpPos)
    return finalLst

def joinLists(lst1, lst2):
    finalLst = lt.newList(datastructure="ARRAY_LIST", cmpfunction=cmpPosition)
    for pos1 in lt.iterator(lst1):
        pos1 = int(pos1)
        if lt.isPresent(lst2, pos1) != 0:
            lt.addLast(finalLst, pos1)
    totreps = lt.size(finalLst)
    return totreps, finalLst

# Segundo Requerimiento



# Tercer Requerimiento

def pickRandomTracks(catalog, lst):
    ltSize = lt.size(lst)
    trackList = lt.newList(datastructure="ARRAY_LIST", cmpfunction=cmpPosition)
    finalList = lt.newList(datastructure="ARRAY_LIST")
    for i in range(5):
        pos = random.randint(1, ltSize)
        track = lt.getElement(lst, pos)
        lt.addLast(trackList, track)
    for pos in lt.iterator(trackList):
        pos= int(pos)
        event = lt.getElement(catalog["reps"], pos)
        lt.addLast(finalList, event)
    return finalList


# Cuarto Requerimiento



# Quinto Requerimiento

def getGenreByTimeRange(catalog, initialTi, finalTi):
    lst = om.values(catalog['time'], initialTi, finalTi)
    lst1 = lt.newList(datastructure = 'SINGLE_LINKED')
    genreList = newGenreList1()
    for lstrep in lt.iterator(lst):
        for lstrep1 in lt.iterator(lstrep):
            #Entiendo que tengo que pedirle el valor a la lista
            lstrep2 = lt.getElement(catalog["reps"], lstrep1)
            #Entiendo que como es una tupla tengo que pedirle el primer valor
            lstrep3 = lstrep2[0]
            #Entiendo que a ese valor le puedo pedir el tempo
            tempo = lstrep3['tempo']
            for genre in lt.iterator(genreList):
                if (float(tempo) >= float(genre['mini']) and float(tempo) <= float(genre['maxi'])):
                    genre['reps'] =  genre['reps'] + 1
                    lt.addLast(genre['avg'],lstrep1)

    maxReps = 0
    maxName = None
    lstGenre = None
            
    for genre in lt.iterator(genreList):
        if genre['reps'] > maxReps:
            maxReps = genre['reps']
            maxName = genre['name']
            lstGenre = genre['avg']

    counter = 0 
    lst2 = lt.newList(datastructure = 'SINGLE_LINKED')
    lst3 = lt.newList(datastructure = 'SINGLE_LINKED')
    lst4 = lt.newList(datastructure = 'SINGLE_LINKED')

    while counter < lt.size(lstGenre):
        avg1 = 0
        # Se le pide el valor de la posicion counter en la lista de tracks del genero mas escuchado a la lista general
        value = lt.getElement(catalog['reps'],lt.getElement(lstGenre, counter))
        # Se le pide la primera parte de la tupla que es la que contiene la informacion util
        value1 = value[0]
        value2 = value1['track_id']
        # Se le piden los hashtags asociados al track_id de la entrada
        hashtags = mp.get(catalog['track'],value2)
        hashtags = me.getValue(hashtags)
        # Se crea una lista que va a contener los vander avg de cada uno de los hashtags
        lst5 = lt.newList(datastructure = 'SINGLE_LINKED')
        # Si la cantidad de hashtags es diferente de cero, para cada hashtag se pide la entrada en la lista de sentimientos
        if lt.size(hashtags) != 0:
            for element in lt.iterator(hashtags):
                  feel = mp.get(catalog['feelings'], element)
                  # Si existe una entrada asociada al hashtag en la lista de sentimientos, se pide el valor
                  if feel != None:
                      feel1 = me.getValue(feel)
                      # Como puede existir mas de una entrada asociada a un hashtag en la lista de sentimientos (y por lo tanto varios valores vader_avg), se usa el primero
                      feel1 = lt.getElement(feel1, 0)
                      # Si el vader_avg no está vacio se saca el valor, se añade a la lista lst5 y se suma a avg 1
                      if feel1['vader_avg'] != '':
                           avg = float(feel1['vader_avg'])
                           lt.addLast(lst5, avg)
                           avg1 = avg1 + avg
                 
        #La lista de valores de avg para esta entrada (hashtags validos) se añade a la lista 2, solo se añade si es diferente a cero porque se necesita sacar el promedio (y no se puede dividir en cero)
        if lt.isEmpty(lst5) == 0:
           lt.addLast(lst2, lst5)     
        #El id de esta entrada se añade a la lst3
        lt.addLast(lst3, value2)
        #La suma de los average se añade a la lst4 
        lt.addLast(lst4, avg1)

        counter = counter + 1
                
    return maxName,  maxReps, lst2, lst3, lst4

# Funciones utilizadas para comparar elementos dentro de una lista

def cmpCharacteristics(char1, char2):
    if (float(char1) == float(char2)):
        return 0
    elif float(char1) > float(char2):
        return 1
    else:
        return -1

def cmpPosition(pos1,pos2):
    if int(pos1) == int(pos2):
        return 0
    elif int(pos1) > int(pos2):
        return 1
    else:
        return -1

def cmpUserId(id1,entry):
    identry = me.getKey(entry)
    if (int(id1) == int(identry)):
        return 0
    elif (int(id1) > int(identry)):
        return 1
    else:
        return -1

def cmpArtistId(id1, entry):
    identry = me.getKey(entry)
    if id1 == identry:
        return 0
    elif id1 > identry:
        return 1
    else:
        return -1

def cmpTempoRange(range1, range2):
    if range1[0]+range1[1] == range2[0]+range2[1]:
        return 0
    elif range1[0]+range1[1] > range2[0]+range2[1]:
        return 1
    else:
        return -1

def compareTimes(time1, time2):
    if (time1 == time2):
        return 0
    elif (time1 > time2):
        return 1
    else:
        return -1

def compareListsSize(list1, list2):
    if (lt.size(list1) == lt.size(list2)):
        return 0
    elif (lt.size(list1) > lt.size(list2)):
        return 1
    else:
        return -1
# Funciones de ordenamiento
