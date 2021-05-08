"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Buscar eventos de escucha en rango de la caracteristica deseada")
    print("3- Buscar musica para festejar")
    print("4- Buscar musica para estudiar")
    print("5- Estudiar un genero musical")
    print("6- Buscar el genero musical mas escuchado en un rango de horas")


def printCharacteristics():
    print("1. Instrumentalness")
    print("2. Liveness")
    print("3. Speechiness")

    print("4. Danceability")
    print("5. Valence")
    print("6. Loudness")

    print("7. Tempo")
    print("8. Acousticness")
    print("9. Energy")


def printGenres():
    print("1. Reggae")
    print("2. Down-Tempo")
    print("3. Chill-out")

    print("4. Hip-hop")
    print("5. Jazz and Funk")
    print("6. Pop")

    print("7. R&B")
    print("8. Rock")
    print("9. Metal")

    print("10. Otro genero")

def printRandomTracks(catalog, lst):
    randomTracks = controller.pickRandomTracks(catalog, lst)
    trackNumber = 1
    for track1 in lt.iterator(randomTracks):
        track = track1[0]
        print("Track"+str(trackNumber)+": "+str(track["track_id"])+" con instrumentalidad de "+str(track["instrumentalness"])+" y tempo de "+str(track["tempo"]))

catalog = {}
charList = controller.newCharList()
genreList = controller.newGenreList()
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = controller.initCatalog()
        controller.loadEvents(catalog)
        numArtist = controller.numArtists(catalog)
        print('Eventos cargados: ' + str(controller.repSize(catalog)))
        print("Artistas unicos: " + str(numArtist))

    elif int(inputs[0]) == 2:
        printCharacteristics()
        charPos = int(input("Ingrese el numero de la caracteristica que desea buscar: "))
        if charPos <= 0 or charPos > 9:
            print("Ingrese una numero valido")
        else:
            bestChar = controller.getChar(charList, charPos)
            minChar = float(input("Ingrese el minimo de "+bestChar+": "))
            maxChar = float(input("Ingrese el maximo de "+bestChar+": "))
            if minChar > 1.00 or minChar < -1.00 or maxChar > 1.00 or maxChar < -1.00:
                print("Ingrese un numero entre 1 y -1.")
            else:
                total = controller.getCharByRange(catalog, bestChar, minChar, maxChar)
                print("\nTotal de eventos de escucha en el rango de "+bestChar+": " + str(total[0]))
                print('Altura del arbol: ' + str(controller.indexHeight(catalog[bestChar])))

    elif int(inputs[0]) == 3:
        minEnergy = float(input("Ingrese el valor minimo de energia (Entre 1.0 y -1.0): "))
        maxEnergy = float(input("Ingrese el valor maximo de energia (Entre 1.0 y -1.0): "))
        minDanceability = float(input("Ingrese el valor minimo de bailabilidad (Entre 1.0 y -1.0): "))
        maxDanceability = float(input("Ingrese el valor maximo de bailabilidad (Entre 1.0 y -1.0): "))
        enregyList = controller.getCharByRange(catalog, "energy", minEnergy, maxEnergy)
        danceabilityList = controller.getCharByRange(catalog, "danceability", minDanceability, maxDanceability)
        answers = controller.joinLists(enregyList[1], danceabilityList[1])
        print("Hay un total de " + str(answers[0]) + " repeticiones entre el rango de bailabilidad " + str(minDanceability) + " - " + str(maxDanceability) + " y para el rango de energia "+str(minEnergy)+" - "+str(maxEnergy))
        printRandomTracks(catalog, answers[1])

    elif int(inputs[0]) == 4:
        minInstrumentalness = float(input("Ingrese el valor minimo de instrumentalidad (Entre 1.0 y -1.0): "))
        maxInstrumentalness = float(input("Ingrese el valor maximo de instrumentalidad (Entre 1.0 y -1.0): "))
        minTempo = float(input("Ingrese el valor minimo para el tempo: "))
        maxTempo = float(input("Ingrese el valor maximo para el tempo: "))
        instrumentalList = controller.getCharByRange(catalog, "instrumentalness", minInstrumentalness, maxInstrumentalness)
        tempoList = controller.getCharByRange(catalog, "tempo", minTempo, maxTempo)
        answers = controller.joinLists(instrumentalList[1], tempoList[1])
        print("Hay un total de " + str(answers[0]) + " repeticiones entre el rango de instrumentalidad " + str(minInstrumentalness) + " - " + str(maxInstrumentalness) + " y para el rango de tempo "+str(minTempo)+" - "+str(maxTempo))
        printRandomTracks(catalog, answers[1])

    elif int(inputs[0]) ==5:
        printGenres()
        genreTuple = input("Ingrese los numeros de los generos que desea buscar separados por comas: ")
        genreTuple = genreTuple.split(",")
        genreTuple = tuple(genreTuple)
        for genrePos in genreTuple:
            genrePos = int(genrePos)
            if genrePos <= 0 or genrePos > 10:
                print("Ingrese una numero valido")
            elif genrePos !=10:
                tempoRange = controller.getGenre(genreList,genrePos)
                genre = tempoRange[2]
                minTempo = tempoRange[0]
                maxTempo = tempoRange[1]
                total = controller.getCharByRange(catalog,"tempo",minTempo,maxTempo)
                print("Para "+str(genre)+" el tempo esta entre "+str(minTempo)+" y "+str(maxTempo)+" BPM...")
                print("\nEl numero de reproducciones para este genero fueron: "+str(total[0]))
            elif genrePos == 10:
                genre = input("Ingrese el nombre del nuevo genero: ")
                minTempo = float(input("Ingrese el valor minimo del tempo: "))
                maxTempo = float(input("Ingrese el valor maximo del tempo: "))
                total = controller.getCharByRange(catalog,"tempo",minTempo,maxTempo)
                print("Para "+str(genre)+" el tempo esta entre "+str(minTempo)+" y "+str(maxTempo)+" BPM...")
                print("\nEl numero de reproducciones para este genero fueron: "+str(total[0]))
    
    elif int(inputs[0]) == 6:
        initialTime = input("Ingrese la hora minima (H:M): ")
        finalTime = input("Ingrese la hora maxima (H:M): ")
        total = controller.getTimeByRange(catalog,initialTime,finalTime)
        print('El genero mas escuchado entre las ' + str(initialTime) + ' y las ' + str(finalTime) + ' es ' + str(total[0]) + ' con ' + str(total[1])+ ' reproducciones')
        print('\n Diez de sus tracks son: \n')
        counter = 0
        while counter < 10:
            print('ID: ' + str(lt.getElement(total[3],counter)) + ' con VADER promedio de: ' + str(lt.getElement(total[2],counter)))
            counter = counter + 1
    

    else:
        sys.exit(0)
sys.exit(0)

