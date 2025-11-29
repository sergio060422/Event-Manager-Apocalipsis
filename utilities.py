from kivy.core.window import Window
from kivy.app import App
import json
from kivy.uix.widget import Widget

Places = []
HeightDescription = [0, 108, 130, 108, 86, 130, 108, 108, 86, 86, 130, 108, 130, 108, 130, 108]
WindowWidth, WindowHeight = 1280, 768
danger_words = {
    1: "Pan comido",
    2: "Vigila tus espaldas",
    3: "Huele a peligro",
    4: "Sal corriendo",
    5: "Muerte segura"
}
dg_colors = {
    1: [0.18,0.80,0.44,1], 
    2: [0.60,0.88,0.60,1],  
    3: [1.00,0.82,0.40,1],  
    4: [1.00,0.48,0.27,1],  
    5: [0.90,0.30,0.20,1]  
}

colors = ["#1A1B3A","#20214D","#262760","#2C2D73","#323386",
          "#383999","#3E3FAC","#4445BF","#4A4BD2","#5051E5",
          "#5A4FD9","#644CCF","#6E49C5","#7846BB","#8243B1"]

colors = [
    "#A3C4BC", "#D5E1DF", "#F2D7B6", "#C9BBCF", "#BFD8B8",
    "#E6CFC7", "#C2D4DD", "#F6EAC2", "#D4A5A5", "#B4C6A6",
    "#EAD9D1", "#C3CEDA", "#D7C8B4", "#B8B8D1", "#D0E1D4"
]
colors = [
    "#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F",
    "#EDC948", "#B07AA1", "#FF9DA7", "#9C755F", "#BAB0AC",
    "#6A9FB5", "#F4A259", "#D95F02", "#66A61E", "#E6AB02"
]



class Utils:
    isSelected = False
    isDismiss = True
    eventCounter = 1

class Disable:
    value = False

class CurrentScreen:
    screen = 0
    before = 0

def deleteAll(parent):
    while len(parent.children):
        parent.remove_widget(parent.children[0])

def getPlaces():
    events = readJson("eventos.json")

    for event in events:
        Places.append(event["ubicacion"])

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

def addToJson(src, value):
    data = readJson(src)
    data.append(value)
    writeJson(src, data)

def get_all():
    with open("recursos.json") as file:
        return json.load(file)
    
def get_one(id):
    with open("recursos.json") as file:
        return json.load(file)[id - 1]
    
def appList():
    return App.get_running_app()

def get_active():
    return appList().mycon.active

class finded:
    ans = 0

def join_child(child, joined):
    if child.__class__.__name__ == joined:
        finded.ans = child

    for x in child.children:
        join_child(x, joined)

def deleteChild(parent, child):
    parent.remove_widget(child)

def on_hover(widget, pos, opacity, screen, src, default, cursor, scroll, dropdown):
    if screen != CurrentScreen.screen or Disable.value:
        return
    if dropdown != None and Utils.isDismiss:
        return

    element = appList().mycon.children[0]

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
    
