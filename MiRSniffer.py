from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.clock import Clock
from os import listdir

kv_path = './kv/'
for kv in listdir(kv_path):
    Builder.load_file(kv_path+kv)


class MirSniffer(ScreenManager):
    pass

class MainScreen(Screen):
    status_mir161 = StringProperty('0')

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self.change_robot_status, 5)

    def change_robot_status(self, *args):
        test_string = self.status_mir161 + '1'
        self.status_mir161 = test_string
    pass

class Mir161(Screen):
    pass

class MainApp(App):
    def build(self):
        return MirSniffer()

if __name__ == '__main__':
    MainApp().run()
