from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from apscheduler.schedulers.background import BackgroundScheduler
import time

screen_manager = ScreenManager()
Builder.load_file('UI/GUI.kv')
Builder.load_file('UI/ImageButton.kv')

Window.clearcolor = (1,1,1,1)
Window.size = (1000, 1000)

class Main(App):
    def build(self):
        Clock.schedule_interval(MainScreen.update_time, 1)
        return screen_manager


class MainScreen(Screen):
    def exitProgram(self):
        quit()

    def update_time(self, *args):
        screen_manager.get_screen('main').ids.clock_label.text = time.asctime() #Needed since method is accessed from Main Class

    def update_current_temp(self):

        screen_manager.get_screen('main').ids.current_temp_label.text = "Current temperature" # TODO write the code to fetch the current tempreature


class ImageButton(ButtonBehavior, Image):
    def increase_temperature(self):
        # TODO implement increase temperature
        print("arrow up imagebutton pressed")

    def decrease_temeprature(self):
        # TODO implement decrease temperature
        print("arrow down imagebutton pressed")

screen_manager.add_widget(MainScreen(name = 'main'))

def initialize():
    refresh_temperature_scheduler = BackgroundScheduler()
    #refresh_temperature_scheduler.add_job(MainScreen.update_current_temp(), 'interval', seconds=10)

    m = Main()
    m.run()