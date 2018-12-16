from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from apscheduler.schedulers.background import BackgroundScheduler
import time

screen_manager = ScreenManager()
Builder.load_file('thermostat/ui/GUI.kv')
Builder.load_file('thermostat/ui/UpcomingEvents.kv')

Window.clearcolor = (1,1,1,1)
Window.size = (1000, 1000)

TEMPERATURE = 68
PROPOSED_TEMP = TEMPERATURE


class Main(App):
    @staticmethod
    def update_time():
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
    @staticmethod
    def exit_program():
        quit()

    @staticmethod
    def update_time():
        screen_manager.get_screen('main').ids.clock_label.text = time.asctime()

    def set_button_press(self):
        global TEMPERATURE, PROPOSED_TEMP
        TEMPERATURE = PROPOSED_TEMP

        screen_manager.get_screen('main').ids.current_temp_label.text = "Current Temp: %sF" % str(TEMPERATURE)
        screen_manager.get_screen('main').ids.set_temperature_label.color = 0, 0, 0, 0

    def see_upcoming_events(self):
        screen_manager.current = 'upcoming_events'


class ImageButton(ButtonBehavior, Image):

    def update_proposed_temp(self, instance):
        global PROPOSED_TEMP

        if instance.change is "increase":
            PROPOSED_TEMP += 1
            self.update_temp(PROPOSED_TEMP)
        else:
            PROPOSED_TEMP -= 1
            self.update_temp(PROPOSED_TEMP)

    @staticmethod
    def update_temp(temp):
        set_temp_label = screen_manager.get_screen('main').ids.set_temperature_label
        set_temp_label.color = 0, 0, 0, 1
        set_temp_label.text = str(temp)


class UpcomingEvents(Screen):

    def on_enter(self):
        # TODO update event labels based on data from calendar
        print(screen_manager.get_screen('upcoming_events').ids)

    def edit_button_pressed(self, instance):
        print(instance.associated_event)


screen_manager.add_widget(MainScreen(name='main'))
screen_manager.add_widget(UpcomingEvents(name='upcoming_events'))


def initialize():
    m = Main()
    m.run()


def update_temperature():
    # TODO implement temperature sensor
    screen_manager.get_screen('main').ids.current_temp_label.text = "Current Temp: %sF" % str(TEMPERATURE)
