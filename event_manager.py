import json
import datetime as dt
from utilities import *
import datetime

sg1 = "por favor verifique que los valores seleccionados sean correctos!"
sg2 = "su aventura debe tener una duracion de al menos 24 horas!"

def setEvent(event):
    writeJson('current_event.json', [event])

def validDate(Ini, End, TimeIni, TimeEnd):
    Ini = Ini.split("/")
    End = End.split("/")
    hi, mi = TimeIni[0], TimeIni[1]
    he, me = TimeEnd[0], TimeEnd[1]
    start, end = 0, 0
    td = 0
    try:
        if len(hi + mi + he + me) > 8:
            raise IndexError()
        
        hi, mi = int(hi), int(mi)
        he, me = int(he), int(me)

        start = dt.datetime(int(Ini[2]), int(Ini[1]), int(Ini[0]), hi, mi).timestamp()
        end = dt.datetime(int(End[2]), int(End[1]), int(End[0]), he, me).timestamp()
     
        if hi < 0 or hi > 24 or he < 0 or he > 24:
            raise IndexError()
        if mi < 0 or mi > 59 or me < 0 or me > 59:
            raise IndexError()
        
        td = dt.datetime(int(Ini[2]), int(Ini[1]), int(Ini[0]) + 1, hi, mi).timestamp()
        
        if td > end: 
            raise Exception()
          
    except Exception as e:
        return sg1 if type(e) == IndexError or type(e) == ValueError else sg2    
    else:
        return ((start, end), (Ini, End), ((hi, mi), (he, me)))

def validResources():
    event = readJson("current_event.json")[0]
    resources = readJson("recursos_seleccionados_event.json")

    for need in event["necesita"]:
        res_need = get_one(need)

        if not (res_need in resources):
            return "uno de los recursos necesarios para el evento no se encuentra entre los seleccionados!"

    #event conflict
    for resource in resources:
        for exclud in resource["excluyente"]:
            value = getOneByName(exclud, "recursos_seleccionados_event.json")

            if value != False:
                return "verifique para cada recurso que su excluyente no se encuentre seleccionado!"
        
        flag = False

        for complement in resource["complementario"]:
            value = getOneByName(complement, "recursos_seleccionados_event.json")
         
            if value != False:
                flag = True
                break
        
        if not flag:
            print(resource["nombre"])
            return "verifique que cada recurso este seleccionado junto con su complementario!"
 

    resorceList = appList().mycon.layo.rlist
    answer = []

    for child in resorceList.children:
        cuantity = int(child.cuantity.text)
        resource = get_one(child.id)
        
        if cuantity > resource["cantidad"]:
            return "verifique que la cantidad seleccionada de cada recurso no exceda la cantidad disponible en el inventario!"            

        answer.append((child.id, cuantity))

    return answer

def interception(l1, r1, l2, r2):
    if (l1 <= l2 and l2 <= r1) or (l2 <= l1 and l1 <= r2):
        return True
    
    return False

def conflict(event1, event2):
    pass

def verifyInterval(event, ini, end):
    nested = []

    for e in readJson("running_events.json"):
        timeEvent = e["tiempoReal"]

        if interception(timeEvent[0], timeEvent[1], ini, end):
            nested.append(e)
    
    resources = {}

    for eventNested in nested:
        resource = eventNested["recursos"]

        for x in resource:
            resources[x[0]] = resources.get(x[0], 0) + x[1] 

    for resource in event["recursos"]:
        type = resource[0]
        total = get_one(type)["cantidad"]
        cuantity = resources.get(type, -1)

        if cuantity != -1 and cuantity + resource[1] > total:
            return False

    return True

def toDate(value):
    return dt.datetime.fromtimestamp(value, tz=dt.timezone.utc)

def getDate(day, month, year):
    return dt.datetime(year, month, day).timestamp() 

def joinTime(event):
    ini = event["tiempoReal"][0]
    end = event["tiempoReal"][1]
    time = end - ini
    default = getDate(1, 1, 2077)
    
    if verifyInterval(event, default, default + time):
        return (default, default + time)

    for e in readJson("running_events.json"):
        tr = e["tiempoReal"]
        if verifyInterval(event, tr[1] + 60, tr[1] + 60  + time):
            return (tr[1] + 60, tr[1] + 60 + time)     

def mergeInformation(Date, Resources):
    event = readJson("current_event.json")[0]

    event["recursos"] = Resources
    event["tiempoReal"] = Date[0]
    event["fechaInicio"] = Date[1][0]
    event["fechaFin"] = Date[1][1]
    event["tiempoInicio"] = Date[2][0]
    event["tiempoFin"] = Date[2][1]
    
    return event    

def createEvent(event):
    if verifyInterval(event, event["tiempoReal"][0], event["tiempoReal"][1]):
        return (True, toDate(event["tiempoReal"][0]), toDate(event["tiempoReal"][1]))
    else:
        hole = joinTime(event)
        dateIni = toDate(hole[0])
        dateEnd = toDate(hole[1])
        event["tiempoReal"] = (hole[0], hole[1])
        return (False, (dateIni, dateEnd), (hole[0], hole[1]))
    