from kivy.app import App
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelHeader
from kivy.graphics import Rectangle

from ect.chatclient import ChatClientClient
from ect.chatclient import ChatClientServer


class GuiApp(App):
    def build(self):
        tab_panel = TabbedPanel()
        tab_panel.do_default_tab = False
        tab_panel.add_widget(self.make_server_tab())
        tab_panel.add_widget(self.make_client_tab())
        tab_panel.set_def_tab(tab_panel.tab_list[1])

        return tab_panel

    def make_server_tab(self):
        server_tab = TabbedPanelHeader(text='Server')
        server_widget = Widget()

        # Config label
        lbl_config = Label(text='Server Config')
        lbl_config.pos = (75,525)
        lbl_config.size = (100, 40)
        lbl_config.halign = "left"
        lbl_config.text_size = lbl_config.size
        lbl_config.bold = True
        server_widget.add_widget(lbl_config)

        # Port label
        lbl_port = Label(text='Port')
        lbl_port.pos = (125,450)
        lbl_port.size = (100, 30)
        lbl_port.halign = "right"
        lbl_port.valign = "middle"
        lbl_port.text_size = lbl_port.size
        server_widget.add_widget(lbl_port)

        # Port input
        txt_port = TextInput(multiline=False)
        txt_port.pos = (250,450)
        txt_port.size = (150, 30)
        server_widget.add_widget(txt_port)

        # Secret label
        lbl_secret = Label(text='Secret')
        lbl_secret.pos = (125,400)
        lbl_secret.size = (100, 30)
        lbl_secret.halign = "right"
        lbl_secret.valign = "middle"
        lbl_secret.text_size = lbl_secret.size
        server_widget.add_widget(lbl_secret)

        # Secret input
        txt_secret = TextInput(multiline=False)
        txt_secret.pos = (250,400)
        txt_secret.size = (150, 30)
        server_widget.add_widget(txt_secret)

        # Start button
        def on_server_btn_start(instance):
            raise NotImplementedError

        btn_start = Button(text='Start Server')
        btn_start.pos = (500, 395)
        btn_start.size = (200, 100)
        btn_start.bind(on_release=on_server_btn_start)
        server_widget.add_widget(btn_start)

        # Separator line
        with server_widget.canvas:
            Rectangle(pos=(75, 350), size=(650, 2))

        # Communication label
        lbl_comm = Label(text='Server Communication')
        lbl_comm.pos = (75,300)
        lbl_comm.size = (400, 40)
        lbl_comm.halign = "left"
        lbl_comm.text_size = lbl_comm.size
        lbl_comm.bold = True
        server_widget.add_widget(lbl_comm)

        # Console
        txt_console = TextInput(multiline=True)
        txt_console.pos = (75, 75)
        txt_console.size = (650, 200)
        txt_console.readonly = True
        server_widget.add_widget(txt_console)

        # Message box
        txt_message = TextInput(multiline=False)
        txt_message.pos = (75,25)
        txt_message.size = (450, 30)
        server_widget.add_widget(txt_message)

        # Send button
        def on_server_btn_send(instance):
            raise NotImplementedError

        btn_send = Button(text='Send')
        btn_send.pos = (535, 25)
        btn_send.size = (90, 30)
        btn_send.bind(on_release=on_server_btn_send)
        server_widget.add_widget(btn_send)

        # Continue button
        def on_server_btn_continue(instance):
            raise NotImplementedError

        btn_continue = Button(text='Continue')
        btn_continue.pos = (635, 25)
        btn_continue.size = (90, 30)
        btn_continue.bind(on_release=on_server_btn_continue)
        server_widget.add_widget(btn_continue)

        server_tab.content = server_widget
        return server_tab

    def make_client_tab(self):
        client_tab = TabbedPanelHeader(text='Client')
        client_widget = Widget()

        # Config label
        lbl_config = Label(text='Client Config')
        lbl_config.pos = (75,525)
        lbl_config.size = (100, 40)
        lbl_config.halign = "left"
        lbl_config.text_size = lbl_config.size
        lbl_config.bold = True
        client_widget.add_widget(lbl_config)

        # IP label
        lbl_ip = Label(text='Server IP')
        lbl_ip.pos = (125,475)
        lbl_ip.size = (100, 30)
        lbl_ip.halign = "right"
        lbl_ip.valign = "middle"
        lbl_ip.text_size = lbl_ip.size
        client_widget.add_widget(lbl_ip)

        # IP input
        txt_ip = TextInput(multiline=False)
        txt_ip.pos = (250,475)
        txt_ip.size = (150, 30)
        client_widget.add_widget(txt_ip)

        # Port label
        lbl_port = Label(text='Port')
        lbl_port.pos = (125,425)
        lbl_port.size = (100, 30)
        lbl_port.halign = "right"
        lbl_port.valign = "middle"
        lbl_port.text_size = lbl_port.size
        client_widget.add_widget(lbl_port)

        # Port input
        txt_port = TextInput(multiline=False)
        txt_port.pos = (250,425)
        txt_port.size = (150, 30)
        client_widget.add_widget(txt_port)

        # Secret label
        lbl_secret = Label(text='Secret')
        lbl_secret.pos = (125,375)
        lbl_secret.size = (100, 30)
        lbl_secret.halign = "right"
        lbl_secret.valign = "middle"
        lbl_secret.text_size = lbl_secret.size
        client_widget.add_widget(lbl_secret)

        # Secret input
        txt_secret = TextInput(multiline=False)
        txt_secret.pos = (250,375)
        txt_secret.size = (150, 30)
        client_widget.add_widget(txt_secret)

        # Start button
        def on_client_btn_start(instance):
            raise NotImplementedError

        btn_start = Button(text='Start Client')
        btn_start.pos = (500, 395)
        btn_start.size = (200, 100)
        btn_start.bind(on_release=on_client_btn_start)
        client_widget.add_widget(btn_start)

        # Separator line
        with client_widget.canvas:
            Rectangle(pos=(75, 350), size=(650, 2))

        # Communication label
        lbl_comm = Label(text='Client Communication')
        lbl_comm.pos = (75,300)
        lbl_comm.size = (400, 40)
        lbl_comm.halign = "left"
        lbl_comm.text_size = lbl_comm.size
        lbl_comm.bold = True
        client_widget.add_widget(lbl_comm)

        # Console
        txt_console = TextInput(multiline=True)
        txt_console.pos = (75, 75)
        txt_console.size = (650, 200)
        txt_console.readonly = True
        client_widget.add_widget(txt_console)

        # Message box
        txt_message = TextInput(multiline=False)
        txt_message.pos = (75,25)
        txt_message.size = (450, 30)
        client_widget.add_widget(txt_message)

        # Send button
        def on_client_btn_send(instance):
            raise NotImplementedError

        btn_send = Button(text='Send')
        btn_send.pos = (535, 25)
        btn_send.size = (90, 30)
        btn_send.bind(on_release=on_client_btn_send)
        client_widget.add_widget(btn_send)

        # Continue button
        def on_client_btn_continue(instance):
            raise NotImplementedError

        btn_continue = Button(text='Continue')
        btn_continue.pos = (635, 25)
        btn_continue.size = (90, 30)
        btn_continue.bind(on_release=on_client_btn_continue)
        client_widget.add_widget(btn_continue)

        client_tab.content = client_widget
        return client_tab


if __name__ == '__main__':
    Config.set('graphics', 'width', '400')
    Config.set('graphics', 'height', '600')
    GuiApp().run()