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
                "userMap":None}

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

    catalog["artists"] = mp.newMap(numelements=40000, prime=20011, maptype="CHAINING", loadfactor = 2.0, comparefunction=cmpArtistId)
    catalog["userMap"] = mp.newMap(numelements=40000, prime=20011, maptype="CHAINING", loadfactor = 2.0, comparefunction=cmpUserId)


    return catalog

#------------------------------------------------
# Funciones para agregar informacion al catalogo
#------------------------------------------------

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

    

def addEntry(dataentry, rep):
    lt.addLast(dataentry,rep)
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
# Funciones de ordenamiento
