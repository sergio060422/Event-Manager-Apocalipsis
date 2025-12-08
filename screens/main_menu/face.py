from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.window import Window
from kivy.uix.screenmanager import SlideTransition
from kivy.lang import Builder
from utilities.utilities import *
from kivy.animation import Animation
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import os, sys, shutil

def on_start(start, touch):
    if start.collide_point(*touch.pos) and not Disable.value:
        screenParent = appList().screenParent
        menu = appList().menu
        nameLabel =  join_child(menu, "PlayerLayout").ids.inputName
        name = appList().mainMenu.name.ids.nameValue
        nameLabel.text = name.text
        CurrentScreen.screen = 0
        transition("main", 0.5, "left")
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
            from utilities.ui_utils import showMessage
            from utilities.ui_utils import Message, Error
            main = appList().mainMenu

            if self.type == "load":    
                path = join_child(main, "FileSelector").selection

                if len(path) > 0:
                    file = readJson(path[0])
                    response = selectFile(file)
                    
                    if not response:
                        title = "¡Error al cargar el archivo!"
                        body = "El archivo que ha intentado cargar no coincide con el formato de aventura o existen conflictos entre las aventuras existentes"
                        pos = (WindowWidth - 390, WindowHeight - 185)
                        showMessage(Error, "Error", title, body, pos, main)
                    else:
                        closeSelector(main)
                        writeJson("data/dynamic/running_events.json", file)                       
                        title = "¡Archivo cargado exitosamente!"
                        body = f"Se cargaron {len(file)} aventuras"
                        pos = (WindowWidth - 390, 0)
                        showMessage(Message, "Message", title, body, pos, main)
            
            if self.type == "save":
                file = os.path.join(os.path.dirname(sys.argv[0]), "data/dynamic/running_events.json")
                dir = os.path.join(join_child(main, "Path").text)
                running = readJson("data/dynamic/running_events.json")

                try:
                    shutil.copy(file, dir)
                except Exception as error:
                    title = "¡Error al guardar el archivo!"
                    body = "Inténtelo de nuevo o compruebe que tenga permiso para copiar archivos en el directorio seleccionado"
                    pos = (WindowWidth - 390, WindowHeight - 185)
                    showMessage(Error, "Error", title, body, pos, main)
                else:
                    title = "¡Archivo guardado exitosamente!"
                    body = f"Se guardaron {len(running)} aventuras" 
                    pos = (WindowWidth - 390, 0)
                    showMessage(Message, "Message", title, body, pos, main)
                    closeSelector(main)

            if self.type == "image":
                main = appList().mycon
                pathImage = join_child(main, "PathImage")
                pathImage.text = self.parent.path.text
                
                try:
                    img = join_child(main, "AdventureImage")
                    img.source = pathImage.text
                except:
                    title = "¡Error al cargar la imagen!"
                    body = "Inténtelo de nuevo y compruebe que la imagen exista y no esté dañada"
                    pos = (WindowWidth - 390, WindowHeight - 185)
                    showMessage(Error, "Error", title, body, pos, main)
                else:
                    title = "Imagen cargada"
                    body = f"Se cargó la imagen correctamente" 
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
        pathLabel = join_child(main, "Path")
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

Builder.load_file("screens/main_menu/styles/face.kv")