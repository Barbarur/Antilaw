from kivy.graphics import Rectangle, Color, RoundedRectangle
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget


class MenuButton(Button):
    pass

class MenuToggleButton(ToggleButton):
    pass


class MenuLabel(Label):
    pass



Builder.load_file("widgetsmenu.kv")


