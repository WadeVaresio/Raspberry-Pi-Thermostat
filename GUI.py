from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock
import time

screen_manager = ScreenManager()
Builder.load_file('GUI.kv')
Window.clearcolor = (1,1,1,1)

class Main(App):
    def build(self):
        Clock.schedule_interval(MainScreen.update_time, 1)
        return screen_manager


class MainScreen(Screen):
    def exitProgram(self):
        quit()

    def update_time(self, *args):
        screen_manager.get_screen('main').ids.clock_label.text = time.asctime() #Needed since method is accessed from Main Class


screen_manager.add_widget(MainScreen(name = 'main'))

def initialize():
    m = Main()
    m.run()