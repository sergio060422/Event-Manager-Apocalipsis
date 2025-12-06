from kivy.uix.label import Label
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
from configuracion import MainConfig, Show, showAnimation, CommandAdventure, FloatContainer, ListAdventures
import json
from kivy.lang import Builder
from kivy.clock import Clock
from confi_info_class import ResourceInfoLayoutP, ResourcesLayoutP, ResourceP
from utilities import *
from calendar_widget import TotalCalendar
from events import MainEventContainter
from kivy.animation import Animation
from kivy.uix.filechooser import FileChooserIconView, FileChooserLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import os, sys, shutil

kv = '''
<Menu>:
    canvas.before:
        Color:
            rgba: 0.07, 0.07, 0.07, 0.85
        RoundedRectangle:
            pos: self.pos
            size: self.size
    canvas.after:
        Color:
            rgba: 1, 1, 1, 1
        Line:
            rounded_rectangle: (self.x, self.y, self.width, self.height, 8)
            width: 1.5
        
    size_hint: None, None
    size: (400, 450)
    pos_hint: {'center_x':  0.75, 'center_y': 0.5}
    orientation: "vertical"

<Option>:
    size_hint: None, None
    width: 250
    pos_hint: {'center_x': 0.5, 'y': 0}

<FileSelectorWindow>:
    size_hint: None, None
    size: (900, 600)
    orientation: "vertical"
    pos_hint: {'center_x': .5, 'center_y': .5}
    canvas.before:
        Color:
            rgba: 0.12, 0.12, 0.12, 0.95
        Rectangle:
            pos: self.pos
            size: self.size
<Title>:
    canvas.after:
        Color:
            rgba: 1, 1, 1, 1
        Line:
            points: (self.x, self.y, self.x + 900, self.y)
            width: 1.2
    canvas.before:
        Color:
            rgba: 0.07, 0.07, 0.07, 0.9
        Rectangle:
            pos: self.pos
            size: (900, 50)
    padding: 10
    font_size: 32
    size_hint: None, None
    size: self.texture_size
    font_name: 'fonts/Roboto,Roboto_Condensed/Roboto_Condensed/RobotoCondensed-VariableFont_wght.ttf'
    size_hint_y: None
    height: 50

<Path>:
    size_hint: None, None
    font_size: 15
    size: (400, 30)
    text_size: (400, 30)
    pos_hint: {'x': 0, 'center_y': .5}
    foreground_color: (1, 1, 1, 1)
    background_color: (0.12, 0.12, 0.12, 1)
    padding: 6
    canvas.after:
        Color:
            rgba: 1, 1, 1, 1
        Line:
            rounded_rectangle: (self.x, self.y, self.width, self.height, 12)
            width: 1.01

<BottomBar>:
    padding: 10
    size_hint_y: None
    height: 60
    spacing: 10

<SelectionButton>:
    background_color: 0, 0, 0, 0
    markup: True
    text: "[b] Seleccionar! [/b]"
    size_hint: None, None
    height: 36
    pos_hint: {'x': 0, 'center_y': .5}
    canvas.before:
        Color:
            rgba: 0.12, 0.12, 0.12, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [12]
    canvas.after:
        Color:
            rgba: 1, 1, 1, 1
        Line:
            rounded_rectangle: (self.x, self.y, self.width, self.height, 8)
            width: 1.01

            
<NameContainer>:
    size_hint: None, None
    pos_hint: {'x': 0, 'y': 0}
    width: 300
    padding: 10
    orientation: "vertical"
    spacing: 8

    Label:
        size_hint: None, None
        size: self.texture_size
        text: "Te llamabas:"
        font_size: 28
        font_name: 'fonts/Roboto,Roboto_Condensed/Roboto_Condensed/RobotoCondensed-VariableFont_wght.ttf'
        
    NameInput:
        id: nameValue
        background_color: 0, 0, 0, 0
        cursor_color: 1, 1, 1, 1
        foreground_color: 1, 1, 1, 1
        size_hint_y: None
        height: 36
        font_size: 18
        hovered: False
        hint_text: "Elige un nombre"
        multiline: False
        canvas.after:
            Color: 
                rgba: 1, 1, 1, 1
            Line:
                points: (self.x, self.y + 4, 200, self.y + 4)
                width: 1
        
    Label:
        index: 0
'''

Builder.load_string(kv)

def on_start(start, touch):
    if start.collide_point(*touch.pos) and not Disable.value:
        screenParent = appList().screenParent
        Window.set_system_cursor('arrow')
        menu = appList().menu
        join_child(menu, "PlayerLayout")
        nameLabel = finded.ans.ids.inputName
        name = appList().mainMenu.name.ids.nameValue
        nameLabel.text = name.text
        CurrentScreen.screen = 0
        screenParent.current = "main"
        screenParent.transition = SlideTransition(duration=0.5, direction="right")

class Path(Label):
    def __init__(self):
        super().__init__()
       
def to_close(main, touch):
    selector = main.fileSelector
    
    if selector != None and not selector.collide_point(*touch.pos):
        closeSelector(main)

class SelectionButton(Button):
    def __init__(self, type):
        super().__init__()
        setup_hover(self, 3)
        self.type = type
    
    hovered = False

    def on_touch_down(self, touch):
        to_close(appList().mycon, touch)
        to_close(appList().mainMenu, touch)

        if self.collide_point(*touch.pos):
            from configuracion import showMessage
            from error import Message, Error
            main = appList().mainMenu

            if self.type == "load":    
                join_child(main, "FileSelector")
                path = finded.ans.selection

                if len(path) > 0:
                    file = readJson(path[0])
                    response = selectFile(file)
                    
                    if not response:
                        title = "Error al cargar el archivo!"
                        body = "El archivo que ha intentado cargar no coincide con el formato de aventura u existen conflictos entre las aventuras existentes"
                        pos = (WindowWidth - 390, WindowHeight - 185)
                        showMessage(Error, "Error", title, body, pos, main)
                    else:
                        closeSelector(main)
                        writeJson("running_events.json", file)                       
                        title = "Archivo cargado exitosamente!"
                        body = f"Se cargaron {len(file)} aventuras"
                        pos = (WindowWidth - 390, 0)
                        showMessage(Message, "Message", title, body, pos, main)
            
            if self.type == "save":
                file = os.path.join(os.path.dirname(sys.argv[0]), "running_events.json")
                join_child(main, "Path")
                dir = os.path.join(finded.ans.text)
                running = readJson("running_events.json")

                try:
                    shutil.copy(file, dir)
                except Exception as error:
                    title = "Error al guardar el archivo!"
                    body = "Intentelo de nuevo y compruebe que tenga permiso para copiar archivos en el directorio seleccionado"
                    pos = (WindowWidth - 390, WindowHeight - 185)
                    showMessage(Error, "Error", title, body, pos, main)
                else:
                    title = "Archivo guardado exitosamente!"
                    body = f"Se guardaron {len(running)} aventuras" 
                    pos = (WindowWidth - 390, 0)
                    showMessage(Message, "Message", title, body, pos, main)
                    closeSelector(main)

            if self.type == "image":
                main = appList().mycon
                join_child(main, "PathImage")
                pathImage = finded.ans
                pathImage.text = self.parent.path.text
                
                try:
                    join_child(main, "AdventureImage")
                    img = finded.ans
                    img.source = pathImage.text
                except:
                    title = "Error al cargar la imagen!"
                    body = "Intentelo de nuevo y compruebe que la imagen no este danada"
                    pos = (WindowWidth - 390, WindowHeight - 185)
                    showMessage(Error, "Error", title, body, pos, main)
                else:
                    title = "Imagen cargada"
                    body = f"Se cargo la imagen correctamente" 
                    pos = (WindowWidth - 390, 0)
                    showMessage(Message, "Message", title, body, pos, main)
                    closeSelector(main)

class BottomBar(BoxLayout):
    def __init__(self, type):
        super().__init__()
        self.add_widget(Label())
        self.path = Path()
        self.add_widget(self.path)
        self.add_widget(SelectionButton(type))

class Title(Label):
    def __init__(self, type):
        super().__init__()
        
        if type == "load":
            self.text = "Seleccione el archivo JSON"
        if type == "save":
            self.text = "Seleccione el directorio donde guardar su archivo"
        if type == "image":
            self.text = "Seleccione la imagen de su aventura"

def selectFile(selected):
    eventList = appList().events.scrollList.running
    return eventList.update(True, selected)

class FileSelector(FileChooserIconView):
    def __init__(self, type):
        super().__init__()
        self.path = '.'
        if type == "load":
            self.filters = ['*.json']
        if type == "save":
            self.filters = ["/"]
        if type == "image":
            self.filters = ["*.png", "*.jpg"]
        self.multiselect = False
        self.type = type
        self.bind(path=self.update_path)
        
        if type != "saves":
            self.bind(selection=self.update_path)
        
    def update_path(self, *args):
        main = appList().mainMenu if self.type != "image" else appList().mycon
        join_child(main, "Path")
        pathLabel = finded.ans
        if type(pathLabel) != int:
            pathLabel.text = self.path if len(self.selection) == 0 else self.selection[0]
        
class FileSelectorWindow(BoxLayout):
    def __init__(self, type):
        super().__init__()
        self.type = type
        self.add_widget(Title(type))
        self.add_widget(FileSelector(type))
        self.add_widget(BottomBar(type))

def openSelector(main, type):
    Disable.value = True
    Window.set_system_cursor('arrow')
    main.fileSelector = FileSelectorWindow(type)
    main.add_widget(main.fileSelector)

def closeSelector(main):
    Disable.value = False
    Window.set_system_cursor('arrow')
    main.remove_widget(main.fileSelector)
    main.fileSelector = None
    
def on_press(button, touch, type):        
    if button.collide_point(*touch.pos) and not Disable.value:
        main = appList().mainMenu
        openSelector(main, type)

def close_program(exit, touch):
    if exit.collide_point(*touch.pos):
        App.get_running_app().stop()

class Option(ButtonBehavior, Image):
    def __init__(self, src, delay):
        super().__init__()
        self.opacity = 0
        self.source = f"assets/{src}"
        InitAnimation(self, delay)
        setup_hover(self, 3, 0.8)

        if src == "start.png":
            self.on_touch_down = lambda touch: on_start(self, touch)
        if src == "load.png":
            self.on_touch_down = lambda touch: on_press(self, touch, "load")
        if src == "save.png":
            self.on_touch_down = lambda touch: on_press(self, touch, "save")
        if src == "exit.png":
            self.on_touch_down = lambda touch: close_program(self, touch)

    hovered = False

def InitAnimation(widget, delay):
    anima = Animation(opacity=1, duration=0.75)
    delay = Animation(opacity=0, duration=delay)
    seq = delay + anima
    seq.start(widget)

class NameInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        setup_hover(self, 3, cursor="ibeam")

    def keyboard_on_textinput(self, window, text): 
        if len(self.text) < 16:
            self.text += text

class NameContainer(BoxLayout):
    def __init__(self):
        super().__init__()
        
class Menu(BoxLayout):
    def __init__(self):
        super().__init__()
        self.add_widget(Option("start.png", 0.25))
        self.add_widget(Option("load.png", 0.45))
        self.add_widget(Option("save.png", 0.65))
        self.add_widget(Option("exit.png", 0.85))
        self.add_widget(Label(
            size_hint_y = None,
            height = 25
        ))

class Container(FloatLayout):
    def __init__(self):
        super().__init__()
        self.background = Image(source="assets/background_face.png")
        self.add_widget(self.background)
        self.add_widget(Menu())
        self.name = NameContainer()
        self.add_widget(self.name)

    fileSelector = None

