# -*- coding: UTF-8 -*-
"""
    Módulo que permite gestionar los distintos eventos enviados por
    los dispositivos GPS.

    Autor   : Jorge A. Toro
    email   : jolthgs@gmail.com, jolth@esdebian.org
    date    : vie jul 20 07:49:38 COT 2012
    version : 1.0.0

    Usage:
        >>> import datetime
        >>> import Event.captureEvent
        >>>
        >>>data = {'codEvent': '06', 'weeks': '1693', 'dayWeek': '4', 'ageData': '2', 'position': '(4.81534,-75.69489)', \
        'type': 'R', 'address': '127.0.0.1,45840', 'geocoding': u'RUEDA MILLONARIA PEREIRA, Calle 18 # CARRERA 7, Pereira, Colombia',\ 
        'data': '>REV061693476454+0481534-0756948900102632;ID=ANT051<', 'course': '026', 'gpsSource': '3', 'time': '76454', 'lat': '4.81534', \
        'typeEvent': 'EV', 'lng': '-75.69489', 'datetime': datetime.datetime(2012, 7, 23, 7, 31, 26, 608343), 'speed': 1.0, 'id': 'ANT051', 'altura': None}
        >>> 
        >>> event = Event.captureEvent.parseEvent(data)
        INSERT: event6
        Insert Positions_gps
        procpid: 3729
        RETURN: 88 5
        Insert Eventos
        Actualizando y Cerranda la conexión
        >>> 
        >>> event
        'Start'
        >>> 

"""
import sys
import traceback


def insertEvent(evento): 
    def insert(data):
        """ 
            Llama la función PL/pgSQL. 
        """
        from DB.pgSQL import PgSQL
        
        ###### SQL:
        # Insert Positions:
        queryPositions = """SELECT fn_save_event_position_gps(%(id)s, %(position)s, %(geocoding)s, 
                         %(speed)s, %(altura)s, %(course)s, %(gpsSource)s, %(address)s, %(datetime)s);"""
        # Insert Eventos:
        queryEventos = """INSERT INTO eventos(gps_id, positions_gps_id, type, fecha) 
                          VALUES (%(gps_id)s, %(positions_id)s, %(codEvent)s, %(datetime)s);"""

        try:
            db = PgSQL()
            db.cur.execute(queryPositions, data) 

            if evento.__name__ == "event5": return evento(data) 
            try:
                data['positions_id'], data['gps_id'] = eval(db.cur.fetchone()[0]) 
            except:
                return 

            db.cur.execute(queryEventos, data) 

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print >> sys.stderr, '-'*60
            print >> sys.stderr, "*** print exception <<insertEvent>>:"
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                               limit=2, file=sys.stderr)
            print >> sys.stderr, '-'*60
            return
        finally:
            db.conn.commit()
            db.cur.close()
            db.conn.close()

        return evento(data) 

    return insert


def insertReport(): pass

        
@insertEvent
def event1(data=None): return "Panic" 
@insertEvent
def event2(data=None): return "Speeding"
@insertEvent
def event5(data=None): return "Report" 
@insertEvent
def event6(data=None): return "Start"
@insertEvent
def event7(data=None): return "Shutdow"
@insertEvent
def event8(data=None): return "Bateri on"
@insertEvent
def event9(data=None): return "Bateri off"

                       
def parseEvent(data=None): 
    """
        Analiza y determina que hacer con cada uno de los eventos. 
    """
    return (callable(getTypeEvent(data)) or None) and getTypeEvent(data)(data) 


def getTypeEvent(data=None, module=sys.modules[parseEvent.__module__]):
    """ 
        >>> captureEvent.getTypeEvent(data)
        <function event5 at 0xb7395844>
        >>> 
    """
    try:
        event = "event%s" % int(data['codEvent'])
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print >> sys.stderr, '-'*60
        print >> sys.stderr, "*** print exception:"
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                  limit=2, file=sys.stderr)
        print >> sys.stderr, '-'*60
        return 
    return hasattr(module, event) and getattr(module, event) or None 


