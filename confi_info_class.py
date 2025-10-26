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
import json
from kivy.lang import Builder
from kivy.clock import Clock

class ResourceInfoLayoutP(StackLayout):
    def __init__(self):
        super().__init__()
    
    screen = BooleanProperty(False)
    
    img_source = StringProperty("assets/1.png")
    name = StringProperty("")
    type = StringProperty("")
    description = StringProperty("")
    complementary = StringProperty("")

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

class ResourceP(FloatLayout):
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
        resource = Utils.get_one(self.id)
        info = Utils.appList().mycon.reso

        if self.collide_point(*pos):
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
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if not self.selected:
                self.my_color = [0, 0.8, 0.6, 0.8]
                self.selected = 1
                self.opacity = 1            
            else:
                self.my_color = [0.1, 0.1, 0.1, 1]
                self.selected = 0
                self.opacity = 0.8

class ResourceListP(StackLayout):
    def __init__(self):
        super().__init__()
        self.orientation = 'lr-tb'
        
    def update(self):
        for i in list(self.children):
            self.remove_widget(i)
        
        with open("recursos_seleccionados.json", "r") as file:
            file = json.load(file)
            for i in file:
                self.add_widget(ResourceP(i["id"]))

class ResourcesLayoutP(BoxLayout):
    def __init__(self):
        super().__init__()
        self.rlist = ResourceListP()
        self.add_widget(self.rlist, index=0)
        self.add_widget(Label(), index=0)
