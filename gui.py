import logging
import socket
from time import sleep

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
from ect.exceptions import BeingAttacked
from ect.exceptions import NoAuthentication
from ect.log import log
from ect.exceptions import NoSharedKey


def is_valid_ip(ip):
    try:
        parts = ip.split('.')
        return len(parts) == 4 and all(0 <= int(part) < 256 for part in parts)
    except:
        return False


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

        self.bob = None
        self.send = False
        self.msg = ""
        self.done_auth = False

        # Console
        txt_console = TextInput(multiline=True)
        txt_console.pos = (75, 75)
        txt_console.size = (650, 200)
        txt_console.readonly = True
        server_widget.add_widget(txt_console)

        def print_console(msg):
            txt_console.text = txt_console.text + '\n' + msg
            txt_console.cursor = (999,999)

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
        txt_port = TextInput(multiline=False, text="9001")
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
        txt_secret = TextInput(multiline=False, text="foobar")
        txt_secret.pos = (250,400)
        txt_secret.size = (150, 30)
        server_widget.add_widget(txt_secret)

        # Start button
        def on_server_btn_start(instance):
            btn_start.disabled = True
            txt_secret.readonly = True
            txt_port.readonly = True

            print_console("Starting Server on port " + txt_port.text)
            self.bob = None
            while self.bob is None:
                try:
                    self.bob = ChatClientServer("0.0.0.0", int(txt_port.text))
                except socket.error as e:
                    log(
                        logging.warning,
                        self,
                        self.make_server_tab,
                        "Error occurred while trying to connect: "
                        "socket.error: {}; retrying...".format(e))
                    sleep(1)
            print_console("Setting shared key to " + txt_secret.text)
            self.bob.set_shared_key(txt_secret.text)

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

        # Message box
        txt_message = TextInput(multiline=False)
        txt_message.pos = (75,25)
        txt_message.size = (450, 30)
        server_widget.add_widget(txt_message)

        # Send button
        def on_server_btn_send(instance):
            if self.done_auth:
                self.send = True
                self.msg = txt_message.text
                btn_send.disabled = True
                txt_message.text = ""
                print_console("Will send [" + self.msg + "] on next 'Continue'")
            else:
                print_console("Finish authentication first!")

        btn_send = Button(text='Send')
        btn_send.pos = (535, 25)
        btn_send.size = (90, 30)
        btn_send.bind(on_release=on_server_btn_send)
        server_widget.add_widget(btn_send)

        # Continue button
        def on_server_btn_continue(instance):
            if self.bob is not None:
                if self.done_auth:
                    try:
                        if self.send:
                            print_console("Sending [" + self.msg + "]")
                            self.bob.send(self.msg)
                            self.send = False
                            btn_send.disabled = False
                            self.msg = ""
                        else:
                            data = self.bob.recv(nb=True)
                            if data is not None:
                                print_console("Received [" + data + "]")
                            else:
                                print_console("No data to receive")
                    except NoAuthentication:
                        print_console("We are not authenticated. Reset authentication steps.")
                        self.bob.mutauth_step(reset=True)
                else:
                    try:
                        print_console("Performing a mutual authentication step")
                        self.bob.mutauth_step()
                    except BeingAttacked:
                        print_console("We are being attacked! Reset authentication steps.")
                        self.bob.mutauth_step(reset=True)
                    except NoSharedKey:
                        print_console("Shared key is not yet shared. Please share first")
                        self.bob.mutauth_step(reset=True)
                    except StopIteration:
                        print_console("Successfully Authenticated")
                        self.done_auth = True


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

        self.alice = None
        self.send = False
        self.msg = ""
        self.done_auth = False

        # Console
        txt_console = TextInput(multiline=True)
        txt_console.pos = (75, 75)
        txt_console.size = (650, 200)
        txt_console.readonly = True
        client_widget.add_widget(txt_console)

        def print_console(msg):
            txt_console.text = txt_console.text + '\n' + msg
            txt_console.cursor = (999,999)

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
        txt_ip = TextInput(multiline=False, text="127.0.0.1")
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
        txt_port = TextInput(multiline=False, text="9001")
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
        txt_secret = TextInput(multiline=False, text="foobar")
        txt_secret.pos = (250,375)
        txt_secret.size = (150, 30)
        client_widget.add_widget(txt_secret)

        # Start button
        def on_client_btn_start(instance):
            if is_valid_ip(txt_ip.text):
                btn_start.disabled = True
                txt_secret.readonly = True
                txt_port.readonly = True
                txt_ip.readonly = True

                print_console("Starting Client on port " + txt_port.text)
                self.alice = None
                while self.alice is None:
                    try:
                        self.alice = ChatClientClient(txt_ip.text,
                                                      int(txt_port.text))
                    except socket.error as e:
                        log(
                            logging.warning,
                            self,
                            self.make_client_tab,
                            "Error occurred while trying to connect: "
                            "socket.error: {}; retrying...".format(e))
                        sleep(1)
                print_console("Setting shared key to " + txt_secret.text)
                self.alice.set_shared_key(txt_secret.text)
            else:
                print_console("Please enter a valid IP address")

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

        # Message box
        txt_message = TextInput(multiline=False)
        txt_message.pos = (75,25)
        txt_message.size = (450, 30)
        client_widget.add_widget(txt_message)

        # Send button
        def on_client_btn_send(instance):
            if self.done_auth:
                self.send = True
                self.msg = txt_message.text
                btn_send.disabled = True
                txt_message.text = ""
                print_console("Will send [" + self.msg + "] on next 'Continue'")
            else:
                print_console("Finish authentication first!")

        btn_send = Button(text='Send')
        btn_send.pos = (535, 25)
        btn_send.size = (90, 30)
        btn_send.bind(on_release=on_client_btn_send)
        client_widget.add_widget(btn_send)

        # Continue button
        def on_client_btn_continue(instance):
            if self.alice is not None:
                if self.done_auth:
                    try:
                        if self.send:
                            print_console("Sending [" + self.msg + "]")
                            self.alice.send(self.msg)
                            self.send = False
                            btn_send.disabled = False
                            self.msg = ""
                        else:
                            data = self.alice.recv(nb=True)
                            if data is not None:
                                print_console("Received [" + data + "]")
                            else:
                                print_console("No data to receive")
                    except NoAuthentication:
                        print_console("We are not authenticated. Reset authentication steps.")
                        self.alice.mutauth_step(reset=True)
                else:
                    try:
                        print_console("Performing a mutual authentication step")
                        self.alice.mutauth_step()
                    except BeingAttacked:
                        print_console("We are being attacked! Reset authentication steps.")
                        self.alice.mutauth_step(reset=True)
                    except NoSharedKey:
                        print_console("Shared key is not yet shared. Please share first")
                        self.alice.mutauth_step(reset=True)
                    except StopIteration:
                        print_console("Successfully Authenticated")
                        self.done_auth = True

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
