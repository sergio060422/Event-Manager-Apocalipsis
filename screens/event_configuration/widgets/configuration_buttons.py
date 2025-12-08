from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from utilities.utilities import *
from core.event_creation import create_adventure

class Backbutton(ButtonBehavior, Image):
    def __init__(self):
        super().__init__()
        self.source = "assets/backbutton.png"
        self.size_hint = (None, None)
        self.width = 150
        self.pos_hint = {'x': 0.02, 'top': 0.99}
        self.hover = setup_hover(self, 1)
    
    hovered = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not Disable.value:
            CurrentScreen.screen = 0
            transition("main", 0.5, "right")
            
class CommandAdventure(BoxLayout):
    def __init__(self):
        super().__init__()
        self.status = False
        self.add_widget(ListAdventures())
        self.add_widget(AdventureButton())

class ListAdventures(ButtonBehavior, Image):
    def __init__(self):
        super().__init__()
        self.source = "assets/listAdventure.png"
        setup_hover(self, 1)

    hovered = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            apps = appList()
            apps.events.scrollList.running.update()

            screenParent = appList().screenParent
            CurrentScreen.before = (CurrentScreen.screen, screenParent.current)
            CurrentScreen.screen = 2
            transition("events", 0.5, "down")

class AdventureButton(ButtonBehavior, Image):
    def __init__(self):
        super().__init__()
        self.source = "assets/adventure.png"
        setup_hover(self, 1)

    hovered = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not Disable.value:
            create_adventure()
