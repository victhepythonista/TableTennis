import kivy

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.app import *
from kivy.vector import Vector
from kivy.clock import  Clock

from kivy.core.window import Window
from kivy.utils import get_color_from_hex

Window.size = ((300,700))
Window.clearcolor = .1,.4,.6,.7

class Table(Widget):
    pass



table = Table()
class TableTennis(App):
    def build(self):
        return table


if __name__ == '__main__':
    TableTennis().run()
