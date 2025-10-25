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

class MainConfig(FloatLayout):
    def __init__(self):
        super().__init__()
        