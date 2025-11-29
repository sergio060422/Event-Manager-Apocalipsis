from kivy.config import Config
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.widget import Canvas
from kivy.uix.stacklayout import StackLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ListProperty
from kivy.core.window import Window
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
import json
from confi_info_class import ResourcesLayoutP, ResourceInfoLayoutP, ResourceP
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from utilities import *
from kivy.uix.scrollview import ScrollView
from calendar_widget import TotalCalendar, getCalendar
from kivy.factory import Factory
from kivy.uix.button import Button
from event_manager import *
from error import *
from kivy.animation import Animation
from utilities import *

class Manage:
    def get_all():
        with open("eventos.json") as file:
            return json.load(file)
        
    def get_one(id):
         with open("eventos.json") as file:
            return json.load(file)[id]
   
    def get_active():
        return appList().mycon.active

class Event(FloatLayout):
    def __init__(self, index, selector):
        super().__init__()
        self.index = index
        self.selector = selector
        self.hover = setup_hover(self, 1, 1, scroll=True, dropdown=self)

    title = StringProperty("")
    bg_color = ListProperty([0.18, 0.18, 0.18, 1])
    hovered = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not Disable.value:
            self.selector.select(self.title)
            self.selector.caller.icon = "assets/minus.png"
            self.selector.evinfo.update(self.index)

class Selector(DropDown):
    def __init__(self, caller, evinfo):
        super().__init__()
        self.max_height = 400
        self.bind(on_select=self.selection)
        self.caller = caller
        self.evinfo = evinfo
        
        for i in range(15):
            e = Event(i, self)
            e.title = Manage.get_one(i)["titulo"]
            self.add_widget(e)
    
    def selection(self, option, value):
        setattr(self.caller, 'name', value)                

def showAnimation(parent, y_val):
    anima1 = Animation(x=0, y=y_val, duration=0.4, t='out_quad')
    anima1.start(parent)

class FloatContainer(FloatLayout):
    def __init__(self, child):
        super().__init__()
        self.add_widget(Show())
        self.add_widget(child)
        self.status = False
        
def configShowAnimation(parent, pos):
    command = parent.command
    c1 = command.children[0]
    c2 = command.children[1]

    if c1.collide_point(*pos) or c2.collide_point(*pos):
        if not command.status:
            showAnimation(command, 100)
            command.status = True
    elif command.status:
        showAnimation(command, 0)
        command.status = False     

class SelectorCaller(FloatLayout):
    def __init__(self):
        super().__init__()
        setup_hover(self, 1)
        Window.bind(mouse_pos=lambda win, pos: self.close(pos))

    def close(self, pos):
        if Disable.value:
            return

        x1, x2 = self.x, self.x + 450

        if pos[0] < x1 or pos[0] > x2:
            self.selector.dismiss()

        if pos[1] > 570 or pos[1] < 130:
            self.selector.dismiss()

        configShowAnimation(appList().mycon, pos)
        configShowAnimation(appList().menu, pos)
        

    def set_bind(self):
        self.selector.bind(on_dismiss=self.change_icon)

    hovered = False
    name = StringProperty(Manage.get_one(0)["titulo"])
    selector = None
    icon = StringProperty("assets/minus.png")

    def change_icon(self, *args):
        self.icon = "assets/minus.png"
        Utils.isDismiss = True

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not Disable.value:
            self.selector.open(self)
            self.icon = "assets/plus.png"
            Utils.isDismiss = False

class NeedResources(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = (30, 0, 30, 0)

Factory.register('NeedResources', cls=NeedResources)

class DateIniButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        setup_hover(self, 1, scroll=True)

    hovered = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and (appList().mycon.children[0].__class__.__name__ != "TotalCalendar") and not Disable.value:
            appList().mycon.add_widget(TotalCalendar(0))
            
      
Factory.register('DateIniButton', DateIniButton)

class DateEndButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        setup_hover(self, 1, scroll=True)
    
    hovered = False
        
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and (appList().mycon.children[0].__class__.__name__ != "TotalCalendar") and not Disable.value:
            appList().mycon.add_widget(TotalCalendar(1))
            
Factory.register('DateEndButton', DateEndButton)

class Date(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "None"

Factory.register('Date', Date)

class TimeInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (1, 1, 1, 0.9)
        setup_hover(self, 1, cursor="ibeam", scroll=True)
    
    hovered = False

    def keyboard_on_textinput(self, window, text):
        try:
            a = int(text)
        except:
            pass
        else: 
            if len(self.text) < 2:
                self.text += text
            elif len(self.text) == 2:
                minu = self.parent.parent.timeIni[1] if self.name == "ini" else self.parent.parent.timeEnd[1]
                self.focus = False
                minu.focus = True
        

Factory.register('Time', TimeInput)

def getSize(widget, target):
    ans = 0

    for child in widget.children:
        if child != target:
            ans += child.height
    
    return ans

class AddNeedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        setup_hover(self, 1, scroll=True)
    
    hovered = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not Disable.value:
            e = Manage.get_one(self.parent.current)
            setEvent(e)
            
            for x in e["necesita"]:
                recurso = get_one(x)
        
                with open("recursos_seleccionados_event.json", "r") as data:
                    data = json.load(data)

                ignore = False

                for i in data:
                    if i["id"] == recurso["id"]:
                        ignore = True             

                if ignore:
                    continue

                with open("recursos_seleccionados_event.json", "w") as file:
                    data.append(recurso)
                    json.dump(data, file, indent=4)
            
            join_child(appList().mycon, "ResourceListP")
            finded.ans.update("recursos_seleccionados_event.json")
        
                
    hovered = False

Factory.register('AddNeedButton', AddNeedButton)        

class EventInfo(BoxLayout):
    def __init__(self):
        super().__init__()
        self.orientation = "vertical"
        self.need = self.ids.need
        self.timeIni = (self.ids.hourIni, self.ids.minuIni)
        self.timeEnd = (self.ids.hourEnd, self.ids.minuEnd)
        self.dateIni = self.ids.dateini
        self.dateEnd = self.ids.datend
        self.current = 0

    img = StringProperty("")
    type = StringProperty("")
    danger = StringProperty("")
    danger_color = ListProperty([0, 0, 0, 0])
    place = StringProperty("")

    danger_words = {
        1: "Pan comido",
        2: "Vigila tus espaldas",
        3: "Huele a peligro",
        4: "Sal corriendo",
        5: "Muerte segura"
    }
    def update(self, i):
        e = Manage.get_one(i)
        setEvent(e)
        self.current = i

        for x in list(self.need.children):
            self.need.remove_widget(x)

        val = 0
        for x in e["necesita"]:
            resource = ResourceP(x, False, False)
            resource.my_color = [0.5, 0.5, 0.5, 1]
            resource.icon.size = (50, 50)
            resource.on_move = None
            resource.on_touch_down = lambda x: None
            self.need.add_widget(resource)

        self.need.height = ((len(e["necesita"]) // 6) + (1 and (len(e["necesita"]) % 6 != 0))) * 65
        self.ids.description.text = e["descripcion"]
        self.img = f"assets/event_images/{i + 1}.png"
        self.type = ""
        
        for i in e["tipo"]:
            if i == "Defensa":
                self.type += "• ⛨ Defensa \n"
            if i == "Refugio":
                self.type += "• 🏠Refugio \n"
            if i == "Supervivencia":
                self.type += "• 🏕️ Supervivencia \n"

        dg = e["peligro"]
        self.danger = "-" + danger_words[dg] + "-"
        self.danger_color = dg_colors[dg]
        self.place = "• " + e["ubicacion"]
        self.height = 500 + self.need.height + HeightDescription[e["id"]] + 75

    def updateIni(self, value):
        self.dateIni.text = value

    def updateEnd(self, value):
        self.dateEnd.text = value

class ScrollEventInfo(ScrollView):
    def __init__(self):
        super().__init__()
        self.evinfo = EventInfo()
        self.add_widget(self.evinfo)
       
class EventHandler(BoxLayout):
    def __init__(self):
        super().__init__()
        self.scevinfo = ScrollEventInfo()
        self.scevinfo.evinfo.update(0)
        self.selcal = SelectorCaller()
        self.selcal.selector = Selector(self.selcal, self.scevinfo.evinfo)
        self.selcal.set_bind()
        self.add_widget(self.selcal, index=0)
        self.add_widget(self.scevinfo, index=0)
       
        
class Backpack(StackLayout):
    def __init__(self):
        super().__init__()

class ConfiEvent(BoxLayout):
    def __init__(self):
        super().__init__()
        self.eventHandler = EventHandler()
        self.add_widget(self.eventHandler)
        self.layo = ResourcesLayoutP()
        self.add_widget(self.layo)

class Backbutton(ButtonBehavior, Image):
    def __init__(self):
        super().__init__()
        self.source = "assets/backbutton.png"
        self.size_hint = (None, None)
        self.width = 150
        self.pos_hint = {'x': 0.02, 'top': 0.99}
        setup_hover(self, 1)
    
    hovered = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not Disable.value:
            CurrentScreen.screen = 0
            screenParent = appList().screenParent
            screenParent.current = "main"
            screenParent.transition = SlideTransition(duration=0.5, direction="left")

class Show(ButtonBehavior, Image):
    def __init__(self):
        super().__init__()
        setup_hover(self, 1, 1)
        self.source = "assets/plus.png"
    
    hovered = False

class CommandAdventure(BoxLayout):
    def __init__(self):
        super().__init__()
        self.status = False
        self.add_widget(ListAdventures())
        self.add_widget(AdventureButton())
 

class ListAdventures(ButtonBehavior, Image):
    def __init__(self):
        super().__init__()
        self.source = "assets/listAdventure.png"
        setup_hover(self, 1)

    hovered = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            apps = appList()
            apps.events.scrollList.running.update()
            writeJson("recursos_seleccionados_event.json", [])

            screenParent = appList().screenParent
            CurrentScreen.before = (CurrentScreen.screen, screenParent.current)
            CurrentScreen.screen = 2
            Window.set_system_cursor("arrow")
            apps.mycon.layo.rlist.update("recursos_seleccionados.json")
            screenParent.transition = SlideTransition(duration=0.5, direction="down")
            screenParent.current = "events"

class AdventureButton(ButtonBehavior, Image):
    def __init__(self):
        super().__init__()
        self.source = "assets/adventure.png"
        setup_hover(self, 1)

    hovered = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not Disable.value:
            join_child(appList().mycon, "EventInfo")
            eventInfo = finded.ans
    
            dateIni = eventInfo.dateIni.text
            dateEnd = eventInfo.dateEnd.text
            timeIni = (eventInfo.timeIni[0].text, eventInfo.timeIni[1].text)
            timeEnd = (eventInfo.timeEnd[0].text, eventInfo.timeEnd[1].text)
            dateValid = validDate(dateIni, dateEnd, timeIni, timeEnd)
            resourceValid = validResources()
           
            if type(dateValid) != tuple or type(resourceValid) != list:
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
                rawEvent = readJson("current_event.json")

                if len(rawEvent) == 1:
                    addToJson("current_event.json", event)

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
                    join_child(main, "ScrollEventInfo")
                    finded.ans.do_scroll = False

                    main.hole = JoinHole(title, body, response[1], response[2])
                    main.add_widget(main.hole)

def addToEventList(event):
    running = appList().events.scrollList.running
    
    from events import RunningEvent

    running.add_widget(RunningEvent(event))

def manageAdventure(response, info, realTime):
    main = appList().mycon
    
    if response:
        current = readJson("current_event.json")[1]
        running = readJson("running_events.json") 

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

        event = readJson("current_event.json")[0]
        title = "Aventura creada exitosamente!"
        body = " " + event["titulo"]
        pos = (WindowWidth - 400, 0)
        showMessage(Message, "Message", title, body, pos)
        current["eventID"] = current["id"]
        current["id"] = dt.datetime.now().timestamp()
        addToJson("running_events.json", current)
        addToEventList(current)

    if main.hole != None:
        main.remove_widget(main.hole)
        Disable.value = False
        for child in main.children:
            child.opacity += 0.6
        join_child(main, "ScrollEventInfo")
        finded.ans.do_scroll = True
        main.hole = None

class Success:
    value = 0

def showMessage(classMessage, name, title, body, position):
    mainConfig = appList().mycon

    if mainConfig.children[0].__class__.__name__ == name and name != "Message":
        deleteChild(mainConfig, mainConfig.children[0])
    elif mainConfig.children[0].__class__.__name__ == name:
        position = (position[0], position[1] + Success.value * 95)
    
    Success.value += (name == "Message")

    message = classMessage(title, body)

    message.opacity = 1
    message.pos = position
    mainConfig.add_widget(message)
    DisolveAnimation(mainConfig, message, 4, 0, 2, name == "Message") 


def DisolveAnimation(parent, widget, duration, opacity, delay, flag=False):
    animaDelay = Animation(duration=delay)
    anima = Animation(opacity=opacity, duration=duration)
    sequence = animaDelay + anima
    sequence.on_complete = lambda widget: CompleteAnimation(parent, widget, flag) 
    sequence.start(widget)

def CompleteAnimation(parent, widget, flag):
    deleteChild(parent, widget)
    Success.value = 0

class MainConfig(FloatLayout):
    def __init__(self):
        super().__init__()
        self.hole = None
        self.img = Image(source="assets/background_config.png")
        self.add_widget(self.img)
        self.backbutton = Backbutton()
        self.add_widget(self.backbutton)
        self.cefi = ConfiEvent()
        self.add_widget(self.cefi)
        self.reso = ResourceInfoLayoutP()
        self.layo = self.cefi.layo
        self.add_widget(self.reso)
        self.command = FloatContainer(CommandAdventure())
        self.add_widget(self.command)
       