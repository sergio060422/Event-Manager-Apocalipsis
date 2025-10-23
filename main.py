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
from kivy.properties import ListProperty
from kivy.core.window import Window
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty
import json
from kivy.lang import Builder
from kivy.clock import Clock

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
            menu = Utils.appList().menu
            resource = Utils.get_one(self.id)
            """
            condicional para comprobar si el evento esta seleccionado o no
                esta seleccionado:
                    -lo deselecciona cambiando el color del borde y si es el unico evento seleccionado cambia la transparencia(opacity) del menu de evento a 0 (lo hace invisible)
                    -comprueba si el evento que se esta mostrando en el menu de eventos es el mismo que el evento que deseleccione para cambiar la visibilidad de este o no
                si no esta seleccionado:
                    -lo selecciona cambiando el color del borde 
                    -comprueba si el menu de eventos donde debe ir la informacion del evento seleccionado esta activo(es decir si es el primer evento seleccionado)
            """
            if not self.selected:
                self.my_color = [0, 0.8, 0.6, 0.8]
                self.selected = 1
                """
                condicional para comprobar si el menu de eventos no esta activo:
                    -actualiza la informacion con la del evento pulsado 
                    -cambia la transparencia(opacity) a 1 (lo muestra)
                """
                if not EventMenu.active:
                    info = menu.rInfo
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

                    info.opacity = 1
                    self.add_resource()              
            else:
                self.my_color = [0.1, 0.1, 0.1, 1]
                self.selected = 0
                self.quit_resource()
                
                if menu.rInfo.name == resource["nombre"]:
                    menu.rInfo.opacity = 0
                
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
    
    img_source = StringProperty("assets/")
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
        
"""
contenedor del jugador con su inventario
"""
class ConfigEvent(BoxLayout):
    def __init__(self):
        super().__init__()
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.size_hint = (None, None)
        self.size = (700, 500)
        self.orientation = "horizontal"
        self.add_widget(PlayerLayout())
        self.add_widget(ResourcesLayout())
"""
componente que muestra la informacion del evento seleccionado, se situa en la esquina superior izquierda
"""
class EventMenu(FloatLayout):
    def __init__(self):
        super().__init__()
        self.background = Image(source="assets/background_main.png")
        self.add_widget(self.background)
        self.add_widget(ConfigEvent())
        self.rInfo = ResourceInfoLayout()
        self.add_widget(self.rInfo)
    active = 0
"""
cuerpo de la aplicacion
"""
class Main(App):
    def build(self):        
        self.menu = EventMenu()
        return self.menu
        
Main().run()
