from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QDialog

from widgets.showInputResult import Widget_ShowInputResult


#new
class showInputResult(QDialog, Widget_ShowInputResult):
    def __init__(self, parent=None):
        super(showInputResult, self).__init__(parent)
        self.setupUi(self)
        flags = Qt.Dialog
        flags = flags | Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint
        self.setWindowFlags(flags)
        self.tw_result.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tw_result.setSelectionBehavior(QAbstractItemView.SelectRows)