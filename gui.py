from kivy.app import App
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.floatlayout import FloatLayout


class GuiWidget(TabbedPanel):
    pass


class GuiApp(App):
    def build(self):
        return GuiWidget()


if __name__ == '__main__':
    Config.set('graphics', 'width', '400')
    Config.set('graphics', 'height', '600')
    GuiApp().run()