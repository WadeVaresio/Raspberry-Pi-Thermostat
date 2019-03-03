import time

from apscheduler.schedulers.background import BackgroundScheduler
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from thermostat.database import Database

screen_manager = ScreenManager()
Builder.load_file('thermostat/ui/GUI.kv')
Builder.load_file('thermostat/ui/UpcomingEvents.kv')

Window.clearcolor = (1, 1, 1, 1)
Window.size = (1000, 1000)

TEMPERATURE = 68.0
PROPOSED_TEMP = TEMPERATURE


class Main(App):

    def build(self):
        """
        Called upon creation of the app, used to initiliaze background processes
        :return:
        """
        self.title = "Raspberry Pi Thermostat"

        update_time_scheduler = BackgroundScheduler()
        update_time_scheduler.add_job(MainScreen.update_time, 'interval', seconds=0.9)

        try:
            update_time_scheduler.start()
        except KeyboardInterrupt:
            update_time_scheduler.shutdown()

        return screen_manager


class MainScreen(Screen):
    @staticmethod
    def exit_program():
        """
        Quit the program
        :return:
        """
        quit()

    @staticmethod
    def update_time():
        """
        Update the time for the current time label
        :return:
        """
        screen_manager.get_screen('main').ids.clock_label.text = time.asctime()

    @staticmethod
    def transition_to_main():
        screen_manager.current = 'main'

    @staticmethod
    def transition_to_upcoming_events():
        # TODO check if calendar events is empty/display popup
        screen_manager.current = 'upcoming_events'

    def temp_slider_change(self):
        self.ids.proposed_temp.color = 0.960, 0.847, 0.380, 1
        self.ids.proposed_temp.text = str(self.ids.temp_slider.value)

        Clock.schedule_once(lambda dt: self.hide_proposed_temp_label(), 10)

    def hide_proposed_temp_label(self):
        global PROPOSED_TEMP, TEMPERATURE
        self.ids.proposed_temp.color = 0, 0, 0, 0
        TEMPERATURE = self.ids.temp_slider.value
        update_temperature()


class UpcomingEvents(Screen):

    def on_enter(self):
        """
        Change the labels to corresponding events from google calendar
        :return: None
        """
        data = Database.get_all_events()

        label_widgets = [self.ids.event_label0, self.ids.event_label1, self.ids.event_label2, self.ids.event_label3, self.ids.event_label4,
                            self.ids.event_label5, self.ids.event_label6, self.ids.event_label7, self.ids.event_label8, self.ids.event_label9]

        button_widgets = [self.ids.edit_event_0, self.ids.edit_event_1, self.ids.edit_event_2, self.ids.edit_event_3, self.ids.edit_event_4,
                          self.ids.edit_event_5, self.ids.edit_event_6, self.ids.edit_event_7, self.ids.edit_event_8, self.ids.edit_event_9]

        index = 0
        for event in data:
            start_time = event[1]
            label_widgets[index].event_start = start_time
            label_widgets[index].text = str(event[3]) + " at " + start_time
            index += 1

        for i in range(index, len(label_widgets)):
            label_widgets[i].color = (0, 0, 0, 0)
            button_widgets[i].color = (0, 0, 0, 0)
            button_widgets[i].background_color = (0, 0, 0, 0)

    @staticmethod
    def edit_button_action(instance):
        """
        Function when an edit event button is pressed on the upcoming events screen
        :param instance: Instance of the button that was just pressed
        :return: None
        """
        print(instance.associated_event)

    @staticmethod
    def back_button_action():
        screen_manager.current = 'main'


screen_manager.add_widget(MainScreen(name='main'))
screen_manager.add_widget(UpcomingEvents(name='upcoming_events'))


def initialize():
    """
    Initialize the gui
    :return: None
    """
    m = Main()
    m.run()


def update_temperature():
    """
    Update the current temperature label using the global: Temperature
    :return:
    """
    screen_manager.get_screen('main').ids.current_temp_label.text = "Current Temp: %sF" % str(TEMPERATURE)
