from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.lang import Builder
from utilities import *
from kivy.factory import Factory
from kivy.uix.button import Button
from kivy.uix.popup import Popup

kv = '''
<Error>:
    opacity: 0
    Label:
        id: errorText
        multiline: True
        text_size: 370, None
        color: 1, 1, 1, 0.8
        size_hint: None, None
        size: self.texture_size
        pos_hint: {'x': 0.05, 'top': 0.95}
        font_size: 20

<JoinHole>:
    orientation: "vertical"
    size_hint: None, None
    size: (410, 250)
    pos_hint: {'center_x': .5, 'center_y': .5}
    padding: 16
    spacing: 12
    canvas.before:
        Color:
            rgba: (0.07, 0.07, 0.07, 1)
        Rectangle:
            pos: self.pos
            size: self.size

           
<AceptJoinButton>:
    size_hint: None, None
    size: (90, 35)
    font_size: 24

<AceptJoinHole>:
    background_color: 0, 0, 0, 0
    markup: True
    text: "[b] Hazlo! [/b]"
    canvas.before:
        Color:
            rgba: 0.12, 0.12, 0.12, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [12]
    canvas.after:
        Color:
            rgba: 0.137, 0.525, 0.212, 1
        Line:
            rounded_rectangle: (self.x, self.y, self.width, self.height, 8)
            width: 1.01
    
<DeniedJoinHole>:
    background_color: 0, 0, 0, 0
    markup: True
    text: "[b] Cancelar [/b]"
    canvas.before:
        Color:
            rgba: 0.12, 0.12, 0.12, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [12]
    canvas.after:
        Color:
            rgba: 0.980, 0.169, 0.133, 1
        Line:
            rounded_rectangle: (self.x, self.y, self.width, self.height, 8)
            width: 1.01 

<ButtonSet>:
    size_hint: None, None
    size: (180, 40)
    pos_hint: {'right': 1, 'y': 0}
    spacing: 5

<TitleHole>:
    font_size: 24
    size_hint: None, None
    multiline: True
    text_size: 400, None
    size: self.texture_size

    canvas.after:
        Color:
            rgba: 0.9, 0.9, 0.9, 0.9
        Line:
            points: (self.x + 4, self.y - 4, self.x + self.width - 24, self.y - 4)
            width: 1.5
    
<BodyHole>:
    multiline: True
    text_size: 400, None
    color: 1, 1, 1, 0.8
    size_hint: None, None
    size: self.texture_size
    font_size: 20
    
'''

Builder.load_string(kv)

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
    from configuracion import manageAdventure
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