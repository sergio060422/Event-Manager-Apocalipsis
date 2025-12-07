from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ListProperty
from kivy.core.window import Window
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty
import json
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
        self.pos_hint = {'center_x': 0.80, 'center_y': 0.18}
        self.foreground_color = (1, 1, 1, 1)
        self.background_color = (0.12, 0.12, 0.12, 0.9)
        self.font_size = 16
        self.padding = [3, 0, 0, 0]
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

class DeleteIcon(Image):
    def __init__(self, parent):
        super().__init__()
        self.size_hint = (None, None)
        self.size = (60, 60)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.source = "assets/deleteIcon.png"
        self.pos = parent.pos

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
        self.delete = DeleteIcon(self)
        self.delete.opacity = 0
        self.add_widget(self.delete)
        Window.bind(mouse_pos=self.on_move)
        
        if hoverable:
            self.on_hover = setup_hover(self, 1, 0.8)
        if not cuantiable:
            self.cuantity.opacity = 0
    
    hovered = False

    def on_move(self, win, pos):  
        if CurrentScreen.screen != 1 or Disable.value:
            return
        
        main = appList().mycon
        resource = get_one(self.id)
        info = main.reso

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
    
            if not calendar.collide_point(*pos) or calendar.width != 360:
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

    def quit_resource(self, id):
        recurso = get_one(id)
        data = readJson("code/recursos_seleccionados_event.json")
        data.remove(recurso)
        writeJson("code/recursos_seleccionados_event.json", data)
        appList().mycon.layo.rlist.update("code/recursos_seleccionados_event.json") 
    
    def on_touch_down(self, touch):
        if CurrentScreen.screen != 1 or Disable.value:
            return
    
        if self.collide_point(*touch.pos):
            if not self.selected:
                childSelected = Utils.isSelected
                
                if childSelected != False:
                    childSelected.my_color = [0.1, 0.1, 0.1, 1]
                    childSelected.selected = 0
                    childSelected.opacity = 1
                    childSelected.icon.opacity = 1
                    childSelected.delete.opacity = 0
                
                self.opacity = 1
                self.my_color = [0.8, 0.8, 0.8, 0.8]
                self.selected = 1
                self.icon.opacity = 0.5
                self.delete.opacity = 1
                Utils.isSelected = self            
            else:
                self.quit_resource(Utils.isSelected.id)        
                main = appList().mycon
                info = main.reso
                info.opacity = 0
        elif Utils.isSelected == self:
            childSelected = Utils.isSelected
            
            if childSelected != False:
                Utils.isSelected = False
                childSelected.my_color = [0.1, 0.1, 0.1, 1]
                childSelected.selected = 0
                childSelected.opacity = 1
                childSelected.icon.opacity = 1
                childSelected.delete.opacity = 0
                

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
                resource = ResourceP(i["id"], True)
                self.add_widget(resource)

class ResourcesLayoutP(BoxLayout):
    def __init__(self):
        super().__init__()
        self.rlist = ResourceListP()
        self.add_widget(self.rlist, index=0)
        self.add_widget(Label(), index=0)
