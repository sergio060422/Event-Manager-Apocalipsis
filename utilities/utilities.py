from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import SlideTransition
import json

Places = set()
HeightDescription = [0, 108, 130, 108, 86, 130, 108, 108, 86, 86, 130, 108, 130, 108, 130, 108, 108, 108, 108]
WindowWidth, WindowHeight = 1280, 768
danger_words = {
    1: "Pan comido",
    2: "Vigila tus espaldas",
    3: "Huele a peligro",
    4: "Sal corriendo",
    5: "Muerte segura"
}

danger_words_inverse = {
    "Pan comido": 1,
    "Vigila tus espaldas": 2,
    "Huele a peligro": 3,
    "Sal corriendo": 4,
    "Muerte segura": 5
}

dg_colors = {
    1: [0.18,0.80,0.44,1], 
    2: [0.60,0.88,0.60,1],  
    3: [1.00,0.82,0.40,1],  
    4: [1.00,0.48,0.27,1],  
    5: [0.90,0.30,0.20,1]  
}

colors = [
    "#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F",
    "#EDC948", "#B07AA1", "#FF9DA7", "#9C755F", "#BAB0AC",
    "#6A9FB5", "#F4A259", "#D95F02", "#66A61E", "#E6AB02",
    "#8E6C8A", "#17BECF", "#BCBD22", "#8A2BE3", "#2A9BE7"
]

def deleteAll(parent):
    while len(parent.children):
        parent.remove_widget(parent.children[0])

def getOneByName(name, src):
    with open(src, 'r') as file:
        for item in json.load(file):
            if item["nombre"] == name:
                return item
    return False

def readJson(src):
    with open(src, 'r') as file:
        return json.load(file)

def writeJson(src, value):
    with open(src, 'w') as file:
        json.dump(value, file, indent=4)

def getPlaces():
    events = readJson("data/static/events.json")

    if not len(Places):
        for event in events:
            Places.add(event["ubicacion"])

def addToJson(src, value):
    data = readJson(src)
    data.append(value)
    writeJson(src, data)

def findMex():
    running = readJson("data/dynamic/running_events.json")
    visited = {}

    for event in running:
        visited[event["eventNum"]] = True
    
    for i in range(1, len(running) + 1):
        vis = visited.get(i, False)

        if not vis:
            return i
    
    return len(running) + 1

def get_all():
    with open("data/static/resources.json") as file:
        return json.load(file)
    
def get_one(id):
    with open("data/static/resources.json") as file:
        return json.load(file)[id - 1]
    
def appList():
    return App.get_running_app()

def get_active():
    return appList().mycon.active

class Success:
    value = 0

class finded:
    ans = 0

class Utils:
    isSelected = False
    isDismiss = True
    spinner = False
    eventCounter = 1
    
    for e in readJson("data/dynamic/running_events.json"):
        eventCounter = max(eventCounter, e["eventNum"] + 1)
    errorHover = False

class Disable:
    value = False

class CurrentScreen:
    screen = 3
    before = 0

class Manage:
    def get_all():
        with open("data/static/events.json") as file:
            return json.load(file)
        
    def get_one(id):
         with open("data/static/events.json") as file:
            return json.load(file)[id]
   
    def get_active():
        return appList().mycon.active

def join_child(child, joined):
    if child.__class__.__name__ == joined:
        finded.ans = child
        return child

    for x in child.children:
        join_child(x, joined)

    if finded.ans != 0:
        return finded.ans

def deleteChild(parent, child):
    parent.remove_widget(child)

def transition(target, duration, direction):
    Window.set_system_cursor("arrow")
    screenParent = appList().screenParent
    screenParent.transition = SlideTransition(duration=duration, direction=direction)
    screenParent.current = target

def on_hover(widget, pos, opacity, screen, src, default, cursor, scroll, dropdown):
    if screen != CurrentScreen.screen or Disable.value:
        return
    
    if dropdown != None and Utils.isDismiss:
        return
  
    if not Utils.isDismiss and cursor == "ibeam":
        return

    if hasattr(widget, "selected") and widget.selected:
        opacity = 1
    
    pos = widget.to_widget(*pos) if scroll else pos
   
    if widget.collide_point(*pos):
        widget.hovered = True
        widget.opacity = opacity
        
        if cursor == None: 
            Window.set_system_cursor('hand')
        else: 
            Window.set_system_cursor(cursor)
        if src != None: 
            widget.source = src
        if dropdown != None:
            widget.bg_color = [0.2, 0.2, 0.2, 1]

    elif not widget.collide_point(*pos) and widget.hovered:
        widget.hovered = False
        widget.opacity = 1
        Window.set_system_cursor('arrow')

        if src != None:
            widget.source = default
        if dropdown != None:
            widget.bg_color = [0.18, 0.18, 0.18, 1]

def setup_hover(widget, flag, opacity=0.9, src=None, default=None, cursor=None, scroll=False, dropdown=None):
    l = lambda win, pos: on_hover(widget, pos, opacity, flag, src, default, cursor, scroll, dropdown)

    Window.bind(mouse_pos=l)

    return l
    