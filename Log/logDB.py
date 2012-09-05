# -*- coding: utf-8 -*-
"""
    Autor: Jorge A. Toro
"""
import sys
from DB.pgSQL import PgSQL

def insertLog(data=None): 
    """ 
        Query, que inserta la data en la tabla de Log 
    """
    query = """INSERT INTO log_gps (name, address, evento, fecha, posicion, ubicacion, grados, altura, satelites, estado_data, trama) 
               VALUES (%(id)s, %(address)s, 
                       %(codEvent)s, %(datetime)s, 
                       %(position)s, %(geocoding)s, 
                       %(course)s, %(altura)s, %(gpsSource)s, 
                       %(ageData)s, %(data)s)
            """
    db = PgSQL()
    return db.exe(query, data)
    
