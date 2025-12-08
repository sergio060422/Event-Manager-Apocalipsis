
from utilities.utilities import *
from core.event_manager import validateEventInfo, checkEvent, mergeInformation, createEvent, validResources
from utilities.ui_utils import *
import datetime as dt

def addToEventList(event):
    running = appList().events.scrollList.running
    
    from screens.event_list.events import RunningEvent

    running.add_widget(RunningEvent(event))

def manageAdventure(response, info, realTime):
    main = appList().mycon
    
    if response:
        current = readJson("data/dynamic/current_event.json")[1]

        if info != None:
            current["fechaInicio"] = [str(info[0].day), str(info[0].month), str(info[0].year)]
            current["fechaFin"] = [str(info[1].day), str(info[1].month), str(info[1].year)]
            current["tiempoInicio"] = [info[0].hour - 5, info[0].minute]
            current["tiempoFin"] = [info[1].hour - 5, info[1].minute]
            current["tiempoReal"] = [*realTime]
            current["eventNum"] = Utils.eventCounter
            Utils.eventCounter += 1
        else:
            current["eventNum"] = Utils.eventCounter
            Utils.eventCounter += 1

        event = readJson("data/dynamic/current_event.json")[0]
        title = "Aventura creada exitosamente!"
        body = " " + event["titulo"]
        pos = (WindowWidth - 400, 0)
        showMessage(Message, "Message", title, body, pos)
        current["eventID"] = current["id"]
        current["id"] = dt.datetime.now().timestamp()
        addToJson("data/dynamic/running_events.json", current)
        addToEventList(current)

    if main.hole != None:
        main.remove_widget(main.hole)
        Disable.value = False
        for child in main.children:
            child.opacity += 0.6
        scroll = join_child(main, "ScrollEventInfo")
        scroll.do_scroll = True
        main.hole = None

def create_adventure():

    eventInfo = join_child(appList().mycon, "EventInfo")

    dateValid = checkEvent(eventInfo)
    resourceValid = validResources()
    
    validDate = validateEventInfo()
    if type(validDate) != bool:
        pos = (WindowWidth - 400, WindowHeight - 140)
        showMessage(Error, "Error", validDate[1], validDate[2], pos, short=True)

    elif type(dateValid) != tuple or type(resourceValid) != list:
        title, body = "No es posible crear la aventura!", ""

        if type(dateValid) != tuple:   
            body = "La fecha introducida no corresponde a un intervalo de tiempo valido, " + dateValid
        else:
            body = "Hay conflictos con los recursos, " + resourceValid

        pos = (WindowWidth - 400, WindowHeight - 200)
        showMessage(Error, "Error", title, body, pos)

    else:
        event = mergeInformation(dateValid, resourceValid)
        response = createEvent(event)
        rawEvent = readJson("data/dynamic/current_event.json")

        if len(rawEvent) == 1:
            addToJson("data/dynamic/current_event.json", event)
        else:
            rawEvent.pop()
            rawEvent.append(event)
            writeJson("data/dynamic/current_event.json", rawEvent)

        if response[0]:
            manageAdventure(True, None, None)
        else:
            title = "Su aventura no puede ser creada en la fecha especificada!"
            body = "La cantidad de uno o varios de los recursos seleccionados excede lo disponible en el inventario. Desea buscar un intervalo de tiempo valido para su aventura?"
            pos = (WindowWidth - 420, WindowHeight - 250)
            main = appList().mycon
            
            Disable.value = True
            Window.set_system_cursor('arrow')
            for child in main.children:
                child.opacity -= 0.6
            scroll = join_child(main, "ScrollEventInfo")
            scroll.do_scroll = False

            main.hole = JoinHole(title, body, response[1], response[2])
            main.add_widget(main.hole)
