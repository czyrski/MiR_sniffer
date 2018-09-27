from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, CardTransition
from kivy.lang import Builder
from os import listdir

kv_path = './kv/'
for kv in listdir(kv_path):
    Builder.load_file(kv_path+kv)


class MirSniffer(ScreenManager):
    pass

class MainScreen(Screen):
    pass

class Mir161(Screen):
    pass


class MainApp(App):
    def build(self):
        return MirSniffer()

if __name__ == '__main__':
    MainApp().run()
