from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from apscheduler.schedulers.background import BackgroundScheduler
from kivy.uix.button import Button
import time

screen_manager = ScreenManager()
Builder.load_file('thermostat/ui/GUI.kv')
#Builder.load_file('ui/UpcomingEvents.kv')
Builder.load_file('thermostat/ui/ImageButton.kv')

Window.clearcolor = (1,1,1,1)
Window.size = (1000, 1000)


# TODO Implement Kivy Google Material Theme
class Main(App):
    def update_time(self):
        screen_manager.get_screen('main').ids.clock_label.text = time.asctime()

    def build(self):
        update_time_scheduler = BackgroundScheduler()
        update_time_scheduler.add_job(self.update_time, 'interval', seconds=0.9)

        try:
            update_time_scheduler.start()
        except KeyboardInterrupt:
            update_time_scheduler.shutdown()

        return screen_manager


class MainScreen(Screen):
    def exit_program(self):
        quit()

    def update_time(self):
        screen_manager.get_screen('main').ids.clock_label.text = time.asctime()

    def set_button_press(self):
        pass

    def see_upcoming_events(self):
        screen_manager.current = 'upcoming_events'


class ImageButton(ButtonBehavior, Image):
    def increase_temperature(self):
        # TODO implement increase temperature
        print("arrow up imagebutton pressed")

    def decrease_temperature(self):
        # TODO implement decrease temperature
        print("arrow down imagebutton pressed")


class UpcomingEvents(Screen):
    layout = GridLayout(rows=5, cols=5)

    def pressed(self):
        screen_manager.current = 'main'

screen_manager.add_widget(MainScreen(name='main'))
screen_manager.add_widget(UpcomingEvents(name='upcoming_events'))


def initialize():
    m = Main()
    m.run()


def update_temperature():
    # TODO implement temperature sensor
    screen_manager.get_screen('main').ids.current_temp_label.text = "Current Temp\n"
