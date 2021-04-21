﻿"""
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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def initCatalog():
    catalog = model.newCatalog()
    return catalog

# Funciones para la carga de datos

def loadEvents(catalog):
    eventsfile1 = cf.data_dir + "subsamples-small/user_track_hashtag_timestamp-small.csv"
    eventsfile2 = cf.data_dir + "subsmples-small/context_content_features-small.csv"
    eventsDict1 = csv.DictReader(open(eventsfile1, encoding='utf-8'))
    eventsDict2 = csv.DictReader(open(eventsfile2, encoding='utf-8'))
    for entry in eventsDict1:
        model.addFirstEntrySet(catalog, entry)
    for entry in eventsDict2:
        model.addSecondEntrySet(catalog, entry)
        


# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
