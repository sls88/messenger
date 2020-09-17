import time
from clientui import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore
from datetime import datetime as dt
import requests

class Messenger(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, url):
        super().__init__()
        self.setupUi(self)

        self.GoButton.pressed.connect(self.push_go_button)

        self.url = url
        self.after_timestamp = 0
        self.load_messages()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.view_messages)
        self.timer.start(1000)


    def push_go_button(self):
        name = self.NameEdit.text()
        text = self.messegeEdit.text()
        data = {'name': name, 'text': text}
        response = None
        try:
            response = requests.post(self.url + "/send", json=data)
        except:
            pass
        if response and response.status_code == 200:
            if response.json()['ok'] != True:
                self.textBrowser.append(response.json()['ok'])
                self.textBrowser.append('')
            self.messegeEdit.clear()
            self.messegeEdit.repaint()
        else:
            self.textBrowser.append('Сервер не отвечает')
            self.textBrowser.append('')
            self.messegeEdit.repaint()

    def pretty_print(self, message):
        """
        2020/09/08 10:00:23  Nick
        Text

        """
        dat = dt.fromtimestamp(message['timestamp'])
        dat = dat.strftime('%Y/%m/%d %H:%M:%S')
        first_line = dat + '  ' + message['name']
        self.textBrowser.append(first_line)
        self.textBrowser.append(message['text'])
        self.textBrowser.append('')

    def view_messages(self):
        response = None
        response_count = None
        try:
            response = requests.get(self.url + "/messages", params={'after_timestamp': self.after_timestamp})
            response_count = requests.get(self.url + "/status")
        except:
            pass
        if response_count and response_count.status_code == 200:
            users_counter = str(response_count.json()['users'])
            messages_counter = str(response_count.json()['messages'])
            self.UsersNumber.display(users_counter)
            self.MessagesNumber.display(messages_counter)
        if response and response.status_code == 200:
            messages = response.json()['messages']
            for message in messages:
                self.pretty_print(message)
                self.after_timestamp = message['timestamp']
            return messages

    def load_messages(self):
        while self.view_messages():
            time.sleep(0.2)


app = QtWidgets.QApplication([])
window = Messenger('https://e725bea3fa5e.ngrok.io')
window.show()
app.exec_()
