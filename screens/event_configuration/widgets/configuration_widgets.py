from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from utilities.utilities import *
from screens.event_configuration.widgets.calendar_widget import TotalCalendar
from kivy.properties import StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ListProperty
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown
from utilities.ui_utils import configShowAnimation
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image

class DateIniButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        setup_hover(self, 1, scroll=True)

    hovered = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and (appList().mycon.children[0].__class__.__name__ != "TotalCalendar") and not Disable.value:
            appList().mycon.add_widget(TotalCalendar(0))
            

class DateEndButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        setup_hover(self, 1, scroll=True)
    
    hovered = False
        
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and (appList().mycon.children[0].__class__.__name__ != "TotalCalendar") and not Disable.value:
            appList().mycon.add_widget(TotalCalendar(1))

class Date(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "None"

class TimeInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (1, 1, 1, 0.9)
        setup_hover(self, 1, cursor="ibeam", scroll=True)
    
    hovered = False

    def keyboard_on_textinput(self, window, text):
        try:
            a = int(text)
        except:
            pass
        else: 
            if len(self.text) < 2:
                self.text += text
            elif len(self.text) == 2:
                minu = self.parent.parent.timeIni[1] if self.name == "ini" else self.parent.parent.timeEnd[1]
                self.focus = False
                minu.focus = True


class FloatContainer(FloatLayout):
    def __init__(self, child):
        super().__init__()
        self.add_widget(Show())
        self.add_widget(child)
        self.status = False   

class Show(ButtonBehavior, Image):
    def __init__(self):
        super().__init__()
        setup_hover(self, 1, 1)
        self.source = "assets/plus.png"
    
    hovered = False

class Event(FloatLayout):
    def __init__(self, index, selector):
        super().__init__()
        self.index = index
        self.selector = selector
        self.hover = setup_hover(self, 1, 1, scroll=True, dropdown=self)

    title = StringProperty("")
    bg_color = ListProperty([0.18, 0.18, 0.18, 1])
    hovered = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not Disable.value:
            self.selector.select(self.title)
            self.selector.caller.icon = "assets/minus.png"
            self.selector.evinfo.update(self.index)

class Selector(DropDown):
    def __init__(self, caller, evinfo):
        super().__init__()
        self.max_height = 400
        self.bind(on_select=self.selection)
        self.caller = caller
        self.evinfo = evinfo
        
        e = Event(-1, self)
        e.title = "-Aventura Personalizada-"
        self.add_widget(e)

        for i in range(18):
            e = Event(i, self)
            e.title = Manage.get_one(i)["titulo"]
            self.add_widget(e)
    
    def selection(self, option, value):
        setattr(self.caller, 'name', value)                

class SelectorCaller(FloatLayout):
    def __init__(self):
        super().__init__()
        setup_hover(self, 1)
        Window.bind(mouse_pos=lambda win, pos: self.close(pos))

    def close(self, pos):
        if Disable.value:
            return

        x1, x2 = self.x, self.x + 450

        if pos[0] < x1 or pos[0] > x2:
            self.selector.dismiss()

        if pos[1] > 570 or pos[1] < 130:
            self.selector.dismiss()

        configShowAnimation(appList().mycon, pos)
        configShowAnimation(appList().menu, pos)
        

    def set_bind(self):
        self.selector.bind(on_dismiss=self.change_icon)

    hovered = False
    name = StringProperty(Manage.get_one(0)["titulo"])
    selector = None
    icon = StringProperty("assets/minus.png")

    def change_icon(self, *args):
        self.icon = "assets/minus.png"
        Utils.isDismiss = True

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not Disable.value:
            self.selector.open(self)
            self.icon = "assets/plus.png"
            Utils.isDismiss = False

