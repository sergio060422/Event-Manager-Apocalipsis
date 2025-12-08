from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from utilities import *
from kivy.uix.button import Button
from core.event_manager import *
from utilities.ui_utils import *
from utilities.utilities import *
from kivy.uix.spinner import Spinner

Builder.load_file("screens/event_configuration/widgets/styles/editable_event.kv")

class AdventureImage(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class PathImage(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def keyboard_on_textinput(self, window, text):
        pass
    
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        add = 1 if keycode[1] == 'right' else -1
        
        if keycode[1] == 'right' or keycode[1] == 'left':
            pos = self.cursor_index() + add
            pos = max(0, pos)
            pos = min(len(self.text), pos)
            self.cursor = self.get_cursor_from_index(pos)
        else:
            return

class SelectImage(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        setup_hover(self, 1, scroll=True)

    hovered = False

    def on_touch_down(self, touch):
        main = appList().mycon

        if self.collide_point(*touch.pos):
            from screens.main_menu.face import openSelector
            openSelector(main, "image")

class Option(DropDown):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  
        self.size_hint = (None, None)
        self.size = (200, 40)
        self.font_size = 18
    
    def on_dismiss(self):
        Disable.value = False

class OptionPlace(DropDown):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  
        self.size_hint = (None, None)
        self.size = (260, 40)
        self.font_size = 18
        
    def on_dismiss(self):
        Disable.value = False
        

class PlaceSelection(Spinner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        setup_hover(self, 1, scroll=True)
        self.dropdown_cls = OptionPlace
        self.bind(on_release=self.on_click)

    hovered = False
    
    def on_click(self, spinner):
        Window.set_system_cursor('arrow')
        Disable.value = True


class TypeAdventure(Spinner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        setup_hover(self, 1, scroll=True)
        self.dropdown_cls = OptionPlace
        self.bind(on_release=self.on_click)

    hovered = False
    
    def on_click(self, spinner):
        Window.set_system_cursor('arrow')
        Disable.value = True

class Description(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        setup_hover(self, 1, cursor="ibeam", scroll=True) 
   

    hovered = False

    def paste(self, data=None):
        return

    def keyboard_on_textinput(self, window, text):
        s = self.text
        self.text += text
        
        if len(self._lines) == 7:
            self.text = s  

class NameAdventure(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        setup_hover(self, 1, cursor="ibeam", scroll=True)
    
    hovered = False

    def paste(self, data=None):
        return
    
    def keyboard_on_textinput(self, window, text): 
        if len(self.text) < 20:
            self.text += text

class EditableAdventure(BoxLayout):
    def __init__(self):
        super().__init__()
        self.timeIni = (self.ids.hourIni, self.ids.minuIni)
        self.timeEnd = (self.ids.hourEnd, self.ids.minuEnd)
        self.dateIni = self.ids.dateini
        self.dateEnd = self.ids.datend
    
def createEditableAdventure(parent):
    parent.childs = []
    parent.height = 1160
    Window.set_system_cursor('arrow')

    for child in parent.children:
        parent.childs.append(child)
    
    parent.childs.reverse()
    deleteAll(parent)

    parent.editable = EditableAdventure()
    parent.add_widget(parent.editable)
   
    
    
 