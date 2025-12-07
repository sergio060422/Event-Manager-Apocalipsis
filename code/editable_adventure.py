from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from utilities import *
from kivy.uix.button import Button
from event_manager import *
from error import *
from utilities import *
from kivy.uix.spinner import Spinner

kv = '''
<EditableAdventure>:
    padding: 20, 0, 0, 0
    size_hint_y: None
    height: 1160
    orientation: "vertical"
    spacing: 8

    Label: 
        markup: True
        text: "[b] Nombre de la aventura:[/b]"
        font_size: 22
        size_hint: None, None
        size: self.texture_size
    
    NameAdventure:
        background_color: 0, 0, 0, 0
        cursor_color: 1, 1, 1, 1
        foreground_color: 1, 1, 1, 1
        size_hint: None, None
        text_size: self.width - 50, 36
        size: (400, 36)
        font_size: 18
        hovered: False
        hint_text: "Elige un nombre"
        multiline: False
        id: name
        canvas.after:
            Color: 
                rgba: 1, 1, 1, 1
            Line:
                points: (self.x, self.y + 4, 400, self.y + 4)
                width: 1
    Label: 
        markup: True
        text: "[b] Descripcion:[/b]"
        font_size: 22
        size_hint: None, None
        size: self.texture_size

    Description:
        size_hint: None, None
        size: 420, 150
        text_size: self.width - 20, None
        halign: "left"
        markup: 0
        font_size: 18
        index: 0
        id: description
        background_color: 0, 0, 0, 0
        cursor_color: 1, 1, 1, 1
        foreground_color: 1, 1, 1, 1
        hint_text: "Describe tu aventura"

        canvas.after:
            Color:
                rgba: 1, 1, 1, 1
            Line:
                rounded_rectangle: (self.x, self.y, self.width, self.height, 12)
                width: 1    

    Label: 
        markup: True
        text: "[b] Tipo de aventura:[/b]"
        font_size: 22
        size_hint: None, None
        size: self.texture_size

    TypeAdventure:
        id: type
        size_hint: None, None
        size: (200, 40)
        values: ["Defensa", "Refugio", "Supervivencia"]
        font_size: 16
        text: "Defensa"
        background_color: 0, 0, 0, 0
        canvas.before:
            Color:
                rgba: (0.18, 0.18, 0.18, 0.85)
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [12]

        canvas.after:
            Color:
                rgba: 1, 1, 1, 1
            Line:
                rounded_rectangle: (self.x, self.y, self.width, self.height, 12)
                width: 1.1

    Label: 
        markup: True
        text: "[b] Peligro: [/b]"
        font_size: 22
        size_hint: None, None
        size: self.texture_size

    TypeAdventure:
        id: danger
        size_hint: None, None
        size: (200, 40)
        values: ["Pan comido", "Vigila tus espaldas", "Huele a peligro", "Sal corriendo", "Muerte segura"]
        font_size: 16
        text: "Pan comido"
        background_color: 0, 0, 0, 0
        canvas.before:
            Color:
                rgba: (0.18, 0.18, 0.18, 0.85)
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [12]

        canvas.after:
            Color:
                rgba: 1, 1, 1, 1
            Line:
                rounded_rectangle: (self.x, self.y, self.width, self.height, 12)
                width: 1.1

    Label: 
        markup: True
        text: "[b] Ubicacion: [/b]"
        font_size: 22
        size_hint: None, None
        size: self.texture_size
    
    PlaceSelection:
        id: place
        size_hint: None, None
        size: (260, 40)
        values: ['Interior del refugio', 'Supermercados WaltMart', 'Fronteras de la ciudad', 'Modulo de purificacion', 'Vecindario del refugio', 'Refugios Infectados', 'Bunker militar del sur', 'Carreteras cercanas al refugio', 'Cuarto de armamento', 'Perimetro del refugio', 'Torres de iluminacion K3', 'Hospital abandonado', 'Cementerio de autos', 'Patio exterior', 'Alrededores del refugio', 'Area 0 de infeccion']
        font_size: 16
        text: "Interior del refugio"
        background_color: 0, 0, 0, 0
        canvas.before:
            Color:
                rgba: (0.18, 0.18, 0.18, 0.85)
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [12]

        canvas.after:
            Color:
                rgba: 1, 1, 1, 1
            Line:
                rounded_rectangle: (self.x, self.y, self.width, self.height, 12)
                width: 1.1
    
    Label: 
        markup: True
        text: "[b] Imagen de la aventura: [/b]"
        font_size: 22
        size_hint: None, None
        size: self.texture_size
    
    AdventureImage:
        size_hint: None, None
        source: "assets/event_running_images/example.png"
        size: (320, 320)

    BoxLayout:
        spacing: 8
        size_hint_y: None
        height: 40
        PathImage:
            size_hint: None, None
            font_size: 15
            size: (320, 30)
            text_size: (400, 30)
            pos_hint: {'x': 0, 'center_y': .5}
            foreground_color: (1, 1, 1, 1)
            background_color: (0.12, 0.12, 0.12, 1)
            cursor_color: (1, 1, 1, 1)
            padding: 6
            text: "assets/event_running_images/example.png"
            canvas.after:
                Color:
                    rgba: 1, 1, 1, 1
                Line:
                    rounded_rectangle: (self.x, self.y, self.width, self.height, 12)
                    width: 1.01  
        SelectImage:
            size_hint: None, None
            pos_hint: {'x': 0, 'center_y': .5}
            size: (90, 30)
            markup: True
            text: "[b] Seleccionar [/b]"
            padding: 10
    Label:
        index: 0
        markup: True
        text: "[b] Fecha de la aventura: [/b]"
        font_size: 24
        size_hint: None, None
        size: self.texture_size 

    BoxLayout:
        size_hint: None, None
        height: 30
        pos_hint: {'x': 0.01, 'y': 0}
        DateIniButton:
            font_size: 20
            text: "Inicio"
            size_hint: None, None
            size: self.texture_size 
            padding: 4
        Label:
            text: "-"
            size_hint: None, None
            pos_hint: {'center_x': .5, "center_y": .5}
            width: 40
        DateEndButton:
            font_size: 20
            text: "Final"
            size_hint: None, None
            size: self.texture_size
            padding: 4
    BoxLayout:
        size_hint: None, None
        pos_hint: {'x': 0.01, 'y': 0}
        height: 30
        Date:
            id: dateini
            font_size: 20
            text: "No seleccionado!"
            size_hint: None, None
            size: self.texture_size 
            padding: 4
        Label:
            text: "-"
            size_hint: None, None
            pos_hint: {'center_x': .5, "center_y": .5}
            width: 40
        Date:
            id: datend
            font_size: 20
            text: "No seleccionado!"
            size_hint: None, None
            size: self.texture_size
            padding: 4
    Label:
        index: 0
        markup: True
        text: "[b] Horario de inicio - fin: [/b]"
        font_size: 24
        size_hint: None, None
        size: self.texture_size 
    BoxLayout:
        size_hint: None, None
        pos_hint: {'x': 0.01, 'y': 0}
        height: 30
        Time:
            id: hourIni
            name: "ini"
            text: "00"
            size_hint: None, None    
            size: (30, 30)
            max_text_length: 20
            multiline: False
        Label:
            text: ":"
            size_hint: None, None
            pos_hint: {'center_x': .5, "center_y": .5}
            width: 20
        Time:
            id: minuIni
            name: "ini"
            text: "00"
            size_hint: None, None    
            size: (30, 30)
            max_text_length: 20
            multiline: False
        Label:
            text: "-"
            size_hint: None, None
            pos_hint: {'center_x': .5, "center_y": .5}
            width: 40
        Time:
            id: hourEnd
            name: "end"
            text: "00"
            size_hint: None, None    
            size: (30, 30)
            max_text_length: 20
            multiline: False
        Label:
            text: ":"
            size_hint: None, None
            pos_hint: {'center_x': .5, "center_y": .5}
            width: 20
        Time:
            id: minuEnd
            name: "end"
            text: "00"
            size_hint: None, None    
            size: (30, 30)
            max_text_length: 20
            multiline: False
    Label:
        index: 0
        markup: True
        text: "[b]Nota:[/b] Los horarios se interpretan en el formato de de 24 horas!"
        font_size: 16
        size_hint: None, None
        pos_hint: {'x': 0.01, 'y': 0}
        size: self.texture_size
        color: 1, 1, 1, 0.8
        padding: 0, 10, 0, 0 

    Label:
        index: 0
    
        
'''

Builder.load_string(kv)

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
            from face import FileSelectorWindow, openSelector
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
   
    
    
 