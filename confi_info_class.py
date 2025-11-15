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
from utilities import *
from kivy.uix.textinput import TextInput

class ResourceInfoLayoutP(StackLayout):
    def __init__(self):
        super().__init__()
    
    screen = BooleanProperty(False)
    
    img_source = StringProperty("assets/1.png")
    name = StringProperty("")
    type = StringProperty("")
    cuantity = StringProperty("")
    description = StringProperty("")
    complementary = StringProperty("")
    exclude = StringProperty("")

class CuantitySelector(TextInput):
    def __init__(self):
        super().__init__()
        self.size_hint = (None, None)
        self.size = (22, 20)
        self.pos_hint = {'center_x': 0.84, 'center_y': 0.15}
        self.foreground_color = (1, 1, 1, 1)
        self.font_size = 16
        self.background_color = (0, 0, 0, 0.5)
        self.padding = 0
        self.cursor_color = (1, 1, 1, 1)
        self.multiline = False

    def keyboard_on_textinput(self, window, text):
        try:
            a = int(text)
        except:
            pass
        else: 
            if len(self.text) < 2:
                self.text += text
  
class ResourceP(FloatLayout):
    def __init__(self, item, cuantiable, hoverable=True):
        super().__init__()
        self.icon = Image(source=f"assets/{item}.png")
        self.icon.size_hint = (None, None)
        self.icon.size = (60, 60)
        self.icon.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.add_widget(self.icon)
        self.selected = 0
        self.id = item
        self.cuantity = CuantitySelector()
        self.cuantity.text = "01"
        self.add_widget(self.cuantity)
        Window.bind(mouse_pos=self.on_move)
        if hoverable:
            self.on_hover = setup_hover(self, 1, 0.8)
        if not cuantiable:
            self.cuantity.opacity = 0
    
    hovered = False

    def on_move(self, win, pos):  
        if CurrentScreen.screen != 1:
            return
        
        resource = get_one(self.id)
        info = appList().mycon.reso

        if self.collide_point(*pos):
            self.cuantity.focus = True
            info.img_source = f"assets/{self.id}.png"
            info.name = resource["nombre"]
            info.cuantity = str(resource["cantidad"])
            info.description = resource["descripcion"]
            info.complementary = resource["complementario"][0]
            info.exclude = resource["excluyente"][0]
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
            
            calendar = appList().mycon.children[0]

            if not calendar.collide_point(*pos):
                info.opacity = 1
        else:
            if self.hovered:
                info.opacity = 0
                self.cuantity.focus = False
                text = self.cuantity.text

                if len(text) == 0 or int(text) == 0:
                    self.cuantity.text = "01"
                elif len(text) < 2:
                    self.cuantity.text = "0" + text



    my_color = ListProperty([0.1, 0.1, 0.1, 1])
    
    def add_resource(self):
        recurso = get_one(self.id)
        with open("recursos_seleccionados_event.json", "r") as data:
            data = json.load(data)
            data.append(recurso)

        with open("recursos_seleccionados_event.json", "w") as file:
            json.dump(data, file, indent=4)
            
    def quit_resource(self):
        recurso = get_one(self.id)
        with open("recursos_seleccionados_event.json", "r") as data:
            data = json.load(data)
            data.remove(recurso)
            
        with open("recursos_seleccionados_event.json", "w") as file:
            json.dump(data, file, indent=4)

    def on_touch_down(self, touch):
        if CurrentScreen.screen != 1:
            return
    
        if self.collide_point(*touch.pos):
            if not self.selected:
                self.my_color = [0, 0.8, 0.6, 0.8]
                self.selected = 1
                self.opacity = 1
                self.quit_resource()         
            else:
                self.my_color = [0.1, 0.1, 0.1, 1]
                self.selected = 0
                self.opacity = 0.8
                self.add_resource()


class ResourceListP(StackLayout):
    def __init__(self):
        super().__init__()
        self.orientation = 'lr-tb'
        
    def update(self, src):
        for i in list(self.children):
            self.remove_widget(i)
            Window.unbind(mouse_pos=i.on_hover)
            Window.unbind(mouse_pos=i.on_move)
        
        with open(src, "r") as file:
            file = json.load(file)
            for i in file:
                self.add_widget(ResourceP(i["id"], True))

class Delete(ButtonBehavior, Image):
    def __init__(self):
        super().__init__()
        setup_hover(self, 1)
        
    hovered = False

    def on_press(self):
        appList().mycon.layo.rlist.update("recursos_seleccionados_event.json") 
        
class ResourcesLayoutP(BoxLayout):
    def __init__(self):
        super().__init__()
        self.rlist = ResourceListP()
        self.add_widget(self.rlist, index=0)
        self.add_widget(Label(), index=0)
        self.add_widget(Delete())
