from PyQt5.QtWidgets import QMainWindow

from widgets.warStoreUI import WarStoreUI


class WarStoreMain(QMainWindow, WarStoreUI):
    def __init__(self, parent=None):
        super(WarStoreMain, self).__init__(parent)
        self.setupUi(self)
