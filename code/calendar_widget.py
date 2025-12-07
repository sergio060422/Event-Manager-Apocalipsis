from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.window import Window
from utilities import *
import calendar

months = [0, "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

def getCalendar():
    return join_child(appList().mycon, "TotalCalendar")

class AdvanceMonth(ButtonBehavior, Image):
    def __init__(self):
        super().__init__()
        self.source = "assets/right.png"
        self.size_hint: None
        self.size = (40, 40)
        self.hover = setup_hover(self, 1)

    hovered = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not Disable.value:
            getCalendar().update(1)

class PreviousMonth(ButtonBehavior, Image):
    def __init__(self, flag):
        super().__init__()
        self.source = "assets/left.png"
        self.size_hint: None
        self.size = (40, 40)
        self.hover = setup_hover(self, 1) if not flag else None

    hovered = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not Disable.value:
            getCalendar().update(0)

class Day(Label):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.hover = setup_hover(self, 1, 0.7)
    
    hovered = False
        
    def on_touch_down(self, touch):
        calendar = getCalendar()
        if self.collide_point(*touch.pos) and not Disable.value:
            evinfo = join_child(appList().mycon, "EventInfo")
            day = self.text
            month = calendar.currentMonth
            year = calendar.currentYear
            
            if calendar.flag:
                evinfo.updateEnd(f"{day}/{month}/{year}")
            else:
                evinfo.updateIni(f"{day}/{month}/{year}")

            appList().mycon.remove_widget(calendar)
        elif not calendar.collide_point(*touch.pos):
            appList().mycon.remove_widget(calendar)


class Calendar(StackLayout):
    def __init__(self, month, year):
        super().__init__()
        self.month = month
        self.year = year

        for i in range(1, calendar.monthrange(self.year, self.month)[1] + 1):
            self.add_widget(Day(str(i)))

class Info(BoxLayout):
    def __init__(self):
        super().__init__()

class ButtonContainer(BoxLayout):
    def __init__(self, flag=True):
        super().__init__()
        self.previous = PreviousMonth(flag)
        self.previous.opacity = 0 if flag else 1
        self.advance = AdvanceMonth()
        self.add_widget(self.previous)
        self.add_widget(Label())
        self.add_widget(self.advance)

class TotalCalendar(BoxLayout):
    def __init__(self, flag):
        super().__init__()
        self.currentMonth = 1
        self.currentYear = 2077
        self.calendar = Calendar(1, 2077)
        self.info = Info()
        self.buttons = ButtonContainer()
        self.flag = flag
        self.add_widget(self.info)
        self.add_widget(self.calendar)
        self.add_widget(self.buttons)
        self.add_widget(Label())

    def update(self, type):
        if type and self.currentYear == 2222:
            return
        if type:
            self.currentMonth %= 12
            self.currentMonth += 1
            self.currentYear += (self.currentMonth == 1)
        elif not (self.currentMonth == 1 and self.currentYear == 2077):
            self.currentMonth -= 1
            self.currentYear -= (self.currentMonth == 0)
            self.currentMonth = 12 if self.currentMonth == 0 else self.currentMonth
        
        flag = True if self.currentMonth == 1 and self.currentYear == 2077 else False
        
        for child in self.calendar.children:
            Window.unbind(mouse_pos=child.hover)
        
        adv = self.buttons.advance
        prv = self.buttons.previous
        Window.unbind(mouse_pos=adv.hover)
        Window.unbind(mouse_pos=prv.hover)

        self.info.ids.month.text = months[self.currentMonth]
        self.info.ids.year.text = str(self.currentYear)

        self.remove_widget(self.calendar)
        self.calendar = Calendar(self.currentMonth, self.currentYear)
        self.add_widget(self.calendar)
        
        self.remove_widget(self.buttons)
        self.buttons = ButtonContainer(flag)
        self.add_widget(self.buttons)
