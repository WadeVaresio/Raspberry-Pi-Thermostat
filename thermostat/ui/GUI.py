from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from apscheduler.schedulers.background import BackgroundScheduler
from thermostat import data
import time

screen_manager = ScreenManager()
Builder.load_file('thermostat/ui/GUI.kv')
Builder.load_file('thermostat/ui/UpcomingEvents.kv')

Window.clearcolor = (1, 1, 1, 1)
Window.size = (1000, 1000)

TEMPERATURE = 68.0
PROPOSED_TEMP = TEMPERATURE


class Main(App):

    @staticmethod
    def update_time():
        """
        Update the time label to represent the current time
        :return: None
        """
        screen_manager.get_screen('main').ids.clock_label.text = time.asctime()

    def build(self):
        """
        Called upon creation of the app, used to initiliaze background processes
        :return:
        """
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
        """
        Quit the program
        :return:
        """
        quit()

    @staticmethod
    def update_time():
        screen_manager.get_screen('main').ids.clock_label.text = time.asctime()

    @staticmethod
    def set_button_press():
        global TEMPERATURE, PROPOSED_TEMP
        TEMPERATURE = PROPOSED_TEMP

        screen_manager.get_screen('main').ids.current_temp_label.text = "Current Temp: %sF" % str(TEMPERATURE)
        screen_manager.get_screen('main').ids.set_temperature_label.color = 0, 0, 0, 0

    @staticmethod
    def transition_to_main():
        screen_manager.current = 'main'

    @staticmethod
    def transition_to_upcoming_events():
        # TODO check if calendar events is empty/display popup
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
    #TODO implement back button
    def on_enter(self):
        """
        Change the labels to corresponding events from google calendar
        :return: None
        """
        if data.no_events():
            self.display_popup()
            return

        label_widgets = [self.ids.event_label0, self.ids.event_label1, self.ids.event_label2, self.ids.event_label3, self.ids.event_label4,
                            self.ids.event_label5, self.ids.event_label6, self.ids.event_label7, self.ids.event_label8, self.ids.event_label9]

        button_widgets = [self.ids.edit_event_0, self.ids.edit_event_1, self.ids.edit_event_2, self.ids.edit_event_3, self.ids.edit_event_4,
                          self.ids.edit_event_5, self.ids.edit_event_6, self.ids.edit_event_7, self.ids.edit_event_8, self.ids.edit_event_9]

        index = 0
        for event in data.get_calendar_events():
            start_time = event['start'].get('dateTime', event['start'].get('date'))
            label_widgets[index].event_start = start_time
            label_widgets[index].text = event['summary'] + " on " + start_time
            index += 1

        for i in range(index, len(label_widgets)):
            label_widgets[i].color = (0, 0, 0, 0)
            button_widgets[i].color = (0, 0, 0, 0)
            button_widgets[i].background_color = (0, 0, 0, 0)

    @staticmethod
    def edit_button_pressed(instance):
        """
        Function when an edit event button is pressed on the upcoming events screen
        :param instance: Instance of the button that was just pressed
        :return: None
        """
        # TODO disable touch ability of "hidden" buttons
        if instance.associated_event >= len(data.get_calendar_events()):
            print("Touching button that should be hidden")
            return

        print(instance.associated_event)


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
    # TODO implement temperature sensor
    screen_manager.get_screen('main').ids.current_temp_label.text = "Current Temp: %sF" % str(TEMPERATURE)
