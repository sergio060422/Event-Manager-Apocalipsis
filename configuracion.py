from kivy.config import Config
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
from confi_info_class import ResourcesLayoutP, ResourceInfoLayoutP
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown

class Event(BoxLayout):
    def __init__(self, index, selector):
        super().__init__()
        self.index = index
        self.selector = selector

    title = StringProperty("a")

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.selector.select(self.title)
            self.selector.caller.icon = "assets/minus.png"

class Selector(DropDown):
    def __init__(self, caller):
        super().__init__()
        self.max_height = 400
        self.bind(on_select=self.selection)
        self.caller = caller

        for i in range(20):
            e = Event(i, self)
            self.add_widget(e)
    
    def selection(self, option, value):
        setattr(self.caller, 'textvalue', value)
                

class SelectorCaller(FloatLayout):
    def __init__(self):
        super().__init__()
        Window.bind(mouse_pos=self.on_selector_hoover)

    def set_bind(self):
        self.selector.bind(on_dismiss=self.change_icon)

    def on_selector_hoover(self, win, pos):
        if self.collide_point(*pos):
            Window.set_system_cursor('hand')

        else:
            Window.set_system_cursor('arrow')
        
    textvalue = StringProperty("-1")
    selector = None
    icon = StringProperty("assets/minus.png")

    def change_icon(self, *args):
        self.icon = "assets/minus.png"
        print("pinga")

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.selector.open(self)
            self.icon = "assets/plus.png"

class EventInfo(BoxLayout):
    def __init__(self):
        super().__init__()
        self.add_widget(Label(), index=0)

class EventHandler(BoxLayout):
    def __init__(self):
        super().__init__()
        self.selcal = SelectorCaller()
        self.selcal.selector = Selector(self.selcal)
        self.selcal.set_bind()
        self.add_widget(self.selcal, index=0)
        self.add_widget(EventInfo())
        
class Backpack(StackLayout):
    def __init__(self):
        super().__init__()


class ConfiEvent(BoxLayout):
    def __init__(self):
        super().__init__()
        self.add_widget(EventHandler())
        self.layo = ResourcesLayoutP()
        self.add_widget(self.layo)

class MainConfig(FloatLayout):
    def __init__(self):
        super().__init__()
        self.img = Image(source="assets/background_config.png")
        self.add_widget(self.img)
        self.cefi = ConfiEvent()
        self.add_widget(self.cefi)
        self.reso = ResourceInfoLayoutP()
        self.layo = self.cefi.layo
        self.add_widget(self.reso)

