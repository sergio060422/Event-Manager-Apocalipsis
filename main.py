from kivy.config import Config
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '768')
from kivy.app import App
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
from configuracion import MainConfig
import json
from kivy.lang import Builder
from kivy.clock import Clock
from confi_info_class import ResourceInfoLayoutP, ResourcesLayoutP

"""
imagen del jugador
"""
class PlayerLayout(BoxLayout):
    def __init__(self):
        super().__init__()
"""
clase de herramientas para usos variados:
get_all: retorna todos los recursos
get_one: retorna el recurso asignado a un id
appList: retorna la lista de componentes existentes en la App
"""
class Utils():
    def get_all():
        with open("recursos.json") as file:
            return json.load(file)
    def get_one(id):
         with open("recursos.json") as file:
            return json.load(file)[id - 1]
    def appList():
        return App.get_running_app()
    rList = []
"""
clase asignado a cada recurso especifico
contiene una foto con la imagen del recurso
"""
class Resource(FloatLayout):
    def __init__(self, item):
        super().__init__()
        self.icon = Image(source=f"assets/{item}.png")
        self.icon.size_hint = (None, None)
        self.icon.size = (60, 60)
        self.icon.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.add_widget(self.icon)
        self.selected = 0
        self.id = item
        Window.bind(mouse_pos=self.on_move)
    
    hovered = 0

    def on_move(self, win, pos):
        menu = Utils.appList().menu
        resource = Utils.get_one(self.id)
        info = menu.rInfo

        if self.collide_point(pos[0], pos[1]):
            info.img_source = f"assets/{self.id}.png"
            info.name = resource["nombre"]
            info.description = resource["descripcion"]
            info.complementary = resource["complementario"][0]

            infotype = ""
                
            for i in range(len(resource["tipo"])):
                infotype += resource["tipo"][i]

                if i < len(resource["tipo"]) - 1:
                    infotype += ", "

            info.type = infotype
            
            comp = ""

            for i in range(len(resource["complementario"])):
                comp += resource["complementario"][i]

                if i < len(resource["complementario"]) - 1:
                    comp += ", "

            info.complementary = comp

            self.hovered = True

            if not self.selected:
                self.opacity = 0.8

            Window.set_system_cursor('hand')  
            info.opacity = 1
        else:
            if self.hovered:
                self.hovered = False
                self.opacity = 1
                Window.set_system_cursor('arrow')

                info.opacity = 0

    my_color = ListProperty([0.1, 0.1, 0.1, 1])
    """
    funcion para la seleccion del evento 
    """
    def add_resource(self):
        recurso = Utils.get_one(self.id)
        with open("recursos_seleccionados.json", "r") as data:
            data = json.load(data)
            data.append(recurso)
            
        with open("recursos_seleccionados.json", "w") as file:
            json.dump(data, file, indent=4)

    def quit_resource(self):
        recurso = Utils.get_one(self.id)
        with open("recursos_seleccionados.json", "r") as data:
            data = json.load(data)
            data.remove(recurso)
            
        with open("recursos_seleccionados.json", "w") as file:
            json.dump(data, file, indent=4)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if not self.selected:
                self.my_color = [0, 0.8, 0.6, 0.8]
                self.selected = 1
                self.opacity = 1
                self.add_resource()              
            else:
                self.my_color = [0.1, 0.1, 0.1, 1]
                self.selected = 0
                self.opacity = 0.8
                self.quit_resource()

"""
componente donde van los recursos
"""
class ResourceList(StackLayout):
    def __init__(self):
        super().__init__()
        self.orientation = 'lr-tb'
        for i in range(1, 25):
            self.add_widget(Resource(i))
    selected = []

"""
componente con la informacion que debe ir dentro del menu de eventos
"""
class ResourceInfoLayout(StackLayout):
    def __init__(self):
        super().__init__()
    
    screen = BooleanProperty(False)
    
    img_source = StringProperty("assets/1.png")
    name = StringProperty("")
    type = StringProperty("")
    description = StringProperty("")
    complementary = StringProperty("")
   
"""
componente contenedor del inventario completo de recursos
"""    
class ResourcesLayout(BoxLayout):
    def __init__(self):
        super().__init__()
        self.add_widget(ResourceList(), index=0)
        self.add_widget(Label(), index=0)
        self.add_widget(ButtonAdvance())
        
"""
contenedor del jugador con su inventario
"""
class ConfigEvent(BoxLayout):
    def __init__(self):
        super().__init__()
        self.add_widget(PlayerLayout())
        self.add_widget(ResourcesLayout())
        
"""
componente contenedor de todo el panel de recursos
"""
class ResourceMenu(FloatLayout):
    def __init__(self):
        super().__init__()
        self.background = Image(source="assets/background_main.png")
        self.add_widget(self.background)
        self.add_widget(ConfigEvent())
        self.rInfo = ResourceInfoLayout()
        self.add_widget(self.rInfo)
    
class ButtonAdvance(ButtonBehavior, Image):
    def __init__(self):
        super().__init__()
        Window.bind(mouse_pos=self.on_move)
    
    hovered = 0

    def on_move(self, win, pos):
        if self.collide_point(pos[0], pos[1]):
            if not self.hovered:
                self.hovered = True
                Window.set_system_cursor('hand')
        else:
            if self.hovered:
                self.hovered = False
                Window.set_system_cursor('arrow')

    def on_press(self):
        screenParent = Utils.appList().screenParent
        Utils.appList().mycon.layo.rlist.update()
        screenParent.current = "config"

class ScreenChild(Screen):
    def __init__(self, nombre, contenido):
        super().__init__()
        self.name = nombre
        self.add_widget(contenido)

class ScreenParent(ScreenManager):
    def __init__(self):
        super().__init__()
        #self.add_widget(ScreenChild("main", Utils.appList().menu))
        self.add_widget(ScreenChild("config", Utils.appList().mycon))
        self.transition = SlideTransition(duration=0.5, direction="left")

"""
cuerpo de la aplicacion
"""
class Main(App):
    def build(self):        
        self.menu = ResourceMenu()
        self.mycon = MainConfig()
        self.screenParent = ScreenParent()
        return self.screenParent

def cleanJSON(*args):
    with open("recursos_seleccionados.json", "w") as file:
        json.dump([], file, indent=4)

Window.bind(on_request_close=cleanJSON)    



Builder.load_file("configuracion.kv")
Builder.load_file("confi_info_class.kv")
Main().run()
