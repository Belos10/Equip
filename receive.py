from PyQt5.QtCore import QObject


class receive(QObject):
    def __init__(self):
        super(receive, self).__init__()

    def slotReceive(self):
        print('receive..............')