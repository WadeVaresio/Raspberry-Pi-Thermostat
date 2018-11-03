from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

screen_manager = ScreenManager()
Builder.load_file('GUI.kv')
Window.clearcolor = (1,1,1,1)

class Main(App):
    def build(self):
        return screen_manager


class MainScreen(Screen):
    def exitProgram(self):
        quit()

screen_manager.add_widget(MainScreen(name = 'main'))

def initialize():
    m = Main()
    m.run()