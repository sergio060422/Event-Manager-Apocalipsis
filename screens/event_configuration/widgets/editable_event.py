from modules.modules import *
from kivy.uix.dropdown import DropDown
# from modules import *
from core.event_manager import *
from modules.ui_utils import *
from modules.utilities import *
from kivy.uix.spinner import Spinner

class AdventureImage(Image):
    """
    Widget de imagen que representa la aventura.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class PathImage(TextInput):
    """
    Campo de texto que muestra la ruta de la imagen seleccionada.
    Deshabilita la escritura directa pero permite navegación con flechas.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def keyboard_on_textinput(self, window, text):
        """Bloquea la entrada de texto normal."""
        pass
    
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        """Permite mover el cursor con las flechas izquierda/derecha."""
        add = 1 if keycode[1] == 'right' else -1
        
        if keycode[1] == 'right' or keycode[1] == 'left':
            pos = self.cursor_index() + add
            pos = max(0, pos)
            pos = min(len(self.text), pos)
            self.cursor = self.get_cursor_from_index(pos)
        else:
            return

class SelectImage(Button):
    """
    Botón para abrir el selector de archivos y elegir una imagen para la aventura.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        setup_hover(self, 1, scroll=True)

    hovered = False

    def on_touch_down(self, touch):
        """Abre el selector de archivos al presionar el botón."""
        main = appList().mycon

        if self.collide_point(*touch.pos):
            from screens.init_menu.file_selector import openSelector
            openSelector(main, "image")

class Option(DropDown):
    """Configuración base para menús desplegables."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  
        self.size_hint = (None, None)
        self.size = (200, 40)
        self.font_size = 18
    
    def on_dismiss(self):
        Disable.value = False

class OptionPlace(DropDown):
    """Configuración específica para el menú desplegable de lugares."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  
        self.size_hint = (None, None)
        self.size = (260, 40)
        self.font_size = 18
        
    def on_dismiss(self):
        Disable.value = False
        

class PlaceSelection(Spinner):
    """
    Selector para elegir la ubicación de la aventura.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        setup_hover(self, 1, scroll=True)
        self.dropdown_cls = OptionPlace
        self.bind(on_release=self.on_click)

    hovered = False
    
    def on_click(self, spinner):
        """Deshabilita otras interacciones mientras el menú está abierto."""
        Window.set_system_cursor('arrow')
        Disable.value = True


class TypeAdventure(Spinner):
    """
    Selector (Spinner) para elegir el tipo de aventura.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        setup_hover(self, 1, scroll=True)
        self.dropdown_cls = OptionPlace
        self.bind(on_release=self.on_click)

    hovered = False
    
    def on_click(self, spinner):
        """Deshabilita otras interacciones mientras el menú está abierto."""
        Window.set_system_cursor('arrow')
        Disable.value = True

class Description(TextInput):
    """
    Campo de texto para la descripción de la aventura.
    Limita el número de líneas permitidas.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        setup_hover(self, 1, cursor="ibeam", scroll=True) 
   

    hovered = False

    # Desactiva la funcionalidad de pegar texto
    def paste(self, data=None):
        return

    def keyboard_on_textinput(self, window, text):
        """Añade texto solo si no excede el límite de 7 líneas."""
        s = self.text
        self.text += text
        
        if len(self._lines) == 7:
            self.text = s  

class NameAdventure(TextInput):
    """
    Campo de texto para el nombre de la aventura.
    Limita la longitud del texto.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        setup_hover(self, 1, cursor="ibeam", scroll=True)
    
    hovered = False

    # Desactiva la funcionalidad de pegar texto
    def paste(self, data=None):
        return
    
    def keyboard_on_textinput(self, window, text): 
        """Añade texto solo si la longitud es menor a 20 caracteres."""
        if len(self.text) < 20:
            self.text += text

class EditableAdventure(BoxLayout):
    """
    Widget principal que contiene todo el formulario de edición de aventura.
    Mapea los IDs de los widgets internos para fácil acceso.
    """
    def __init__(self):
        super().__init__()
        self.timeIni = (self.ids.hourIni, self.ids.minuIni)
        self.timeEnd = (self.ids.hourEnd, self.ids.minuEnd)
        self.dateIni = self.ids.dateini
        self.dateEnd = self.ids.datend
    
def createEditableAdventure(parent):
    """
    Reemplaza el contenido actual del padre con el formulario de edición de aventura.
    Guarda los hijos anteriores para poder restaurarlos si es necesario (a.
    """
    parent.childs = []
    parent.height = 1160
    Window.set_system_cursor('arrow')

    for child in parent.children:
        parent.childs.append(child)
    
    parent.childs.reverse()
    deleteAll(parent)

    parent.editable = EditableAdventure()
    parent.add_widget(parent.editable)
   
    
Factory.register('NameAdventure', cls=NameAdventure)
Factory.register('Description', cls=Description)
Factory.register('TypeAdventure', cls=TypeAdventure)
Factory.register('PlaceSelection', cls=PlaceSelection)
Factory.register('AdventureImage', cls=AdventureImage)
Factory.register('PathImage', cls=PathImage)
Factory.register('SelectImage', cls=SelectImage)
 
Builder.load_file("screens/event_configuration/widgets/styles/editable_event.kv")
