from kivy.config import Config
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '768')
Config.set('input', 'mouse', 'mouse,disable_multitouch')
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ListProperty
from kivy.core.window import Window
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from screens.event_configuration.configuration import MainConfig
from screens.event_configuration.widgets.configuration_widgets import FloatContainer
from screens.event_configuration.widgets.configuration_buttons import Backbutton, CommandAdventure, ListAdventures
from kivy.lang import Builder
from utilities.utilities import *
from screens.event_list.events import MainEventContainter
from screens.main_menu.face import Container

class PlayerLayout(BoxLayout):
    def __init__(self):
        super().__init__()

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
        setup_hover(self, 0, 0.8)
    
    hovered = False

    def on_move(self, win, pos):
        if CurrentScreen.screen != 0:
            return
            
        resource = get_one(self.id)
        info = appList().menu.rInfo

        if self.collide_point(*pos):
            info.img_source = f"assets/{self.id}.png"
            info.name = resource["nombre"]
            info.cuantity = str(resource["cantidad"])
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
            info.exclude = resource["excluyente"][0]  
            info.opacity = 1
        else:
            if self.hovered:
                info.opacity = 0

    my_color = ListProperty([0.1, 0.1, 0.1, 1])

    def add_resource(self):
        recurso = get_one(self.id)
        data = readJson("data/dynamic/selected_resources.json")
        data.append(recurso)
        writeJson("data/dynamic/selected_resources.json", data)

    def quit_resource(self):
        recurso = get_one(self.id)
        data = readJson("data/dynamic/selected_resources.json")
        data.remove(recurso)
        writeJson("data/dynamic/selected_resources.json", data)

    def on_touch_down(self, touch):
        if CurrentScreen.screen != 0:
            return
        
        if self.collide_point(*touch.pos):
            if not self.selected:
                self.my_color = [0.8, 0.8, 0.8, 0.8]
                self.selected = 1
                self.opacity = 1
                self.add_resource()              
            else:
                self.my_color = [0.1, 0.1, 0.1, 1]
                self.selected = 0
                self.opacity = 0.8
                self.quit_resource()

class ResourceList(StackLayout):
    def __init__(self):
        super().__init__()
        self.orientation = 'lr-tb'
        for i in range(1, 25):
            self.add_widget(Resource(i))

class ResourceInfoLayout(StackLayout):
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
   
class ResourcesLayout(BoxLayout):
    def __init__(self):
        super().__init__()
        self.add_widget(ResourceList(), index=0)
        self.add_widget(Label(), index=0)
        
class ConfigEvent(BoxLayout):
    def __init__(self):
        super().__init__()
        self.add_widget(PlayerLayout())
        self.add_widget(ResourcesLayout())
        
class ResourceMenu(FloatLayout):
    def __init__(self):
        super().__init__()
        self.background = Image(source="assets/background_main.png")
        self.add_widget(self.background)
        self.add_widget(BackButtonMain())
        self.add_widget(ConfigEvent())
        self.rInfo = ResourceInfoLayout()
        self.add_widget(self.rInfo)
        self.command = FloatContainer(CommandADventureMain())
        self.add_widget(self.command)
        

class CommandADventureMain(CommandAdventure):
    def __init__(self):
        super().__init__()
        self.remove_widget(self.children[0])
        self.remove_widget(self.children[0])
        self.add_widget(ListAdventuresMain())
        self.add_widget(ButtonAdvance())

class ListAdventuresMain(ListAdventures):
    def __init__(self):
        super().__init__()
        setup_hover(self, 0)

class BackButtonMain(Backbutton):
    def __init__(self):
        super().__init__()
        Window.unbind(mouse_pos=self.hover)
        setup_hover(self, 0)
        
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not Disable.value:
            CurrentScreen.screen = 3
            transition("menu", 0.5, "right")
    
class ButtonAdvance(ButtonBehavior, Image):
    def __init__(self):
        super().__init__()
        setup_hover(self, 0)

    hovered = False

    def on_press(self):
        data = readJson("data/dynamic/selected_resources.json")
        writeJson("data/dynamic/selected_resources_event.json", data)

        CurrentScreen.screen = 1
        appList().mycon.layo.rlist.update("data/dynamic/selected_resources.json")
        transition("config", 0.5, "left")
       
class ScreenChild(Screen):
    def __init__(self, nombre, contenido):
        super().__init__()
        self.name = nombre
        self.add_widget(contenido)

class ScreenParent(ScreenManager):
    def __init__(self, mainMenu, menu, mycon, events):
        super().__init__()
        self.add_widget(ScreenChild("menu", mainMenu))
        self.add_widget(ScreenChild("main", menu))
        self.add_widget(ScreenChild("config", mycon))
        self.add_widget(ScreenChild("events", events))

class Main(App):
    def build(self):
        self.mainMenu = Container()        
        self.mycon = MainConfig()
        self.menu = ResourceMenu()
        self.events = MainEventContainter()
        self.screenParent = ScreenParent(self.mainMenu, self.menu, self.mycon, self.events)
        return self.screenParent

def cleanJSON(*args):
    writeJson("data/dynamic/selected_resources.json", [])
    writeJson("data/dynamic/selected_resources_event.json", [])

Window.bind(on_request_close=cleanJSON)
Builder.load_file("screens/event_configuration/widgets/styles/calendar_widget.kv")    
Builder.load_file("screens/event_configuration/styles/configuration.kv")
Builder.load_file("screens/event_configuration/widgets/styles/resource_widgets.kv")

Main().run()