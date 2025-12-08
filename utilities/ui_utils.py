from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.lang import Builder
from utilities import *
from kivy.factory import Factory
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from utilities.utilities import * 
from kivy.animation import Animation

Builder.load_file("utilities/styles/ui_utils.kv")

def sortEvents(eventList):
    running = readJson("data/dynamic/running_events.json")
    pairList = []

    for e in running:
        pairList.append([e["eventNum"], e])

    pairList.sort(key=lambda item: item[0])
    ordered = [x[1] for x in pairList]
    eventList.update(True, ordered)

   

def DisolveAnimation(parent, widget, duration, opacity, delay, flag=False):
    animaDelay = Animation(duration=delay)
    anima = Animation(opacity=opacity, duration=duration)
    sequence = animaDelay + anima
    sequence.on_complete = lambda widget: CompleteAnimation(parent, widget, flag) 
    sequence.start(widget)

def CompleteAnimation(parent, widget, flag):
    deleteChild(parent, widget)
    Success.value = 0

def showMessage(classMessage, name, title, body, position, alter=None, short=False):
    mainConfig = appList().mycon if alter == None else alter

    if mainConfig.children[0].__class__.__name__ == name and name != "Message":
        deleteChild(mainConfig, mainConfig.children[0])
    elif mainConfig.children[0].__class__.__name__ == name:
        position = (position[0], position[1] + Success.value * 95)
    
    Success.value += (name == "Message")

    message = classMessage(title, body)

    if short:
        message.height = 140
  
    message.opacity = 1
    message.pos = position
    mainConfig.add_widget(message)
    DisolveAnimation(mainConfig, message, 4, 0, 2, name == "Message") 

def showAnimation(parent, y_val):
    anima1 = Animation(x=0, y=y_val, duration=0.4, t='out_quad')
    anima1.start(parent)
    
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

class Error(Popup):
    def __init__(self, title, text):
        super().__init__()
        self.title = title
        self.title_size = 24
        self.size_hint = (None, None)
        self.size = (400, 190)
        child = join_child(self.children[0].children[0], "Label")
        child.text = text
    
    def on_touch_down(self, touch):
        self.dismiss = True

class Message(Error):
    def __init__(self, title, text):
        super().__init__(title, text)
        self.size_hint = (None, None)
        self.size = (400, 100)
        self.title_size = 22

class ButtonSet(BoxLayout):
    def __init__(self, info, realTime):
        super().__init__()
        self.add_widget(DeniedJoinHole())
        self.add_widget(AceptJoinHole(info, realTime))

def getConfig():
    from core.event_creation import manageAdventure
    return manageAdventure

def errorHover(widget, pos):
    if Utils.errorHover:    
        if widget.collide_point(*pos):
            widget.hovered = True
            widget.opacity = 0.9
            Window.set_system_cursor('hand')

        elif not widget.collide_point(*pos) and widget.hovered:
            widget.hovered = False
            widget.opacity = 1
            Window.set_system_cursor('arrow')

class AceptJoinHole(Button):
    def __init__(self, info, realTime):
        super().__init__()
        self.info = info
        self.realTime = realTime
        Utils.errorHover = True
        Window.bind(mouse_pos=lambda win, pos: errorHover(self, pos))
    
    hovered = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            Utils.errorHover = False
            
            manageAdventure = getConfig()
            manageAdventure(True, self.info, self.realTime)

class DeniedJoinHole(Button):
    def __init__(self):
        super().__init__()
        Window.bind(mouse_pos=lambda win, pos: errorHover(self, pos))
    
    hovered = False
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            Utils.errorHover = False
            manageAdventure = getConfig()
            manageAdventure(False, None, None)

class TitleHole(Label):
    def __init__(self, content):
        super().__init__(text=content)

class BodyHole(Label):
    def __init__(self, content):
        super().__init__(text=content)
            
class JoinHole(BoxLayout):
    def __init__(self, title, body, info, realTime):
        super().__init__()
        self.add_widget(TitleHole(title))
        self.add_widget(BodyHole(body))
        self.add_widget(ButtonSet(info, realTime))

Factory.register('Error', Error)